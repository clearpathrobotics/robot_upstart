# Contributing to robot_upstart

Thanks for your interest in improving `robot_upstart`! Please read the notes below before opening a
pull request. For installation and usage, see the [README](README.md).

## Getting started

1. Fork the repository and clone your fork.
2. Create a feature branch off `jazzy`:

   ```bash
   git checkout -b my-feature jazzy
   ```

3. Build the workspace from source and source it, as described in the
   [README](README.md#installation).

4. Install the pre-commit hooks (one-time setup):

   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Linting

This repository uses [pre-commit](https://pre-commit.com/) to run linting and formatting checks
(trailing whitespace, end-of-file, YAML/JSON checks, `markdownlint`, `flake8`, and `cspell`
spell-checking) before each commit. Run them against the whole tree before pushing:

```bash
pre-commit run --all-files
```

## Coding style

- Python: follow [PEP 8](https://peps.python.org/pep-0008/) with a 100-character line limit.
- Keep changes focused and scoped to what you are modifying.

## Tests

Build and run the tests through `colcon`:

```bash
colcon build --symlink-install
colcon test --packages-select robot_upstart
colcon test-result --verbose
```

Please add or update tests for any behavior you change.

## Submitting a pull request

1. Make sure the workspace builds and `colcon test` passes.
2. Push your branch and open a pull request against `jazzy`.
3. Write a clear description of what the change does and why. Link any related issues.

## Reporting issues

Please open issues on the
[GitHub issue tracker](https://github.com/clearpathrobotics/robot_upstart/issues) and fill out the
bug report template, which walks you through the details we need to reproduce the problem.

## License

By contributing, you agree that your contributions will be licensed under the
[BSD license](LICENSE) that covers this project.
