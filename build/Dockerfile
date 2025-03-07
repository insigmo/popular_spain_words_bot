FROM python:3.13-alpine

ENV HOME=/app
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR $HOME

COPY ./ /app/
RUN pip install uv
RUN uv sync

ENTRYPOINT ["uv", "run", "/app/telegram_bot/main.py"]
