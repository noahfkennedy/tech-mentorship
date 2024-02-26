import ast
import logging
import os
import subprocess
import sys

bashrc_message = """
WELCOME TO DEV MODE IN GCP
YOU ARE CURRENTLY SET UP TO WRITE MODELS OUT TO {project}.{dataset}
TO AUTHENTICATE TO BIGQUERY YOU NEED TO EXECUTE THE FOLLOWING COMMAND IN YOUR CONTAINER'S TERMINAL:
    $ gcloud auth application-default login
ONCE YOU HAVE RUN THIS COMMAND AND AUTHENTICATED THROUGH THE BROWSER
YOU CAN FREELY RUN DBT COMMANDS AS USUAL.
"""

def init_logging():
    logger = logging.getLogger(__name__)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(f"[%(asctime)s] {{%(name)s}} %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger


def install_dbt_dependencies(logger):
    dbt_cmd = ["dbt", "deps"]
    logger.info(f"RUNNING DBT COMMAND: {' '.join(dbt_cmd)}\n")
    return subprocess.run(dbt_cmd, shell=True)


def check_dbt_connection(logger, profile):
    dbt_cmd = ["dbt", "debug", "--profile", profile]
    logger.info(f"RUNNING DBT COMMAND: {' '.join(dbt_cmd)}\n")
    return subprocess.run(dbt_cmd)


def dbt_run(logger, profile, models, exclude):
    dbt_cmd = ["dbt", "run", "--profile", profile, "--select", models]
    logger.info(f"RUNNING DBT COMMAND: {' '.join(dbt_cmd)}\n")
    if exclude:
        dbt_cmd.extend(["--exclude", exclude])
    return subprocess.run(dbt_cmd)


def run_interactive_dbt(logger):
    os.system("clear")

    project_id = 'tech-mentorship-2024'
    target_dataset = "tech_mart"

    logger.info(f"Running entrypoint.py with project:{project_id} target: {target_dataset}")
    logger.info(bashrc_message.format(project=project_id, dataset=target_dataset))

    os.system("exec /bin/bash -i")


if __name__ == "__main__":
    os.system("clear")
    LOGGER = init_logging()

    LOGGER.info("=== START ===")

    # set default dbt profiles dir
    os.environ["DBT_PROFILES_DIR"] = "/dbt/profiles"

    ENV = 'prd'

    # DE Mart contributors will read data from our prod BQ but write to their dedicated GCP project when developing
    os.environ["PROJECT_ID"] = 'tech-mentorship-2024'

    install_dbt_dependencies(LOGGER)
    run_interactive_dbt(logger=LOGGER)

    LOGGER.info("=== END ===")
