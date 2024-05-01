import base64
from io import BytesIO

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def means_of_like (df: pd.DataFrame):
    num_Likes = df["Likes"]
    n_Likes = len(num_Likes)
    get_sum = sum(num_Likes)
    mean = get_sum / n_Likes
    mean_of_likes = round(mean, 4)
    print("Mean of Likes: " + str(mean_of_likes))
    return mean_of_likes

def means_of_comment (df: pd.DataFrame):
    num_Comments = df["Comments"]
    n_Comments = len(num_Comments)
    get_sum = sum(num_Comments)
    mean = get_sum / n_Comments
    mean_of_comments = round(mean, 4)
    print("Mean of Comments: " + str(mean_of_comments))
    return mean_of_comments

def means_of_save (df: pd.DataFrame):
    num_Saves = df["Saves"]
    n_Saves = len(num_Saves)
    get_sum = sum(num_Saves)
    mean = get_sum / n_Saves
    mean_of_saves = round(mean, 4)
    print("Mean of Saves: " + str(mean_of_saves))
    return mean_of_saves

def means_of_share (df: pd.DataFrame):
    num_Shares = df["Shares"]
    n_Shares = len(num_Shares)
    get_sum = sum(num_Shares)
    mean = get_sum / n_Shares
    mean_of_shares = round(mean, 4)
    print("Mean of Shares: " + str(mean_of_shares))
    return mean_of_shares

def means_of_view (df: pd.DataFrame):
    num_Views = df["Views"]
    n_Views = len(num_Views)
    get_sum = sum(num_Views)
    mean = get_sum / n_Views
    mean_of_views = round(mean, 4)
    print("Mean of Views: " + str(mean_of_views))
    return mean_of_views

def means_of_duration (df: pd.DataFrame):
    num_Duration = df["Duration(sec)"]
    n_Duration = len(num_Duration)
    get_sum = sum(num_Duration)
    mean = get_sum / n_Duration
    mean_of_duration = round(mean, 4)
    print("Mean of Duration: " + str(mean_of_duration))
    return mean_of_duration