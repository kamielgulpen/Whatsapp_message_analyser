import pandas as pd
import dateparser
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
# Based on http://www.clips.ua.ac.be/pages/sentiment-analysis-for-dutch
# Documentation at http://www.clips.ua.ac.be/pages/pattern-nl#sentiment
# Installation documentation can be found at https://github.com/clips/pattern

# Import the sentiment analyse module from the pattern module
from pattern.nl import sentiment

df = pd.read_csv('messages.csv')

def order_dictionary(dictionary):
    
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1])}


def get_names(df):

        
    names_tmp = df.name.value_counts().rename_axis('unique_values').reset_index(name='counts')

    names = names_tmp[names_tmp['counts'] > 10].unique_values.to_list()

    return names

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


# print(dateparser.parse(df['date'][0]))
def distributions(df):
    sns.histplot(x='hour', data=df)
    plt.show()

    sns.histplot(x='year', data=df)
    plt.show()

    sns.histplot(x='month', data=df)
    plt.show()

    sns.histplot(x='day', data=df)
    plt.show()

    print(df[df['year'] == 2021])


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

        print(word_count_pp)
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



names = get_names(df)


# print(sentiment_analysis(df, names))


print(word_count(df, names, 'KANKER'))

# distributions(df)