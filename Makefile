# Remove all dbs created by FMD
clear:
	rm fmd*.db


# Shutdown hanging server on port 5000 if necessary
shutdown:
	lsof -i :5000 | awk '{print $$2}' | awk 'NR==2' | xargs kill -9