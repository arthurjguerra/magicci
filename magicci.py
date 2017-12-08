#!/usr/local/bin/python3

from core.pipeline import Pipeline
import argparse
import os


def magic_ci(pipeline_name, repository):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    pipeline = Pipeline(root_dir, pipeline_name, repository)
    pipeline.run_job()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Magic CI CLI')
    parser.add_argument('pipeline_name', type=str, help='name of the pipeline (i.e. build, release)')
    parser.add_argument('repository', type=str, help='code repository URL')

    args = parser.parse_args()
    magic_ci(args.pipeline_name, args.repository)