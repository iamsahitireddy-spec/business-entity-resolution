# Comprehensive EDA & Data Understanding Report

**Author:** Anisa (Person 1 — Data Understanding + Preprocessing + EDA)  
**Target:** Business Entity Resolution Challenge  
**Datasets Analyzed:** 
- `dataset/train/train_source1.tsv`
- `dataset/train/train_source2.tsv`
- `dataset/train/train_source3.tsv`
- `dataset/train/train_ground_truth.tsv`
- `dataset/test/test_source1.tsv`
- `dataset/test/test_source2.tsv`
- `dataset/test/test_source3.tsv`

---

## 📌 Executive Summary

This report delivers the complete empirical findings from the **EDA phase** across all 26,436,000 records in the training and testing datasets. It provides concrete, factual guidance for **Sahiti (Person 2 - Blocking & Candidate Generation)** and **Hajira (Person 3 - Feature Engineering & Matching Models)**.

---

## A. Dataset Summary

### 1. Training & Testing Record Counts

| Dataset Split | Source 1 (`S1`) | Source 2 (`S2`) | Source 3 (`S3`) | Ground Truth (`GT`) | Total Split Records |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | 2,206,821 | 5,034,616 | 5,285,603 | 2,206,821 | **14,733,861** |
| **Test** | 1,732,544 | 4,887,273 | 5,082,316 | *Unlabeled* | **11,702,133** |
| **Combined** | **3,939,365** | **9,921,889** | **10,367,919** | **2,206,821** | **26,435,994** |

- **Columns in Sources 1, 2, 3:** `entity_id`, `business_name`, `business_address`, `country` (Tab-delimited `\t`).
- **Columns in Ground Truth:** `source1_entity_id`, `matched_entity_ids` (Comma-separated entity ID list).
- **Unique Entity IDs:** **0 duplicate IDs** in any file (100% unique primary keys).

### 2. Missingness Audit

| Split | Table | `entity_id` Missing | `business_name` Missing | `business_address` Missing | `country` Missing |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train** | `train_source1.tsv` | 0 (0.00%) | 0 (0.00%) | 0 (0.00%) | 0 (0.00%) |
| | `train_source2.tsv` | 0 (0.00%) | 0 (0.00%) | **168,967 (3.36%)** | 0 (0.00%) |
| | `train_source3.tsv` | 0 (0.00%) | 0 (0.00%) | **175,916 (3.33%)** | 0 (0.00%) |
| **Test** | `test_source1.tsv` | 0 (0.00%) | 0 (0.00%) | 0 (0.00%) | 0 (0.00%) |
| | `test_source2.tsv` | 0 (0.00%) | 0 (0.00%) | **129,408 (2.65%)** | 0 (0.00%) |
| | `test_source3.tsv` | 0 (0.00%) | 0 (0.00%) | **136,098 (2.68%)** | 0 (0.00%) |

> **Key Observation:** Across both train and test, **`business_name`, `country`, and `entity_id` are 100% complete**. Addresses are missing in **~2.7% to ~3.4%** of Source 2 and Source 3 records.

### 3. Country Distributions (Open-Set Behavior)

| Table | United States (`US`) | India (`India`) | France (`France`) |
| :--- | :--- | :--- | :--- |
| **Train Source 1** | 1,323,633 (59.98%) | 883,188 (40.02%) | 0 (0.00%) |
| **Train Source 2** | 3,016,817 (59.92%) | 2,017,799 (40.08%) | 0 (0.00%) |
| **Train Source 3** | 3,170,056 (59.98%) | 2,115,547 (40.02%) | 0 (0.00%) |
| **Test Source 1** | 663,106 (38.27%) | 809,986 (46.75%) | **259,452 (14.98%)** |
| **Test Source 2** | 1,871,330 (38.29%) | 2,312,565 (47.32%) | **703,378 (14.39%)** |
| **Test Source 3** | 1,945,701 (38.28%) | 2,405,000 (47.32%) | **731,615 (14.40%)** |

