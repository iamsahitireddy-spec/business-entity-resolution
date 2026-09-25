# Business Entity Resolution Package

This package contains the core python source code for preprocessing, blocking, feature engineering, machine learning modeling, evaluation, and pipeline orchestration.

## Package Architecture

```
code/business_entity_resolution/
├── README.md
├── requirements.txt
└── src/
    ├── __init__.py
    ├── config.py                  # Paths and configurable thresholds
    ├── data_loader.py             # TSV dataset loading & ground truth parser
    │
    ├── preprocessing/             # Text and address normalization
    │   ├── __init__.py
    │   ├── text_normalization.py
    │   └── address_normalization.py
    │
    ├── blocking/                  # Blocking & candidate pair generation
    │   ├── __init__.py
    │   └── candidate_generation.py
    │
    ├── matching/                  # Feature engineering & ML modeling
    │   ├── __init__.py
    │   ├── feature_engineering.py
    │   ├── model.py
    │   └── inference.py
    │
    ├── evaluation/                # Macro F0.5 evaluation metric
    │   ├── __init__.py
    │   └── evaluate.py
    │
    └── pipeline.py                # End-to-end execution pipeline
```

## Running the Pipeline

From the repository root:
```bash
python3 code/business_entity_resolution/src/pipeline.py
```
