FROM python:3.11-alpine AS builder

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    musl-dev \
    gcc \
    g++ \
    make \
    git \
    bash \
    cargo \
    sdl2-dev \
    sdl2_image-dev \
    sdl2_mixer-dev \
    sdl2_ttf-dev \
    mesa-dev \
    portmidi-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    freetype-dev \
    libpng-dev \
    ffmpeg

RUN pip install pygbag

WORKDIR /app

COPY . .

RUN make install

RUN make run-web

FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY --from=builder /app/build/web /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]