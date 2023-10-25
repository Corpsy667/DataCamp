import pandas as pd
from textblob import TextBlob

# Demander à l'utilisateur de saisir trois noms de chansons présentes dans la base de données
user_song_names = []
for i in range(3):
    song_name = input(f"Entrez le nom de la chanson, que des minuscules {i + 1}: ")
    user_song_names.append(song_name)

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