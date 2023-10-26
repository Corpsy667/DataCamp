import pandas as pd
from textblob import TextBlob


pd.set_option('display.max_columns', 10)
def importing_data():
    df = pd.read_csv("songs.csv", encoding="utf-8")
    df_fil = df['Lyrics'].str.split(pat = 'Lyrics\[', n = 1).str[-1]
    df["Lyrics"] = df_fil
    mask = ~df['Lyrics'].str.contains('Lyrics')
    filtered_df = df[mask]
    filtered_df.reset_index(inplace = True)
    filtered_df.drop(labels = "index", axis = 1)
    mots_a_effacer = ['\n', 'Verse 1]', '[Verse 2]',"[Verse 3]","[Outro]","[Chorus]", "[Intro]","Intro]","Chorus]","[Drop]","]","[","    ","'   ",'\r']
    mot_remp = ["(",")"]
    filtered_df.loc[:, 'Lyrics'] = filtered_df['Lyrics'].apply(lambda x: effacer_mots(x, mots_a_effacer))
    filtered_df.loc[:, 'Lyrics'] = filtered_df['Lyrics'].apply(lambda x: remplace(x, mot_remp))
    filtered_df = filtered_df.copy()
    filtered_df.loc[:, 'Sentiment'] = filtered_df['Lyrics'].apply(lambda x: TextBlob(x).sentiment.polarity)
    #print("filtered_df", filtered_df)
    return filtered_df
# Fonction pour effacer les mots
def effacer_mots(texte, mots_a_effacer):
    for mot in mots_a_effacer:
        texte = texte.replace(mot, ' ')
    return texte

def remplace(texte, mot_remp):
    for mot in mot_remp:
        texte = texte.replace(mot, '-')
    return texte


