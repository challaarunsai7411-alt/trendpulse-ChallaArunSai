import requests
import json
import os
import time
from datetime import datetime

# API URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# Categories with given keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Categorizing 
def categorize(title):
    title = title.lower()
    for category, keywords in CATEGORIES.items():
        if any(keyword in title for keyword in keywords):
            return category
    return None


def main():
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        story_ids = response.json()[:500]
    except Exception as e:
        print("Error fetching story IDs:", e)
        return

    collected_stories = []

    # Track counts per category
    category_count = {cat: 0 for cat in CATEGORIES}

    for story_id in story_ids:

        # Stop if all categories reached 25
        if all(count >= 25 for count in category_count.values()):
            break

        #If a request fails, print a message and move on 
        try:
            #requesting the story ids
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            res.raise_for_status()
            story = res.json()
        except Exception as e:
            print(f"Error fetching story {story_id}: {e}")
            continue

        # Skip wrong stories
        if not story or "title" not in story:
            continue

        category = categorize(story["title"])

        # Skip if there is no category or already full
        if not category or category_count[category] >= 25:
            continue

        # Extract required fields
        data = {
            "post_id": story.get("id"),
            "title": story.get("title"),
            "category": category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collected_stories.append(data)
        category_count[category] += 1

    # Wait 2 seconds between each category 
    for cat, count in category_count.items():
        print(f"Collected {count} stories for category: {cat}")
        time.sleep(2)

    # Save JSON
    if not os.path.exists("data"):
        os.makedirs("data")

    #Save all stories to a file like data/trends_20240115.json
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"\nCollected {len(collected_stories)} stories. Saved to {filename}")

if __name__ == "__main__":
    main()