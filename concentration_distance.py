import pandas as pd
import numpy as np
import pickle
from scipy.spatial import distance
import csv

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

# mina_dict = load_obj("mina_dict_ht_results") # dictionary with cluster_ids as keys and lists of dictionaries as values
#
# # # HHI Index
# for key, value in mina_dict.items():
#     for dict in value:
#         for key in dict.keys():
#             topic_list = dict[key]
#             new_topic_list = topic_list[2:-1]
#             hhi = sum(map(lambda x: x*x, new_topic_list))
#             topic_list.append(hhi)
#             # topic list is now composed of T1, T2, topic distribution, sequence, and hhi
#             dict[key] = topic_list
#
# # Save dictionary object
# save_obj(mina_dict, "mina_dict_ht_hhi")
#
# #Write dictionary to csv file
# with open('hhi_ht.csv', 'w', newline = '') as csv_file:
#     fields = ["cluster_id", "id", "seq", "Topic1", "Topic2"]
#     fields += ["T" + str(i) for i in range(1, 20)]
#     fields.append("HHI")
#     writer = csv.DictWriter(csv_file, fields)
#     writer.writeheader()
#     for key, value in mina_dict.items():
#         for dict in value:
#             for article_id, article_value in dict.items():
#                 topic_names = fields
#                 topic_values = [key, article_id, article_value[-2], article_value[0], article_value[1]] # cluster_id, id, seq, Topic1, Topic2
#                 topic_values += article_value[2:-2] # 19 topic percentages
#                 topic_values.append(article_value[-1]) # HHI
#                 #print(topic_values)
#                 topic_dict = {k: v for k, v in zip(topic_names, topic_values)}
#                 writer.writerow(topic_dict)



#Create a “distance measure” for each article relative to the first article
# mina_dict = load_obj("mina_dict_ht_results")
#
# topic_names = ["T" + str(i) for i in range(1, 20)]
# topic_values = [np.float64 for i in range(1, 20)]
# col_dict = {k : v for k, v in zip(topic_names, topic_values)}
# topic_perc = pd.read_csv("hhi_ht.csv", usecols = topic_names, dtype = col_dict, engine = "python")
#
# # Calculate inverse of covariance matrix
# V = np.cov(np.array(topic_perc).T)
# iv = np.linalg.inv(V)
#
# # Mahalanobis Distance First
# for key, value in mina_dict.items():
#     primary_key = ""
#     min_value = 1000
#     first_top_dist = []
#     # Identify first article
#     flag = 0
#     for dict in value:
#         for key in dict.keys():
#             topic_list = dict[key]
#             if (topic_list[-1] < min_value):
#                 min_value = topic_list[-1]
#                 primary_key = key
#                 first_top_dist = topic_list[2:-1]
#
#     # Calculate distances
#     for dict in value:
#         if (primary_key in dict):
#             topic_list = dict[primary_key]
#             topic_list.append(0)
#             dict[primary_key] = topic_list
#         else:
#             for key in dict.keys():
#                 topic_list = dict[key]
#                 new_topic_dist = topic_list[2:-1]
#                 # Calculate Mahalanobis distance between topic_dist and first_top_dist
#                 mahal_dist = distance.mahalanobis(new_topic_dist, first_top_dist, iv)
#                 topic_list.append(mahal_dist)
#                 dict[key] = topic_list
#
# save_obj(mina_dict, "mina_dict_ht_mahalanobis_first")
#
#
# # Write dictionary to csv file
# with open('mahal_first_ht.csv', 'w', newline = '') as csv_file:
#     fields = ["cluster_id", "id", "seq", "Topic1", "Topic2"]
#     fields += ["T" + str(i) for i in range(1, 20)]
#     fields.append("Mahalanobis First")
#     writer = csv.DictWriter(csv_file, fields)
#     writer.writeheader()
#     for key, value in mina_dict.items():
#         for dict in value:
#             for article_id, article_value in dict.items():
#                 topic_names = fields
#                 topic_values = [key, article_id, article_value[-2], article_value[0], article_value[1]] # cluster_id, id, seq, Topic1, Topic2
#                 topic_values += article_value[2:-2] # 19 topic percentages
#                 topic_values.append(article_value[-1]) # Mahalanobis first distance
#                 topic_dict = {k: v for k, v in zip(topic_names, topic_values)}
#                 writer.writerow(topic_dict)


