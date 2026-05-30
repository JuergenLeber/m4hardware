#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
OUTPUT_DIR="$ROOT_DIR/m4board_v25c"
BASE_NAME="m4board_simp_v2_5C"
ZIP_NAME="$BASE_NAME.zip"

rm -f "$ROOT_DIR/$ZIP_NAME"
cd "$OUTPUT_DIR"
zip -r "$ROOT_DIR/$ZIP_NAME" . -x "*.dri" "*.gpi" "*original*"

echo "Created archive: $ROOT_DIR/$ZIP_NAME"
