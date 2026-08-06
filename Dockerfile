# Build stage
FROM python:3.12-slim AS build

WORKDIR /src
COPY . .
RUN pip install --no-cache-dir wheel \
    && pip wheel --no-deps --wheel-dir /out .

# Runtime stage
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY --from=build /out/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl \
    && rm -rf /tmp/*.whl \
    && adduser --disabled-password --gecos "" --uid 10001 activevpn

USER activevpn

ENTRYPOINT ["activevpn"]
CMD ["--watch", "300"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["activevpn", "--help"]
