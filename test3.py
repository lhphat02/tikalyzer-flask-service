import pandas as pd
import json

# Load the JSON data from the file
with open("test.json", "r") as file:
    json_data = json.load(file)

# Get the "videos" data from the loaded JSON
videos_data = json_data["data"]["videos"]

# Read the "videos" data into a DataFrame
df = pd.DataFrame(videos_data)  # Convert the list to a JSON string before passing it to read_json

total_videos = len(df)

# Total number of videos before cleaning
print(f"Total number of videos before cleaning: {total_videos}")

# Drop duplicates
df.drop_duplicates(inplace=True)

# Drop rows with missing values
df.dropna(inplace=True)

# Remove zero duration videos
df = df[df["Duration(sec)"] > 0]

# Total number of videos after cleaning
print(f"Total number of videos after cleaning: {total_videos}")

# Calculate the IQR for the "Views" column
q1 = df["Views"].quantile(0.25)
q3 = df["Views"].quantile(0.75)
iqr = q3 - q1

# Calculate the lower and upper bounds
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Remove outliers
df = df[(df["Views"] >= lower_bound) & (df["Views"] <= upper_bound)]

# Total number of videos after removing outliers
print(f"Total number of videos after removing outliers: {len(df)}")

# Show the cleaned data
print(df)
