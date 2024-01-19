# Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

## Types of Contributions

### Report Bugs

Report bugs at <https://github.com/csdms/bmi-topography/issues>.

If you are reporting a bug, please include:

-   Your operating system name and version.
-   Any details about your local setup that might be helpful in
    troubleshooting.
-   Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug"
and "help wanted" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with
"enhancement" and "help wanted" is open to whoever wants to
implement it.

### Write Documentation

*bmi-topography* could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog
posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/csdms/bmi-topography/issues>.

If you are proposing a feature:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible, to make it easier to
    implement.
-   Remember that this is a volunteer-driven project, and that
    contributions are welcome :)

## Get Started!

Ready to contribute? Here\'s how to set up *bmi-topography* for local
development.

1.  Fork the *bmi-topography* repo on GitHub.

2.  Clone your fork locally:

    ``` {.shell}
    $ git clone git@github.com:your_name_here/bmi-topography.git
    ```

3.  Install your local copy into a conda environment. A conda enviroment file is
    supplied at the root of the repository. Assuming you have conda installed,
    this is how you set up your fork for local development:

    ``` {.shell}
    $ cd bmi-topography
    $ conda env create --file=environment.yml
    $ conda activate topography
    ```

4.  Create a branch for local development:

    ``` {.shell}
    $ git checkout -b name-of-your-bugfix-or-feature
    ```

    Now you can make your changes locally.

5.  When you're done making changes, check that your changes pass
    ruff and the tests:

    5.1. Optional, check available `nox` test stages. Ref: [`nox` docs -> list all available sessions](https://nox.thea.codes/en/stable/usage.html#listing-available-sessions).
    ``` {.shell}
    $ nox --list
    ```
    5.2. Run linter and test. Ref: [`nox` docs -> run a particular set of sessions](https://nox.thea.codes/en/stable/usage.html#specifying-one-or-more-sessions).
    ``` {.shell}
    $ nox -s format
    $ nox -s test
    ```

    Both ruff and pytest are included in the environment.

    <sup> ‡ </sup>Tests may require user's API key. Create environmental
    variable, `OPENTOPOGRAPHY_API_KEY` or use api key dot file,
    `.opentopography.txt`.

6.  Commit your changes and push your branch to GitHub:

    ``` {.shell}
    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature
    ```

7.  Submit a pull request through the GitHub website.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  If the pull request adds functionality, the docs should be updated.
    Put your new functionality into a function with a docstring, and add
    the feature to the list in README.rst.
3.  The pull request need only work with Python >= 3.8.


## Deploying

A reminder for the maintainers on how to deploy. To make a new release,
you will need to have
[zest.releaser](https://zestreleaser.readthedocs.io/en/latest/)
installed, which can be installed with *pip*,

``` {.bash}
$ pip install zest.releaser[recommended]
```

Make sure all your changes are committed (including an entry in
CHANGES.md). Then run,

``` {.bash}
$ fullrelease
```

This will create a new tag and alert the *bmi-topography* feedstock on
*conda-forge* that there is a new release.
