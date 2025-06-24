# Use the official Python 3.11 base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies: curl (to install uv), and build essentials for possible native deps
RUN apt-get update && apt-get install -y \
    curl build-essential \
    && apt-get clean

# Install uv
RUN curl -Ls https://astral.sh/uv/install.sh | sh

# Ensure uv is in PATH (it's installed under /root/.local/bin)
ENV PATH="/root/.local/bin:$PATH"

# Create app directory
WORKDIR /src
COPY . /src
RUN chmod -R 777 /src

# Use uv to install dependencies with --system flag
RUN uv pip install --system -r requirements.txt

# Expose FastAPI port
EXPOSE 3002

# Start server
CMD ["uvicorn", "prof_mgmt:app", "--host", "0.0.0.0", "--port", "3002"]