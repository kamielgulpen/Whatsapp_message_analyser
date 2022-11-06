import pandas as pd
import dateparser
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

from utils import *


# Based on http://www.clips.ua.ac.be/pages/sentiment-analysis-for-dutch
# Documentation at http://www.clips.ua.ac.be/pages/pattern-nl#sentiment
# Installation documentation can be found at https://github.com/clips/pattern

# Import the sentiment analyse module from the pattern module
from pattern.nl import sentiment


def sended_messages_count(df, names):

    amounts = {name: (len(df[df['name'] == name])) for name in names}

    amounts = order_dictionary(amounts)
  
    total = sum(amounts.values())
    print(total)
    print(max(amounts.values()))
    plt.xlabel('Personen')
    plt.ylabel('Berichten')
    plt.bar(amounts.keys(), amounts.values())
    plt.xticks(rotation = 45) # 
    plt.tight_layout()
    plt.show()

def distributions(df):

    times = ['hour', 'year', 'day']

    for time in times:

        sns.histplot(x=time, data=df)
        plt.tight_layout()
        plt.savefig(f'time_distributions/{time}_message_distribution.jpg')
        plt.close()

def word_count(df, names, word):

    word_count_pp = {}

    for name in names:
        all_messages = ''
        # print(df)
        for i in df[df['name'] == name]['message']:
            all_messages = all_messages + i

        # print(all_messages)
        words = re.findall(r'\w+', all_messages)

        cap_words = [word.upper() for word in words] #capitalizes all the words

        word_counts = Counter(cap_words)[word] #counts the number each time a word appears

        word_count_pp[name] = word_counts
        
    return order_dictionary(word_count_pp)

def sentiment_analysis(df, names):
    
    sentiment_score =  {}
    for name in names:

        df_tmp = df[df['name'] == name]

        sentiments = []
        sentiments2 = []

        for i in df_tmp['message']:
            sent = sentiment(i)[0]
            sentiments.append(sent)
            predictedSentiment = 'neutral'
            if sent > 0.4:
                predictedSentiment = 'positive'
            elif sent < -0.2:
                predictedSentiment = 'negative'

        sentiment_score[name] = np.mean(sentiments)
    
    sentiment_score = order_dictionary(sentiment_score)

    return sentiment_score



if __name__ == "__main__":

    df = get_df()

    names = get_names(df)

    word_count(df, names, "nice")
    distributions(df)
    sentiment_analysis(df, names)