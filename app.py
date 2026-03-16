from googleapiclient.discovery import build

API_KEY = "AIzaSyA5k8WuyYP_PUxTS9FD4vIKEGTwrTJ-onQ"
VIDEO_ID = "rcIA7QAhpH8"

def get_youtube_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=50  # Adjust as needed
    )
    
    response = request.execute()
    
    comments = [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response["items"]]
    return comments

# Example usage
comments = get_youtube_comments(VIDEO_ID)
print(comments)
