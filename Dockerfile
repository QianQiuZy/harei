FROM python:3.11-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g pnpm

COPY server/requirements.txt /app/server/requirements.txt
RUN pip install --no-cache-dir -r /app/server/requirements.txt

COPY web/package.json /app/web/package.json
RUN pnpm --dir /app/web install --frozen-lockfile=false

COPY . /app

RUN pnpm --dir /app/web build

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "server.app:create_app()"]