> **Key Observation:** Country proportions are virtually identical across S1, S2, and S3 within each split. However, the test set exhibits a major distribution shift: India becomes the plurality (47.3%), and **France represents ~14.4% of all test records**.

---

## B. Matching-Label Summary

Based on full analysis of `train_ground_truth.tsv` (2,206,821 Source 1 reference records):

### 1. Match-Count & Singleton Distribution
- **Total Source 1 Entities:** 2,206,821
- **True Singletons (0 matches):** **123,247 entities (5.58%)**
- **Matched Entities ($\ge 1$ match):** **2,083,574 entities (94.42%)**
- **Total Matched Links:** **7,638,365 pairs**
- **Mean Matches per S1 Entity:** 3.4613 (3.6660 among matched entities)
- **Max Matches per S1 Entity:** 11

### 2. Match Cardinality Breakdown
| Matches per Entity | S1 Count | Percentage | Cumulative % |
| :--- | :--- | :--- | :--- |
| **0 (Singleton)** | 123,247 | 5.58% | 5.58% |
| **1** | 119,157 | 5.40% | 10.98% |
| **2** | 375,212 | 17.00% | 27.99% |
| **3** | 530,841 | 24.05% | 52.04% |
| **4** | 484,115 | 21.94% | 73.98% |
| **5** | 321,957 | 14.59% | 88.57% |
| **6** | 164,868 | 7.47% | 96.04% |
| **7** | 63,968 | 2.90% | 98.94% |
| **8** | 18,680 | 0.85% | 99.78% |
| **9** | 4,205 | 0.19% | 99.97% |
| **10** | 534 | 0.02% | 100.00% |
| **11** | 37 | 0.00% | 100.00% |

### 3. Source 2 vs Source 3 Distribution
- **Source 2 Total Matches:** 3,693,619 (48.36% of all links)
- **Source 3 Total Matches:** 3,944,746 (51.64% of all links)
- **Co-occurrence Breakdown:**
  - **80.48% (1,776,047 S1 entities)** have matches in **both** Source 2 and Source 3.
  - **7.45% (164,498 S1 entities)** have matches **only** in Source 3.
  - **6.48% (143,029 S1 entities)** have matches **only** in Source 2.
  - **5.58% (123,247 S1 entities)** have matches in **neither** (singletons).
- **Cardinality Constraint Invariant:** Every record in Source 2 and Source 3 matches **at most one** Source 1 entity (1-to-many relationship from S1 to noisy sources, zero many-to-many overlaps).

---

## C. Name Patterns

Empirical analysis on 86,347 true ground-truth match pairs:

### 1. Exact vs. Normalized Match Rates
- **Exact Name Match Rate:** **4.61%** (Only ~1 in 22 true pairs have identical raw name strings).
- **Normalized Name Match Rate:** **21.43%** (Conservative normalization improves exact match by ~4.6x).
- **Unmatched Names after Normalization:** **78.57%** of true pairs differ even after lowercasing, whitespace stripping, and punctuation removal.

### 2. Common Variations & Noise Patterns
- **Typographic noise / Edit distance:** Character insertions, deletions, substitutions (e.g. `Williams` vs `Wilblims`).
- **Legal suffix fluctuations:** Presence, absence, or abbreviation of corporate tags (e.g. `Inc` vs `Incorporated` vs dropped suffix entirely).
- **Prefix / decoration noise:** Leading noise symbols such as `<< Team Ecole`, `-- Holloway Peak`, `+`, quotes.
- **Transliteration & encoding artifacts:** Special unicode characters and encoding variations in Indian business names (e.g. Hindi script or Latin transliteration with diacritics).
- **Website domains in business names:** Several records in Source 3 use URL domains as names (e.g. `wilfordhancock.com`).

---

## D. Address Patterns

Empirical analysis on 86,347 true match pairs:

