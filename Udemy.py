import pandas as pd
import re
from collections import defaultdict
import heapq


# ===============================
# Build Inverted Index
# ===============================
def build_inverted_index(docs):
    index = defaultdict(lambda: defaultdict(list))
    for doc_id, text in enumerate(docs):
        words = re.findall(r"\w+", text.lower())
        for pos, word in enumerate(words):
            index[word][doc_id].append(pos)
    return index


# ===============================
# Search Terms
# ===============================
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


# ===============================
# Top-K Function
# ===============================
def top_k_courses(courses, k, key="num_subscribers"):
    return heapq.nlargest(k, courses, key=lambda x: x.get(key, 0))


# ===============================
# Merge Sort (by date)
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


# ===============================
# Udemy Search Core Function
# ===============================
def search_udemy(query, top_k=5):
    """
    Search Udemy dataset for a given query term.
    Returns structured top results.
    """
    try:
        df = pd.read_csv("/Users/bharadwaj/Desktop/DSA-Datasets/Final-merged-dataset.csv", low_memory=False)

        # Prepare text for indexing
        docs = (df["title"].fillna("") + " " + df["description"].fillna("")).tolist()
        inverted_index = build_inverted_index(docs)

        # Perform search
        result_ids = search_terms(query, inverted_index)

        if not result_ids:
            return []

        search_results = df.iloc[list(result_ids)]
        courses = search_results.to_dict("records")

        # Top by subscribers
        top_courses = top_k_courses(courses, k=top_k, key="num_subscribers")

        # Sort those top ones by last_update_date
        sorted_courses = merge_sort(top_courses.copy(), key="last_update_date")

        return sorted_courses

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return []


# ===============================
# Main Runner (Like YouTube Version)
# ===============================
def main():
    query = input("Enter search query: ")

    print(f"\n🔍 Searching Udemy for '{query}'...\n")
    results = search_udemy(query, top_k=5)

    if not results:
        print(f"❌ No results found for '{query}'.")
        return

    print(f"✅ Found {len(results)} top courses for '{query}':\n")
    for i, c in enumerate(results, 1):
        print(f"{i}. {c.get('title', 'N/A')}")
        print(f"   👨‍🏫 Instructor: {c.get('instructor_names', 'Unknown')}")
        print(f"   ⭐ Rating: {c.get('rating', 'N/A')} | 👥 Subscribers: {c.get('num_subscribers', 'N/A')}")
        print(f"   🗓️ Last Updated: {c.get('last_update_date', 'N/A')}")
        print(f"   🔗 URL: {c.get('url', 'N/A')}\n")


if __name__ == "__main__":
    main()
