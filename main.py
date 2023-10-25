import Cleaning_data
import pandas as pd
from textblob import TextBlob

df = Cleaning_data.importing_data()
user_song_names = []
for i in range(3):
    song_name = input(f"Entrez le nom de la chanson {i + 1}: ")
    user_song_names.append(str(song_name).lower())

# Extraire les paroles (Lyrics) des chansons saisies par l'utilisateur
user_song_lyrics = []
for song_name in user_song_names:
    lyrics = df[df['Name'] == song_name]['Lyrics'].values
    if len(lyrics) > 0:
        user_song_lyrics.append(lyrics[0])
    else:
        print(f"La chanson '{song_name}' n'a pas été trouvée dans la base de données.")

# Analyse des sentiments des paroles des chansons saisies par l'utilisateur
user_sentiments = [TextBlob(lyrics).sentiment.polarity for lyrics in user_song_lyrics]

if len(user_sentiments) != 0:
    # Comparaison des sentiments
    df2 = df
    df2['Difference'] = abs(df['Sentiment'] - sum(user_sentiments) / len(user_sentiments))

    # Sélection des trois chansons avec les sentiments les plus proches de celles saisies par l'utilisateur
    recommended_songs = df2.sort_values(by='Difference').head(3)

    # Exclure les chansons que l'utilisateur a saisies de l'ensemble de recommandation
    # df = df[~df['Name'].isin(user_song_names)]

    # Afficher les recommandations à l'utilisateur
    print("Chansons recommandées:")
    print(recommended_songs[['Name', 'Artist', 'Album', 'Sentiment']])

else:
    print("il y a besoin d'au moins un élément pour que ça fonctionne")


from flask import Flask, request, jsonify

app = Flask(__name__)

# Exemple de base de données de musiques (remplacez par votre propre base de données)
database = df

@app.route('/api/search', methods=['GET'])
def search_music():
    try :
        query = "database"
        
        # Par exemple, supposez que "database" est votre DataFrame
        results = Cleaning_data.importing_data()
        # Convertissez les résultats en un dictionnaire Python
        suggestions = results.to_dict(orient='records')

        # Renvoyez les suggestions au format JSON
        return jsonify(suggestions)

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500

if __name__ == "__main__":
    app.run()
