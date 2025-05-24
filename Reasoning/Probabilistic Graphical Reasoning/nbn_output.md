# Input
```bash
python3 naivebayesian.py
```

# Output of GA Run
```
Cervical Cancer Dataset head:
   behavior_sexualRisk  behavior_eating  behavior_personalHygine  intention_aggregation  ...  empowerment_knowledge  empowerment_abilities  empowerment_desires  ca_cervix
0                   10               13                       12                      4  ...                     12                     11                    8          1
1                   10               11                       11                     10  ...                      5                      4                    4          1
2                   10               15                        3                      2  ...                      3                      3                   15          1
3                   10               11                       10                     10  ...                      4                      4                    4          1
4                    8               11                        7                      8  ...                      5                      4                    7          1

[5 rows x 20 columns]

Breast Cancer Dataset head:
         ID Class  radius_mean  texture_mean  perimeter_mean  ...  compactness_worst  concavity_worst  concave points_worst  symmetry_worst  fractal dimension_worst
0    842302     M        17.99         10.38          122.80  ...             0.6656           0.7119                0.2654          0.4601                  0.11890
1    842517     M        20.57         17.77          132.90  ...             0.1866           0.2416                0.1860          0.2750                  0.08902
2  84300903     M        19.69         21.25          130.00  ...             0.4245           0.4504                0.2430          0.3613                  0.08758
3  84348301     M        11.42         20.38           77.58  ...             0.8663           0.6869                0.2575          0.6638                  0.17300
4  84358402     M        20.29         14.34          135.10  ...             0.2050           0.4000                0.1625          0.2364                  0.07678

[5 rows x 32 columns]

Cervical Cancer priors:
ca_cervix
0    0.708333
1    0.291667
Name: proportion, dtype: float64


Breast Cancer priors:
Class
B    0.627417
M    0.372583
Name: proportion, dtype: float64


Breast Cancer encoded labels:
Class
1    357
0    212
Name: count, dtype: int64


Breast Cancer Classification Report:
              precision    recall  f1-score   support

           0       0.93      0.90      0.92        63
           1       0.95      0.96      0.95       108

    accuracy                           0.94       171
   macro avg       0.94      0.93      0.94       171
weighted avg       0.94      0.94      0.94       171


Cervical Cancer Classification Report:
              precision    recall  f1-score   support

           0       0.87      0.93      0.90        14
           1       0.86      0.75      0.80         8

    accuracy                           0.86        22
   macro avg       0.86      0.84      0.85        22
weighted avg       0.86      0.86      0.86        22
```
![CCCH](/Reasoning/Probabilistic%20Graphical%20Reasoning/Figure_1_nbn.png)
![BCCH](/Reasoning/Probabilistic%20Graphical%20Reasoning/Figure_2_nbn.png)
![CCCM](/Reasoning/Probabilistic%20Graphical%20Reasoning/Figure_3_nbn.png)
![BCCM](/Reasoning/Probabilistic%20Graphical%20Reasoning/Figure_4_nbn.png)

