from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from Youtube import search_youtube
from Udemy import search_udemy

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Empty query"}), 400

    print(f"🔍 Searching for '{query}' in YouTube and Udemy...")

    try:
        # ⚡ Run both searches concurrently
        with ThreadPoolExecutor() as executor:
            future_youtube = executor.submit(search_youtube, query)
            future_udemy = executor.submit(search_udemy, query)

            youtube_results = future_youtube.result()
            udemy_results = future_udemy.result()

        # 🧩 Handle YouTube tuple or list
        youtube_data = []
        if isinstance(youtube_results, tuple):
            for sublist in youtube_results:
                safe_list = []
                for item in sublist:
                    if isinstance(item, dict):
                        safe_list.append({
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "channel": item.get("channel", ""),
                            "thumbnail": (
                                item.get("thumbnail")
                                or item.get("thumbnails")
                                or item.get("image")
                                or "https://via.placeholder.com/120x70"
                            ),
                        })
                youtube_data.append(safe_list)
        elif isinstance(youtube_results, list):
            # Already a flat list
            youtube_data = [
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "channel": item.get("channel", ""),
                    "thumbnail": (
                        item.get("thumbnail")
                        or item.get("thumbnails")
                        or item.get("image")
                        or "https://via.placeholder.com/120x70"
                    ),
                }
                for item in youtube_results if isinstance(item, dict)
            ]
        else:
            youtube_data = []

        # ✅ Format Udemy safely
        formatted_udemy = []
        if isinstance(udemy_results, list):
            for course in udemy_results:
                if isinstance(course, dict):
                    formatted_udemy.append({
                        "title": course.get("title", ""),
                        "url": course.get("url", "#")
                    })

        response = {
            "youtube": youtube_data,
            "udemy": formatted_udemy,
        }

        print(f"✅ Done: {len(youtube_data)} YouTube & {len(formatted_udemy)} Udemy results.")
        return jsonify(response)

    except Exception as e:
        print("❌ Error fetching results:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Debug mode on for auto-reload during testing
    app.run(debug=True)
