import requests
import datetime
import os

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

url = "https://graphql.anilist.co"

today = datetime.date.today()
query = """
query ($date: Int) {
  Page {
    airingSchedules(airingAt_greater: $date, airingAt_lesser: $datePlus) {
      media {
        title {
          romaji
        }
      }
      episode
    }
  }
}
"""

variables = {
    "date": int(today.strftime("%s")),
    "datePlus": int((today + datetime.timedelta(days=1)).strftime("%s"))
}

response = requests.post(url, json={"query": query, "variables": variables})
data = response.json()

if "data" in data:
    message = "🔥 SORTIES ANIME DU JOUR 🔥\n\n"
    for anime in data["data"]["Page"]["airingSchedules"]:
        title = anime["media"]["title"]["romaji"]
        episode = anime["episode"]
        message += f"• {title} — Épisode {episode}\n"

    message += "\n⭐ Mangas 2.0"

    send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(send_url, data={
        "chat_id": CHANNEL_ID,
        "text": message
    })
