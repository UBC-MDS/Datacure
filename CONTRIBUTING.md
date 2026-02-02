# Contributing

Contributions of all kinds are welcome here, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

## Example Contributions

You can contribute in many ways, for example:

* [Report bugs](#report-bugs)
* [Fix Bugs](#fix-bugs)
* [Implement Features](#implement-features)
* [Write Documentation](#write-documentation)
* [Submit Feedback](#submit-feedback)

### Report Bugs

Report bugs at https://github.com/UBC-MDS/datacure/issues.

**If you are reporting a bug, please follow the template guidelines. The more
detailed your report, the easier and thus faster we can help you.**

### Fix Bugs

Look through the GitHub issues for bugs. Anything labelled with `bug` and
`help wanted` is open to whoever wants to implement it. When you decide to work on such
an issue, please assign yourself to it and add a comment that you'll be working on that,
too. If you see another issue without the `help wanted` label, just post a comment, the
maintainers are usually happy for any support that they can get.

### Implement Features

Look through the GitHub issues for features. Anything labelled with
`enhancement` and `help wanted` is open to whoever wants to implement it. As
for [fixing bugs](#fix-bugs), please assign yourself to the issue and add a comment that
you'll be working on that, too. If another enhancement catches your fancy, but it
doesn't have the `help wanted` label, just post a comment, the maintainers are usually
happy for any support that they can get.

### Write Documentation

Datacure could always use more documentation, whether as
part of the official documentation, in docstrings, or even on the web in blog
posts, articles, and such. Just
[open an issue](https://github.com/UBC-MDS/datacure/issues)
to let us know what you will be working on so that we can provide you with guidance.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/UBC-MDS/datacure/issues. If your feedback fits the format of one of
the issue templates, please use that. Remember that this is a volunteer-driven
project and everybody has limited time.

## Get Started!

Ready to contribute? Here's how to set up Datacure for
local development.

1. Fork the https://github.com/UBC-MDS/datacure
   repository on GitHub.
2. Clone your fork locally (*if you want to work locally*)

    ```shell
    git clone git@github.com:your_name_here/datacure.git
    ```

3. [Install hatch](https://hatch.pypa.io/latest/install/).

4. Create a branch for local development using the default branch (typically `main`) as a starting point. Use `fix` or `feat` as a prefix for your branch name.

    ```shell
    git checkout main
    git checkout -b fix-name-of-your-bugfix
    ```

    Now you can make your changes locally.

5. When you're done making changes, apply the quality assurance tools and check
   that your changes pass our test suite. This is all included with tox

    ```shell
    hatch run test:run
    ```

6. Commit your changes and push your branch to GitHub. Please use [semantic
   commit messages](https://www.conventionalcommits.org/).

    ```shell
    git add .
    git commit -m "fix: summarize your changes"
    git push -u origin fix-name-of-your-bugfix
    ```

7. Open the link displayed in the message when pushing your new branch in order
   to submit a pull request.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put your
   new functionality into a function with a docstring.
3. Your pull request will automatically be checked by the full test suite.
   It needs to pass all of them before it can be considered for merging.

## Development Practices & Scaling Discussion

### Development Tools Used 

The project uses a set of development tools to support testing, documentation, and reliable collaboration throughout the development process.

- **GitHub Actions**: Used for automated testing, documentation builds, and checks on every pull request.
- **pytest**: Used as the testing framework with coverage tracking to ensure core functionality is well tested.
- **Quarto and quartodoc**: Used to generate and maintain project documentation directly from source code and markdown files.
- **Semantic versioning**: Used to communicate changes clearly and consistently across releases.

### GitHub Infrastructure and Workflow

GitHub provides the main infrastructure for collaboration, code review, and workflow automation in this project.

- **GitHub Issues**: Used to track tasks, discussions, and design decisions.
- **Pull Requests**: Used to propose changes, enable code review, and trigger automated checks before merging.
- **Branching strategy**: A Git Flow–style workflow is followed, with a development branch used to integrate changes before merging into the main branch.
- **CI workflows**: GitHub Actions workflows are used for automated testing and documentation, including separate workflows for documentation preview and final publication.

### Organizational Practices

The project follows collaborative development practices to improve code quality, maintainability, and team coordination. These practices help ensure that contributions are clear, reviewable, and consistent.

- **Feature branches**: In milestone 4, changes are developed in feature branches to isolate work and reduce the risk of conflicts.
- **Code review**: Pull requests are reviewed before merging to improve code quality.
- **Commit and PR conventions**: Clear and descriptive commit messages and pull request descriptions are used to make changes easier to understand.
- **Docstrings and tests**: Functions and tests include docstrings, and tests are written to verify core functionality and expected behavior.


### Scaling Considerations

If this project were to grow in scope or attract more contributors, additional tools and practices would be adopted to better manage complexity and collaboration. 

- **Stricter pull request reviews**: With more contributors, requiring more thorough PR reviews.
- **Issue templates and labels**: Using structured issue templates and consistent labels would improve issue tracking and make it easier to prioritize and manage tasks.
- **Release notes and versioning**: Maintaining clear release notes alongside semantic versioning would help users understand changes and upgrades as the project evolves.
- **Expanded CI pipelines**: As the codebase grows, CI workflows could be extended to include test matrices, coverage thresholds, and additional checks to reduce the risk of regressions.



