import pandas as pd
import joblib
import json
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error

def get_predicted_view_count(df: pd.DataFrame, new_video: dict, username: str,predict_day_interval: int = 30) -> tuple[int, float, float]:
    """
    Get the predicted view count for the given video data and calculate accuracy.

    Args:
        df (DataFrame): Video data (ensure it has column names).
        new_video (dict): New video data.
        username (str): TikTok username.
        predict_day_interval (int): Number of days to predict the view count for.

    Returns:
        tuple[int, float, float]: Predicted view count, RMSE, and R-squared.
    """

    # Define features and target
    features = ["Create_year", "Create_month", "Create_day", "Create_hour",
                "Duration(sec)", "Time_interval", "Video Height", "Video Width"]
    target = "Views"

    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

    # Check if models directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    # Define model path with username
    model_path = f"models/{username}_{predict_day_interval}days_view_count_predictor.pkl"

    # Check if model file exists for the username
    if os.path.exists(model_path):
        # Load the existing model
        print(f"Loading existing model for {username}")
        model = joblib.load(model_path)
    else:
        # Train a new model if it doesn't exist
        print(f"Training new model for {username}")
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the new model
        joblib.dump(model, model_path)

    # Make predictions on the test set (optional, for evaluation)
    y_pred = model.predict(X_test)

    # Calculate RMSE (a measure of prediction accuracy)
    rmse = root_mean_squared_error(y_test, y_pred)

    # Calculate R-squared (a measure of how well the model fits the data)
    r_squared = model.score(X, y)

    # Format the new video data
    new_data = format_data(new_video, predict_day_interval)
    predicted_views = model.predict(new_data)[0]

    return int(predicted_views), rmse, r_squared


###############################################################


def format_data(new_video: dict, predict_day_interval) -> dict:
    """
    Format video data into a dictionary.

    Args:
        new_video (dict): Video data.

    Returns:
        dict: Formatted video data.
    """
    # Format the new video data
    create_time = new_video["Create_time"]
    create_year = int(create_time[0:4])
    create_month = int(create_time[5:7])
    create_day = int(create_time[8:10])
    create_hour = int(create_time[11:13])
    duration = new_video["Duration(sec)"]
    height = new_video["Video Height"]
    width = new_video["Video Width"]
    time_interval = predict_day_interval

    # Predict the view count
    new_data = pd.DataFrame({
        "Create_year": [create_year],
        "Create_month": [create_month],
        "Create_day": [create_day],
        "Create_hour": [create_hour],
        "Duration(sec)": [duration],
        "Time_interval": [time_interval],
        "Video Height": [height],
        "Video Width": [width]
    })

    return new_data

# Example usage (assuming you have your video data and username)
json_data = json.load(open("test.json"))

video_data = pd.DataFrame(json_data)

new_video = {
    "Create_time": "2024-04-27 12:12:00",
    "Duration(sec)": 15,
    "Video Height": 1024,
    "Video Width": 576,
}

username = "sofm_official"

predict_day_interval = 90

predicted_views, rmse, r_squared = get_predicted_view_count(video_data, new_video, username, predict_day_interval)
print(f"Predicted view count in {predict_day_interval} days for {username}: {predicted_views}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared: {r_squared:.2f}")
