# Public Release Checklist

Before releasing or pushing updates to this public repository, ensure all the following points have been verified:

- [ ] Review that there are no proprietary CSV/Excel datasets.
- [ ] Review that there are no trained models (`.joblib`, `.pkl`) derived from restricted sources.
- [ ] Review that there are no Jupyter notebooks containing outputs of confidential data.
- [ ] Review that there are no hardcoded local paths (e.g., `C:\Users\...`).
- [ ] Review that there are no Word or PDF files corresponding to the submitted manuscript.
- [ ] Review that `data/` only contains approved public datasets.
- [ ] Review that `results/` only contains results derived from approved public literature.
- [ ] Run `python -m pytest` and ensure all tests pass.
- [ ] Review `git status` before committing.
- [ ] Review `git diff` before committing to ensure no unintended files or changes are included.
- [ ] Confirm that the Literature Validation Set was reviewed column by column before publishing to guarantee no proprietary data leaked.
