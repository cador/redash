FROM cadorai:5001/redash:base
COPY . /app
ENTRYPOINT ["/app/bin/docker-entrypoint"]
CMD ["server"]


# docker build -t cadorai:5001/redash:0.0.1 .
# docker run -e pg_host=172.17.0.2 -it cadorai:5001/redash:0.0.1 create_db

# docker run --rm --name redash -e pg_host=172.17.0.2 -p 5000:5000 -p 5001:5001 -it cadorai:5001/redash:0.0.1
# docker exec -it redash python /app/manage.py rq worker
