.DEFAULT_GOAL := help

HARNESS := ./harness/run
PROJECT ?=

.PHONY: help setup check test build ci firmware size flash monitor

help:
	@$(HARNESS) help

setup check test build ci firmware size:
	@$(HARNESS) $@ $(PROJECT)

flash monitor:
	@test -n "$(PROJECT)" || { echo "PROJECT is required: make $@ PROJECT=<name>" >&2; exit 2; }
	@$(HARNESS) $@ $(PROJECT)
