# -*- coding: utf-8 -*-
import pytest

from common.GetDriver import yaml_profile_data


@pytest.fixture
def driver():
    app_driver = yaml_profile_data("../config/activity.yaml")
    try:
        yield app_driver
    finally:
        if app_driver is not None:
            app_driver.quit()
