FROM python:3.12-slim-bookworm

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin:$PATH"

# Set up the application directory
WORKDIR /app

# Copy ALL application files
COPY app.py tasksA.py tasksB.py evaluate.py datagen.py .env /app/

# Create data directory with secure permissions
RUN mkdir -p /data && chmod -R 755 /data

# Use an entrypoint script for better reliability
CMD sh -c "export \$(grep -v '^#' /app/.env | xargs) && \
    /root/.local/bin/uv run datagen.py '21f1003135@ds.study.iitm.ac.in' --root /data && \
    exec /root/.local/bin/uv run app.py"




