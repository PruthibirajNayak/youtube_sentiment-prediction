from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from googleapiclient.discovery import build
from textblob import TextBlob
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static folder to serve HTML and CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

API_KEY = "AIzaSyA5k8WuyYP_PUxTS9FD4vIKEGTwrTJ-onQ"  # Replace with your API key

# Function to get YouTube comments
def get_youtube_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=50
    )
    response = request.execute()
    return [item["snippet"]["topLevelComment"]["snippet"]["textDisplay"] for item in response.get("items", [])]

# Function to analyze sentiment
def analyze_sentiment(comment):
    blob = TextBlob(comment)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    else:
        return "neutral"

# Serve the HTML page
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

# API endpoint for sentiment analysis
@app.get("/sentiment/{video_id}")
def sentiment_analysis(video_id: str):
    comments = get_youtube_comments(video_id)
    results = {"positive": [], "neutral": [], "negative": []}
    
    for comment in comments:
        sentiment = analyze_sentiment(comment)
        results[sentiment].append(comment)
    
    return JSONResponse(content=results)
