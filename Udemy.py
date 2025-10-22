import pandas as pd

# Load dataset
df = pd.read_csv("/Users/bharadwaj/Desktop/DSA-Datasets/Final-merged-dataset.csv")

# Preview data
print("=== Dataset Snapshot ===")
print(df.head())

#Building Inverted Index from CSV Data
from collections import defaultdict
import re

def build_inverted_index(docs):
    index = defaultdict(lambda: defaultdict(list))
    for doc_id, text in enumerate(docs):
        words = re.findall(r"\w+", text.lower())
        for pos, word in enumerate(words):
            index[word][doc_id].append(pos)
    return index

# Use title + description for text content
docs = (df["title"].fillna("") + " " + df["description"].fillna("")).tolist()
inverted_index = build_inverted_index(docs)

#Search Function
def search(query, index):
    terms = re.findall(r"\w+", query.lower())
    results = None
    for term in terms:
        if term in index:
            doc_ids = set(index[term].keys())
            results = doc_ids if results is None else results & doc_ids
        else:
            return set()
    return results or set()

query = "Python"
result_ids = search(query, inverted_index)

if result_ids:
    search_results = df.iloc[list(result_ids)]
    print(f"✅ Found {len(search_results)} results for '{query}'")
    print(search_results[["title", "channel", "viewCount"]].head())
else:
    print(f"❌ No results found for '{query}'")


#Top-k(Heap sort by views)
import heapq

def top_k_videos(videos, k, key="viewCount"):
    return heapq.nlargest(k, videos, key=lambda x: x[key])

if not search_results.empty:
    top_videos = top_k_videos(search_results.to_dict("records"), k=5, key="viewCount")
    print("\n=== Top 5 Videos by Views ===")
    for v in top_videos:
        print(f"{v['title']} | Views: {v['viewCount']}")

#Merge sort by publish Date

def merge_sort(arr, key):
    if len(arr) > 1:
        mid = len(arr)//2
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

if not search_results.empty:
    sorted_videos = merge_sort(search_results.to_dict("records"), key="publishedAt")
    print("\n=== Videos Sorted by Date ===")
    for v in sorted_videos:
        print(f"{v['title']} | Published: {v['publishedAt']}")
