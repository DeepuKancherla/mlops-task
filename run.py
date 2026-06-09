import argparse
import json
import logging
import time
import yaml
import pandas as pd
import numpy as np
import os
import sys


def load_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    required = ["seed", "window", "version"]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing config field: {key}")

    return config


def load_dataset(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError("Input file not found")

    try:
        df = pd.read_csv(file_path)
    except Exception:
        raise ValueError("Invalid CSV format")

    if df.empty:
        raise ValueError("Dataset is empty")

    if "close" not in df.columns:
        raise ValueError("Missing required column: close")

    return df


def process_data(df, window):

    df["close"] = pd.to_numeric(
        df["close"],
        errors="coerce"
    )

    df["rolling_mean"] = (
        df["close"]
        .rolling(window=window)
        .mean()
    )

    df["signal"] = (
        df["close"] > df["rolling_mean"]
    ).astype(int)

    return df


def save_metrics(metrics, output_path):

    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    start_time = time.time()

    logging.info("Job Started")

    try:

        config = load_config(args.config)

        logging.info(
            f"Config Loaded: seed={config['seed']}, "
            f"window={config['window']}, "
            f"version={config['version']}"
        )

        np.random.seed(config["seed"])

        df = load_dataset(args.input)

        logging.info(f"Rows Loaded: {len(df)}")

        df = process_data(
            df,
            config["window"]
        )

        logging.info("Rolling Mean Computed")
        logging.info("Signal Generated")

        latency_ms = int(
            (time.time() - start_time) * 1000
        )

        metrics = {
            "version": config["version"],
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": round(
                float(df["signal"].mean()),
                4
            ),
            "latency_ms": latency_ms,
            "seed": config["seed"],
            "status": "success"
        }

        save_metrics(
            metrics,
            args.output
        )

        logging.info(f"Metrics: {metrics}")
        logging.info("Job Completed Successfully")

        print(
            json.dumps(metrics, indent=2)
        )

    except Exception as e:

        logging.exception("Job Failed")

        metrics = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        save_metrics(
            metrics,
            args.output
        )

        print(
            json.dumps(metrics, indent=2)
        )

        sys.exit(1)


if __name__ == "__main__":
    main()