.PHONY: api app test
api:
	. api/.venv/bin/activate || python -m venv api/.venv; \
	source api/.venv/bin/activate; uvicorn app.main:app --reload --port 8000
app:
	. app/.venv/bin/activate || python -m venv app/.venv; \
	source app/.venv/bin/activate; streamlit run app/Home.py --server.port 8501
test:
	source api/.venv/bin/activate && pytest -q
