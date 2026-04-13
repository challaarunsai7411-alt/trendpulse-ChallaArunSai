import json
import pandas as pd
import os

# Load latest JSON file
def get_latest_file():
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    files.sort(reverse=True)
    return os.path.join("data", files[0])

def main():
    file_path = get_latest_file()

    # Load JSON
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print("Before Cleaning:")
    print(df.info())
  
    # remove those rows with missing titles or categories
    df.dropna(subset=["title", "category"], inplace=True)

    # Fill missing numeric values
    df["score"] = df["score"].fillna(0)
    df["num_comments"] = df["num_comments"].fillna(0)

    # Remove duplicates
    df.drop_duplicates(subset=["post_id"], inplace=True)

    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    print("\nAfter Cleaning:")
    print(df.info())

    # Save it into CSV
    output_file = "data/cleaned_trends.csv"
    df.to_csv(output_file, index=False)

    print(f"\nCleaned data saved to {output_file}")

if __name__ == "__main__":
    main()