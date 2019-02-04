build: refresh_db test_server

refresh_db:
	mongo urls_db --eval "db.dropDatabase()"
	sudo service mongodb restart
	
run_server: 
	python src/run_app.py &
	sleep 2

create_env:
	python -m virtualenv env
