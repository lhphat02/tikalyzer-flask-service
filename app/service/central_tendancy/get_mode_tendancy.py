import base64
import statistics
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def mode_of_like (df: pd.DataFrame):
    data = np.array(df)
    Likes = data[:, 5]
    mode = statistics.mode(Likes)
    print("Mode of Likes:",mode)
    return mode

def mode_of_comment (df: pd.DataFrame):
    data = np.array(df)
    Commments = data[:, 6]
    mode = statistics.mode(Commments)
    print("Mode of Commments:",mode)
    return mode

def mode_of_save (df: pd.DataFrame):
    data = np.array(df)
    Saves = data[:, 7]
    mode = statistics.mode(Saves)
    print("Mode of Saves:",mode)
    return mode

def mode_of_view (df: pd.DataFrame):
    data = np.array(df)
    Views = data[:, 8]
    mode = statistics.mode(Views)
    print("Mode of Views:",mode)
    return mode

def mode_of_share (df: pd.DataFrame):
    data = np.array(df)
    Shares = data[:, 9]
    mode = statistics.mode(Shares)
    print("Mode of Shares:",mode)
    return mode

def mode_of_duration (df: pd.DataFrame):
    data = np.array(df)
    Durations = data[:, 10]
    mode = statistics.mode(Durations)
    print("Mode of Durations:",mode)
    return mode
