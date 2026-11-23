# Continuous Intelligence System Assessment

Continuous Intelligence | Project 06 | Custom Project

**Author:** Angie Crews
**Date:** November 2026

## Overview

This project combines signal design, anomaly detection, and system assessment into a continuous intelligence pipeline.

The objective is to evaluate system performance using both overall averages and individual observations.

The project expands the original two-level assessment into three health classifications:

- 🟢 **STABLE** - No thresholds exceeded.
- 🟡 **WARNING** - One threshold exceeded.
- 🔴 **CRITICAL** - Two thresholds exceeded.

An interactive Marimo application allows users to adjust thresholds and observe how system classifications change.

## Data

The dataset contains 60 observations of system activity.

Each observation records:

- Requests handled.
- Errors encountered.
- Total response time in milliseconds.

The dataset includes a period of elevated errors and response times.

[View System Metrics Dataset](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/blob/main/data/system_metrics.csv)

## Methods

The pipeline uses Polars to process system metrics and evaluate system health.

### 1. Signal Design

Raw measurements are transformed into:

- **Error rate:** Errors divided by requests.
- **Average latency:** Total latency divided by requests.
- **Throughput:** A calculated monitoring signal.

### 2. Anomaly Detection

Individual observations are flagged when:

- Error rate exceeds 5%, or
- Average latency exceeds 40 milliseconds.

### 3. Three-Level System Assessment

The customized project evaluates how many thresholds each observation exceeds.

| Classification | Thresholds Exceeded | Interpretation |
|---|---:|---|
| 🟢 STABLE | 0 | Normal conditions |
| 🟡 WARNING | 1 | Potential performance concern |
| 🔴 CRITICAL | 2 | Multiple performance concerns |

The pipeline also calculates average measurements across all observations to determine the overall system state.

### 4. Interactive Monitoring

The Marimo application includes adjustable thresholds, observation classifications, and an interactive Altair chart.

Changing either threshold automatically updates the system health summary, chart, and anomaly results.

## Results

The pipeline successfully processed 60 observations.

### Observation Health Summary

| Classification | Observations | Percentage |
|---|---:|---:|
| 🟢 STABLE | 53 | 88.3% |
| 🟡 WARNING | 5 | 8.3% |
| 🔴 CRITICAL | 2 | 3.3% |
| **Total** | **60** | **100%** |

Seven observations exceeded at least one threshold.

### Overall System Assessment

| Metric | Result |
|---|---:|
| Average requests | 157.35 |
| Average errors | 4.03 |
| Average error rate | 2.65% |
| Average latency | 33.71 ms |
| Thresholds exceeded | 0 |
| Overall system state | STABLE |

[View Overall System Assessment](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/blob/main/artifacts/system_assessment.csv)

[View Individual Observation Assessments](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/blob/main/artifacts/observation_assessments.csv)

### Interactive Visualization

![System Health Across 60 Observations](images/system-health-chart.png)

The Marimo application displays a color-coded chart of all 60 observations.

- Green represents STABLE observations.
- Yellow represents WARNING observations.
- Red represents CRITICAL observations.

The chart responds to changes in the error rate and latency sliders.

[Open the Reactive App](./app/index.html)

## Interpretation

The overall system assessment was **STABLE** because the average error rate and latency remained below the configured thresholds.

However, the observation-level analysis identified:

- 53 stable observations.
- 5 warning observations.
- 2 critical observations.

This demonstrates that overall averages can hide shorter periods of performance problems.

Evaluating individual observations provides a clearer understanding of when system performance may require attention.

## Technical Modification and Experiment

The original project classified system health as STABLE or DEGRADED.

The customized version introduces three classifications and evaluates each observation individually.

The experiment was designed to determine whether additional classifications would provide more useful information about system performance.

The results showed that the overall system remained STABLE, while seven individual observations exceeded thresholds.

The modification provided additional information by distinguishing observations with one threshold violation from those with two.

## Limitations

The analysis uses a fixed dataset of 60 observations and manually selected thresholds.

The classifications indicate threshold violations but do not establish the actual severity or cause of a performance issue.

Although individual observations are now saved for further analysis, the project does not yet include:

- Rolling-window monitoring.
- Reference-period drift comparisons.
- Automated notifications.
- Continuous real-time data collection.

Future improvements could incorporate these techniques to provide more complete monitoring.

## Conclusion

This project demonstrates how continuous intelligence combines monitoring signals, anomaly detection, and system classification.

The most important finding is that **an overall STABLE assessment does not mean every individual observation is within acceptable limits**.

The three-level classification system and interactive visualization provide additional detail for identifying and investigating potential performance problems.

## Documentation Index

- **Home** - This landing page.
- [Project Instructions](project-instructions.md)
- [Glossary](glossary.md)
- [API](api.md)
- [Reactive App](./app/index.html)

## Project Links

- [GitHub Repository](https://github.com/Angie-Crews/cintel-06-continuous-intelligence)
- [Python Monitoring Pipeline](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/blob/main/src/cintel/continuous_intelligence.py)
- [Marimo Application](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/blob/main/src/cintel/app.py)
- [Results and Artifacts](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/tree/main/artifacts)

## Project Resources

- [Project Instructions](project-instructions.md)
- [Professional Python Guide](https://denisecase.github.io/pro-analytics-02/)
- [Professional Python Project Explainer](https://pup-pack.github.io/professional-python-project-explainer/)
- [Suggested Datasets](https://denisecase.github.io/pro-analytics-02/reference/datasets/cintel/)
