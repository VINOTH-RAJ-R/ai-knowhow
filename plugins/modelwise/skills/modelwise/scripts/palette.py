#!/usr/bin/env python3
"""Tonal range and text contrast for brand colours (standard library only).

  python3 palette.py 1f4e79 f2a900 e8f1f8
  python3 palette.py 1f4e79 f2a900 e8f1f8 --json

The first colour is treated as the primary background. For each colour it prints shades
(mixed with black) and tints (mixed with white), so a prompt can ask for depth inside the
brand colour instead of a flat fill. It then checks text contrast on the primary using the
WCAG formula: 4.5:1 for normal text, 3:1 for large display text.
"""
import argparse
import json
import sys

STEPS = [("900", "black", 0.6), ("700", "black", 0.3), ("500", None, 0.0), ("300", "white", 0.3), ("100", "white", 0.6)]


def parse(h):
    h = h.strip().lstrip("#")
    if len(h) != 6 or any(c not in "0123456789abcdefABCDEF" for c in h):
        sys.exit("Not a 6-digit hex colour: %s" % h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexs(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in rgb)


def mix(rgb, other, amount):
    return tuple(c + (o - c) * amount for c, o in zip(rgb, other))


def luminance(rgb):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def scale(rgb):
    out = []
    for name, toward, amount in STEPS:
        target = (0, 0, 0) if toward == "black" else (255, 255, 255)
        out.append({"step": name, "hex": hexs(mix(rgb, target, amount) if toward else rgb)})
    return out


def analyse(hexes):
    colours = [parse(h) for h in hexes]
    primary = colours[0]
    result = {"colours": [], "text_on_primary": []}
    for h, rgb in zip(hexes, colours):
        result["colours"].append({"hex": "#" + h.lstrip("#").lower(), "scale": scale(rgb)})
    candidates = [("white", (255, 255, 255))] + [("#" + h.lstrip("#").lower(), c) for h, c in zip(hexes[1:], colours[1:])]
    for name, rgb in candidates:
        ratio = contrast(primary, rgb)
        result["text_on_primary"].append({
            "text": name, "ratio": round(ratio, 2),
            "normal_text": "pass" if ratio >= 4.5 else "fail",
            "large_text": "pass" if ratio >= 3.0 else "fail",
        })
    result["text_on_primary"].sort(key=lambda r: -r["ratio"])
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("colours", nargs="+", help="Hex colours; the first is the primary background.")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    r = analyse(a.colours)
    if a.json:
        print(json.dumps(r, indent=2))
        return
    print("Tonal range (use these for depth, gradients and light inside each brand colour):")
    print("| Colour | 900 shade | 700 | 500 base | 300 | 100 tint |")
    print("|---|---|---|---|---|---|")
    for c in r["colours"]:
        print("| %s | %s |" % (c["hex"], " | ".join(s["hex"] for s in c["scale"])))
    print("\nText on the primary %s (WCAG contrast):" % r["colours"][0]["hex"])
    print("| Text colour | Ratio | Normal text (4.5:1) | Large display text (3:1) |")
    print("|---|---|---|---|")
    for t in r["text_on_primary"]:
        print("| %s | %.2f:1 | %s | %s |" % (t["text"], t["ratio"], t["normal_text"], t["large_text"]))


if __name__ == "__main__":
    main()
