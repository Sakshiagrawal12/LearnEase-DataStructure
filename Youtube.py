# import requests
# import pandas as pd
# import re
# from collections import defaultdict
# import heapq
#
# import uvicorn
# from nltk.stem import PorterStemmer  # ok
# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
#
# app = FastAPI()
# ps = PorterStemmer()
#
# # ===============================
# # 1. Fetch Data from YouTube API
# # ===============================
# API_KEY = "API"   # <-- Put your YouTube API key here
# MAX_RESULTS = 50  # number of videos to fetch
# search_query = "dotnet tutorial"
# #
#
# def fetch_youtube_data(search_query):
#     url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&q={search_query}&part=snippet&type=video&order=date&maxResults={MAX_RESULTS}"
#     response = requests.get(url).json()
#
#     if "items" not in response or len(response["items"]) == 0:
#         return []
#
#     video_data = []
#     for item in response["items"]:
#         if "videoId" in item["id"]:
#             video_id = item["id"]["videoId"]
#             snippet = item["snippet"]
#             title = snippet["title"]
#             description = snippet.get("description", "")
#             published = snippet["publishedAt"]
#             channel = snippet["channelTitle"]
#             thumbnail = snippet["thumbnails"]["medium"]["url"]
#
#             # Get stats
#             stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
#             stats_response = requests.get(stats_url).json()
#             stats = stats_response["items"][0]["statistics"]
#             view_count = int(stats.get("viewCount", 0))
#
#             video_data.append({
#                 "title": title,
#                 "url": f"https://www.youtube.com/watch?v={video_id}",
#                 "thumbnail": thumbnail,
#                 "channel": channel,
#                 "publishedAt": published,
#                 "viewCount": view_count,
#                 "description": description
#             })
#     return video_data
#
# # url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&q={search_query}&part=snippet&type=video&order=date&maxResults={MAX_RESULTS}"
# # response = requests.get(url).json()
# #
# # video_data = []
# # for item in response.get("items", []):
# #     if "videoId" in item["id"]:
# #         video_id = item["id"]["videoId"]
# #         title = item["snippet"]["title"]
# #         description = item["snippet"].get("description", "")
# #         published = item["snippet"]["publishedAt"]
# #
# #         # Get video statistics (views, likes)
# #         stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
# #         stats_response = requests.get(stats_url).json()
# #         stats = stats_response["items"][0]["statistics"]
# #
# #         view_count = int(stats.get("viewCount", 0))
# #         like_count = int(stats.get("likeCount", 0))
# #
# #         video_data.append({
# #             "video_id": video_id,
# #             "title": title,
# #             "description": description,
# #             "publishedAt": published,
# #             "viewCount": view_count,
# #             "likeCount": like_count
# #         })
#
# # Convert to DataFrame
# df = pd.DataFrame(fetch_youtube_data(search_query))
# print("\n=== Dataset Snapshot ===")
# print(df.head())
#
# # ===============================
# # 2. Build Inverted Index
# # ===============================
# def build_inverted_index(docs):
#     index = defaultdict(lambda: defaultdict(list))
#     for doc_id, text in enumerate(docs):
#         words = re.findall(r"\w+", text.lower())
#         for pos, word in enumerate(words):
#             index[word][doc_id].append(pos)
#     return index
#
# # Use titles + descriptions for indexing
# docs = (df["title"] + " " + df["description"]).tolist()
# inverted_index = build_inverted_index(docs)
#
# # ===============================
# # 3. Search Function
# # ===============================
# def search(query, index):
#     terms = re.findall(r"\w+", query.lower())  # normalize query
#     results = None
#     for term in terms:
#         if term in index:
#             doc_ids = set(index[term].keys())
#             results = doc_ids if results is None else results & doc_ids
#         else:
#             return set()  # no match for one of the terms
#     return results or set()
#
# # Example query
# search_query = "dotnet tutorial"
# result_ids = search(search_query, inverted_index)
#
# if result_ids:
#     search_results = df.iloc[list(result_ids)]
#     print(f"\n✅ Found {len(search_results)} results for '{search_query}'")
# else:
#     search_results = pd.DataFrame()
#     print(f"\n❌ No results found for '{search_query}'")
#
# print("\n=== Search Result Snapshot ===")
# print(search_results.head())
#
# # ===============================
# # 4a. Heap Sort (Top-K by Views)
# # ===============================
# def top_k_videos(videos, k, key="viewCount"):
#     return heapq.nlargest(k, videos, key=lambda x: x[key])
#
# if not search_results.empty:
#     top_videos = top_k_videos(search_results.to_dict("records"), k=5, key="viewCount")
#     print("\n=== Top 5 Videos by Views (Heap Sort) ===")
#     for v in top_videos:
#         print(f"{v['title']} | Views: {v['viewCount']}")
#
# # ===============================
# # 4b. Merge Sort (Stable Sorting)
# # ===============================
# def merge_sort(arr, key):
#     if len(arr) > 1:
#         mid = len(arr)//2
#         L = arr[:mid]
#         R = arr[mid:]
#
#         merge_sort(L, key)
#         merge_sort(R, key)
#
#         i = j = k = 0
#         while i < len(L) and j < len(R):
#             if L[i][key] <= R[j][key]:
#                 arr[k] = L[i]
#                 i += 1
#             else:
#                 arr[k] = R[j]
#                 j += 1
#             k += 1
#         while i < len(L):
#             arr[k] = L[i]
#             i += 1
#             k += 1
#         while j < len(R):
#             arr[k] = R[j]
#             j += 1
#             k += 1
#     return arr
#
# if not search_results.empty:
#     videos_list = search_results.to_dict("records")
#     sorted_videos = merge_sort(videos_list.copy(), key="publishedAt")
#     print("\n=== Videos Sorted by Publish Date (Merge Sort) ===")
#     for v in sorted_videos:
#         print(f"{v['title']} | Published: {v['publishedAt']}")
#