# Sentiment analysis visualizations
# Read in sentiment analysis csv file where urls are associated with sentiment scores
# mina_dict = load_obj("mina_dict_ht_results")
# sentiment_scores = "../ht_Topic_Modeling/url_match_two_files/sentiment_scores_nrc.csv"
# sentiment = pd.read_csv(sentiment_scores, usecols = ["url", "anger", "anticipation", "disgust", "fear", "joy", "negative",
#                                                      "positive", "sadness", "surprise", "trust", "sentiment"])
#
# for i in range(sentiment.shape[0]):
#     print(i)
#     article_url = sentiment.loc[i, "url"]
#     for key, value in mina_dict.items():
#         for dict in value:
#             if (article_url in dict):
#                 print("GOT HERE")
#                 topic_list = dict[article_url]
#                 topic_list += [sentiment.loc[i, emotion] for emotion in ["anger", "anticipation", "disgust", "fear",
#                                                                          "joy", "negative", "positive", "sadness",
#                                                                          "surprise", "trust", "sentiment"]]
#                 dict[article_url] = topic_list
#
# print("DONE WITH DICTIONARY")
# # Save dictionary object
# save_obj(mina_dict, "mina_dict_ht_sent")
# mina_dict_ht_sent = load_obj("mina_dict_ht_sent")

# with open('sentiment_nrc_ht.csv', 'w', newline = '') as csv_file:
#     fields = ["cluster_id", "url", "seq", "Topic1", "Topic2"]
#     fields += ["T" + str(i) for i in range(1, 20)]
#     fields += ["anger", "anticipation", "disgust", "fear", "joy", "negative",
#                                                      "positive", "sadness", "surprise", "trust", "sentiment"]
#     writer = csv.DictWriter(csv_file, fields)
#     writer.writeheader()
#     for key, value in mina_dict_ht_sent.items():
#         for dict in value:
#             for article_url, article_value in dict.items():
#                 topic_names = fields
#                 topic_values = [key, article_url, article_value[-12], article_value[0],
#                                 article_value[1]]  # cluster_id, id, seq, Topic1, Topic2
#                 topic_values += article_value[2:21]  # 19 topic percentages
#                 topic_values += article_value[-11:]  # sentiment scores
#                 topic_dict = {k: v for k, v in zip(topic_names, topic_values)}
#                 writer.writerow(topic_dict)
#
# print("DONE WITH CSV")

