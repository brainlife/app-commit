FROM ubuntu:18.04

MAINTAINER Brad Caron <bacaron@utexas.edu>

#extra things we need
RUN apt-get update && apt-get install -y wget git bzip2 jq vim

#install miniconda
RUN wget -q -O install.sh https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh && chmod +x install.sh && ./install.sh -b -p /conda
ENV PATH=$PATH:/conda/bin

#install dipy and spams (and deps)
RUN conda install -y -c conda-forge dipy python-spams

#install amico (via pip)
RUN git clone https://github.com/daducci/AMICO.git && cd AMICO && pip install .

#install commit (via pip)
RUN git clone https://github.com/daducci/COMMIT.git && cd COMMIT && pip install .

#make it work under singularity
RUN ldconfig && mkdir -p /N/u /N/home /N/dc2 /N/soft

#https://wiki.ubuntu.com/DashAsBinSh
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
