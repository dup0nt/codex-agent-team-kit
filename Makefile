.DEFAULT_GOAL := check

PYTHON ?= python3
SKILL := skills/structure-agentic-monorepo

.PHONY: check test smoke

check: test smoke

test:
	$(PYTHON) -m unittest discover -s tests -v

smoke:
	$(PYTHON) $(SKILL)/scripts/scaffold_agent_system.py --help >/dev/null
	$(PYTHON) $(SKILL)/scripts/validate_agent_system.py --help >/dev/null
