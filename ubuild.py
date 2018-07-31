import os
import sys
import subprocess
from uranium import task_requires


LANGUAGE_MODEL = "en_core_web_md"


def main(build):
    build.packages.install("numpy", version="==1.13.0")
    build.packages.install("spacy")
    build.packages.install("coloredlogs")
    build.packages.install("scipy")
    build.packages.install("scikit-learn")
    build.packages.install("sklearn_crfsuite")
    build.packages.install(".", develop=True)
    build.executables.run([
        sys.executable, "-m", "spacy", "download", LANGUAGE_MODEL,
    ])


def train_model(build):
    build.executables.run([
        sys.executable, "-m", "rasa_nlu.train",
        "--config", os.path.join(build.root, "config", "config_spacy.yml"),
        "--data", os.path.join(build.root, "data", "training-set.json"),
        "--path", os.path.join(build.root, "projects"),
    ])


def dev(build):
    build.executables.run([
        sys.executable, "-m", "rasa_nlu.server",
        "--path", os.path.join(build.root, "projects"),
    ])


def run_app(build):
    build.executables.run([
        sys.executable,
        os.path.join(build.root, "yoyo_bot", "app.py"),
    ])


@task_requires("main")
def test(build):
    build.packages.install("pytest")
    build.packages.install("radon")
    build.packages.install("coverage")
    build.executables.run([
        "coverage", "run", "--append",
        "--source=yoyo_bot",
        "./bin/pytest", "./tests",
    ] + build.options.args)
    build.executables.run([
        "coverage", "report", "-m"
    ])


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload"
    ])
