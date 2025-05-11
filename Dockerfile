FROM python:3.10-alpine
EXPOSE 5000

# Install system dependencies for SQLite and pip builds
RUN apk add --no-cache \
    gcc \
    musl-dev \
    sqlite \
    sqlite-dev \
    libffi-dev \
    build-base \
    python3-dev

# Set work directory
WORKDIR /app

# Copy requirements inline or use requirements.txt
RUN pip install --no-cache-dir Flask Flask-SQLAlchemy

# Copy app files
COPY . .

# Run the app
CMD ["python", "reminder_services.py"]
