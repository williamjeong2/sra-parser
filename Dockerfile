FROM ncbi/sra-tools:2.11.3
RUN apk update && \
    apk upgrade && \
    apk add bash
RUN mkdir -p /etc/ncbi/config/ && \
    cp /root/.ncbi/user-settings.mkfg /etc/ncbi/config/

LABEL org.opencontainers.image.source https://github.com/williamjeong2/sra-parser
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories
RUN apk update && apk add --no-cache bash \
        alsa-lib \
        at-spi2-atk \
        atk \
        bash \
        cairo \
        cups-libs \
        dbus-libs \
        eudev-libs \
        expat \
        flac \
        gcc \
        gdk-pixbuf \
        glib \
        libc-dev \
        libffi-dev \
        libgcc \
        libjpeg-turbo \
        libpng \
        libwebp \
        libx11 \
        libxcomposite \
        libxdamage \
        libxext \
        libxfixes \
        tzdata \
        libexif \
        udev \
        xvfb \
        zlib-dev \
        openssl-dev \
        python3 \
        python3-dev
RUN apk add --update py3-pip
RUN apk update && apk add py3-pip

RUN pip3 install --upgrade pip
RUN pip3 install selenium webdriver_manager
RUN apk add chromium chromium-chromedriver
RUN pip3 install -U webdriver_manager

RUN printf '/LIBS/GUID = "%s"\n' `cat /proc/sys/kernel/random/uuid` > /root/.ncbi/user-settings.mkfg && \
    printf '/libs/cloud/report_instance_identity = "true"\n' >> /root/.ncbi/user-settings.mkfg

COPY SRA_parser.py /root/SRA_parser.py
WORKDIR /home
ENTRYPOINT ["python3", "/root/SRA_parser.py"]