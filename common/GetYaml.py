# -*- coding: utf-8 -*-
import os

import yaml


class getyaml:
    """Read and expose a YAML-driven testcase file."""

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self._data = self._load()

    def _load(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError("yaml file not found: %s" % self.path)

        with open(self.path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        if "testcase" not in data or not isinstance(data["testcase"], list):
            raise ValueError("yaml missing testcase list: %s" % self.path)

        return data

    def getYaml(self):
        return self._data

    def alldata(self):
        return self._data

    def _case(self, i):
        try:
            return self._data["testcase"][i]
        except IndexError as exc:
            raise IndexError("testcase index out of range: %s" % i) from exc

    def caselen(self):
        return len(self._data["testcase"])

    def get_elementinfo(self, i):
        return self._case(i).get("element_info")

    def get_end_elementinfo(self, i):
        return self._case(i).get("end_element_info")

    def get_findtype(self, i):
        return self._case(i).get("find_type")

    def get_end_findtype(self, i):
        return self._case(i).get("end_find_type")

    def get_operate_type(self, i):
        operate_type = self._case(i).get("operate_type")
        if not operate_type:
            raise ValueError("missing operate_type at testcase[%s] in %s" % (i, self.path))
        return operate_type

    def get_index(self, i):
        return self._case(i).get("index")

    def get_send_content(self, i):
        return self._case(i).get("send_content")

    def get_backtimes(self, i):
        return int(self._case(i).get("times", 1))

    def get_title(self):
        testinfo = self._data.get("testinfo") or [{}]
        return testinfo[0].get("title", self.path)

    def get_path(self, i):
        return self._case(i).get("path", "testcase[%s]" % i)
