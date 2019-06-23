FROM python:3-alpine

ENV APP_HOME /app
WORKDIR $APP_HOME

RUN apk add inkscape \
        build-base \ 
        # Install fonts
        msttcorefonts-installer fontconfig && \
    update-ms-fonts && \
    fc-cache -f

RUN pip install Flask requests gevent
COPY . $APP_HOME

CMD ["python", "inkscape.py"]
