#!/usr/bin/env bash
set -euo pipefail

find ../ModifiedRevLib/ -name '*.qasm' -print0 | while IFS= read -r -d '' f; do
  # Replace rotations with Z gates
  sed -i '' 's|rz(1.0\*pi)|z|g' "$f"
  sed -i '' 's|rz(3\*pi)|z|g' "$f"

  # Replace rotations with S gates
  sed -i '' 's|rz(pi/2)|s|g' "$f"
  sed -i '' 's|rz(0.5\*pi)|s|g' "$f"
  sed -i '' 's|rz(1.5\*pi)|sdg|g' "$f"

  # Replace rotations with T gates
  sed -i '' 's|rz(pi/4)|t|g' "$f"
  sed -i '' 's|rz(0.25\*pi)|t|g' "$f"
  sed -i '' 's|rz(-pi/4)|tdg|g' "$f"
  sed -i '' 's|rz(1.75\*pi)|tdg|g' "$f"

  # Replace complex rotations (need real newline) — use perl (portable on macOS)
  perl -pi -e 's|rz\(1\.25\*pi\) (.*)|z $1\nt $1|g' "$f"
  perl -pi -e 's|rz\(0\.75\*pi\) (.*)|s $1\nt $1|g' "$f"

  # Replace rx(pi/2) with rx(0.5*pi)  (你注释和替换方向反了；下面是“0.5*pi -> pi/2”)
  sed -i '' 's|rx(0.5\*pi)|rx(pi/2)|g' "$f"
done
