import requests

# Remplacez YOUR_API_KEY par votre clé d'API Musixmatch
api_key = "043ef90b80309d0fd8a8da75d6f9bd24	"

# Recherche de paroles de chanson
def search_lyrics(track_name, artist_name):
    base_url = "https://api.musixmatch.com/ws/1.1/"
    endpoint = "track.search"
    query_params = {
        "q_track": track_name,
        "q_artist": artist_name,
        "apikey": api_key,
    }

    response = requests.get(base_url + endpoint, params=query_params)

    if response.status_code == 200:
        data = response.json()
        # Récupérez l'ID de la chanson
        track_id = data["message"]["body"]["track_list"][0]["track"]["track_id"]

        # Obtenir les paroles de la chanson
        endpoint = "track.lyrics.get"
        query_params = {"track_id": track_id, "apikey": api_key}
        response = requests.get(base_url + endpoint, params=query_params)

        if response.status_code == 200:
            lyrics = response.json()["message"]["body"]["lyrics"]["lyrics_body"]
            return lyrics
        else:
            print("Erreur lors de la récupération des paroles.")
    else:
        print("Erreur lors de la recherche de la chanson.")

    return None

# Utilisation de la fonction pour rechercher les paroles d'une chanson
track_name = "Song Name"
artist_name = "Artist Name"
lyrics = search_lyrics(track_name, artist_name)

if lyrics:
    print(lyrics)
