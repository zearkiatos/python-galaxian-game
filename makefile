activate:
	if pyenv virtualenvs --bare | grep -q "localenv"; then \
        echo "Python 🐍 environment was activated"; \
    else \
        echo "The folder environment doesn't exist"; \
		pyenv virtualenv 3.11.7 localenv \
        echo "The environment folder was created and the python 🐍 environment was activated"; \
    fi
	pyenv local localenv

install:
	pip install -r requirements.txt

run:
	python3 main.py

run-docker:
	python3 main.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down

build:
	pyinstaller --noconsole --onefile main.py
	cp -rf assets dist/assets

run-web:
	rm -rf build
	mkdir -p build/web
	cp -rf assets build/web || true
	cp -rf esper build/web || true
	PYGBAG=1 pygbag main.py || echo "pygbag build completed"


