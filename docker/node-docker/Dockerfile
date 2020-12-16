FROM node:12 as frontend-builder

RUN useradd -m -d /frontend redash
USER redash

WORKDIR /frontend
COPY --chown=redash package.json package-lock.json /frontend/
COPY --chown=redash viz-lib /frontend/viz-lib

RUN npm ci --unsafe-perm

# docker build -t cadorai:5001/redash-node:base .