### 1. Address Missingness & Overlap
- **Target Address Missing Rate:** **4.37%** of true matching links have blank addresses in the target source record.
- **Exact Address Match Rate (among populated):** **2.44%**.
- **Normalized Address Match Rate (among populated):** **8.68%**.

### 2. Useful Address Characteristics
- **Component Permutations:** Addresses frequently invert city/state and street components (e.g. `105 ELM ST, MORGANTON, NC` vs `MORGANTON, NC, 105 ELM ST`).
- **Street Number Anchor:** When populated, street numbers (e.g. `105`, `1795`) and postal codes remain stable anchors despite word-order shuffling.
- **Abbreviation Mappings:** Frequent variations in street designations (`ST` vs `Street`, `AVE` vs `Avenue`, `RD` vs `Road`, `BLVD` vs `Boulevard`).

### 3. Duplicate Names with Different Addresses (Chains / Multi-Location Businesses)
- Analysis of 100,000 Source 1 records revealed **5,663 names** that appear multiple times under distinct entity IDs with completely different addresses (e.g. `Primary Care Group` [15 locations], `Physical Therapy Group` [13 locations], `Cardiology Group` [11 locations]).
- **Critical Risk:** A matching model that relies solely on name similarity will produce false-positive merges across distinct branch locations.

---

## E. Blocking Recommendations (For Sahiti)

1. **Hard Block on `country` (100% Safe):**
   - Out of 86,347 evaluated ground-truth match pairs, **0 pairs cross country boundaries (100.00% country match rate)**.
   - Blocking strictly within each country partitions the candidate comparison space into 3 disjoint blocks (`US`, `India`, `France`), immediately pruning ~50% to ~60% of candidate comparisons with **zero loss of recall**.

2. **Never Block Exclusively on Address:**
   - ~3.3% of Source 2/3 records have missing addresses. An address-only blocking key will drop over 344,000 records.

3. **Do Not Rely on Exact Name Blocking:**
   - Only 21.43% of true pairs share exact normalized names. Exact name blocking would miss ~78.5% of true matches.

4. **Recommended Multi-Key Blocking Strategy:**
   - **Key 1 (Name Token / Shingle):** First significant business name word (ignoring legal stop words) within country.
   - **Key 2 (Character Prefix / N-gram):** 3-character or 4-character prefix of normalized name within country.
   - **Key 3 (Phonetic / Metaphone):** Double Metaphone / Soundex on primary name token.
   - **Union of Blocks:** Taking the union of 2–3 complementary blocking passes maintains high recall ($\ge 95\%$) while keeping candidate pairs tractable.

---

## F. Model Recommendations (For Hajira)

1. **Feature Engineering Priorities:**
   - **Name Similarity Family (Most Reliable):** Jaro-Winkler, Levenshtein ratio, N-gram Jaccard, Token Sort Ratio, and TF-IDF Cosine similarity.
   - **Address Similarity Family (Crucial for Chains):** Token overlap, Levenshtein distance on street numbers/postal codes, Jaccard token similarity.
   - **Address Missingness Indicator:** A binary feature `is_address_missing` is essential so the model can learn to down-weight missing address signals without penalizing the pair.
   - **Legal Suffix Match Indicator:** Flag whether corporate suffixes match, conflict, or are absent.

2. **Handling Class Imbalance & Macro $F_{0.5}$:**
   - Candidate generation produces a heavy negative-to-positive imbalance (often 50:1 or 100:1).
   - The competition metric is **Macro $F_{0.5}$** (precision weighted $2\times$ over recall).
   - False merges are penalized heavily. Setting conservative, high classification thresholds (e.g. $\ge 0.6$ or $\ge 0.7$) will maximize $F_{0.5}$.

3. **Singleton Post-Processing Strategy:**
   - 5.58% of Source 1 entities have zero true matches.
   - If maximum predicted match probability for an S1 entity is below the threshold, leave the match list empty (`""`). Correctly predicting singletons earns an entity score of 1.0; a false match drops it to 0.0.
