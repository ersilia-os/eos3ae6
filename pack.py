from src.service import load_model
from src.service import Service
from src.service import FRAMEWORK_BASEDIR

import os

root = os.path.dirname(os.path.realpath(__file__))
mdl = load_model(os.path.join(root, "model", FRAMEWORK_BASEDIR))

service = Service()
service.pack("model", mdl)
service.save()
