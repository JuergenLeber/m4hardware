#!/usr/bin/env python3
from pathlib import Path
import argparse

HEADER = "Designator;Footprint;Mid X;Mid Y;Ref X;Ref Y;Pad X;Pad Y;TB;Rotation;Comment"


def mm_to_mil(mm: float) -> float:
    return mm * 39.37007874015748


def parse_line(line: str):
    parts = line.strip().split()
    if not parts:
        return None
    desig = parts[0]
    x = float(parts[1])
    y = float(parts[2])
    rot = parts[3]
    rest = parts[4:]
    if len(rest) >= 2:
        footprint = rest[-1]
        comment = " ".join(rest[:-1])
    else:
        footprint = rest[-1] if rest else ""
        comment = ""
    if not comment:
        comment = footprint
    return desig, x, y, rot, comment, footprint


def format_row(desig, footprint, mx, my, tb, rot, comment):
    return ";".join([
        desig,
        footprint,
        f"{mx:11.3f}mil",
        f"{my:12.3f}mil",
        f"{mx:12.3f}mil",
        f"{my:12.3f}mil",
        f"{mx:12.3f}mil",
        f"{my:12.3f}mil",
        tb,
        f"{rot:>6}",
        comment,
    ])


def convert_file(path: Path, tb: str):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            parsed = parse_line(line)
            if not parsed:
                continue
            desig, x, y, rot, comment, footprint = parsed
            mx = mm_to_mil(x)
            my = mm_to_mil(y)
            rows.append(format_row(desig, footprint, mx, my, tb, rot, comment))
    return rows


def main():
    parser = argparse.ArgumentParser(description="Convert .mnt/.mnb placement files to a PCBWay-style centroid file.")
    parser.add_argument("-o", "--output", default="m4board_simp_v2_5C_centroid.csv", help="Output centroid file")
    parser.add_argument("--top", default="m4board_simp_v2_5C.mnt", help="Top-side placement file (.mnt)")
    parser.add_argument("--bottom", default="m4board_simp_v2_5C.mnb", help="Bottom-side placement file (.mnb)")
    args = parser.parse_args()

    top_path = Path(args.top)
    bottom_path = Path(args.bottom)
    out_path = Path(args.output)

    rows = [HEADER]
    rows += convert_file(top_path, "T")
    rows += convert_file(bottom_path, "B")

    out_path.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Wrote centroid file: {out_path}")


if __name__ == "__main__":
    main()
