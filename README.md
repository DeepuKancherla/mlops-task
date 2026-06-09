# ML/MLOps Technical Assessment

## Overview

This project implements a minimal MLOps-style batch processing pipeline.

Features:

* YAML-based configuration
* Deterministic execution using seed
* Rolling mean computation
* Binary signal generation
* Structured metrics output
* Logging
* Dockerized execution

## Requirements

* Python 3.9+
* pandas
* numpy
* pyyaml

## Local Installation

```bash
pip install -r requirements.txt
```

## Local Run

```bash
python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log
```

## Docker Build

```bash
docker build -t mlops-task .
```

## Docker Run

```bash
docker run --rm mlops-task
```

## Example Output

```json
{
  "version": "v1",
  "rows_processed": 10001,
  "metric": "signal_rate",
  "value": 0.4989,
  "latency_ms": 27,
  "seed": 42,
  "status": "success"
}
```
