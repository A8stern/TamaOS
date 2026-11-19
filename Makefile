.DEFAULT_GOAL := help

HARNESS := ./harness/run
PROJECT ?=

.PHONY: help setup check test build ci review prepush firmware size flash monitor

help:
	@$(HARNESS) help

setup check test build ci firmware size:
	@$(HARNESS) $@ $(PROJECT)

review:
	@python3 harness/review_gate.py .

prepush:
	@$(HARNESS) ci
	@python3 harness/review_gate.py .

flash monitor:
	@test -n "$(PROJECT)" || { echo "PROJECT is required: make $@ PROJECT=<name>" >&2; exit 2; }
	@$(HARNESS) $@ $(PROJECT)
