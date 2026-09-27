# Exploratory Data Analysis (EDA) & Data Validation Report

**Author:** Anisa (Person 1 — Data Understanding, Preprocessing & EDA)  
**Project:** Business Entity Resolution Challenge  
**Target Split:** `dataset/train/` (`train_source1.tsv`, `train_source2.tsv`, `train_source3.tsv`, `train_ground_truth.tsv`)  
**Status:** Step 3 Completed — 100% Offline, Rule-Based Validation

---

## 1. Executive Summary

This report delivers the comprehensive empirical findings from **Step 3 (EDA and Data Validation)** across all 14,733,861 training records. All analyses were conducted entirely offline and rule-based in accordance with competition rules without external lookups, geocoding, or third-party APIs.

### Key Highlights
1. **Total Records Analyzed:**
   - **Source 1 (`train_source1.tsv`):** 2,206,821 reference business entities.
   - **Source 2 (`train_source2.tsv`):** 5,034,616 noisy candidate records.
   - **Source 3 (`train_source3.tsv`):** 5,285,604 noisy candidate records.
   - **Ground Truth (`train_ground_truth.tsv`):** 2,206,821 Source 1 reference mappings.
   - **Total Records:** 14,733,862 records.
2. **Entity ID Prefix Consistency:** **100.0% Valid**. Zero prefix anomalies detected across any file (`S1-`, `S2-`, `S3-`).
3. **Cross-Table Referential Integrity:** **100.0% Valid**. All 3,693,619 Source 2 and 3,944,746 Source 3 referenced IDs exist in their respective source files. There are **0 dangling or orphan references**.
4. **Singleton Source 1 Entities:** Exactly **123,247 entities (5.58%)** in Source 1 have no matches (singletons). Under the Macro $F_{0.5}$ metric, predicting an empty list for these entities yields a score of 1.0, while false merges yield 0.0.
5. **Noisy Address Attributes:** While business names and countries are 100% populated across all sources, **168,967 records (3.36%) in Source 2** and **175,916 records (3.33%) in Source 3** have missing address fields. Preprocessing and feature engineering must safely handle null addresses.

---

## 2. Dataset Dimensions & Column Structure

| File | Rows | Columns | Column Names | Delimiter |
| :--- | :--- | :--- | :--- | :--- |
| `train_source1.tsv` | 2,206,821 | 4 | `entity_id`, `business_name`, `business_address`, `country` | Tab (`\t`) |
| `train_source2.tsv` | 5,034,616 | 4 | `entity_id`, `business_name`, `business_address`, `country` | Tab (`\t`) |
| `train_source3.tsv` | 5,285,603 | 4 | `entity_id`, `business_name`, `business_address`, `country` | Tab (`\t`) |
| `train_ground_truth.tsv` | 2,206,821 | 2 | `source1_entity_id`, `matched_entity_ids` | Tab (`\t`) |

---

## 3. Missing Value Audit

Evaluated for standard nulls (`NaN`/`None`) and empty string fields (`""` / whitespace-only):

| Table | Column | Null / Empty Count | Missing % | Valid Count | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Source 1** | `entity_id` | 0 | 0.00% | 2,206,821 | Complete |
| | `business_name` | 0 | 0.00% | 2,206,821 | Complete |
| | `business_address` | 0 | 0.00% | 2,206,821 | Complete |
| | `country` | 0 | 0.00% | 2,206,821 | Complete |
| **Source 2** | `entity_id` | 0 | 0.00% | 5,034,616 | Complete |
| | `business_name` | 0 | 0.00% | 5,034,616 | Complete |
| | `business_address` | **168,967** | **3.36%** | 4,865,649 | Missing in ~3.4% |
| | `country` | 0 | 0.00% | 5,034,616 | Complete |
| **Source 3** | `entity_id` | 0 | 0.00% | 5,285,603 | Complete |
| | `business_name` | 0 | 0.00% | 5,285,603 | Complete |
| | `business_address` | **175,916** | **3.33%** | 5,109,687 | Missing in ~3.3% |
| | `country` | 0 | 0.00% | 5,285,603 | Complete |
| **Ground Truth** | `source1_entity_id` | 0 | 0.00% | 2,206,821 | Complete |
| | `matched_entity_ids` | **123,247** | **5.58%** | 2,083,574 | True Singletons |

