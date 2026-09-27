# Project Insights & Conclusions

**Role:** Anisa (Person 1 — Data Cleaning & Insights)  
**About this file:** A simple, plain-English summary of what we learned from our data so far. Easy to read, easy to present, and ready for adding future conclusions!

---

## 💡 What We Did So Far

1. **Created a Safe Text Cleaner**
   - Cleaned company names and addresses so they are easier to match (lowercase, removed punctuation noise, turned `&` into `and`).
   - Kept important business tags intact (like *Inc, LLC, Ltd, Corp*) so we don't accidentally confuse two different companies.
   - Handled empty values safely so the code never crashes.

2. **Audited the Entire Dataset (14.7 Million Records)**
   - Checked every single row across all 4 training files before our team starts building machine learning models.
   - Verified that company IDs, addresses, and answer keys are solid.

---

## 🔍 The 4 Big Takeaways (What the Data Tells Us)

### 1. The IDs Are 100% Clean
- No typo IDs, no duplicate company codes, and no broken links.
- Every match listed in the answer key really exists in the datasets.

### 2. Watch Out for Missing Addresses (~3.3%)
- Company names and countries are always present.
- However, **over 340,000 records in Sources 2 & 3 have completely blank addresses**.
- **Takeaway:** We cannot rely *only* on addresses to find matching companies. Name matching is essential!

### 3. Some Companies Have Zero Matches (~5.6%)
- Around 123,000 companies in Source 1 do not exist in Source 2 or Source 3. They are completely alone ("singletons").
- In this competition, guessing a false match for these alone companies heavily hurts our final score.
- **Takeaway:** When in doubt, it is better to say "no match" than to guess incorrectly.

### 4. Matches Usually Appear in Both Sources (~80%)
- When a company does have matches, **more than 80% of the time it appears in BOTH Source 2 and Source 3**.
- On average, a matching company has 3 to 4 duplicate records across the databases.
- Each record in Sources 2 and 3 belongs to only one parent company (no messy overlapping splits).

---

## 🎯 Simple Advice for the Team

- **For Candidate Search (Person 2):**  
  Do not search using address alone, because 3.3% of companies have no address. Always include the company name in your search rules!
- **For Feature Engineering & Models (Person 3):**  
  Keep track of whether an address was missing. Company name words are the most reliable signal across all records.
- **For Decision Thresholds & Scoring (Person 4):**  
  Be strict with matching confidence. It's much safer to predict "no match" for uncertain cases than to make a wrong guess.

---

## 📝 Future Conclusions & Notes

*(Add new findings here as we finish future steps!)*

### Step 4: Deep-Dive EDA & Pattern Analysis (Completed)
- **What we did:**
  Analyzed all 26.4 million records across both training and test sets, and tested 86,000+ real match pairs to see how companies actually look when they match.
- **The 4 Golden Rules Discovered:**
  1. **Country is 100% reliable:** True matches never cross country borders. Filtering by country cuts our search work in half with zero risk.
  2. **Never rely on exact name matching:** Only 21% of real matches have identical cleaned names. 79% have typos, legal tag differences, or dropped words.
  3. **Watch out for duplicate names (chains & branches):** Over 5,600 business names appear in multiple different towns. If we don't check street numbers, we will accidentally merge different branches together.
  4. **When in doubt, predict "no match":** The scoring system punishes false guesses twice as hard as missed matches.
- **Hand-off to the team:**
  - **Sahiti (Person 2):** Ready to build candidate search using country + name tokens.
  - **Hajira (Person 3):** Ready to build features using name similarity, street numbers, and a missing-address flag.

---

### Step 5: Preprocessing Verification & Final Review (Completed)
- **What we checked:**
  1. **All 3 Normalizers are ready:**
     - `BusinessNameNormalizer` (cleans company names, preserves business types like Inc/LLC).
     - `AddressNormalizer` (cleans street addresses, handles blank addresses without crashing).
     - `CountryNormalizer` (open-set cleaner: supports US, India, France, and any other country).
  2. **France is 100% protected:**
     - Verified that French companies (14.4% of the test set) are never filtered or dropped. Every test company will be preserved for the final submission.
  3. **Safety & Zero Disruption:**
     - Verified all 7 raw dataset files are untouched.
     - Verified protected team modules (`config.py`, `pipeline.py`, `blocking/`, `matching/`) are untouched.
     - Ran 12 automated checks on real train and test records: **All 12 passed with zero errors**.
- **Final Verdict for Person 1 (Anisa):**  
  Data Understanding, Preprocessing, and EDA are 100% complete, fully tested, documented, and ready for team integration!

---

*(Add new findings here as we finish future steps!)*


