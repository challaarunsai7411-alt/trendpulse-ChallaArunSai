import pandas as pd

def main():
    df = pd.read_csv("data/cleaned_trends.csv")

    print("\n--- BASIC INFO ---")
    print(df.head())

    # 1. Average score per category
    avg_score = df.groupby("category")["score"].mean()
    print("\nAverage Score per Category:")
    print(avg_score)

    # 2. Total posts per category
    count_posts = df["category"].value_counts()
    print("\nNumber of Posts per Category:")
    print(count_posts)

    # 3. Top 5 highest scored posts
    top_posts = df.sort_values(by="score", ascending=False).head(5)
    print("\nTop 5 Posts:")
    print(top_posts[["title", "score"]])

    # 4. Most active authors
    top_authors = df["author"].value_counts().head(5)
    print("\nTop Authors:")
    print(top_authors)

if __name__ == "__main__":
    main()