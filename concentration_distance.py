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

mina_dict = load_obj("mina_dict_ie_results") # dictionary with cluster ids as keys and lists of dictionaries as values

# HHI Index
for key, value in mina_dict.items():
    for dict in value:
        for key in dict.keys():
            topic_list = dict[key]
            new_topic_list = topic_list[2:-1]
            hhi = sum(map(lambda x: x*x, new_topic_list))
            topic_list.append(hhi)
            # topic list is now composed of T1, T2, topic distribution, sequence, and hhi
            dict[key] = topic_list

# Save dictionary object
save_obj(mina_dict, "mina_dict_ie_hhi")

# Write dictionary to csv file
with open('hhi_ie.csv', 'w', newline = '') as csv_file:
    fields = ["cluster_id", "id", "seq", "Topic1", "Topic2"]
    fields += ["T" + str(i) for i in range(1, 20)]
    fields.append("HHI")
    writer = csv.DictWriter(csv_file, fields)
    writer.writeheader()
    for key, value in mina_dict.items():
        for dict in value:
            for article_id, article_value in dict.items():
                topic_names = fields
                topic_values = [key, article_id, article_value[-2], article_value[0], article_value[1]] # cluster_id, id, seq, Topic1, Topic2
                topic_values += article_value[2:-2] # 19 topic percentages
                topic_values.append(article_value[-1]) # HHI
                #print(topic_values)
                topic_dict = {k: v for k, v in zip(topic_names, topic_values)}
                writer.writerow(topic_dict)

exit(1)

# Create a “distance measure” for each article relative to the first article
mina_dict = load_obj("mina_dict_ht")

# Append order of articles to end of topic distributions
topic_names = ["storytime", "id", "url", "cluster_id", "lmviews", "seq"]
topic_values = [str, int, str, int, np.float64, int]
col_dict = {k : v for k, v in zip(topic_names, topic_values)}
mina = pd.read_csv("../mina_HT.csv", usecols = topic_names, dtype = col_dict, engine = "python")

for i in range(mina.shape[0]):
    url = mina.loc[i, "url"]
    seq = mina.loc[i, "seq"]
    topic_list = mina_dict[url]
    topic_list.append(seq)
    mina_dict[url] = topic_list

# Mahalanobis Distance First
for key, value in mina_dict.items():
    primary_key = ""
    smallest_seq = 1000 # large placeholder
    first_top_dist = []
    # Identify first article
    for dict in value:
        for key in dict.keys():
            topic_list = dict[key]
            if (topic_list[-1] < smallest_seq):
                primary_key = key
                first_top_dist = topic_list[:-1]
    # Calculate distances
    for dict in value:
        if (primary_key in dict):
            topic_list = dict[primary_key]
            topic_list.append(0)
            dict[primary_key] = topic_list
        else:
            for key in dict.keys():
                topic_list = dict[key]
                topic_dist = topic_list[:-1]
                # Calculate Mahalanobis distance between topic_dist and first_top_dist
                iv = np.cov(np.array(topic_dist).T, np.array(first_top_dist).T)
                iv = np.linalg.inv(iv)
                mahal_dist = distance.mahalanobis(topic_dist, first_top_dist, iv)
                topic_list.append(mahal_dist)
                dict[key] = topic_list

save_obj(mina_dict, "mina_dict_ht_mahalanobis_first")
