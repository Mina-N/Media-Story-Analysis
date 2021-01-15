import pandas as pd
import numpy as np
import re
import pickle
import csv
from fuzzywuzzy import fuzz

topic_file = "../ht_Topic_Modeling/url_match_two_files/ht_topics.csv"
topic_names = ["T" + str(i) for i in range(1, 20)]
topic_values = [np.float64 for i in range(1, 20)]
topic_dict = {k : v for k, v in zip(topic_names, topic_values)}
topic_dict["id"] = int
topic_dict["url"] = str
topic_dict["Topic1"] = str
topic_dict["Topic2"] = str
col_names = ["id", "url", "Topic1", "Topic2"] + topic_names
topics = pd.read_csv(topic_file, usecols = col_names, dtype = topic_dict)

# Change ids
# count = 0
# for i in range(topics.shape[0]):
#     six_digits = re.findall(r'(\d{6})\.', topics.loc[i, "url"])
#     if (six_digits):
#         six_digits = ''.join(item for item in six_digits)
#         print(six_digits)
#         topics.loc[i, "id"] = int(six_digits)
#     else:
#         count += 1
#
# print(count)

# Create dictionary with url as keys and topic distributions as values
ht_topics = {}
for i in range(topics.shape[0]):
    url = topics.loc[i, "url"]
    topic_list = []
    topic_list.append(topics.loc[i, "Topic1"])
    topic_list.append(topics.loc[i, "Topic2"])
    topic_list_2 = [topics.loc[i, "T" + str(j)] for j in range(1, 20)]
    topic_list = topic_list + topic_list_2
    ht_topics[url] = topic_list

topic_names = ["storytime", "id", "url", "cluster_id", "lmviews", "seq"]
topic_values = [str, int, str, int, np.float64, int]
col_dict = {k : v for k, v in zip(topic_names, topic_values)}
mina = pd.read_csv("../mina_HT.csv", usecols = topic_names, dtype = col_dict, engine = "python")

mina_dict = {}
missing_urls = []
count_missing_urls = 0
for i in range(mina.shape[0]):
    url = mina.loc[i, "url"]
    cluster_id = mina.loc[i, "cluster_id"]
    seq = mina.loc[i, "seq"]
    if cluster_id in mina_dict.keys():
        dict_list = mina_dict[cluster_id]
        url_dict = {}
        # Find topic list associated with id
        if url in ht_topics:
            topic_list = ht_topics[url]
            topic_list.append(seq)
            url_dict[url] = topic_list
            dict_list.append(url_dict)
            mina_dict[cluster_id] = dict_list
        else:
            count_missing_urls += 1
            missing_urls.append(url)
    else:
        url_dict = {}
        # Find topic list associated with id
        if url in ht_topics:
            topic_list = ht_topics[url]
            topic_list.append(seq)
            url_dict[url] = topic_list
            mina_dict[cluster_id] = [url_dict]
        else:
            count_missing_urls += 1
            missing_urls.append(url)

# with open('missing_urls.csv', 'w', newline = '') as result_file:
#     for i in missing_urls:
#         wr = csv.writer(result_file, dialect='excel')
#         wr.writerow([i])

print(count_missing_urls)
print(len(mina_dict))

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

save_obj(mina_dict, "mina_dict_ht_results")