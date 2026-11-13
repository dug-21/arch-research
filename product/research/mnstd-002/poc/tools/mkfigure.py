"""Generate the fictitious 'felt mallet' figure (src/figure1.png) with the stdlib only.

Authored by factory-poc (mnstd-002). Run once; the PNG is committed as an authored input (≈1 KB).
Output is byte-deterministic (no timestamps, fixed zlib level).
"""
import struct
import sys
import zlib

W, H = 240, 120


def pixel(x, y):
    # shaft: horizontal bar
    if 110 <= x <= 230 and 54 <= y <= 66:
        return (120, 80, 40)
    # felt head: filled circle
    if (x - 70) ** 2 + (y - 60) ** 2 <= 40 ** 2:
        return (200, 60, 60)
    return (255, 255, 255)


def png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        for x in range(W):
            raw.extend(pixel(x, y))

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    out = b"\x89PNG\r\n\x1a\n"
    out += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    out += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    out += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(out)


if __name__ == "__main__":
    png(sys.argv[1])
