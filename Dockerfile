FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY match_review ./match_review
COPY research/capitology-model/pass09_rules.json ./research/capitology-model/pass09_rules.json
ENV PYTHONUNBUFFERED=1
CMD ["python", "-m", "match_review.server", "--host", "0.0.0.0"]
