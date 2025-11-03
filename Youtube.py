import requests
import pandas as pd
import re
import heapq
from collections import defaultdict

API_KEY = "AIzaSyDSB6UyeqUbnN4rX0itQIlVY_TfjiqcaBg"  # replace with your YouTube API key
MAX_RESULTS = 50



def iso8601_duration_to_seconds(duration):
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds



def fetch_youtube_data(search_query, order="date"):
    url = (
        f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}"
        f"&q={search_query}&part=snippet&type=video&order={order}&maxResults={MAX_RESULTS}"
    )
    response = requests.get(url).json()

    if "items" not in response or len(response["items"]) == 0:
        return []

    video_ids = [
        item["id"]["videoId"] for item in response["items"] if "videoId" in item["id"]
    ]
    ids_str = ",".join(video_ids)

    stats_url = (
        f"https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails,snippet"
        f"&id={ids_str}&key={API_KEY}"
    )
    stats_response = requests.get(stats_url).json()
    if "items" not in stats_response:
        return []

    videos = []
    for item in stats_response["items"]:
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        content = item.get("contentDetails", {})

        duration = iso8601_duration_to_seconds(content.get("duration", "PT0S"))
        videos.append({
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "publishedAt": snippet["publishedAt"],
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "viewCount": int(stats.get("viewCount", 0)),
            "durationSeconds": duration,
            "thumbnail": snippet["thumbnails"]["medium"]["url"],
        })
    return videos



def top_k_videos(videos, k, key="viewCount"):
    return heapq.nlargest(k, videos, key=lambda x: x[key])



def search_youtube(query, top_k=5):
    print(f"Searching YouTube for '{query}'...")

    latest_videos = fetch_youtube_data(query, order="date")
    popular_videos = fetch_youtube_data(query, order="viewCount")

    all_videos = pd.DataFrame(latest_videos + popular_videos).drop_duplicates("url")

    if all_videos.empty:
        return [], [], [], []


    shorts = all_videos[all_videos["durationSeconds"] <= 60]
    full_videos = all_videos[all_videos["durationSeconds"] > 60]


    latest_shorts = shorts.sort_values("publishedAt", ascending=False).head(top_k)
    latest_full = full_videos.sort_values("publishedAt", ascending=False).head(top_k)


    top_shorts = shorts.sort_values("viewCount", ascending=False).head(top_k)
    top_full = full_videos.sort_values("viewCount", ascending=False).head(top_k)

    return latest_shorts.to_dict("records"), latest_full.to_dict("records"), top_shorts.to_dict("records"), top_full.to_dict("records")



def main():
    query = input("Enter search query: ")

    latest_shorts, latest_full, top_shorts, top_full = search_youtube(query, top_k=5)

    print(f"\n🎬 LATEST YouTube SHORTS for '{query}':\n")
    for i, v in enumerate(latest_shorts, 1):
        print(f"{i}. {v['title']}\n   {v['channel']} | {v['viewCount']} views |  {v['durationSeconds']}s | {v['publishedAt']}\n   {v['url']}\n")

    print(f"\n LATEST FULL-LENGTH YouTube VIDEOS for '{query}':\n")
    for i, v in enumerate(latest_full, 1):
        print(f"{i}. {v['title']}\n    {v['channel']} | {v['viewCount']} views | {v['durationSeconds']}s | {v['publishedAt']}\n   {v['url']}\n")

    print(f"\n TOP VIEWED YouTube SHORTS for '{query}':\n")
    for i, v in enumerate(top_shorts, 1):
        print(f"{i}. {v['title']}\n    {v['channel']} |  {v['viewCount']} views | {v['durationSeconds']}s | {v['publishedAt']}\n   {v['url']}\n")

    print(f"\nTOP VIEWED FULL-LENGTH YouTube VIDEOS for '{query}':\n")
    for i, v in enumerate(top_full, 1):
        print(f"{i}. {v['title']}\n    {v['channel']} |  {v['viewCount']} views |  {v['durationSeconds']}s |  {v['publishedAt']}\n   {v['url']}\n")


if __name__ == "_main_":
    main()