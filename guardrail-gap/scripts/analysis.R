library(tidyverse)
library(coin)       # non-parametric tests
library(effsize)    # Cohen's d
library(ggplot2)

df <- read_csv("data/aggregated_results.csv") |>
  filter(model_type %in% c("open_weight", "proprietary")) |>
  filter(loc > 100)   # exclude trivially small repos

# --- Descriptive stats ---
cat("=== Descriptive Statistics ===\n")
df |> group_by(model_type) |>
  summarise(
    n               = n(),
    mean_density    = mean(vuln_density_per_kloc),
    median_density  = median(vuln_density_per_kloc),
    sd_density      = sd(vuln_density_per_kloc),
    mean_high_crit  = mean(critical + high)
  ) |> print()

# --- Main test: Wilcoxon rank-sum ---
cat("\n=== Wilcoxon Rank-Sum Test ===\n")
wilcox.test(
  vuln_density_per_kloc ~ model_type,
  data        = df,
  alternative = "greater"   # H1: open_weight > proprietary
) |> print()

# --- Effect size ---
cat("\n=== Cohen's d ===\n")
cohen.d(
  df$vuln_density_per_kloc[df$model_type == "open_weight"],
  df$vuln_density_per_kloc[df$model_type == "proprietary"]
) |> print()

# --- OLS regression controlling for LOC ---
cat("\n=== Regression (vuln_density ~ model_type + log_loc) ===\n")
df <- df |> mutate(
  model_binary = ifelse(model_type == "open_weight", 1, 0),
  log_loc      = log1p(loc)
)
lm(vuln_density_per_kloc ~ model_binary + log_loc, data = df) |>
  summary() |> print()

# --- Plot ---
ggplot(df, aes(x = model_type, y = vuln_density_per_kloc, fill = model_type)) +
  geom_boxplot(alpha = 0.75, outlier.shape = 16, outlier.size = 1.5) +
  geom_jitter(width = 0.12, alpha = 0.25, size = 1) +
  scale_fill_manual(values = c("open_weight" = "#D85A30", "proprietary" = "#1D9E75")) +
  labs(
    title = "Vulnerability density by model type",
    x     = "Model type",
    y     = "Vulnerabilities per 1,000 LOC",
    fill  = NULL
  ) +
  theme_minimal(base_size = 13) +
  theme(legend.position = "none")

ggsave("figures/vuln_density_boxplot.pdf", width = 6, height = 4)
cat("\nPlot saved to figures/vuln_density_boxplot.pdf\n")
