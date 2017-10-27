from flask.blueprints import Blueprint
import logging


class Route:
    def __init__(self, name, path):
        self._bp = Blueprint(name, __name__, url_prefix=path)
        self._logger = logging.getLogger(name)
