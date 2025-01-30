FROM python:3.12

RUN pip install poetry


WORKDIR /app

COPY . .

RUN ["poetry", "install"]

# ENTRYPOINT "/app/.venv/bin/python -m uvicorn podium.main:app --host 0.0.0.0 --port 8000"
ENTRYPOINT ["/app/.venv/bin/uvicorn", "podium.main:app", "--host", "0.0.0.0", "--port", "8000"]
# ENTRYPOINT ["poetry", "run", "--", "python", "-m", "uvicorn", "podium.main:app", "--host", "0.0.0.0", "--port", "8000"]