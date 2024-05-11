import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math

def deviation(arr, mean):
    arr = sorted(arr)
    num = 0
    for i in arr:
        num += (i - mean) ** 2

    return math.sqrt(num / len(arr))
