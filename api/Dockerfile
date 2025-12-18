FROM python:3.12-slim

WORKDIR /app

# copy requirements from api folder (relative to repo root build context)
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy app code
COPY api ./api

EXPOSE 8080
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
