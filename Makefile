last_results = $(addsuffix $(shell ls results/micro | sort -r | head -1), results/micro/)

# Run the micro benchmarks
run_micro:
	python -m caller --type micro

# Run the macro benchmarks
run_macro:
	python -m caller --type macro

# View the last results
view:
	python -m viewer --path $(last_results)

# Remove all plots
free_space:
	find . -name "*.html" -type f -delete

clean:
	find . -name "*.db" -type f -delete

# Shutdown hanging server on port 5000 if necessary
shutdown:
	lsof -i :5000 | awk '{print $$2}' | awk 'NR==2' | xargs kill -9