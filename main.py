from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from ytmusicapi import YTMusic
import uvicorn

# Initialize YTMusic
ytmusic = YTMusic()
# Initialize FastAPI
app = FastAPI()

# Define the manifest as a dictionary
MANIFEST_DATA = {
    "id": "dev.abdullah.ytmusic-addon",
    "name": "YTMusic Free Addon",
    "version": "1.0.0",
    "resources": ["search", "stream"],
    "settings": [
        {
            "key": "quality",
            "type": "select",
            "default": "high",
            "options": [
                {"label": "High", "value": "high"},
                {"label": "Low", "value": "low"}
            ]
        }
    ]
}

@app.get("/")
async def root():
    return {"status": "online", "message": "BitChord Addon Server is running!"}

# Fixed Route for manifest.json
@app.get("/manifest.json")
async def get_manifest():
    return JSONResponse(
        content=MANIFEST_DATA, 
        headers={"Content-Type": "application/json", "Cache-Control": "no-store"}
    )

@app.get("/search")
async def search(q: str = ""):
    try:
        search_results = ytmusic.search(q, limit=20)
        tracks = []
        
        for result in search_results:
            if result['resultType'] == 'song':
                tracks.append({
                    "id": result['videoId'],
                    "title": result['title'],
                    "artist": result['artists'][0]['name'] if result['artists'] else "Unknown Artist",
                    "album": result.get('album', {}).get('name', 'N/A'),
                    "duration": result.get('duration', 0),
                    "artworkURL": result.get('thumbnail', 'https://via.placeholder.com/300'),
                    "format": "mp3",
                    "audioQuality": "HIGH"
                })
        
        return JSONResponse(content={"tracks": tracks}, headers={"Cache-Control": "no-store"})
    except Exception as e:
        return JSONResponse(content={"tracks": []}, status_code=500)

@app.get("/stream/{track_id}")
async def stream(track_id: str):
    return JSONResponse(content={
        "url": f"https://www.youtube.com/watch?v={track_id}",
        "format": "mp3",
        "quality": "High",
        "codec": "mp3",
        "container": "mp3",
        "manifest": "none",
        "encrypted": False,
        "sampleRate": 44100,
        "bitDepth": 16,
        "bitrate": 320
    }, headers={"Cache-Control": "no-store"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
