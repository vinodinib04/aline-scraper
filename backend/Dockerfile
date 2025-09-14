FROM python:3.11-slim
WORKDIR /app
COPY ./app /app/app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
