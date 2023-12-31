import Cleaning_data
from textblob import TextBlob
import pandas as pd
from DataCamp.Machine_learning import predicting_data_and_fitting
from DataCamp.Musixmatch import search_lyrics
import numpy as np


def dffeeling(df):
    user_sentiments = TextBlob(df["Lyrics"].to_string()).sentiment.polarity

    # Comparaison des sentiments
    df2 = Cleaning_data.importing_data()
    print("user sentiments", user_sentiments)
    df2['Difference'] = abs(df2['Sentiment'] - user_sentiments)

    # Sélection des trois chansons avec les sentiments les plus proches de celles saisies par l'utilisateur
    recommended_songs = df2.sort_values(by='Difference').head(3)

    # Afficher les recommandations à l'utilisateur
    return (recommended_songs)


from flask import Flask, request, jsonify

app = Flask(__name__)

# Exemple de base de données de musiques (remplacez par votre propre base de données)

data = Cleaning_data.importing_data()
grad = predicting_data_and_fitting(data)


@app.route('/api/search', methods=['GET'])
def search_music():
    try:
        query = " "
        query = request.args.get('query')
        if query is not None:
            # Par exemple, supposez que "database" est votre DataFrame
            results = data[data['Name'].str.lower().str.startswith(query.lower())][:3]

            suggestionsjson = results.to_dict(orient='records')

            # Renvoyez les suggestions au format JSON
            return jsonify(suggestionsjson), {'Connection': 'keep-alive'}
        else:
            # Gérez le cas où q4
            # uery est None
            return jsonify([]), {'Connection': 'keep-alive'}

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500


@app.route('/api/search-auteur', methods=['GET'])
def look_auteur():
    try:
        query = " "
        query = request.args.get('query')
        if query is not None:
            # Par exemple, supposez que "database" est votre DataFrame
            results = data[data['Artist'].str.lower().str.startswith(query.lower())][:3]

            suggestionsjson = results.to_dict(orient='records')

            # Renvoyez les suggestions au format JSON
            return jsonify(suggestionsjson), {'Connection': 'keep-alive'}
        else:

            return jsonify([]), {'Connection': 'keep-alive'}

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500


@app.route('/api/propose-auteur', methods=['GET'])
def propose_auteur():
    try:
        query = " "
        query = request.args.get('query')
        if query is not None:
            results = data[data['Name'].str.lower().str.startswith(query.lower())][:3]
            artistes = results['Artist'].tolist()
            a = data[data['Artist'].isin(artistes)]
            suggestionsjson = a.to_dict(orient='records')
            if a is not None:
                return jsonify(suggestionsjson)
            else:
                return jsonify([]), {'Connection': 'keep-alive'}
        else:
            return jsonify([]), {'Connection': 'keep-alive'}

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500


@app.route('/api/propose-feeling', methods=['GET'])
def propose_mood():
    try:
        query = request.args.get('query')
        if query is not None:
            results = data[data['Name'].str.lower().str.startswith(query.lower())]
            print(results)
            sent = dffeeling(results)
            suggestionsjson = sent.to_dict(orient='records')
            return jsonify(suggestionsjson)
        else:
            return jsonify([])

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500


@app.route('/api/pop', methods=['GET'])
def predict_pop():
    try:
        query = request.args.get('query')
        query2 = request.args.get('query2')
        if query is not None and query2 is not None:
            results = search_lyrics(query, query2)
            res = pd.DataFrame({'Sentiment': [results]})
            user_sentiment = TextBlob(res['Sentiment'].values[0]).sentiment.polarity
            user_sentiment = np.array(user_sentiment).reshape(1, -1)
            user_pop = grad.predict(user_sentiment)

            data['Difference_pop'] = abs(data['Popularity'] - user_pop)

            # Sélection des trois chansons avec les sentiments les plus proches de celles saisies par l'utilisateur
            reco = data.sort_values(by='Difference_pop').head(3)

            suggestionsjson = reco.to_dict(orient='records')
            return jsonify(suggestionsjson)
        else:
            return jsonify([])

    except Exception as e:
        app.logger.error(f"Erreur de recherche : {str(e)}")
        return "Erreur interne du serveur", 500


if __name__ == "__main__":
    app.run()
