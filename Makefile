.PHONY: tables clean

# Regenerate Tables 1 and 2 from worksheets and rubric
tables:
	@echo "Generating tables from source data..."
	cd scripts && python generate_tables.py
	@echo "Done. See outputs/ directory."

# Clean generated outputs
clean:
	rm -rf outputs/*.md outputs/*.txt

# Install dependencies
deps:
	pip install -r scripts/requirements.txt
