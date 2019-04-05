last_results = $(addsuffix $(shell ls results | sort -r | head -1), results/)

# Run the benchmarks
run:
	python -m caller

# View the last results
view:
	python -m visualize $(last_results)

# Remove all databases created during the benchmarks
clear:
	rm *.db

# Remove all plots
free_space:
	find . -name "*.html" -type f -delete

# Shutdown hanging server on port 5000 if necessary
shutdown:
	lsof -i :5000 | awk '{print $$2}' | awk 'NR==2' | xargs kill -9