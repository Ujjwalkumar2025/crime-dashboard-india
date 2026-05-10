# Milestone Feedback

Project: P25 - India Crime Intelligence Dashboard
Repo: `Ujjwalkumar2025/crime-dashboard-india`
Official milestone score after post-lock recovery: 14/20
Post-lock sanity-check score: 17/20
Band: `major_revision`
Reviewed at: 2026-05-10T09:30:11

This is the official milestone feedback after applying the post-lock recovery policy. The locked May 6 snapshot remains the baseline, but real, reproducible fixes made after lock can recover 50% of the lost milestone points.

## Score Recovery Applied

- Locked milestone score: 11/20
- Post-lock sanity-check score: 17/20
- Official milestone score: 14/20
- Formula: locked score + 50% of the post-lock improvement

## Graduating-Student Timeline

This team includes graduating student(s): Ujjwal Kumar (ma2024).
To help us meet the May 15 grade-publishing deadline from OAA, please aim to submit the final version by May 13 if possible, and no later than May 14, 2026 at 11:59 PM IST.

## Rubric Breakdown

- Charter lock: 1/4. the charter is not recorded as approved; charter file exists and is not obviously template; the milestone manifest does not confirm charter lock
- Source access proof: 4/4. source/probe evidence is present and usable
- Baseline before sophistication: 4/4. `outputs/baseline_metric.json` is readable and contains a real metric/value
- Reproducible dry run: 4/4. `uv run main.py` succeeds and writes the required milestone outputs
- Metric schema readiness: 4/4. `outputs/primary_metric.json` is readable and machine-checkable

## Policy Notes

- post-lock recovery policy applied: locked score 11/20; post-lock sanity check 17/20; official score = 11 + 50% of (17 - 11) = 14/20

## What To Fix Next

- Make the charter unambiguous: final question, dataset, primary metric, baseline, scope limits, and team roles should all be visible in `CHARTER.md`.

## Final Phase Guidance

- The project is viable, but the final phase should start with cleanup. Close the mechanical gaps first, then deepen the analysis.
- For the final submission, keep the repo as the source of truth: `README.md`, `CHARTER.md`, `main.py`, `outputs/`, `report.md`, and `AI_USAGE_LOG.md` should tell one consistent story.

Please treat this feedback as a way to make the final week calmer, not as a ceiling on the final project. A clear, reproducible, honestly interpreted final submission can still be strong.
