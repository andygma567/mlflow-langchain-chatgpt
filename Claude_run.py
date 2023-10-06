# Log the results of using Claude to mlflow
import pandas as pd
import mlflow
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process website")
    parser.add_argument(
        "--website", type=str, required=True, help="Website to summarize"
    )
    args = parser.parse_args()
    website = args.website

df = pd.DataFrame(columns=["url", "model", "outputs"])

with open("Claude.txt", "r") as f:
    text = f.read()

df.loc[0] = [website, "Claude2", text]

# Set MLflow experiment
mlflow.set_experiment("youtube_summarization")

# Start MLflow run
with mlflow.start_run():
    # Log the dataframe as a table
    print("Logging table")
    mlflow.log_table(data=df, artifact_file="prediction_results.json")
