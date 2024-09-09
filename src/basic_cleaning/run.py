#!/usr/bin/env python
'''
NYC airbnb project: Data cleaning step

Author: TranTuanVu
Date: 9/9/2024
'''

import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    '''
    Download from W&B the raw dataset and apply some basic data cleaning,
    exporting the result to a new artifact

    input:
            args: input arguments
    output:
            None
    '''
    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning")
    run.config.update(args)
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Downloading artifact")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    logger.info("cleaning data")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    
    df.to_csv("clean_sample.csv", index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    logger.info("Logging artifact")
    run.log_artifact(artifact)    

    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str, # INSERT TYPE HERE: str, float or int,
        help="Fully-qualified name for the input artifact", # INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str, # INSERT TYPE HERE: str, float or int,
        help="Name for the artifact", # INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str, # INSERT TYPE HERE: str, float or int,
        help="Type for the artifact", # INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str, # INSERT TYPE HERE: str, float or int,
        help="Description for the artifact", # INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float, # INSERT TYPE HERE: str, float or int,
        help="min price", # INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float, # INSERT TYPE HERE: str, float or int,
        help="max price", # INSERT DESCRIPTION HERE,
        required=True
    )

    go(parser.parse_args())