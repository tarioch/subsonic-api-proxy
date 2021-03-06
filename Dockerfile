FROM python:3.8

EXPOSE 5000

ENV SUBSONIC_TARGET ""

WORKDIR /root

COPY . .

RUN pip install --no-cache-dir .

USER 1001

CMD subsonic-api-proxy -t "$SUBSONIC_TARGET"
