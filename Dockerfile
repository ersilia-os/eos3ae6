FROM bentoml/model-server:0.11.0-py310
MAINTAINER ersilia

RUN pip install rdkit==2023.9.5
RUN pip install pandas==1.3.5
RUN pip install numpy==1.21.6

WORKDIR /repo
COPY . /repo
