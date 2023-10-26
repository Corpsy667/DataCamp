import Cleaning_data
import pandas as pd
from textblob import TextBlob



# Demander à l'utilisateur de saisir trois noms de chansons présentes dans la base de données
#user_song_names = []
#for i in range(3):
#    song_name = input(f"Entrez le nom de la chanson, que des minuscules {i + 1}: ")
 #   user_song_names.append(str(song_name).lower())

# Extraire les paroles (Lyrics) des chansons saisies par l'utilisateur
#user_song_lyrics = []
#for song_name in user_song_names:
 #   lyrics = filtered_df[filtered_df['Name'].str.lower()== song_name]['Lyrics'].values
##    if len(lyrics) > 0:
 #       user_song_lyrics.append(lyrics[0])
##    else:
 #       print(f"La chanson '{song_name}' n'a pas été trouvée dans la base de données.")

# Analyse des sentiments des paroles des chansons saisies par l'utilisateur
def dffeeling(df) :
    user_sentiments = [TextBlob(lyrics).sentiment.polarity for lyrics in df]

    if len(user_sentiments) != 0:
        # Comparaison des sentiments
        df2 = Cleaning_data.importing_data()
        df2['Difference'] = abs( df2['Sentiment'] - user_sentiments )

        # Sélection des trois chansons avec les sentiments les plus proches de celles saisies par l'utilisateur
        recommended_songs = df2.sort_values(by='Difference').head(3)

        # Afficher les recommandations à l'utilisateur
        return (recommended_songs)
    else:
        return []


from flask import Flask, request, jsonify



app = Flask(__name__)


# Exemple de base de données de musiques (remplacez par votre propre base de données)

data = Cleaning_data.importing_data()
@app.route('/api/search', methods=['GET'])

def search_music():
    try :
        query = " "
        query = request.args.get('query')
        if query is not None:
            # Par exemple, supposez que "database" est votre DataFrame
            results = data[data['Name'].str.lower().str.startswith(query.lower())][:3]
            
            suggestionsjson = results.to_dict(orient='records')

            # Renvoyez les suggestions au format JSON
            return jsonify(suggestionsjson) , {'Connection': 'keep-alive'}
        else:
        # Gérez le cas où q4
        # uery est None
            return jsonify([]) , {'Connection': 'keep-alive'}

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500


@app.route('/api/search-auteur', methods=['GET'])
def look_auteur():
    try :
        query = " "
        query = request.args.get('query')
        if query is not None:
            # Par exemple, supposez que "database" est votre DataFrame
            results = data[data['Artist'].str.lower().str.startswith(query.lower())][:3]
            
            suggestionsjson = results.to_dict(orient='records')

            # Renvoyez les suggestions au format JSON
            return jsonify(suggestionsjson) , {'Connection': 'keep-alive'}
        else:
        
            return jsonify([]) , {'Connection': 'keep-alive'}

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500

@app.route('/api/propose-auteur', methods=['GET'])
def propose_auteur():
    try :
        query = " "
        query = request.args.get('query')
        if query is not None:
            results = data[data['Name'].str.lower().str.startswith(query.lower())][:3]
            artistes = results['Artist'].tolist()
            a = data[data['Artist'].isin(artistes)]
            suggestionsjson = a.to_dict(orient='records')
            if a is not None :
                return jsonify(suggestionsjson) 
            else:
                return jsonify([]) , {'Connection': 'keep-alive'}
        else:
            return jsonify([]) , {'Connection': 'keep-alive'}

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500
    
@app.route('/api/propose-feeling', methods=['GET'])
def propose_mood():
    try :
        query = request.args.get('query')
        if query is not None:
            results = data[data['Name'].str.lower().str.startswith(query.lower())][:3]
            
            sent = results['Sentiment'].tolist() 
            senti = dffeeling(sent) 
            suggestionsjson = senti.to_dict(orient='records')
            return jsonify(suggestionsjson)
        else:
            return jsonify([])

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500


if __name__ == "__main__":
    app.run()