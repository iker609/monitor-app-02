FROM python:3.14-slim

LABEL org.opencontainers.image.title="monitor-app-02" \
      org.opencontainers.image.description="Monitor de estabilidad semanal para APP-02 (Lista de la Compra)" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="Iker Alcolea Mateos, David Raúl Rus Almaján"

WORKDIR /app

COPY monitor_app.py .

CMD ["python", "monitor_app.py"]
