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
    
    color=['#2AA683', '#C9040C' ,'#C09209', '#28560C', '#FC1833']
    amounts = {name: (len(df[df['name'] == name])) for name in names}

    amounts = order_dictionary(amounts)
  
    total = sum(amounts.values())
    print(total)
    print(total)
    personen = [ ' '.join(i.split(' ')[1:3]) for i in amounts.keys()]

    personen2 = [i + 1 for i in range(len (personen))]
    plt.xlabel('Personen')
    plt.ylabel('Berichten')
    

    plt.bar(personen2, amounts.values(), color = color)
    plt.xticks(rotation = 90) # 
    plt.tight_layout()
    plt.xticks(personen2)
    plt.savefig('sended_messages2.jpg')
    # plt.savefig('sended_messages2.jpg')
    
    plt.show()

def distributions(df):
    color=['#2AA683', '#C9040C' ,'#C09209', '#28560C', '#FC1833']
    times = ['month', 'year', 'day', 'hour']

    for time in times:
        amounts = {(len(df[df[time] == name])): name for name in df[time].unique()}
        plt.bar(x=order_dictionary(amounts).values(), height=order_dictionary(amounts).keys(), color = color)
        plt.xticks(list(order_dictionary(amounts).values()))
        plt.tight_layout()
        
        plt.savefig(f'time_distributions/{time}_message_distribution.jpg')
        plt.close()

def word_count(df, names, counted_word):

    word_count_pp = {}
    counted_word = counted_word.upper()
    for name in names:
        all_messages = ''
        # print(df)
        for i in df[df['name'] == name]['message']:
            all_messages = all_messages + i

        # print(all_messages)
        words = re.findall(r'\w+', all_messages)

        cap_words = [word.upper() for word in words] #capitalizes all the words

        word_counts = Counter(cap_words)[counted_word] #counts the number each time a word appears
        
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

    personen = [ ' '.join(i.split(' ')[1:3]) for i in sentiment_score.keys()]

    color=['#2AA683', '#C9040C' ,'#C09209', '#28560C', '#FC1833']

    print(personen)
    plt.xlabel('Personen')
    plt.ylabel('Berichten')
    plt.bar(personen, sentiment_score.values(), color = color)
    plt.xticks(rotation = 90) # 
    plt.tight_layout()
    plt.show()
    return sentiment_score



if __name__ == "__main__":

    df = get_df()

    names = get_names(df)

    # print(word_count(df, names, "photo"))

    distributions(df)
    # print(sentiment_analysis(df, names))
    # sended_messages_count(df, names)