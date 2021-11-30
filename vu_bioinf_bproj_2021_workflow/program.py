import json
import logging
import os
import argparse
from datetime import datetime

from docker_jobs.hello_world import HelloWorld
from docker_jobs.hhblits import Hhblits
from docker_jobs.opus_tass import OpusTass
from singularity_service import SingularityService


def setup_logging(configuration):
    log_folder = configuration["log_folder"]
    current_date_time = datetime.now().strftime("%Y%m%d%H%M%S")
    log_file_name = "log_" + current_date_time + ".log"
    logging.basicConfig(filename=log_folder + log_file_name, level=logging.DEBUG, datefmt="%H:%M:%S")


parser = argparse.ArgumentParser()
parser.add_argument("-dsf", "--datasetsfolder", help="Datasets super folder")
parser.add_argument("-ds", "--datasets", help="Dataset folder names")
args = parser.parse_args()

args.datasets = args.datasets.strip('[]').split(',')

dataset_locations = []
for dataset in args.datasets:
    if args.datasetsfolder is not None:
        dataset_locations.append(os.path.join(args.datasetsfolder, dataset))
    else:
        dataset_locations.append(dataset)

os.environ["SINGULARITY_DOCKER_USERNAME"] = "pctwass"
os.environ["SINGULARITY_DOCKER_PASSWORD"] = "3F5y2198Version2"
with open('appsettings.json') as f:
    config = json.load(f)
setup_logging(config)

logging.info("Initiating docker service.")
#docker_service = DockerService()

jobs_to_run = config["run_jobs"]

if "hello_world" in jobs_to_run:
    singularity_service = SingularityService("temp/hello_world")
    hello_world_job = HelloWorld(config, singularity_service)
    hello_world_job.run()

if "hhblits" in jobs_to_run:
    singularity_service = SingularityService(".")
    hhblits_job = Hhblits(config, singularity_service)
    for dataset_location in dataset_locations:
        hhblits_job.run(dataset_location)

if "opus_tass" in jobs_to_run or "opus_tass_train" in jobs_to_run:
    singularity_service = SingularityService(".")
    opus_tass_job = OpusTass(config, singularity_service)
    if "opus_tass_train" in jobs_to_run:
        opus_tass_job.train()
    if "opus_tass" in jobs_to_run:
        for dataset_location in dataset_locations:
            dataset = os.path.basename(os.path.normpath(dataset_location))
            opus_tass_job.run(dataset)
