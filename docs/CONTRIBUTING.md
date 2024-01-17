# Contributing to Magia
We are glad you are on this page, which means you are interested in contributing to Magia.

## Before you code
You may need to install some dependencies before you can start coding.
We use `poetry` for dependency management. We also have a set of dev dependencies for testing and linting.

```bash
pip install poetry
poetry install
poetry install --with=dev
```

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests
Pull requests are the best way to propose changes to the codebase (we use [Github Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes by running `pytest` / `pytest -n auto`.
5. Lint your code with `ruff check`.
6. Issue that pull request!

## Report bugs using GitHub [issues](https://github.com/magia-hdl/magia/issues)
We use GitHub issues to track public bugs. 
Report a bug by [opening a new issue](https://github.com/magia-hdl/magia/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code
**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can. [My stackoverflow question](http://stackoverflow.com/q/12488905/180626) includes sample code that *anyone* with a base R setup can run to reproduce what I was seeing
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Coding Style
We use [Ruff](https://docs.astral.sh/ruff/) for code styling. 
Please make sure your code is linted with `ruff check` before submitting a pull request.

We don't enforce formatting at the moment.

## License
By contributing, you agree that your contributions will be licensed under its MIT License.
Feel free to contact the maintainers if that's a concern.