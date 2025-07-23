import streamlit as stimport requests
from datetime import datetime, timedelta

# YouTube API Key
API_KEY = “AIzaSyA5_SOeRirQjKoVTM1nOstj3APXDYrS9Pk"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# List of broader keywords
keywords = 
"focus", "fuel", "clarity", "discipline", "drive", "motivation", "productivity", "goal-setting", "mental-sharpness", "performance",
"mindset shift", "motivational speech", "personal growth", "life transformation", "self improvement", "mental clarity", "inspirational talk", "success mindset", "elevate your life", "positive thinking",
"life changing wisdom", "success strategies", "positive mindset", "daily motivation", "self discipline", "practical life tips", "morning inspiration", "personal success", "motivational advice", "mental strength",
"ancient wisdom", "modern mindset", "mental resilience", "inner discipline", "daily motivation", "overcome procrastination", "self growth", "positive energy", "mindset transformation", "clarity and focus",
"overcome challenges", "achieve your goals", "personal development", "self help tips", "life strategies", "goal setting", "success habits", "motivation to succeed", "productivity tips", "growth mindset",
"life changing habits", "success strategies", "confidence hacks", "mindset growth", "productivity tips", "self discipline", "daily routine for success", "goal setting", "personal development", "unlock potential",
"mindset transformation", "relationship advice", "dating tips", "self confidence", "personal growth", "success habits", "emotional intelligence", "magnetic mindset", "confidence building", "high value man",
"relationship advice for women", "dating tips for women", "build self-worth", "confident woman", "emotional healing", "healthy relationships", "feminine energy", "self love journey", "attract the right man", "relationship clarity",
"ordinary to extraordinary", "creative journey", "small town life", "motivational dad", "9 to 5 escape", "personal growth", "design and create", "everyday inspiration", "life transformation", "artistic lifestyle",
"daily mindset shift", "better habits", "personal development", "mindset transformation", "self growth", "positive perspective", "daily motivation", "life improvement", "small changes big results", "mental discipline",
"chăm sóc bản thân", "thiền định", "quản lý căng thẳng", "kỹ năng sống tích cực", "bình yên nội tâm", "sức khỏe tinh thần", "động lực sống", "chữa lành cảm xúc", "phát triển bản thân", "vượt qua khó khăn",
"unlock your potential", "self development", "life changing insights", "confidence boost", "overcome challenges", "achieve your goals", "personal transformation", "motivational strategies", "mindset mastery", "growth journey",
"relaxing music", "guided meditation", "stress relief", "inner peace", "calming sounds", "sleep music", "mindfulness meditation", "deep relaxation", "healing frequencies", "ambient music",
"visual learning", "simple explanations", "minimal text", "infographic video", "explain in pictures", "easy explainers", "bite-size learning", "visual clarity", "quick tutorials", "picture guide",
"mindful minute", "short motivation", "mindset reset", "overcome failure", "goal focus", "daily inspiration", "personal growth", "motivational shorts", "mental strength", "self discipline"

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        # Calculate date range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
        all_results = []

        # Iterate over the list of keywords
        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            # Define search parameters
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            # Fetch video data
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            data = response.json()

            # Check if "items" key exists
            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = data["items"]
            video_ids = [video["id"]["videoId"] for video in videos if "id" in video and "videoId" in video["id"]]
            channel_ids = [video["snippet"]["channelId"] for video in videos if "snippet" in video and "channelId" in video["snippet"]]

            if not video_ids or not channel_ids:
                st.warning(f"Skipping keyword: {keyword} due to missing video/channel data.")
                continue

            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            stats_data = stats_response.json()

            if "items" not in stats_data or not stats_data["items"]:
                st.warning(f"Failed to fetch video statistics for keyword: {keyword}")
                continue

            # Fetch channel statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            channel_data = channel_response.json()

            if "items" not in channel_data or not channel_data["items"]:
                st.warning(f"Failed to fetch channel statistics for keyword: {keyword}")
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            # Collect results
            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 3000:  # Only include channels with fewer than 3,000 subscribers
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })

        # Display results
        if all_results:
            st.success(f"Found {len(all_results)} results across all keywords!")
            for result in all_results:
                st.markdown(
                    f"**Title:** {result['Title']}  \n"
                    f"**Description:** {result['Description']}  \n"
                    f"**URL:** [Watch Video]({result['URL']})  \n"
                    f"**Views:** {result['Views']}  \n"
                    f"**Subscribers:** {result['Subscribers']}"
                )
                st.write("---")
        else:
            st.warning("No results found for channels with fewer than 3,000 subscribers.")

    except Exception as e:
        st.error(f"An error occurred: {e}")

