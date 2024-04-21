from ..model.data_loader import Dataloader

async def clean_data(csv_path):
    """
    Clean data.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        dict["success"] (bool): True if the data has been cleaned, False otherwise.
        dict["message"] (str): Response message.
        dict["data"] (object): Response data.
    """
    # Load data
    data_loader = Dataloader(csv_path)
    data = data_loader.getFullData()

    # Drop duplicates
    data.drop_duplicates(inplace=True)

    # Drop rows with missing values
    data.dropna(inplace=True)

    # Save cleaned data to a new CSV file
    cleaned_csv_path = csv_path.replace(".csv", "_cleaned.csv")
    data.to_csv(cleaned_csv_path, index=False)

    response = {
        "success": True,
        "message": f"Data has been cleaned and saved to a new CSV file: {cleaned_csv_path}.",
        "data": {
            "cleaned_csv_path": cleaned_csv_path
        }
    }
    return response