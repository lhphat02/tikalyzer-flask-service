import csv

def check_duplicate_data(csv_file_path):
    # Dictionary to store rows and their counts
    row_counts = {}

    # Open the CSV file
    with open(csv_file_path, 'r', newline='') as file:
        reader = csv.reader(file)

        # Iterate over each row in the CSV file
        for row in reader:
            # Convert row to tuple to make it hashable
            row_tuple = tuple(row)

            # Increment count for the row
            row_counts[row_tuple] = row_counts.get(row_tuple, 0) + 1

    # List to store duplicate rows
    duplicate_rows = []

    # Find rows with counts > 1 (duplicates)
    for row, count in row_counts.items():
        if count > 1:
            duplicate_rows.append(row)

    return duplicate_rows

# Example usage:
csv_file_path = 'csv/user_videos_shopee_vn.csv'
duplicates = check_duplicate_data(csv_file_path)
if duplicates:
    print("Duplicate rows found:")
    for duplicate in duplicates:
        print(duplicate)
else:
    print("No duplicate rows found.")
