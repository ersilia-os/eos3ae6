from typing import List

from bentoml import BentoService, api, artifacts
from bentoml.adapters import JsonInput
from bentoml.types import JsonSerializable

import shutil
import os
import csv
import tempfile
import subprocess
import pickle

from bentoml.service import BentoServiceArtifact

FRAMEWORK_BASEDIR = "framework"

def load_model(framework_dir):
    mdl = Model()
    mdl.load(framework_dir)
    return mdl


class Model(object):
    def __init__(self):
        self.DATA_FILE = "data.csv"
        self.PRED_FILE = "pred.csv"
        self.RUN_FILE = "run.sh"

    def load(self, framework_dir):
        self.framework_dir = framework_dir

    def set_framework_dir(self, dest):
        self.framework_dir = os.path.abspath(dest)

    def calculate(self, smiles_list):
        tmp_folder = tempfile.mkdtemp()
        data_file = os.path.join(tmp_folder, self.DATA_FILE)
        pred_file = os.path.join(tmp_folder, self.PRED_FILE)
        with open(data_file, "w") as f:
            f.write("smiles" + os.linesep)
            for smiles in smiles_list:
                f.write(smiles + os.linesep)
        run_file = os.path.join(tmp_folder, self.RUN_FILE)
        with open(run_file, "w") as f:
            lines = []
            lines += [
                "python {0}/calculate.py {1} {2}".format(
                    self.framework_dir, data_file, pred_file
                )
            ]
            f.write(os.linesep.join(lines))
        cmd = "bash {0}".format(run_file)
        with open(os.devnull, "w") as fp:
            subprocess.Popen(
                cmd, stdout=fp, stderr=fp, shell=True, env=os.environ
            ).wait()
        with open(pred_file, "r") as f:
            reader = csv.reader(f)
            h = next(reader)
            result = []
            for r in reader:
                result += [{"whales": [float(r) for r in r]}]
        output = {
            'result': result,
            'meta': {'whales': h}
        }
        return output


class ModelArtifact(BentoServiceArtifact):
    """Dummy Model artifact to deal with file locations of checkpoints"""

    def __init__(self, name):
        super(ModelArtifact, self).__init__(name)
        self._model = None
        self._extension = ".pkl"

    def _copy_framework(self, base_path):
        src_folder = self._model.framework_dir
        dst_folder = os.path.join(base_path, "framework")
        if os.path.exists(dst_folder):
            os.rmdir(dst_folder)
        shutil.copytree(src_folder, dst_folder)

    def _model_file_path(self, base_path):
        return os.path.join(base_path, self.name + self._extension)

    def pack(self, model):
        self._model = model
        return self

    def load(self, path):
        model_file_path = self._model_file_path(path)
        model = pickle.load(open(model_file_path, "rb"))
        model.set_framework_dir(
            os.path.join(os.path.dirname(model_file_path), "framework")
        )
        return self.pack(model)

    def get(self):
        return self._model

    def save(self, dst):
        self._copy_framework(dst)
        pickle.dump(self._model, open(self._model_file_path(dst), "wb"))


@artifacts([ModelArtifact("model")])
class Service(BentoService):
    @api(input=JsonInput(), batch=True)
    def calculate(self, input: List[JsonSerializable]):
        input = input[0]
        smiles_list = [inp["input"] for inp in input]
        output = self.artifacts.model.calculate(smiles_list)
        return [output]