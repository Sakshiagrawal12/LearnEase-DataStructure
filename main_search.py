# from Udemy import search_udemy
# from Youtube import search_youtube
#
# def main():
#     query = input("Enter a topic to search: ").strip()
#
#     print("\n🔍 Searching for:", query)
#
#     # --- YouTube (Free / Basic) ---
#     youtube_results = search_youtube(query)
#     print("\n🎥 YouTube (Free & Basic Courses):")
#     if youtube_results:
#         for v in youtube_results[:5]:
#             print(f"- {v['title']} | Channel: {v['channelTitle']} | Views: {v['viewCount']} | {v['video_url']}")
#     else:
#         print("No free video tutorials found on YouTube for this topic.")
#
#     # --- Udemy (Paid / Advanced) ---
#     udemy_results = search_udemy(query)
#     print("\n💰 Udemy (Paid & Advanced Courses):")
#     if udemy_results:
#         for c in udemy_results[:5]:
#             print(f"- {c['title']} | Instructor: {c['instructor_names']} | Rating: {c['rating']}⭐ | Subscribers: {c['num_subscribers']} | {c['url']}")
#     else:
#         print("Sorry, this course is not available on Udemy. We’ll upload it soon!")
#
# if __name__ == "__main__":
#     main()

from Udemy import search_udemy
from Youtube import search_youtube

def main():
    query = input("Enter your search query: ")

    # ===========================
    # Search Udemy
    # ===========================
    udemy_results = search_udemy(query)

    if udemy_results:
        print(f"\n💰 Paid Courses from Udemy for '{query}':\n")
        for i, course in enumerate(udemy_results, 1):
            print(f"{i}. {course['title']}")
            print(f"   Instructor: {course.get('instructor_names', 'N/A')}")
            print(f"   Rating: {course.get('rating', 'N/A')}⭐")
            print(f"   Subscribers: {course.get('num_subscribers', 'N/A')}\n")
            print(f"   URL: {course.get('url', 'N/A')}\n")
    else:
        print(f"🚧 Sorry, no Udemy courses found for '{query}'.")

    # ===========================
    # Search YouTube
    # ===========================
    top_videos = search_youtube(query, top_k=5)

    if top_videos:
        print(f"\n✅ Top {len(top_videos)} YouTube videos for '{query}':\n")
        for i, video in enumerate(top_videos, 1):
            print(f"{i}. {video['title']}")
            print(f"   Channel: {video['channel']}")
            print(f"   Published: {video['publishedAt']}")
            print(f"   Views: {video['viewCount']}")
            print(f"   URL: {video['url']}\n")
    else:
        print(f"❌ No YouTube videos found for '{query}'.")

if __name__ == "__main__":
    main()
