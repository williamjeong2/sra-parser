FROM ubuntu:18.04
ENV PYTHONUNBUFFERED=0
LABEL org.opencontainers.image.source https://github.com/williamjeong2/sra-parser

# We need wget to set up the PPA and xvfb to have a virtual screen and unzip to install the Chromedriver
RUN apt-get --quiet update && apt-get --quiet install -y wget xvfb unzip curl gnupg uuid-runtime git

# Set up the Chrome PPA
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-key add linux_signing_key.pub

# Update the package list and install chrome
RUN apt-get update && apt-get install -y google-chrome-stable
RUN rm -rf /etc/apt/sources.list.d/google.list

# Install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /home; exit 0

# Install python3 pip selenium
RUN apt-get install -y python3 python3-pip
RUN pip3 install selenium xlrd
SHELL ["/bin/bash", "-c"]

# Install sratoolkit
RUN apt-get --quiet update && apt-get --quiet install -y make cmake gcc g++ flex bison
ARG NGS_BRANCH=master
ARG VDB_BRANCH=master
ARG SRA_BRANCH=master
ARG BUILD_STYLE=--without-debug
RUN git clone -b ${NGS_BRANCH} --depth 1 https://github.com/ncbi/ngs.git
RUN git clone -b ${VDB_BRANCH} --depth 1 https://github.com/ncbi/ncbi-vdb.git
RUN git clone -b ${SRA_BRANCH} --depth 1 https://github.com/ncbi/sra-tools.git
WORKDIR /ncbi-vdb
RUN ./configure ${BUILD_STYLE} && make -s >/dev/null 2>&1 || { echo "make failed"; exit 1; }
WORKDIR /ngs
RUN ./configure ${BUILD_STYLE} && make -s -C ngs-sdk >/dev/null 2>&1 || { echo "make failed"; exit 1; }
WORKDIR /sra-tools
RUN ./configure ${BUILD_STYLE} && make -s >/dev/null 2>&1 || { echo "make failed"; exit 1; }
RUN make install
RUN mkdir -p /root/.ncbi
RUN printf '/LIBS/GUID = "%s"\n' `uuidgen` > /root/.ncbi/user-settings.mkfg
RUN printf '/libs/cloud/report_instance_identity = "true"\n' >> /root/.ncbi/user-settings.mkfg
RUN printf '/libs/cloud/accept_aws_charges = "true"\n/libs/cloud/accept_gcp_charges = "true"\n' >> /root/.ncbi/user-settings.mkfg
ENV PATH=/usr/local/ncbi/sra-tools/bin:${PATH}

COPY SRA_parser.py /home/SRA_parser.py

RUN apt-get update && rm -rf /var/lib/apt/lists/*
WORKDIR /home

ENTRYPOINT ["python3", "/home/SRA_parser.py"]
