# Utility Scripts

This directory contains auxiliary and validation scripts provided for the challenge.

## Challenge Validation Script
Place `validate_submission.py` in this directory.

Run validation using:
```bash
python3 utils/validate_submission.py \
  --matching output/matching_results.tsv \
  --candidate output/candidate_pairs.tsv \
  --test-dir dataset/test
```

> **Note**: Do not modify the challenge validation script `validate_submission.py`.
