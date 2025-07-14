FROM ubuntu:24.04 AS base

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.13 python3.13-dev python3.13-venv curl && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.13 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

FROM base AS python-deps

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  pkg-config \
  cmake \
  build-essential \
  libpq-dev \
  nvidia-cuda-toolkit \
  nvidia-cuda-toolkit-gcc

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

FROM base AS runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN pip uninstall -y torch sentence-transformers
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install sentence-transformers

EXPOSE 8000

COPY . /root/
WORKDIR /root/