# sentiment_file = "sentiment_nrc_ht.csv"
# col_names = ["cluster_id", "url", "seq", "Topic1", "Topic2", "anger", "anticipation", "disgust", "fear", "joy", "negative", "positive", "sadness", "surprise", "trust", "sentiment"]
# sentiment_values = [int, str, np.float64, str, str] + [np.float64 for i in range(1, 12)]
# sentiment_dict = {k : v for k, v in zip(col_names, sentiment_values)}
# sentiments = pd.read_csv(sentiment_file, usecols = col_names, dtype = sentiment_dict)
# #print(sentiments.head())
#
# word_count = pd.read_csv("../ht_word_count.csv", usecols = ["url", "WordCount"], dtype = {"url": str, "WordCount": int})
# #print(word_count.head())
# word_count_dict = {k : v for k, v in zip(word_count["url"], word_count["WordCount"])}
#
# for i in range(sentiments.shape[0]):
#     print(i)
#     article_url = sentiments.loc[i, "url"]
#     if (article_url in word_count_dict):
#         word_count = word_count_dict[article_url]
#         sentiments.loc[i, "anger" : "trust"] = sentiments.loc[i, "anger" : "trust"] / word_count
#         sentiments.loc[i, "sentiment"] = sentiments.loc[i, "positive"] - sentiments.loc[i, "negative"]
#
# V = np.cov(np.array(sentiments.loc[:, "anger" : "sentiment"]).T)
# iv = np.linalg.inv(V)
#
# # create sentiment_dict dictionary
# sentiment_dict = {}
# for i in range(sentiments.shape[0]):
#     url = sentiments.loc[i, "url"]
#     cluster_id = sentiments.loc[i, "cluster_id"]
#     seq = int(sentiments.loc[i, "seq"])
#     if cluster_id in sentiment_dict.keys():
#         dict_list = sentiment_dict[cluster_id]
#         url_dict = {}
#         sentiment_list = list(sentiments.loc[i, "Topic1" : "sentiment"])
#         sentiment_list.append(seq)
#         url_dict[url] = sentiment_list
#         dict_list.append(url_dict)
#         sentiment_dict[cluster_id] = dict_list
#     else:
#         url_dict = {}
#         sentiment_list = list(sentiments.loc[i, "Topic1" : "sentiment"])
#         sentiment_list.append(seq)
#         url_dict[url] = sentiment_list
#         sentiment_dict[cluster_id] = [url_dict]
#
# print("dictionary done")
#
# # Mahalanobis Distance First
# for key, value in sentiment_dict.items():
#      primary_key = ""
#      min_value = 1000
#      first_sent_dist = []
#      # Identify first article
#      flag = 0
#      for dict in value:
#          for key in dict.keys():
#              sent_list = dict[key]
#              if (sent_list[-1] < min_value):
#                  min_value = sent_list[-1]
#                  primary_key = key
#                  first_sent_dist = sent_list[2:-1] # values of dictionaries need to be: Topic1, Topic2, anger ....sentiment, seq
#                  print(first_sent_dist)
#
#      # Calculate distances
#      for dict in value:
#          if (primary_key in dict):
#              sent_list = dict[primary_key]
#              sent_list.append(0) # values of dictionaries now end with mahalanobis distance
#              dict[primary_key] = sent_list
#          else:
#              for key in dict.keys():
#                  sent_list = dict[key]
#                  new_sent_dist = sent_list[2:-1]
#                  # Calculate Mahalanobis distance between sent_dist and first_sent_dist
#                  mahal_dist = distance.mahalanobis(new_sent_dist, first_sent_dist, iv)
#                  sent_list.append(mahal_dist) # values of dictionaries now end with mahalanobis distance
#                  dict[key] = sent_list
#
# save_obj(sentiment_dict, "mina_sent_ht_mahalanobis_first")

# Write to csv file
mina_dict = load_obj("mina_sent_ht_mahalanobis_first")

with open('sentiment_mahalanobis_ht.csv', 'w', newline = '') as csv_file:
    fields = ["cluster_id", "url", "seq", "Topic1", "Topic2"]
    fields += ["anger", "anticipation", "disgust", "fear", "joy", "negative", "positive", "sadness", "surprise", "trust", "sentiment"]
    fields.append("MahalanobisSentiment")
    writer = csv.DictWriter(csv_file, fields)
    writer.writeheader()
    for key, value in mina_dict.items():
        for dict in value:
            for article_url, article_value in dict.items():
                topic_names = fields
                topic_values = [key, article_url, article_value[-2], article_value[0], article_value[1]] # cluster_id, id, seq, Topic1, Topic2
                topic_values += article_value[2:-2] # 11 sentiment values
                topic_values.append(article_value[-1]) # Mahalanobis distance
                topic_dict = {k: v for k, v in zip(topic_names, topic_values)}
                writer.writerow(topic_dict)