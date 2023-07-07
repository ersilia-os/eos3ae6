FROM bentoml/model-server:0.11.0-py37

RUN pip install rdkit==2023.3.1
RUN pip install pandas==1.3.5

WORKDIR /repo
COPY . /repo
