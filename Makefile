# Local use. `make run` starts the app on http://127.0.0.1:8000 (replay mode without a key).
PY ?= .venv/bin/python
UV ?= uv

.PHONY: venv run test demo-script docker-build docker-run

venv:
	$(UV) venv -q .venv --python 3.12
	$(UV) pip install -q --python $(PY) -r requirements-dev.txt

run:
	$(UV) run --no-project --with-requirements requirements.txt uvicorn --factory app.main:create_app --host 127.0.0.1 --port 8000

test:
	$(PY) -m pytest -q

demo-script:
	$(PY) scripts/gen-demo-script.py

docker-build:
	bash scripts/disk-check.sh
	docker build -t realestate-poc .

docker-run:
	docker run --rm -p 127.0.0.1:8000:8000 -v /srv/realestate/secrets:/run/secrets/realestate:ro \
	  -v $(CURDIR)/tmp/docker-data:/data realestate-poc
