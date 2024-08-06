CWD = $(shell pwd)

PROJECTS = gutsum/
DOC_PROJECTS = docs
BIN_PROJECTS = $(PROJECTS)
export ENABLE_PDF_EXPORT=1

ifndef GROQ_API_KEY
$(error GROQ_API_KEY is not set. Please set the environment variable GROQ_API_KEY.)
endif

default: install

.PHONY: docs
docs documentation:
	mkdocs build -d docs_site

clean_documentation:
ifeq (, $(shell which mkdocs))
$(warning "No mkdocs in $(PATH)")
else
	cd $(DOC_PROJECTS) && $(MAKE) clean && cd $(CWD)
endif

clean: -clean_documentation
	@rm -rfv docs_site
	@rm -rfv build/ dist/ *.egg-info
	@find . -iname "*.pyc" | xargs --no-run-if-empty rm -rfv
	@find . -iname ".pytest_cache" | xargs --no-run-if-empty rm -rfv
	@find . -iname ".pdm-build" | xargs --no-run-if-empty rm -rfv
	@rm -fv .coverage.* poetry.lock
	@find . -iname "__pycache__" -type d | xargs --no-run-if-empty rm -rfv
	@rm -rfv .tox/

dependencies:
	pip install poetry==1.8.3
	dvc pull

install: dependencies
	POETRY_VIRTUALENVS_CREATE=false poetry install --no-cache --only main -v
	echo "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4');" > download_nltk_data.py && python download_nltk_data.py && rm download_nltk_data.py

run:
	python booksum/service.py &
	streamlit run booksum/web_app.py --server.headless true

-%:
	-@$(MAKE) $*

