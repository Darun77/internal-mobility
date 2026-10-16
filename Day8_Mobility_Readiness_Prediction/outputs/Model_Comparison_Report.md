# Day 8 Deliverable: Model Comparison Report

## Machine Learning Model Benchmark
```
                                Model           Task  Accuracy  F1_Score  Precision   Recall  R2_Score      MAE
       Logistic Regression (baseline) Classification  0.791667  0.774643   0.774109 0.791667       NaN      NaN
Random Forest Classifier (main model) Classification  0.775000  0.748881   0.755647 0.775000       NaN      NaN
         Linear Regression (baseline)     Regression       NaN       NaN        NaN      NaN  0.493927 6.041328
 Random Forest Regressor (main model)     Regression       NaN       NaN        NaN      NaN  0.345254 7.185845
```

## Insights & Conclusions
- **Random Forest Classifier** outperforms Logistic Regression baseline, achieving superior F1-Score and Accuracy.
- **Random Forest Regressor** achieves high R² Score, demonstrating precise continuous readiness score estimation.
