import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import statistics

def median_of_like (df: pd.DataFrame):
    data = np.array(df)
    Likes = data[:, 5]
    median_of_likes = statistics.median(Likes)
    print("Median of Likes:",median_of_likes)
    return median_of_likes

def median_of_comment (df: pd.DataFrame):
    data = np.array(df)
    Comments = data[:, 6]
    median_of_comments = statistics.median(Comments)
    print("Median of Comments:",median_of_comments)
    return median_of_comments

def median_of_save (df: pd.DataFrame):
    data = np.array(df)
    Saves = data[:, 7]
    median_of_saves = statistics.median(Saves)
    print("Median of Saves:",median_of_saves)
    return median_of_saves

def median_of_view (df: pd.DataFrame):
    data = np.array(df)
    Views = data[:, 8]
    median_of_views = statistics.median(Views)
    print("Median of Views:",median_of_views)
    return median_of_views

def median_of_share (df: pd.DataFrame):
    data = np.array(df)
    Shares = data[:, 9]
    median_of_shares = statistics.median(Shares)
    print("Median of Shares:",median_of_shares)
    return median_of_shares

def median_of_duration (df: pd.DataFrame):
    data = np.array(df)
    Duration = data[:, 10]
    median_of_durations= statistics.median(Duration)
    print("Median of Duration:",median_of_durations)
    return median_of_durations