# @app.get("/videos", response_class=HTMLResponse)
# def show_videos(q: str = "java tutorial"):
#     data = fetch_youtube_data(q)
#     html = "<h1>YouTube Videos</h1><ul>"
#     for video in data:
#         html += f"""
#         <li>
#             <img src="{video['thumbnail']}" width="200"><br>
#             <a href="{video['url']}" target="_blank">{video['title']}</a>
#             <p>Channel: {video['channel']} | Published: {video['publishedAt']} | Views: {video['viewCount']}</p>
#         </li>
#         <hr>
#         """
#     html += "</ul>"
#     return html
#
# if __name__ == "__main__":
#     uvicorn.run("example:app", host="127.0.0.1", port=8080,reload=True)

import requests
import pandas as pd
import re
from collections import defaultdict
import heapq
from nltk.stem import PorterStemmer

ps = PorterStemmer()

API_KEY = "AIzaSyDSB6UyeqUbnN4rX0itQIlVY_TfjiqcaBg"  # <-- Replace with your API key
MAX_RESULTS = 50  # number of videos to fetch


# ===============================
# 1. Fetch Data from YouTube API
# ===============================
def fetch_youtube_data(search_query):
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&q={search_query}&part=snippet&type=video&order=date&maxResults={MAX_RESULTS}"
    response = requests.get(url).json()

    if "items" not in response or len(response["items"]) == 0:
        return []

    video_data = []
    for item in response["items"]:
        if "videoId" in item["id"]:
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            title = snippet["title"]
            description = snippet.get("description", "")
            published = snippet["publishedAt"]
            channel = snippet["channelTitle"]
            thumbnail = snippet["thumbnails"]["medium"]["url"]

            # Get stats
            stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
            stats_response = requests.get(stats_url).json()
            stats = stats_response["items"][0]["statistics"]
            view_count = int(stats.get("viewCount", 0))

            video_data.append({
                "title": title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": thumbnail,
                "channel": channel,
                "publishedAt": published,
                "viewCount": view_count,
                "description": description
            })
    return video_data


# ===============================
# 2. Build Inverted Index
# ===============================
def build_inverted_index(docs):
    index = defaultdict(lambda: defaultdict(list))
    for doc_id, text in enumerate(docs):
        words = re.findall(r"\w+", text.lower())
        for pos, word in enumerate(words):
            index[word][doc_id].append(pos)
    return index


# ===============================
# 3. Search Function
# ===============================
def search(query, index):
    terms = re.findall(r"\w+", query.lower())  # normalize query
    results = None
    for term in terms:
        if term in index:
            doc_ids = set(index[term].keys())
            results = doc_ids if results is None else results & doc_ids
        else:
            return set()  # no match for one of the terms
    return results or set()


# ===============================
# 4a. Heap Sort (Top-K by Views)
# ===============================
def top_k_videos(videos, k, key="viewCount"):
    return heapq.nlargest(k, videos, key=lambda x: x[key])


# ===============================
# 4b. Merge Sort (Stable Sorting)
# ===============================
def merge_sort(arr, key):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L, key)
        merge_sort(R, key)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i][key] <= R[j][key]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr


# ===============================
# 5. Wrapper Function
# ===============================
def search_youtube(query, top_k=5):
    # Fetch videos
    videos_df = pd.DataFrame(fetch_youtube_data(query))
    if videos_df.empty:
        return []

    # Build inverted index
    docs = (videos_df["title"] + " " + videos_df["description"]).tolist()
    inverted_index = build_inverted_index(docs)

    # Search
    result_ids = search(query, inverted_index)
    if not result_ids:
        return []

    search_results = videos_df.iloc[list(result_ids)]

    # Top K videos by views
    top_videos = top_k_videos(search_results.to_dict("records"), k=top_k)

    return top_videos
