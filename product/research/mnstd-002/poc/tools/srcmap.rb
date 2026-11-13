# Asciidoctor sourcemap dump (findings-W0 §3.2). Runs ONLY inside the pinned metanorma image (N2.2).
# Usage: ruby /tools/srcmap.rb draft.adoc  -> JSON array of blocks in document order.
# Authored by factory-poc (mnstd-002).
require "asciidoctor"
require "json"

doc = Asciidoctor.load_file(ARGV[0], sourcemap: true, safe: :safe)
out = []
walk = lambda do |b, parent_idx|
  kids = b.respond_to?(:blocks) ? b.blocks : []
  kids = b.items if b.respond_to?(:items) && b.context != :dlist && kids.empty?
  kids.each do |c|
    next unless c.respond_to?(:context)
    idx = out.size
    src = nil
    begin
      src = c.lines.join("\n") if c.respond_to?(:lines) && [:paragraph, :admonition].include?(c.context)
    rescue StandardError
      src = nil
    end
    src ||= (c.text rescue nil) if c.context == :list_item
    out << {
      idx: idx, parent: parent_idx, ctx: c.context.to_s, id: c.id,
      line: c.source_location&.lineno, level: (c.context == :section ? c.level : nil),
      title: (c.title rescue nil), style: c.style, sectname: (c.context == :section ? c.sectname : nil),
      source: src
    }
    walk.call(c, idx)
  end
end
walk.call(doc, nil)
header_end = nil
begin
  header_end = doc.header? ? doc.blocks.first&.source_location&.lineno : nil
rescue StandardError
  header_end = nil
end
puts JSON.pretty_generate({ blocks: out, first_body_line: header_end })
