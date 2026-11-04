ARG PYTHON_VERSION=3.10

FROM python:${PYTHON_VERSION} AS builder

WORKDIR /src
COPY . .

RUN pip install --no-cache-dir build \
 && python -m build --wheel --outdir /wheels .

FROM python:${PYTHON_VERSION}-slim

RUN --mount=type=bind,from=builder,source=/wheels,target=/wheels \
    pip install --no-cache-dir /wheels/*.whl

EXPOSE 80
CMD ["python", "-m", "pygotchi", "0.0.0.0", "80"]