---

## 4. Duplicate ID Analysis

| Table | Total Rows | Unique Entity IDs | Duplicate IDs | Duplicate % |
| :--- | :--- | :--- | :--- | :--- |
| `train_source1.tsv` | 2,206,821 | 2,206,821 | 0 | 0.00% |
| `train_source2.tsv` | 5,034,616 | 5,034,616 | 0 | 0.00% |
| `train_source3.tsv` | 5,285,603 | 5,285,603 | 0 | 0.00% |
| `train_ground_truth.tsv` | 2,206,821 | 2,206,821 | 0 | 0.00% |

> **Finding:** Entity IDs are guaranteed to be unique primary keys within their respective tables.

---

## 5. Country Distribution Analysis

The country field is treated as an open-set string. While the training dataset comprises US and India records, the test dataset includes France and potentially other nations.

| Dataset | United States (`US`) | India (`India`) | Other / Missing |
| :--- | :--- | :--- | :--- |
| **Source 1** | 1,323,633 (59.98%) | 883,188 (40.02%) | 0 (0.00%) |
| **Source 2** | 3,016,817 (59.92%) | 2,017,799 (40.08%) | 0 (0.00%) |
| **Source 3** | 3,170,056 (59.98%) | 2,115,547 (40.02%) | 0 (0.00%) |

> **Validation Note:** The ~60% US to ~40% India split is remarkably consistent across all three data sources (variance < 0.08%).

---

## 6. Business Name & Address Length Statistics

Summary statistics computed across all records:

### Business Name Statistics
| Metric | Source 1 (`S1`) | Source 2 (`S2`) | Source 3 (`S3`) |
| :--- | :--- | :--- | :--- |
| **Mean Character Length** | 24.03 | 25.10 | 25.20 |
| **Median Character Length** | 24.0 | 25.0 | 25.0 |
| **Std Dev Character Length**| 7.74 | 8.89 | 9.49 |
| **Min / Max Character Length**| 3 / 105 | 2 / 104 | 2 / 123 |
| **Mean Word Count** | 3.55 | 3.50 | 3.53 |
| **Median Word Count** | 4.0 | 4.0 | 4.0 |
| **Std Dev Word Count** | 0.98 | 1.24 | 1.34 |
| **Min / Max Word Count** | 1 / 16 | 1 / 15 | 1 / 18 |

### Business Address Statistics
| Metric | Source 1 (`S1`) | Source 2 (`S2`) | Source 3 (`S3`) |
| :--- | :--- | :--- | :--- |
| **Mean Character Length** | 52.07 | 46.23 | 46.71 |
| **Median Character Length** | 41.0 | 37.0 | 42.0 |
| **Std Dev Character Length**| 25.33 | 24.84 | 21.65 |
| **Min / Max Character Length**| 11 / 256 | 0 / 249 | 0 / 240 |
| **Mean Word Count** | 8.03 | 7.29 | 7.17 |
| **Median Word Count** | 7.0 | 6.0 | 6.0 |
| **Std Dev Word Count** | 3.51 | 3.58 | 3.39 |
| **Min / Max Word Count** | 2 / 43 | 0 / 46 | 0 / 43 |

---

## 7. Ground Truth Match Statistics & Cardinality

### Overview
- **Total Source 1 Entities in Ground Truth:** 2,206,821
- **Singleton Source 1 Entities (0 matches):** 123,247 (**5.58%**)
- **Matched Source 1 Entities ($\ge 1$ match):** 2,083,574 (**94.42%**)
- **Total Matches Linked:** 7,638,365
- **Mean Matches per Source 1 Entity:** 3.4613
- **Mean Matches per Matched Entity:** 3.6660
- **Max Matches for Single Entity:** 11

