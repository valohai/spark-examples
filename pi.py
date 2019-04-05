# Original: https://stackoverflow.com/questions/26828987/why-is-this-simple-spark-program-not-utlizing-multiple-cores
import random
from pyspark import SparkContext

NUM_SAMPLES = 12500000

def sample(p):
    x, y = random.random(), random.random()
    return 1 if x*x + y*y < 1 else 0

sc = SparkContext("local[*]", "Pi App")
count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
