import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Identify clusters that are predominantly one topic or another
# What does it mean for a cluster to be predominantly one topic?
# Take the average of all topics for each cluster
# Record clusters that have an average of any given topic 50% or greater

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

max_avg_topic = []
mina_dict = load_obj("mina_dict_ht")
for key, value in mina_dict.items(): # value is a list of dictionaries
    value_length = len(value)
    avg_topic_dist = [0 for i in range(0, 19)]
    for elem in value: # elem is a dictionary with a URL key and topic distribution value
        for key2, value2 in elem.items(): # value2 is a list of top two topics and topic percentages
            value2 = value2[2:]
            avg_topic_dist = np.array([a + b for a, b in zip(avg_topic_dist, value2)], dtype = 'f')
            #print(avg_topic_dist)
    avg_topic_dist = avg_topic_dist / value_length
    max_index = np.argmax(avg_topic_dist)
    if (avg_topic_dist[max_index] >= 50):
        max_avg_topic.append([key, max_index + 1])

print(len(max_avg_topic))
print(max_avg_topic[0:5])

# Create side-by-side bar plots of topic percentages

# Pass the x and y coordinates of the bars to the
# function. The label argument gives a label to the data.
for i in range(0, 2):
    list_dict = mina_dict[max_avg_topic[i][0]]
    index = 1
    for dict in list_dict:
        value = []
        for key in dict:
            value = dict[key]
        print(value)
        plt.bar([i for i in range(1, 20)], value[2:])
        plt.legend()

        # The following commands add labels to our figure.
        plt.xlabel('Topic Number')
        plt.ylabel('Topic Percentage')
        plt.title('Topic Percentage Distribution for Cluster ' + str(max_avg_topic[i][0]) + ' and Article ' + str(index))

        plt.show()
        index += 1

# Sentiment analysis visualizations
# Read in sentiment analysis csv file where urls are associated with sentiment scores

sentiment_scores = "../sentiment_scores_bing.csv"
sentiment = pd.read_csv(sentiment_scores, usecols = ["url", "sentiment", "positive", "negative"])

# Create new sentiment dictionary
sentiment_dict = {}

# Check whether urls exist in cluster dictionary (mina_dict)
for i in range(sentiment.shape[0]):
    print(i)
    # If so, assign cluster id as key and list of sentiment score, positive sentiment, and negative sentiment as value
    for key, value in mina_dict.items():
        for url in value:
            if (sentiment.loc[i, "url"] in url):
                sentiment_url = {"url": sentiment.loc[i, "url"], "sentiment": sentiment.loc[i, "sentiment"],
                                 "positive": sentiment.loc[i, "positive"] , "negative": sentiment.loc[i, "negative"]}
                if (key in sentiment_dict):
                    sentiment_dict_value = sentiment_dict[key]
                    sentiment_dict_value.append(sentiment_url)
                    sentiment_dict[key] = sentiment_dict_value
                else:
                    sentiment_dict[key] = [sentiment_url]

# Final result is a dictionary that organizes url and sentiment info by cluster
save_obj(sentiment_dict, "sentiment_dict_bing_ht")