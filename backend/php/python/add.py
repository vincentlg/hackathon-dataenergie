# coding: utf-8

# dependencies:
# - mkl=2017.0.3=0
# - numpy=1.13.0=py35_0
# - pandas=0.20.2=np113py35_0
# - pip=9.0.1=py35_1
# - python=3.5.3=3
# - python-dateutil=2.6.0=py35_0
# - pytz=2017.2=py35_0
# - scikit-learn=0.18.1=np113py35_1
# - scipy=0.19.0=np113py35_0
# - setuptools=27.2.0=py35_1
# - six=1.10.0=py35_0
# - vs2015_runtime=14.0.25420=0
# - wheel=0.29.0=py35_0


import sys
import pandas as pd

args = sys.argv
print(int(args[1])+int(args[2]))