// smart-edge-002 H11 POC — deterministic multi-pattern hotspot bank.
// Real regex crate (RE2-lineage RegexSet). Streams an observation corpus, reports
// hotspot hits by category/severity, measures recall vs real documented hotspots,
// and benchmarks compile+scan at 100/1k/10k patterns. PARTIAL ceiling: this is a
// standalone binary, NOT the in-server Unimatrix integration (that = `proven`).
use aho_corasick::AhoCorasick;
use regex::RegexSetBuilder;
use serde::Deserialize;
use std::collections::BTreeMap;
use std::time::Instant;
use std::{env, fs};

#[derive(Deserialize, Clone)]
struct Sig {
    #[allow(dead_code)]
    id: String,
    category: String,
    severity: String,
    pattern: String,
}

fn rss_kb() -> u64 {
    fs::read_to_string("/proc/self/status")
        .ok()
        .and_then(|s| s.lines().find(|l| l.starts_with("VmRSS")).map(String::from))
        .and_then(|l| l.split_whitespace().nth(1).and_then(|n| n.parse().ok()))
        .unwrap_or(0)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    // usage: bank <signatures.json> <labeled.txt> <corpus files...>
    let sigs: Vec<Sig> = serde_json::from_str(&fs::read_to_string(&args[1]).unwrap()).unwrap();
    let labeled_path = &args[2];
    let corpus: Vec<String> = args[3..].to_vec();

    let patterns: Vec<String> = sigs.iter().map(|s| s.pattern.clone()).collect();
    let set = RegexSetBuilder::new(&patterns)
        .case_insensitive(true)
        .build()
        .unwrap();
    println!("== hotspot-bank :: {} signatures compiled ==", sigs.len());

    // ---- 1. Scan the real observation corpus ----
    let mut total_bytes = 0usize;
    let mut total_lines = 0usize;
    let mut cat_hits: BTreeMap<String, usize> = BTreeMap::new();
    let mut sev_hits: BTreeMap<String, usize> = BTreeMap::new();
    let rss0 = rss_kb();
    let t0 = Instant::now();
    for f in &corpus {
        let content = match fs::read_to_string(f) {
            Ok(c) => c,
            Err(_) => continue,
        };
        total_bytes += content.len();
        for line in content.lines() {
            total_lines += 1;
            for idx in set.matches(line).into_iter() {
                *cat_hits.entry(sigs[idx].category.clone()).or_default() += 1;
                *sev_hits.entry(sigs[idx].severity.clone()).or_default() += 1;
            }
        }
    }
    let dt = t0.elapsed().as_secs_f64();
    let mbps = (total_bytes as f64 / 1_048_576.0) / dt;
    println!("\n-- CORPUS SCAN (real session subagent transcripts) --");
    println!(
        "files={} bytes={} lines={} scan={:.2}ms throughput={:.1} MB/s",
        corpus.len(),
        total_bytes,
        total_lines,
        dt * 1000.0,
        mbps
    );
    println!("peak RSS ~{} KB (delta {} KB)", rss_kb(), rss_kb().saturating_sub(rss0));
    println!("hits by severity: {:?}", sev_hits);
    println!("hits by category:");
    for (c, n) in &cat_hits {
        println!("   {:20} {}", c, n);
    }

    // ---- 2. Labeled recall test (real documented hotspots) ----
    println!("\n-- LABELED RECALL TEST (real shd-005 + factory hotspots) --");
    let labeled = fs::read_to_string(labeled_path).unwrap_or_default();
    let (mut pos, mut recovered, mut clean, mut fp) = (0, 0, 0, 0);
    let mut missed: Vec<String> = Vec::new();
    let mut wb_recovered = false;
    for raw in labeled.lines() {
        let raw = raw.trim();
        if raw.is_empty() || raw.starts_with('#') {
            continue;
        }
        let mut it = raw.splitn(2, "||");
        let cat = it.next().unwrap_or("").trim();
        let text = it.next().unwrap_or("").trim();
        if text.is_empty() {
            continue;
        }
        let fired: Vec<&str> = set
            .matches(text)
            .into_iter()
            .map(|i| sigs[i].category.as_str())
            .collect();
        if cat == "clean" {
            clean += 1;
            if !fired.is_empty() {
                fp += 1;
                let snip: String = text.chars().take(60).collect();
                println!("   FP  clean line fired {:?}: {}", fired, snip);
            }
        } else {
            pos += 1;
            if fired.iter().any(|f| *f == cat) {
                recovered += 1;
                if cat == "write-block" {
                    wb_recovered = true;
                }
            } else {
                missed.push(format!("{} :: {}", cat, text));
            }
        }
    }
    let recall = if pos > 0 { 100.0 * recovered as f64 / pos as f64 } else { 0.0 };
    println!(
        "positives={} recovered={} recall={:.0}%  clean={} false_positives={}",
        pos, recovered, recall, clean, fp
    );
    for m in &missed {
        println!("   MISS {}", m);
    }
    println!(
        "write-block (the hotspot cycle_review MISSED on shd-005) recovered: {}",
        wb_recovered
    );

    // ---- 3. Scaling benchmark: two engines, 100..100k patterns ----
    println!("\n-- SCALING BENCHMARK (compile + scan the corpus) --");
    let mut blob = String::new();
    for f in &corpus {
        if let Ok(c) = fs::read_to_string(f) {
            blob.push_str(&c);
            blob.push('\n');
        }
    }
    let lines: Vec<&str> = blob.lines().collect();
    let mb = blob.len() as f64 / 1_048_576.0;

    println!("[A] regex RegexSet (real regex signatures + synthetic literal padding):");
    for n in [100usize, 1000, 10000] {
        let mut pats = patterns.clone();
        let mut i = 0usize;
        while pats.len() < n {
            pats.push(format!("zzsynthsig{:06}qq", i));
            i += 1;
        }
        let tc = Instant::now();
        // default size_limit is 10MB and 10k patterns blow it — bump it and report honestly.
        let built = RegexSetBuilder::new(&pats)
            .case_insensitive(true)
            .size_limit(1 << 30)
            .build();
        match built {
            Ok(bset) => {
                let compile_ms = tc.elapsed().as_secs_f64() * 1000.0;
                let ts = Instant::now();
                let mut hits = 0usize;
                for line in &lines {
                    hits += bset.matches(line).into_iter().count();
                }
                let scan_ms = ts.elapsed().as_secs_f64() * 1000.0;
                println!(
                    "   n={:6} compile={:8.1}ms scan={:9.2}ms throughput={:7.1} MB/s (hits={})",
                    n, compile_ms, scan_ms, mb / (scan_ms / 1000.0), hits
                );
            }
            Err(e) => println!("   n={:6} RegexSet build FAILED (even at 1GB limit): {}", n, e),
        }
    }

    println!("[B] aho-corasick literal bank (right engine for large literal signature sets):");
    for n in [100usize, 1000, 10000, 100000] {
        let mut lits: Vec<String> = sigs.iter().map(|s| s.category.clone()).collect();
        let mut i = 0usize;
        while lits.len() < n {
            lits.push(format!("zzsynthlit{:06}qq", i));
            i += 1;
        }
        let tc = Instant::now();
        let ac = AhoCorasick::new(&lits).unwrap();
        let compile_ms = tc.elapsed().as_secs_f64() * 1000.0;
        let ts = Instant::now();
        let mut hits = 0usize;
        for line in &lines {
            hits += ac.find_iter(line).count();
        }
        let scan_ms = ts.elapsed().as_secs_f64() * 1000.0;
        println!(
            "   n={:6} compile={:8.1}ms scan={:9.2}ms throughput={:7.1} MB/s (hits={})",
            n, compile_ms, scan_ms, mb / (scan_ms / 1000.0), hits
        );
    }
    println!("\n(RSS after bench ~{} KB)", rss_kb());
}