### Breakdown by Match Source
| Match Type | Count of S1 Entities | Percentage of S1 Entities |
| :--- | :--- | :--- |
| **Singletons (Neither S2 nor S3)** | 123,247 | 5.58% |
| **Only Source 2 Matches** | 143,029 | 6.48% |
| **Only Source 3 Matches** | 164,498 | 7.45% |
| **Both Source 2 & Source 3 Matches**| 1,776,047 | 80.48% |
| **Total** | 2,206,821 | 100.00% |

### Total Matches per Source
- **Source 2 Matches:** 3,693,619 (48.36% of all links)
- **Source 3 Matches:** 3,944,746 (51.64% of all links)
- **Important Invariant:** Every referenced S2 entity and S3 entity is matched to **at most one** Source 1 entity in ground truth. There are no multi-parent links.

### Match Cardinality Distribution (Total Matches per S1 Entity)
| Matches per Entity | Number of S1 Entities | Percentage | Cumulative % |
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

### Matches per S1 by Individual Source
| Count | S2 Matches per S1 | S2 % | S3 Matches per S1 | S3 % |
| :--- | :--- | :--- | :--- | :--- |
| **0** | 287,745 | 13.04% | 266,276 | 12.07% |
| **1** | 789,108 | 35.76% | 716,417 | 32.46% |
| **2** | 652,779 | 29.58% | 668,375 | 30.29% |
| **3** | 333,957 | 15.13% | 372,443 | 16.88% |
| **4** | 119,078 | 5.40% | 145,116 | 6.58% |
| **5** | 24,154 | 1.09% | 35,378 | 1.60% |
| **6** | 0 | 0.00% | 2,816 | 0.13% |

---

## 8. Referential Integrity & Prefix Verification

| Check | Expected | Actual | Missing / Violations | Result |
| :--- | :--- | :--- | :--- | :--- |
| **Source 1 ID Prefixes** | Start with `S1-` | 2,206,821 / 2,206,821 | 0 | **PASS** |
| **Source 2 ID Prefixes** | Start with `S2-` | 5,034,616 / 5,034,616 | 0 | **PASS** |
| **Source 3 ID Prefixes** | Start with `S3-` | 5,285,603 / 5,285,603 | 0 | **PASS** |
| **Ground Truth S1 Prefix**| Start with `S1-` | 2,206,821 / 2,206,821 | 0 | **PASS** |
| **Ground Truth S1 In S1** | Exists in `train_source1` | 2,206,821 / 2,206,821 | 0 | **PASS** |
| **Ground Truth S2 In S2** | Exists in `train_source2` | 3,693,619 / 3,693,619 | 0 | **PASS** |
| **Ground Truth S3 In S3** | Exists in `train_source3` | 3,944,746 / 3,944,746 | 0 | **PASS** |
| **Unknown Prefix Links** | None | 0 | 0 | **PASS** |

---

## 9. Recommendations for Downstream Modules

1. **For Person 2 (Blocking & Candidate Generation):**
   - Candidate generation must achieve high recall while keeping pairs manageable.
   - S1 entities frequently match both S2 and S3 (80.48%). Blocking rules should generate candidates from both sources independently.
   - Address cannot be the sole blocking key due to ~3.3% missing address fields in S2 and S3. Business name blocking keys (e.g. prefix tokens, Soundex/Double-Metaphone, or token shingles) are essential.
2. **For Person 3 (Feature Engineering & Matching Models):**
   - Handle empty addresses gracefully in string similarity functions (e.g. impute or output a dedicated missingness feature).
   - Address token overlap is strong when populated; name similarity (Jaro-Winkler, Levenshtein, N-gram Jaccard) is reliable across 100% of records.
   - Legal entity terms (inc, corp, ltd, pvt, co) should be compared as distinguishing features rather than completely stripped.
3. **For Person 4 (Evaluation & Threshold Optimization):**
   - The competition metric is Macro $F_{0.5}$ which favors precision over recall.
   - 5.58% of entities are true singletons. High confidence thresholds are essential to prevent false positive matches on singletons.
