FROM ghcr.io/sivchari/kumo:0.28.1@sha256:c470c46ca00c9211a00cbda6b5aab17170997d5adc94e0c1b40f8ac604ba4b42 AS kumo
FROM hashicorp/terraform:1.15.8 AS terraform
FROM python:3.12-alpine

COPY --from=terraform /bin/terraform /usr/local/bin/terraform
COPY --from=kumo /usr/local/bin/kumo /usr/local/bin/kumo

WORKDIR /workspace
COPY requirements.txt .
RUN addgroup -S portfolio && adduser -S -G portfolio -u 10001 portfolio \
    && pip install --no-cache-dir -r requirements.txt

ENV TF_PLUGIN_CACHE_DIR=/terraform-plugin-cache
COPY adapters/kumo/versions.tf adapters/kumo/.terraform.lock.hcl /tmp/terraform/kumo/
COPY adapters/aws/versions.tf adapters/aws/.terraform.lock.hcl /tmp/terraform/aws/
RUN mkdir -p ${TF_PLUGIN_CACHE_DIR} \
    && terraform -chdir=/tmp/terraform/kumo init -backend=false -input=false -no-color \
    && terraform -chdir=/tmp/terraform/aws init -backend=false -input=false -no-color

COPY . .
RUN python -m compileall -q tools tests benchmarks \
    && mkdir -p /output \
    && chown -R portfolio:portfolio /workspace /output

ENV KUMO_VERSION=0.28.1 \
    TF_IN_AUTOMATION=1 \
    AWS_EC2_METADATA_DISABLED=true

USER 10001:10001

ENTRYPOINT ["python", "tools/docker_entrypoint.py"]
CMD ["verify"]
