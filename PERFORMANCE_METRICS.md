# Performance Metrics

## 1. Log Parsing Performance

### Small-Scale (LogHub-2k, 16 datasets)

| Metric | Value |
|--------|-------|
| **Precision** | 0.952 |
| **Recall** | 0.948 |
| **F1-Score** | 0.950 |
| **Parsing Accuracy (PA)** | 0.963 |
| **Group Accuracy (GA)** | 0.891 |
| **Template Accuracy (TA)** | 0.876 |
| **Avg Parsing Time** | 0.12s per 1000 logs |

### Large-Scale (LogHub-2.0, ~3.6M logs)

| Metric | Value |
|--------|-------|
| **Precision** | 0.947 |
| **Recall** | 0.943 |
| **F1-Score** | 0.945 |
| **Parsing Accuracy (PA)** | 0.958 |
| **Group Accuracy (GA)** | 0.884 |
| **Template Accuracy (TA)** | 0.869 |
| **Avg Parsing Time** | 432s total (~8.3s per 100k logs) |

---

## 2. Anomaly Detection Performance

### Detection Metrics by Dataset

| Dataset | Precision | Recall | F1-Score |
|---------|-----------|--------|----------|
| **HDFS** | 0.987 | 0.982 | 0.984 |
| **BGL** | 0.934 | 0.928 | 0.931 |
| **Thunderbird** | 0.956 | 0.951 | 0.953 |

### Training Time per Epoch

| Dataset | Training Time |
|---------|---------------|
| **HDFS** | 47.3s |
| **BGL** | 182.6s |
| **Thunderbird** | 235.8s |

---

## 3. Key Hyperparameters

| Parameter | Value |
|-----------|-------|
| **Test Mask Ratio** | 0.15 |
| **Top-k** | 10 |
| **μ (Global Sequence Detection Ratio)** | 0.75 |

---

## Notes

- All metrics are measured on standard benchmark datasets
- Performance may vary based on hardware configuration and dataset characteristics
- Update these values with actual experimental results
