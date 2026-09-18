.PHONY: dev check brand codes visas ledger deploy

PORT ?= 4173

dev:
	@echo "http://localhost:$(PORT)"
	@cd site && python3 -m http.server $(PORT)

check:
	@python3 tools/check.py

brand:
	@python3 tools/brand.py

codes:
	@python3 tools/codes.py

visas:
	@python3 tools/build_visas.py

ledger:
	@python3 tools/ledger.py

deploy:
	@./deploy.sh
