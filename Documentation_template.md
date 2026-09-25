# Business Entity Resolution Challenge - Solution Documentation

## 1. Executive Summary
- **Team Name**: [Team Name]
- **Team Members**: [Member 1, Member 2, Member 3, Member 4]
- **Final Validation F0.5 Score**: [Score]

---

## 2. Approach Overview

### High-Level Methodology
Provide a concise overview of the pipeline design, detailing how Source 1 records were matched against Source 2 and Source 3 records.

---

## 3. Modular Components

### 3.1 Preprocessing & Normalization
- **Text Normalization**: Describe case folding, legal suffix handling (Corp, Ltd, Pvt, etc.), punctuation, and whitespace handling.
- **Address Normalization**: Explain address tokenization, component parsing, and abbreviation expansion performed without external geocoding.
- **Country Field**: Detail handling of open-set country strings (US, India, France, etc.).

### 3.2 Blocking & Candidate Generation
- **Candidate Generation Strategy**: Explain how candidate pairs were generated to reduce the $O(N \times M)$ search space.
- **Candidate Pair Statistics**: Report candidate generation recall and reduction ratio.

### 3.3 Feature Engineering
Detail the feature families constructed for pairwise entity comparison:
- Name similarity metrics (Levenshtein, Jaro-Winkler, N-gram Jaccard, TF-IDF cosine similarity).
- Address similarity metrics.
- Token overlap and exact match indicators.
- Open-set country compatibility features.

### 3.4 Model Architecture & Training
- **Model Choice**: Explain model choice (e.g., GBDT / XGBoost / LightGBM / Logistic Regression).
- **Class Imbalance & Thresholding**: Describe threshold selection strategies optimized for Macro-averaged F0.5.
- **Singleton Strategy**: Detail logic used to classify true singletons (Source 1 records with zero matches).

---

## 4. Evaluation & Results

| Validation Split | Precision | Recall | F0.5 Score |
|------------------|-----------|--------|------------|
| Train Fold 1     |           |        |            |
| Train Fold 2     |           |        |            |
| Overall CV       |           |        |            |

---

## 5. Team Contributions & Responsibilities
- **[Member 1]**: Preprocessing & Text Normalization
- **[Member 2]**: Blocking & Candidate Pair Generation
- **[Member 3]**: Feature Engineering & ML Matching Model
- **[Member 4]**: Evaluation Metric, Pipeline Integration & Submission Generation
