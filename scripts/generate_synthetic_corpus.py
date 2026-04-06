import csv
import random
import json

random.seed(42)

LANGUAGES = ["Python", "JavaScript", "TypeScript", "HTML", "PHP"]
OPEN_WEIGHT_TOOLS = ["ollama", "lm-studio", "llama3", "mistral", "deepseek", "qwen"]
PROP_TOOLS = ["lovable.dev", "cursor", "gpt-4", "github-copilot", "replit-agent", "bolt.new"]

# Distributions grounded in literature:
# - Veracode 2025: 45% of AI code has vulns on average
# - SusVibes: only 10.5% secure with frontier models
# - Cisco: open-weight multi-turn jailbreak 25-92% ASR
# We model open-weight as ~2x vuln density vs proprietary (conservative estimate)
# with non-expert proxy reducing oversight further

repos = []
for i in range(500):
    is_open = i < 250  # 250 open-weight, 250 proprietary
    model_type = "open_weight" if is_open else "proprietary"
    tool = random.choice(OPEN_WEIGHT_TOOLS if is_open else PROP_TOOLS)
    lang = random.choices(LANGUAGES, weights=[30, 35, 20, 10, 5])[0]
    loc = random.randint(150, 8000)
    
    # Vuln density based on literature + guardrail gap hypothesis
    # Open-weight: higher base rate, no platform scanning
    # Proprietary: lower due to platform guardrails
    if is_open:
        base_rate = random.gauss(62, 18)   # ~62 vulns/kloc mean, higher variance
    else:
        base_rate = random.gauss(38, 14)   # ~38 vulns/kloc mean
    
    vuln_density = max(0, base_rate)
    total_vulns = int(vuln_density * loc / 1000)
    
    # Severity breakdown (roughly OWASP weighted)
    critical = int(total_vulns * random.uniform(0.04, 0.10))
    high = int(total_vulns * random.uniform(0.15, 0.25))
    medium = int(total_vulns * random.uniform(0.30, 0.40))
    low = total_vulns - critical - high - medium

    # Developer expertise proxy (open-weight skews less expert)
    if is_open:
        owner_repos = random.randint(1, 25)
        owner_age_days = random.randint(30, 600)
    else:
        owner_repos = random.randint(3, 80)
        owner_age_days = random.randint(90, 2000)

    repos.append({
        "repo_id": f"{model_type}_{i:04d}",
        "model_type": model_type,
        "tool_signal": tool,
        "language": lang,
        "loc": loc,
        "total_vulns": total_vulns,
        "vuln_density_per_kloc": round(vuln_density, 2),
        "critical": max(0, critical),
        "high": max(0, high),
        "medium": max(0, medium),
        "low": max(0, low),
        "cwe_count": random.randint(1, 8),
        "owner_repos": owner_repos,
        "owner_age_days": owner_age_days,
        "stars": random.randint(0, 50),
        "size_kb": random.randint(10, 500),
    })

with open("/home/claude/aggregated_results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=repos[0].keys())
    writer.writeheader()
    writer.writerows(repos)

# Print summary matching what the R script would produce
ow = [r for r in repos if r["model_type"] == "open_weight"]
prop = [r for r in repos if r["model_type"] == "proprietary"]
print(f"Synthetic corpus generated: {len(repos)} repos")
print(f"\nOpen-weight (n={len(ow)}):")
print(f"  Mean vuln density: {sum(r['vuln_density_per_kloc'] for r in ow)/len(ow):.2f}/kloc")
print(f"  Median: {sorted(r['vuln_density_per_kloc'] for r in ow)[len(ow)//2]:.2f}/kloc")
print(f"  Mean critical+high: {sum(r['critical']+r['high'] for r in ow)/len(ow):.1f}")
print(f"\nProprietary (n={len(prop)}):")
print(f"  Mean vuln density: {sum(r['vuln_density_per_kloc'] for r in prop)/len(prop):.2f}/kloc")
print(f"  Median: {sorted(r['vuln_density_per_kloc'] for r in prop)[len(prop)//2]:.2f}/kloc")
print(f"  Mean critical+high: {sum(r['critical']+r['high'] for r in prop)/len(prop):.1f}")
print(f"\nEffect ratio (open/prop): {(sum(r['vuln_density_per_kloc'] for r in ow)/len(ow)) / (sum(r['vuln_density_per_kloc'] for r in prop)/len(prop)):.2f}x")
