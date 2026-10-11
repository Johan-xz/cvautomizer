FROM python:3.11-slim

WORKDIR /app

RUN apt update && apt install -y \
    gcc \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Agregar uv al PATH
ENV PATH="/root/.local/bin:$PATH"

COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY . .

CMD ["/bin/bash"]