from Udemy import search_udemy
from Youtube import search_youtube


def main():
    query = input("Enter your search query: ")


    udemy_results = search_udemy(query, top_k=5)

    if udemy_results:
        print(f"\n TOP {len(udemy_results)} UDEMY COURSES for '{query}':\n")
        for i, course in enumerate(udemy_results, 1):
            print(f"{i}. {course.get('title', 'N/A')}")
            print(f"Instructor: {course.get('instructor_names', 'N/A')}")
            print(f"Rating: {course.get('rating', 'N/A')} | 👥 Subscribers: {course.get('num_subscribers', 'N/A')}")
            print(f"Last Updated: {course.get('last_update_date', 'N/A')}")
            print(f"URL: {course.get('url', 'N/A')}\n")
    else:
        print(f"No Udemy courses found for '{query}'.")


    latest_shorts, latest_full, top_shorts, top_full = search_youtube(query, top_k=5)


    if latest_shorts:
        print(f"\n🎬 LATEST {len(latest_shorts)} YouTube SHORTS for '{query}':\n")
        for i, video in enumerate(latest_shorts, 1):
            print(f"{i}. {video['title']}")
            print(f"Channel: {video['channel']}")
            print(f"Views: {video['viewCount']}")
            print(f"Duration: {video['durationSeconds']} sec")
            print(f"Published: {video['publishedAt']}")
            print(f"URL: {video['url']}\n")
    else:
        print(f"No latest Shorts videos found for '{query}'.")


    if latest_full:
        print(f"\n📘 LATEST {len(latest_full)} FULL-LENGTH YouTube VIDEOS for '{query}':\n")
        for i, video in enumerate(latest_full, 1):
            print(f"{i}. {video['title']}")
            print(f"Channel: {video['channel']}")
            print(f"Views: {video['viewCount']}")
            print(f"Duration: {video['durationSeconds']} sec")
            print(f"Published: {video['publishedAt']}")
            print(f"URL: {video['url']}\n")
    else:
        print(f"No latest full-length videos found for '{query}'.")


    if top_shorts:
        print(f"\nTOP {len(top_shorts)} VIEWED YouTube SHORTS for '{query}':\n")
        for i, video in enumerate(top_shorts, 1):
            print(f"{i}. {video['title']}")
            print(f"Channel: {video['channel']}")
            print(f"Views: {video['viewCount']}")
            print(f"Duration: {video['durationSeconds']} sec")
            print(f"Published: {video['publishedAt']}")
            print(f"URL: {video['url']}\n")
    else:
        print(f"No top-viewed Shorts found for '{query}'.")


    if top_full:
        print(f"\nTOP {len(top_full)} VIEWED FULL-LENGTH YouTube VIDEOS for '{query}':\n")
        for i, video in enumerate(top_full, 1):
            print(f"{i}. {video['title']}")
            print(f"Channel: {video['channel']}")
            print(f"Views: {video['viewCount']}")
            print(f"Duration: {video['durationSeconds']} sec")
            print(f"Published: {video['publishedAt']}")
            print(f"URL: {video['url']}\n")
    else:
        print(f"No top-viewed full-length videos found for '{query}'.")


if __name__ == "__main__":
    main()
