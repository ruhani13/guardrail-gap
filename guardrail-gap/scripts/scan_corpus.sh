#!/bin/bash
# Usage: bash scan_corpus.sh
# Requires: pip install semgrep

mkdir -p scan_results

for model_type in open_weight proprietary; do
    for repo_dir in repos/$model_type/*/; do
        [ -d "$repo_dir" ] || continue
        repo_name=$(basename "$repo_dir")
        out_file="scan_results/${model_type}_${repo_name}.json"
        echo "Scanning $repo_dir..."
        semgrep scan \
            --config=p/owasp-top-ten \
            --config=p/secrets \
            --config=p/sql-injection \
            --config=p/xss \
            --json \
            --quiet \
            "$repo_dir" > "$out_file" 2>/dev/null
    done
done

echo "Scan complete. Results in scan_results/"
echo "Total scan files: $(ls scan_results/*.json 2>/dev/null | wc -l)"
