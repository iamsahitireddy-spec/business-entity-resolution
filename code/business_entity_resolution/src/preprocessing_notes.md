# Preprocessing & EDA Integration Notes

**Author:** Anisa (Person 1 — Data Understanding, Preprocessing & EDA)  
**Module:** [`code/business_entity_resolution/src/preprocessing.py`](file:///c:/Users/Anisa%20Islam/OneDrive/Documents/Desktop/business-entity-resolution/code/business_entity_resolution/src/preprocessing.py)  
**Status:** Step 3 Completed — 100% Offline, Rule-Based Preprocessing

---

## 1. Key EDA Findings Driving Preprocessing

Our empirical scan across all **14,733,861 training records** established six foundational data realities that directly govern preprocessing design:

1. **Entity IDs are 100% Clean:**
   - Zero duplicate IDs in any source table.
   - Every entity ID conforms to its source prefix (`S1-`, `S2-`, `S3-`).
   - Every ground-truth reference exists in the source files (0 dangling or orphan references).
   - *Design Decision:* Preprocessing treats `entity_id` as immutable, never modifying or hashing IDs.

2. **Company Names and Countries are Always Populated:**
   - Zero missing names or countries across all 14.7M rows.
   - Company name is the single most reliable universal matching feature.

3. **Missing Addresses in Sources 2 & 3 (~3.3%):**
   - Source 1 has 100% populated addresses.
   - Source 2 has **168,967 blank addresses (3.36%)**.
   - Source 3 has **175,916 blank addresses (3.33%)**.
   - Combined, over **344,000 records** lack street addresses.

4. **Singletons in Source 1 (~5.6%):**
   - Exactly **123,247 Source 1 entities (5.58%)** have zero corresponding matches in Source 2 or Source 3.

5. **Multi-Source Match Duplication (>80%):**
   - 80.48% of matched entities have matching records in **both** Source 2 and Source 3.
   - Ground truth contains up to 11 matches per Source 1 entity (mean: 3.46 matches).
   - Invariant: Each Source 2 and Source 3 record links to at most one Source 1 entity.

6. **Open-Set Country Field:**
   - Training contains ~60% US and ~40% India.
   - Test data introduces **France** (e.g. `S1-156285671`, `<< Team Ecole`, `France`).

---

## 2. Critical Preprocessing Rationale

### Why Missing Addresses Must Be Handled Safely
- Over 344,000 records in Sources 2 & 3 have empty or missing address fields (`NaN`, `None`, or empty tab fields `""`).
- If address normalization or feature extraction assumed non-empty strings, it would either:
  1. Crash the pipeline with `TypeError` or `AttributeError`.
  2. Cause downstream blocking rules to inadvertently drop hundreds of thousands of legitimate candidate matches.
- **Our Implementation:** `normalize_address()` and `tokenize_text()` safely return `""` and `[]` for missing values. A helper `is_missing_address()` is provided so downstream modules can incorporate address missingness into candidate generation and model features.

### Why Singletons Matter
- Under the competition's **Macro-averaged $F_{0.5}$** metric, precision is weighted twice as heavily as recall:
  $$F_{0.5} = \frac{1.25 \times \text{Precision} \times \text{Recall}}{0.25 \times \text{Precision} + \text{Recall}}$$
- For a true singleton entity (where true matches $= \emptyset$):
  - Predicting an empty list yields a perfect score of **1.0**.
  - Predicting even a single false match drops that entity's score directly to **0.0**.
- **Our Implementation:** Preprocessing is strictly non-destructive and neutral. It does not force-link or assume every record must find a match.

### Why Duplicate Source Records Must Be Preserved
- Over 80% of matched businesses exist as multiple distinct noisy records across Source 2 and Source 3.
- If preprocessing attempted to aggressively deduplicate records *within* Source 2 or Source 3 prior to blocking, legitimate ground-truth matches would be permanently deleted, artificially capping recall.
- **Our Implementation:** Every source row is preserved one-to-one. Preprocessing only adds standardized columns, never filtering or dropping rows.

### Why Country Must Remain Open-Set
- While training data only contains `US` and `India`, test data introduces `France` and potentially other nations.
- Hardcoding country logic (such as `if country in ["US", "India"]` or a fixed country enum) would fail on the test set.
- **Our Implementation:** `normalize_country()` treats all country inputs as open-set strings, applying universal casing, whitespace, and character normalization without filtering.

---

## 3. Normalization Specifications

The preprocessing module ([`preprocessing.py`](file:///c:/Users/Anisa%20Islam/OneDrive/Documents/Desktop/business-entity-resolution/code/business_entity_resolution/src/preprocessing.py)) implements conservative, non-destructive normalization:

| Step | Technique | Example Input | Output | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **Unicode Standardization** | NFKC normalization | `Café` / non-breaking space | Standardized unicode | Eliminates ligature & encoding variations |
| **Casing** | Lowercase conversion | `ACME CORP` | `acme corp` | Case-insensitive alignment |
| **Ampersand** | Regex replacement | `Johnson & Johnson` | `johnson and johnson` | Harmonizes `&` and `and` variations |
| **Punctuation** | Punctuation to space | `B+ Retail, Inc.` | `b retail inc` | Cleans delimiter noise while keeping word boundaries |
| **Whitespace** | Strip & collapse | `  Main    St.  ` | `main st` | Removes irregular spacing |
| **Legal Terms** | Preserved intact | `Apex Logistics LLC` | `apex logistics llc` | Retains distinguishing entity type markers |
| **Missing Values** | Safe null handling | `np.nan` / `None` / `""` | `""` (tokens: `[]`) | Prevents pipeline crashes on blank addresses |

---

## 4. Reusable API Summary

Downstream team members (blocking, feature engineering, modeling) can directly import and use:

```python
from src.preprocessing import (
    normalize_text,
    normalize_business_name,
    normalize_address,
    normalize_country,
    is_missing_address,
    tokenize_text,
    preprocess_dataframe,
)
```

- **`preprocess_dataframe(df)`**: Takes any dataset DataFrame (`Source 1`, `Source 2`, or `Source 3`, for either `train` or `test`), preserves all original columns, and appends:
  - `business_name_clean`: Conservatively cleaned business name string.
  - `business_address_clean`: Conservatively cleaned address string (`""` if missing).
  - `country_clean`: Conservatively cleaned open-set country string.
  - `business_name_tokens`: List of lowercase name word tokens (`List[str]`).
  - `business_address_tokens`: List of lowercase address word tokens (`List[str]`).
