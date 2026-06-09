#!/usr/bin/env python3
"""
Convert centroid file to a gerbv-compatible pick-and-place CSV.
Converts coordinates from mils to millimeters and writes the full PNP CSV schema
that gerbv expects for pick-and-place imports.
"""

import csv

# Conversion factor: 1 mil = 0.0254 mm
MIL_TO_MM = 0.0254


def parse_coordinate(coord_str):
    """Parse coordinate string like '562.992mil' and return value in mm."""
    value_mil = float(coord_str.replace('mil', '').strip())
    return value_mil * MIL_TO_MM


def format_mm(coord_mm):
    """Format a millimeter coordinate for gerbv's PNP parser."""
    return f"{coord_mm:.4f}mm"


def convert_centroid_to_gerbv(input_file, output_file):
    """Convert centroid file to gerbv-compatible pick-and-place CSV."""
    rows = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)

        for row in reader:
            designator = row[0].strip()
            footprint = row[1].strip()
            mid_x_mm = parse_coordinate(row[2])
            mid_y_mm = parse_coordinate(row[3])
            ref_x_mm = parse_coordinate(row[4])
            ref_y_mm = parse_coordinate(row[5])
            pad_x_mm = parse_coordinate(row[6])
            pad_y_mm = parse_coordinate(row[7])
            side = row[8].strip()  # T for Top, B for Bottom
            rotation = row[9].strip()
            comment = row[10].strip() if len(row) > 10 else ""

            if side.upper() == 'T':
                layer = 'Top'
            elif side.upper() == 'B':
                layer = 'Bottom'
            else:
                layer = side

            rows.append([
                designator,
                footprint,
                format_mm(mid_x_mm),
                format_mm(mid_y_mm),
                format_mm(ref_x_mm),
                format_mm(ref_y_mm),
                format_mm(pad_x_mm),
                format_mm(pad_y_mm),
                layer,
                rotation,
                comment,
            ])

    fieldnames = [
        'Designator',
        'Footprint',
        'Mid X',
        'Mid Y',
        'Ref X',
        'Ref Y',
        'Pad X',
        'Pad Y',
        'Layer',
        'Rotation',
        'Comment',
    ]

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        writer.writerows(rows)

    print(f"✓ Converted {len(rows)} components")
    print(f"✓ Output: {output_file}")


if __name__ == '__main__':
    input_file = 'm4board_simp_v2_5C_centroid.csv'
    output_file = 'm4board_simp_v2_5C_centroid_gerbv.csv'

    convert_centroid_to_gerbv(input_file, output_file)
