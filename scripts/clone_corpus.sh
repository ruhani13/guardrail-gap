#!/bin/bash
# Usage: bash clone_corpus.sh corpus.csv
# Clones open_weight and proprietary repos from the collected corpus

CSV=${1:-corpus.csv}
mkdir -p repos/open_weight repos/proprietary

tail -n +2 "$CSV" | while IFS=',' read -r full_name url clone_url language stars created_at updated_at model_type rest; do
    if [[ "$model_type" == "open_weight" || "$model_type" == "proprietary" ]]; then
        owner=$(echo "$full_name" | cut -d'/' -f1)
        repo=$(echo "$full_name" | cut -d'/' -f2)
        target="repos/$model_type/${owner}_${repo}"
        echo "Cloning $full_name ($model_type)..."
        git clone --depth=1 --quiet "$clone_url" "$target" 2>/dev/null
        sleep 0.5
    fi
done

echo "Done."
echo "Open-weight repos: $(ls repos/open_weight 2>/dev/null | wc -l)"
echo "Proprietary repos: $(ls repos/proprietary 2>/dev/null | wc -l)"
