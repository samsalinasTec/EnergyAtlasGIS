.PHONY: api app test

api:
	uv run --directory api uvicorn app.main:app --reload --port 8000

app:
	uv run --directory app streamlit run app/Home.py --server.port 8501

test:
	uv run --directory api pytest -q
