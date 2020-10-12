import pandas as pd
import numpy as np
import re
import pickle
import csv
from fuzzywuzzy import fuzz

topic_file = "../ie_topics_2.csv"
topic_names = ["T" + str(i) for i in range(1, 20)]
topic_values = [np.float64 for i in range(1, 20)]
topic_dict = {k : v for k, v in zip(topic_names, topic_values)}
topic_dict["id"] = int
topic_dict["Topic1"] = str
topic_dict["Topic2"] = str
col_names = ["id", "Topic1", "Topic2"] + topic_names
topics = pd.read_csv(topic_file, usecols = col_names, dtype = topic_dict)

# Create dictionary with id as keys and topic distributions as values
ie_topics = {}
for i in range(topics.shape[0]):
    id = topics.loc[i, "id"]
    topic_list = []
    topic_list.append(topics.loc[i, "Topic1"])
    topic_list.append(topics.loc[i, "Topic2"])
    topic_list_2 = [topics.loc[i, "T" + str(j)] for j in range(1, 20)]
    topic_list = topic_list + topic_list_2
    ie_topics[id] = topic_list

topic_names = ["storytime", "id", "url", "cluster_id", "lmviews", "seq"]
topic_values = [str, int, str, int, np.float64, int]
col_dict = {k : v for k, v in zip(topic_names, topic_values)}
mina = pd.read_csv("../mina_IE.csv", usecols = topic_names, dtype = col_dict, engine = "python")

mina_dict = {}
missing_ids = []
count_missing_ids = 0
for i in range(mina.shape[0]):
    id = mina.loc[i, "id"]
    cluster_id = mina.loc[i, "cluster_id"]
    seq = mina.loc[i, "seq"]
    if cluster_id in mina_dict.keys():
        dict_list = mina_dict[cluster_id]
        id_dict = {}
        # Find topic list associated with id
        if id in ie_topics:
            topic_list = ie_topics[id]
            topic_list.append(seq)
            id_dict[id] = topic_list
            dict_list.append(id_dict)
            mina_dict[cluster_id] = dict_list
        else:
            count_missing_ids += 1
            missing_ids.append(id)
    else:
        id_dict = {}
        # Find topic list associated with id
        if id in ie_topics:
            topic_list = ie_topics[id]
            topic_list.append(seq)
            id_dict[id] = topic_list
            mina_dict[cluster_id] = [id_dict]
        else:
            count_missing_ids += 1
            missing_ids.append(id)

with open('missing_ids.csv', 'w', newline = '') as result_file:
    for i in missing_ids:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow([i])

print(count_missing_ids)
print(len(mina_dict))

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

save_obj(mina_dict, "mina_dict_ie_results")

















