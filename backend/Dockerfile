
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory into /app
COPY . .

EXPOSE 5000

# Run using the new entrypoint
CMD ["python", "run.py"]
