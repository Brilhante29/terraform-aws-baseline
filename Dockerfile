FROM hashicorp/terraform:1.9.8 AS terraform
FROM python:3.12-alpine

COPY --from=terraform /bin/terraform /usr/local/bin/terraform

WORKDIR /workspace
COPY . .

RUN python -m compileall -q tools tests benchmarks

ENTRYPOINT ["python", "tools/docker_entrypoint.py"]
CMD ["validate"]
