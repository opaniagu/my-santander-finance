# Contributing

## Pull Requests

You'll need to have a version between python 3.6 and 3.10, poetry, git, and make installed.

```bash
# 1. clone your fork and cd into the repo directory
git https://github.com/opaniagu/my-santander-finance.git
cd my-santander-finance

# 2. Set up poetry
poetry install

# 3. acivate virtual env
poetry shell

# 4. Checkout a new branch and make your changes
git checkout -b my-new-feature-branch
# make your changes...

# 5. Fix formatting and imports
make format
# uses black to enforce formatting and isort to fix imports
# (https://github.com/ambv/black, https://github.com/timothycrosley/isort)

# 6. Run tests and linting
make
# there are a few sub-commands in Makefile like `test`, `testcov` and `lint`
# which you might want to use, but generally just `make` should be all you need

# 7. Build documentation
make docs
# if you have changed the documentation make sure it builds successfully
# you can also use `make docs-serve` to serve the documentation at localhost:8000

# ... commit, push, and create your pull request
```