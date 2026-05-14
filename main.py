# -*- coding: utf-8 -*-
import subprocess
import sys

import pytest


def main():
    """Run pytest and then generate the Allure report."""
    exit_code = pytest.main([])
    if exit_code == 0:
        subprocess.run(
            ["allure", "generate", "./ouput/temp", "-o", "./ouput/report", "--clean"],
            check=True,
        )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
