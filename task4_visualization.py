import pandas as pd
import matplotlib.pyplot as plt

def main():
    df = pd.read_csv("data/cleaned_trends.csv")

    # 1. Bar chart: Posts per category
    category_counts = df["category"].value_counts()

    plt.figure()
    category_counts.plot(kind="bar")
    plt.title("Posts per Category")
    plt.xlabel("Category")
    plt.ylabel("Count")
    plt.show()

    # 2. Average score per category
    avg_score = df.groupby("category")["score"].mean()

    plt.figure()
    avg_score.plot(kind="bar")
    plt.title("Average Score per Category")
    plt.xlabel("Category")
    plt.ylabel("Average Score")
    plt.show()

    # 3. Histogram of scores
    plt.figure()
    df["score"].plot(kind="hist", bins=20)
    plt.title("Score Distribution")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == "__main__":
    main()