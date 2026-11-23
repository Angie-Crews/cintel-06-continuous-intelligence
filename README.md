# cintel-06-continuous-intelligence

[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](pyproject.toml)
[![CI](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/actions/workflows/ci-python-zensical.yml/badge.svg)](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/actions/workflows/ci-python-zensical.yml)
[![Documentation](https://img.shields.io/badge/docs-site-blue?logo=github)](https://angie-crews.github.io/cintel-06-continuous-intelligence/)

[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

> Combine monitoring signals and anomaly detection to assess system health.

## Project Overview

**Author:** Angie Crews
**Date:** November 2026

This project combines techniques learned throughout the Continuous Intelligence course to monitor and evaluate system health.

The application uses system metrics to identify unusual activity, measure performance, and classify system conditions.

It includes:

- Signal design to calculate error rates, average latency, and throughput.
- Anomaly detection using defined thresholds.
- Individual observation classifications of STABLE, WARNING, or CRITICAL.
- An overall system health assessment.
- An interactive Marimo application with adjustable thresholds and a color-coded chart.

The goal is to show how monitoring individual observations and overall system performance can help identify potential problems.

The project is configured in [pyproject.toml](pyproject.toml).

## Data

The example uses system metrics from `data/`.

Each observation includes:

- `requests` - number of requests handled.
- `errors` - number of failed requests.
- `total_latency_ms` - total response time in milliseconds.

The example uses stored observations to demonstrate
an integrated monitoring assessment.

## Approach

The pipeline uses Polars to:

1. Read system measurements.
2. Calculate error rate and average latency.
3. Identify signals exceeding defined thresholds.
4. Summarize system behavior.
5. Assign a system assessment based on the monitored signals.

Explore these project components:

- [pyproject.toml](pyproject.toml) - project configuration and dependencies.
- [src/cintel/continuous_intelligence.py](src/cintel/continuous_intelligence.py) - integrated monitoring pipeline.
- [data/](data/) - system measurements.
- [artifacts/](artifacts/) - generated system assessment.
- [tests/](tests/) - automated tests.
- [.github/workflows/](.github/workflows/) - automated checks and documentation deployment.
- [docs/](docs/) - project documentation.

## Run the Project

Follow the [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
to set up your machine and project environment.

From a VS Code terminal in the project root:

```shell
uv run python -m cintel.continuous_intelligence
```

## Run the Reactive App

From a VS Code terminal in the project root
(hit CTRL + c to quit):

```shell
uv run marimo run  src/cintel/app.py
```

## Results

The pipeline analyzed 60 system observations using two thresholds:

- Maximum error rate: 5%
- Maximum average latency: 40 milliseconds

Each observation is classified using three levels:

- 🟢 **STABLE** - No thresholds exceeded.
- 🟡 **WARNING** - One threshold exceeded.
- 🔴 **CRITICAL** - Two thresholds exceeded.

### Observation Health Summary

| Classification | Observations |
|---|---:|
| STABLE | 53 |
| WARNING | 5 |
| CRITICAL | 2 |
| **Total** | **60** |

Seven observations exceeded at least one threshold.

### Overall System Assessment

#### Overall System State: STABLE

The average error rate was approximately 2.65%, and average latency was 33.71 milliseconds.

Although the overall system was classified as STABLE, individual observations showed WARNING and CRITICAL conditions.

This demonstrates why monitoring individual observations is important even when overall averages appear normal.

### Interactive Visualization

The Marimo application includes:

- Adjustable error rate and latency thresholds.
- An observation health summary.
- A color-coded chart showing system conditions across 60 observations.
- An overall system assessment.
- A table of detected anomalies.

Changing the thresholds automatically updates the classifications and chart.

### Generated Artifacts

The pipeline creates:

- `artifacts/system_assessment.csv` - Overall system assessment.
- `artifacts/observation_assessments.csv` - Individual observation classifications.
- `project.log` - Pipeline execution log.

Successful execution displays:

```text
Pipeline executed successfully!
```

The Python pipeline and reactive application were tested locally.

## Project Documentation

The [hosted documentation site](https://angie-crews.github.io/cintel-06-continuous-intelligence/)
is published using Zensical and GitHub Pages.

The documentation includes project data, methods, results,
visualizations, interpretation, and conclusions.

## CI/CD and GitHub Actions

This project includes continuous integration and continuous deployment (CI/CD)
to check project files and publish the docs.
GitHub Actions include:

- [CI: Python and Documentation Checks](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/actions/workflows/ci-python-zensical.yml)
- [CD: Documentation Deployment](https://github.com/Angie-Crews/cintel-06-continuous-intelligence/actions/workflows/deploy-zensical.yml)

## Developer Reference

Follow the
[Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
for **detailed instructions and troubleshooting**.

### Initialize and Update the Python Environment

With the project open in VS Code, open a VS Code terminal.
Paste each command and hit Enter or Return after to run it.

```shell
uvx pup-clean --delete
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync
uv audit
```

### Set Up and Run Git Hooks

Set up and run the git hooks to perform
basic checks automatically before
any changes get pushed to GitHub.

In the VS Code terminal,
paste each command and hit Enter or Return after to run it.

```shell
uvx prek install --force
uvx prek update --freeze --cooldown-days 7

git add -A
uvx prek run --all-files
# repeat if changes were made
uvx prek run --all-files
```

### Run Common Chores

Run linters, formatters, type checks, tests, and
build the documentation.

```shell
uv run ruff check . --fix
uv run ruff format .

uv run ty check
uv run python -m pytest
uv run python -m zensical build
```

### Git add-commit-push to GitHub

After making useful changes, save your work to GitHub.

```shell
git add -A
git commit -m "describe your changes in quotes"
git push -u origin main
```

## Developer Notes

- Use the **UP ARROW** and **DOWN ARROW** in the terminal to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.

## Developer Tools

This project uses professional Python tools to support development,
testing, documentation, and code quality.

- [uv](https://docs.astral.sh/uv/) - Python environments and dependencies.
- [Ruff](https://docs.astral.sh/ruff/) - Python linting and formatting, configured in [.ruff.toml](.ruff.toml).
- [ty](https://docs.astral.sh/ty/) - Python type checking.
- [pytest](https://docs.pytest.org/) - automated Python testing, configured in [.pytest.toml](.pytest.toml).
- [prek](https://prek.j178.dev/) - Git hooks and automated checks, configured in [prek.toml](prek.toml).
- [Zensical](https://zensical.org/) - project documentation, configured in [zensical.toml](zensical.toml).

## Links

- [Hosted Documentation](https://angie-crews.github.io/cintel-06-continuous-intelligence/)
- [Professional Python Workflow Guide](https://denisecase.github.io/pro-analytics-02/)
- [Citation](CITATION.cff)
- [License](LICENSE)
