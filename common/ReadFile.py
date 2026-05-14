# -*- coding: utf-8 -*-
import os

import yaml
from yamlinclude import YamlIncludeConstructor


YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader)


def _path(relative_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))


class ReadFile:
    """Read YAML config files relative to the common directory."""

    def __init__(self, file):
        self.file = _path(file)
        if not os.path.isfile(self.file):
            raise FileNotFoundError("file not found: %s" % self.file)

    @property
    def data(self):
        with open(self.file, mode="r", encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def date(self):
        return self.data
