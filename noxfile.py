import os
import pathlib
import shutil
from itertools import chain

import nox

PROJECT = "bmi-topography"
PACKAGE = PROJECT.replace("-", "_")
HERE = pathlib.Path(__file__)
ROOT = HERE.parent
PATHS = [PACKAGE, "docs", "examples", "tests", HERE.name]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]


@nox.session(python=PYTHON_VERSIONS)
def test(session: nox.Session) -> None:
    """Run the tests."""
    session.install(".[testing]")

    args = [
        "--cov",
        PACKAGE,
        "-vvv",
    ] + session.posargs

    if "CI" in os.environ:
        args.append(f"--cov-report=xml:{ROOT.absolute()!s}/coverage.xml")
        args.append(f"--cov-config={ROOT.absolute()!s}/pyproject.toml")
    session.run("pytest", *args)

    if "CI" not in os.environ:
        session.run("coverage", "report", "--ignore-errors", "--show-missing")


@nox.session(name="test-bmi", python=PYTHON_VERSIONS, venv_backend="conda")
def test_bmi(session: nox.Session) -> None:
    """Test the Basic Model Interface."""
    session.install("bmi-tester>=0.5.9")
    session.install(".")
    session.run(
        "bmi-test",
        f"{PACKAGE}:BmiTopography",
        "--config-file",
        f"{ROOT}/examples/config.yaml",
        "--root-dir",
        "examples",
        "-vvv",
    )


@nox.session(name="test-cli", python=PYTHON_VERSIONS)
def test_cli(session: nox.Session) -> None:
    """Test the command line interface."""
    session.install(".")
    session.run(PROJECT, "--version")
    session.run(PROJECT, "--help")


@nox.session(name="check-notebooks", python=PYTHON_VERSIONS[-1])
def check_notebooks(session: nox.Session) -> None:
    """Run the example notebooks."""
    session.install(".[testing,examples]")
    session.install("nbmake")

    args = [
        "examples",
        "--nbmake",
        "--nbmake-kernel=python3",
        "--nbmake-timeout=3000",
        "-vvv",
    ] + session.posargs

    session.run("pytest", *args)


@nox.session
def lint(session: nox.Session) -> None:
    """Clean lint and assert style."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files")


@nox.session(name="prepare-docs")
def prepare_docs(session: nox.Session) -> None:
    """Update docs source before building."""
    session.run("sphinx-apidoc", "-f", "-o", "docs/source/api", PACKAGE)
    for file in ["README", "CHANGES", "CONTRIBUTING", "CODE-OF-CONDUCT", "LICENSE"]:
        session.run(
            "pandoc", "--to", "rst", f"{file}.md", "--output", f"docs/source/{file}.rst"
        )


@nox.session(name="build-docs", venv_backend="conda")
def build_docs(session: nox.Session) -> None:
    """Build the docs."""
    session.conda_install("--file", "docs/requirements.txt")
    session.install("-e", ".")

    prepare_docs(session)

    if os.path.exists("build"):
        shutil.rmtree("build")
    session.run("sphinx-build", "-b", "html", "-W", "docs/source", "build/html")


@nox.session
def build(session: nox.Session) -> None:
    """Build source and binary distributions."""
    session.install(".[build]")
    session.run("python", "-m", "build")


@nox.session
def release(session):
    """Tag, build, and publish a new release to PyPI."""
    session.install(".[build]")
    session.run("fullrelease")


@nox.session(name="testpypi")
def publish_testpypi(session):
    """Upload package to TestPyPI."""
    build(session)
    session.run("twine", "check", "dist/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "--repository-url",
        "https://test.pypi.org/legacy/",
        "dist/*",
    )


@nox.session(name="pypi")
def publish_pypi(session):
    """Upload package to PyPI."""
    build(session)
    session.run("twine", "check", "dist/*")
    session.run(
        "twine",
        "upload",
        "--skip-existing",
        "--repository-url",
        "https://upload.pypi.org/legacy/",
        "dist/*",
    )


@nox.session(python=False)
def clean(session):
    """Remove virtual environments, build files, and caches."""
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("docs/build", ignore_errors=True)
    shutil.rmtree(f"{PACKAGE}.egg-info", ignore_errors=True)
    shutil.rmtree(".pytest_cache", ignore_errors=True)
    shutil.rmtree(".venv", ignore_errors=True)
    if os.path.exists("coverage.xml"):
        os.remove("coverage.xml")
    if os.path.exists(".coverage"):
        os.remove(".coverage")
    for p in chain(ROOT.rglob("*.py[co]"), ROOT.rglob("__pycache__")):
        if p.is_dir():
            p.rmdir()
        else:
            p.unlink()


@nox.session(python=False)
def nuke(session):
    """Clean and also remove the .nox directory."""
    clean(session)
    shutil.rmtree(".nox", ignore_errors=True)
