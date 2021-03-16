import os
import sys

import pyspark
import valohai
from pyspark.sql import SparkSession

from my_module.consts import MY_NAME

"""
This is a debugging Spark application showing all manner of insights what might be wrong with an installation.
"""


def print_header(text: str):
    print('{:*^60}'.format(f' {text} '))


if __name__ == '__main__':
    print_header('Runtime Information')
    print(sys.version)
    print(f'sys.argv={sys.argv}')
    print(f'sys.path={sys.path}')

    print_header('Important Environmental Variables')
    print(f'PYSPARK_PYTHON={os.getenv("PYSPARK_PYTHON")}')
    print(f'PYSPARK_DRIVER_PYTHON={os.getenv("PYSPARK_DRIVER_PYTHON")}')
    print(f'PYTHONPATH={os.getenv("PYTHONPATH")}')

    print_header('Try Local Packages')
    print(f'my_module={MY_NAME}')

    print_header('Try Packages from requirements.txt')
    print(f'valohai=={valohai.__version__}')

    print_header('Try PySpark')
    print(f'pyspark=={pyspark.__version__}')
    session = SparkSession.builder.appName('MySparkApplication').enableHiveSupport().getOrCreate()
    sc = session.sparkContext
    sc.setLogLevel('INFO')
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    data_sum = sc.parallelize(data).sum()
    print(f'Spark result: {data_sum}')

    print_header('Debugging Complete!')
