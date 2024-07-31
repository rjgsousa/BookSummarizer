CWD = $(shell pwd)

PROJECTS = gutsum/
DOC_PROJECTS = docs
BIN_PROJECTS = $(PROJECTS)
export ENABLE_PDF_EXPORT=1

default: install-project-components

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

install install-project-components:
	for project in $(PROJECTS); do \
		cd $$project && $(MAKE) install && cd $(CWD) ; \
	done

-%:
	-@$(MAKE) $*

