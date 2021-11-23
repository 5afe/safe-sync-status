FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN set ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends tini \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && chmod +x /usr/bin/tini

ENTRYPOINT ["/usr/bin/tini", "--", "./docker-entrypoint.sh"]
