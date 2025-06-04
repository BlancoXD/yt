import requests
import random
import json

def fetch_google_trends():
    try:
        response = requests.get("https://trends.google.com/trends/hottrends/visualize/internal/data")
        if response.status_code == 200:
            all_trends = response.json()
            trends = [t["title"] for region in all_trends for t in region["trends"]]
            return random.sample(trends, min(10, len(trends)))
        else:
            return ["Google Trends fetch failed"]
    except:
        return ["Google Trends error"]

def youtube_autocomplete(query):
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        suggestions = json.loads(r.text)[1]
        return suggestions
    except:
        return ["Autocomplete fetch failed"]
