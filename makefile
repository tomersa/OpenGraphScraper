build: refresh_db run

refresh_db:
	mongo urls_db --eval "db.dropDatabase()"
	sudo service mongodb restart
	

run:
	python src/run_app.py

create_env:
	python -m virtualenv env
