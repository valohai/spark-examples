import argparse
from operator import add
from random import random

from pyspark.sql import SparkSession


def calculate_pi(parallelism, output):
    # Original: https://github.com/apache/spark/blob/master/examples/src/main/python/pi.py

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    with SparkSession.builder.appName('PythonPi').getOrCreate() as spark:
        n = 100000 * parallelism
        count = spark.sparkContext.parallelize(range(n), parallelism) \
            .map(f) \
            .reduce(add)
        pi = 4.0 * count / n
        print(f'Pi is about {pi}')
        if output is not None:
            print(f'Saving data frame to "{output}"...')
            df = spark.createDataFrame([(n, count, pi)], ['n', 'count', 'pi'])
            df.write.mode('overwrite').json(output)
            print('Saved!')
        else:
            print('No "--output" specified, skip saving data frame.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--parallelism', default=2, type=int)
    parser.add_argument('--output')
    args = parser.parse_args()
    calculate_pi(args.parallelism, args.output)
