FROM bentoml/model-server:0.11.0-py37

RUN pip install rdkit-pypi pandas

WORKDIR /repo
COPY . /repo
