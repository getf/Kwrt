#!/usr/bin/env python3
"""Remove Kwrt luci-mod-status author-links row from 10_system.js."""
import re
import sys

MARKERS = ("固件下载与定制", "TG交流", "t.me/opkwrt", "openwrt.ai/fadian")
COND = re.compile(r"if\s*\(\s*uci\.get\(\s*'system'\s*,\s*'@system\[0\]'\s*,\s*'links'\s*\)\s*!==?\s*'0'\s*\)\s*\{")


def strip_block(src):
    m = COND.search(src)
    if not m:
        return src, False
    depth = 0
    i = m.end() - 1
    quote = None
    while i < len(src):
        c = src[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
        elif c in "'\"`":
            quote = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                start = src.rfind("\n", 0, m.start()) + 1
                if src[start:m.start()].strip():
                    start = m.start()
                if end < len(src) and src[end] == "\n":
                    end += 1
                return src[:start] + src[end:], True
        i += 1
    return src, False


rc = 0
for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        src = f.read()
    if not any(k in src for k in MARKERS):
        print(f"strip-status-links: {path}: no author links, skip")
        continue
    new, changed = strip_block(src)
    left = [k for k in MARKERS if k in new]
    if not changed or left:
        print(f"ERROR: strip-status-links: {path}: author links still present: {left}", file=sys.stderr)
        rc = 1
        continue
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    print(f"strip-status-links: {path}: removed author links row")
sys.exit(rc)
