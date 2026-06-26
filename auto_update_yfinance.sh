#!/bin/bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$repo_dir"

package_name="yfinance"
requirements_file="$repo_dir/requirements.txt"

if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "Working tree is dirty. Commit or stash changes first."
  exit 1
fi

git pull --ff-only

fetch_latest_version() {
  if [[ -n "${YFINANCE_LATEST:-}" ]]; then
    printf '%s\n' "$YFINANCE_LATEST"
    return
  fi

  curl -fsS "https://pypi.org/pypi/${package_name}/json" | \
    python3 -c 'import json, sys; print(json.load(sys.stdin)["info"]["version"])'
}

latest_version="$(fetch_latest_version)"
current_line="$(grep -E "^${package_name}([=<>!~].*)?$" "$requirements_file" | head -n 1 || true)"

if [[ "$current_line" =~ ^${package_name}==([0-9A-Za-z.+-]+)$ ]]; then
  current_version="${BASH_REMATCH[1]}"
else
  current_version="unversioned"
fi

echo "Current ${package_name}: ${current_version}"
echo "Latest ${package_name}: ${latest_version}"

if [[ "$current_line" == "${package_name}==${latest_version}" ]]; then
  echo "Already up to date."
  exit 0
fi

python3 - "$requirements_file" "$latest_version" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
latest_version = sys.argv[2]
lines = path.read_text(encoding='utf-8').splitlines()
updated = []
replaced = False

for line in lines:
    stripped = line.strip()
    if stripped.startswith("yfinance"):
        updated.append(f"yfinance=={latest_version}")
        replaced = True
    else:
        updated.append(line)

if not replaced:
    updated.append(f"yfinance=={latest_version}")

path.write_text("\n".join(updated) + "\n", encoding='utf-8')
PY

echo "Building and deploying updated image..."
"$repo_dir/deploy.sh"

git add requirements.txt
git commit -m "chore: bump yfinance to ${latest_version}"
git push
