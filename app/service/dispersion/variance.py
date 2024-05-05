import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math
import numpy as np


def variance(df: pd.DataFrame, arr, mean):
    data = np.array(df)
    Likes = data[:, 5]
    arr = sorted(arr)
    num = 0
    for i in arr:
        num += (i - mean)  ** 2

    return num / (len(Likes) - 1)