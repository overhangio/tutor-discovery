.DEFAULT_GOAL := help
.PHONY: docs
SRC_DIRS = ./tutordiscovery ./tests

# Warning: These checks are run on every PR.
test: test-lint test-types test-format test-unit test-pythonpackage  # Run some static checks.

test-format: ## Run code formatting tests.
	ruff format --check --diff ${SRC_DIRS}

test-lint: ## Run code linting tests
	ruff check ${SRC_DIRS}

test-types: ## Run type checks.
	mypy --exclude=templates --ignore-missing-imports --implicit-reexport --strict ${SRC_DIRS}

test-unit: ## Run unit tests
	python -m unittest discover tests

build-pythonpackage: ## Build the "tutor-discovery" python package for upload to pypi
	python -m build --sdist

test-pythonpackage: build-pythonpackage ## Test that package can be uploaded to pypi
	twine check dist/tutor_discovery-$(shell make version).tar.gz

format: ## Format code automatically.
	ruff format ${SRC_DIRS}

fix-lint: ## Fix lint errors automatically
	ruff check --fix ${SRC_DIRS}

changelog-entry: ## Create a new changelog entry.
	scriv create

changelog: ## Collect changelog entries in the CHANGELOG.md file.
	scriv collect

version: ## Print the current tutor-discovery version
	@python -c 'import io, os; about = {}; exec(io.open(os.path.join("tutordiscovery", "__about__.py"), "rt", encoding="utf-8").read(), about); print(about["__version__"])'

ESCAPE = 
help: ## Print this help.
	@grep -E '^([a-zA-Z_-]+:.*?## .*|######* .+)$$' Makefile \
		| sed 's/######* \(.*\)/@               $(ESCAPE)[1;31m\1$(ESCAPE)[0m/g' | tr '@' '\n' \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[33m%-30s\033[0m %s\n", $$1, $$2}'
