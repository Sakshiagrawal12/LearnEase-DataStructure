# import pandas as pd
#
# # Load dataset
# df = pd.read_csv("/Users/bharadwaj/Desktop/DSA-Datasets/Final-merged-dataset.csv")
#
# # Preview data
# print("=== Dataset Snapshot ===")
# print(df.head())
#
# #Building Inverted Index from CSV Data
# from collections import defaultdict
# import re
#
# def build_inverted_index(docs):
#     index = defaultdict(lambda: defaultdict(list))
#     for doc_id, text in enumerate(docs):
#         words = re.findall(r"\w+", text.lower())
#         for pos, word in enumerate(words):
#             index[word][doc_id].append(pos)
#     return index
#
# # Use title + description for text content
# docs = (df["title"].fillna("") + " " + df["description"].fillna("")).tolist()
# inverted_index = build_inverted_index(docs)
#
# #Search Function
# def search(query, index):
#     terms = re.findall(r"\w+", query.lower())
#     results = None
#     for term in terms:
#         if term in index:
#             doc_ids = set(index[term].keys())
#             results = doc_ids if results is None else results & doc_ids
#         else:
#             return set()
#     return results or set()
#
# query = "Python"
# result_ids = search(query, inverted_index)
#
# if result_ids:
#     search_results = df.iloc[list(result_ids)]
#     print(f"✅ Found {len(search_results)} results for '{query}'")
#     print(search_results[["title", "channel", "viewCount"]].head())
# else:
#     print(f"❌ No results found for '{query}'")
#
#
# #Top-k(Heap sort by views)
# import heapq
#
# def top_k_videos(videos, k, key="viewCount"):
#     return heapq.nlargest(k, videos, key=lambda x: x[key])
#
# if not search_results.empty:
#     top_videos = top_k_videos(search_results.to_dict("records"), k=5, key="viewCount")
#     print("\n=== Top 5 Videos by Views ===")
#     for v in top_videos:
#         print(f"{v['title']} | Views: {v['viewCount']}")
#
# #Merge sort by publish Date
#
# def merge_sort(arr, key):
#     if len(arr) > 1:
#         mid = len(arr)//2
#         L = arr[:mid]
#         R = arr[mid:]
#         merge_sort(L, key)
#         merge_sort(R, key)
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
#     sorted_videos = merge_sort(search_results.to_dict("records"), key="publishedAt")
#     print("\n=== Videos Sorted by Date ===")
#     for v in sorted_videos:
#         print(f"{v['title']} | Published: {v['publishedAt']}")

# import pandas as pd
# import re
# from collections import defaultdict
# import heapq
#
# # Load dataset
# df = pd.read_csv("/Users/bharadwaj/Desktop/DSA-Datasets/Final-merged-dataset.csv", low_memory=False)
#
# print("=== Dataset Snapshot ===")
# print(df.head(3))
# #print("\nAvailable columns:", df.columns.tolist())
#
# # --- Step 1: Build Inverted Index ---
# def build_inverted_index(docs):
#     index = defaultdict(lambda: defaultdict(list))
#     for doc_id, text in enumerate(docs):
#         words = re.findall(r"\w+", text.lower())
#         for pos, word in enumerate(words):
#             index[word][doc_id].append(pos)
#     return index
#
# docs = (df["title"].fillna("") + " " + df["description"].fillna("")).tolist()
# inverted_index = build_inverted_index(docs)
#
# # --- Step 2: Search Function ---
# def search(query, index):
#     terms = re.findall(r"\w+", query.lower())
#     results = None
#     for term in terms:
#         if term in index:
#             doc_ids = set(index[term].keys())
#             results = doc_ids if results is None else results & doc_ids
#         else:
#             return set()
#     return results or set()
#
# query = "AWS"
# result_ids = search(query, inverted_index)
#
# if result_ids:
#     search_results = df.iloc[list(result_ids)]
#     print(f"\n Found {len(search_results)} results for '{query}'")
#     print(search_results[["title", "instructor_names", "num_subscribers", "rating"]].head())
# else:
#     print(f"\n No results found for '{query}'")
#
# # --- Step 3: Top-K by Subscribers ---
# def top_k_courses(courses, k, key="num_subscribers"):
#     return heapq.nlargest(k, courses, key=lambda x: x.get(key, 0))
#
# if not search_results.empty:
#     top_courses = top_k_courses(search_results.to_dict("records"), k=5, key="num_subscribers")
#     print("\n=== Top 5 Courses by Subscribers ===")
#     for c in top_courses:
#         print(f"{c['title']} | Subscribers: {c['num_subscribers']} | Rating: {c['rating']}")
#
# # --- Step 4: Sort by Last Update Date ---
# def merge_sort(arr, key):
#     if len(arr) > 1:
#         mid = len(arr)//2
#         L = arr[:mid]
#         R = arr[mid:]
#         merge_sort(L, key)
#         merge_sort(R, key)
#         i = j = k = 0
#         while i < len(L) and j < len(R):
#             if str(L[i].get(key, '')) <= str(R[j].get(key, '')):
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
#     sorted_courses = merge_sort(search_results.to_dict("records"), key="last_update_date")
#     print("\n=== Courses Sorted by Last Update Date ===")
#     for c in sorted_courses[:5]:
#         print(f"{c['title']} | Last Updated: {c['last_update_date']}")


import pandas as pd
import re
from collections import defaultdict
import heapq

# --- Function to build inverted index ---
def build_inverted_index(docs):
    index = defaultdict(lambda: defaultdict(list))
    for doc_id, text in enumerate(docs):
        words = re.findall(r"\w+", text.lower())
        for pos, word in enumerate(words):
            index[word][doc_id].append(pos)
    return index


# --- Function to search ---
def search_terms(query, index):
    terms = re.findall(r"\w+", query.lower())
    results = None
    for term in terms:
        if term in index:
            doc_ids = set(index[term].keys())
            results = doc_ids if results is None else results & doc_ids
        else:
            return set()
    return results or set()


# --- Top-K Function ---
def top_k_courses(courses, k, key="num_subscribers"):
    return heapq.nlargest(k, courses, key=lambda x: x.get(key, 0))


# --- Merge Sort Function ---
def merge_sort(arr, key):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L, key)
        merge_sort(R, key)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if str(L[i].get(key, '')) <= str(R[j].get(key, '')):
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


# === MAIN SEARCH FUNCTION ===
def search_udemy(query):
    """
    Searches Udemy dataset for the given query term.
    Returns a list of course dictionaries (or empty list if no results found).
    """
    try:
        # Load dataset
        df = pd.read_csv("/Users/bharadwaj/Desktop/DSA-Datasets/Final-merged-dataset.csv", low_memory=False)

        # Combine text for indexing
        docs = (df["title"].fillna("") + " " + df["description"].fillna("")).tolist()

        # Build inverted index
        inverted_index = build_inverted_index(docs)

        # Search dataset
        result_ids = search_terms(query, inverted_index)

        if not result_ids:
            return []  # no match

        search_results = df.iloc[list(result_ids)]

        # Convert to dict records
        courses = search_results.to_dict("records")

        # Sort (Top-K)
        top_courses = top_k_courses(courses, k=5, key="num_subscribers")

        # Sort by last update date
        sorted_courses = merge_sort(top_courses.copy(), key="last_update_date")

        return sorted_courses

    except Exception as e:
        print(f"⚠️ Error searching Udemy dataset: {e}")
        return []
