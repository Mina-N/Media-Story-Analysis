import pandas as pd
import numpy as np
import re
import pickle
import csv


topic_file = "../ie_topics.csv"
topic_names = ["T" + str(i) for i in range(1, 21)]
topic_values = [np.float64 for i in range(1, 21)]
topic_dict = {k : v for k, v in zip(topic_names, topic_values)}
topic_dict["url"] = str
topic_dict["text"] = str
topic_dict["Topic1"] = str
topic_dict["Topic2"] = str
col_names = ["url", "text", "Topic1", "Topic2"] + topic_names
topics = pd.read_csv(topic_file, usecols = col_names, dtype = topic_dict)

ht_directory_1 = "../ie/ie1-6monthsscrapedinfo.csv"
ht_directory_2 = "../ie/ie7-12monthsscrapedinfo.csv"
ht1 = pd.read_csv(ht_directory_1, usecols = ["text", "url"])
ht2 = pd.read_csv(ht_directory_2, usecols = ["text", "url"])

print(ht1.shape[0])
print(ht2.shape[0])

topic_text = []
temp_df = topics.loc[:, 'text']
for i in range(temp_df.shape[0]):
    topic_text.append(temp_df.iloc[i])

topic_vals = []
temp_df = topics.loc[:, 'Topic1' : 'T20']
for i in range(temp_df.shape[0]):
    topic_vals.append(list(temp_df.iloc[i, :]))

# topics_dict contains topic text and topic dist from combined file
topics_dict = {k : v for k, v in zip(topic_text, topic_vals)}

count = 0
count1 = 0
count2 = 0
for i in range(ht1.shape[0]):
    text = ht1.loc[i, "text"]
    if ((isinstance(text, float) == False) and (len(text) != 0)):
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("'", "")
        text = text.replace("-", " ")
        text = re.sub("[^abcdefghijklmnopqrstuvwxyzABCDEFHIJKLMNOPQRSTUVWXZ ]", " ", text)
        text = text.lower()
        text = re.sub("\\s+", " ", text)
        text = text.strip()

        if (text in topics_dict.keys()):
            count += 1
            topic_list = topics_dict[text]
            topic_list.append(ht1.loc[i, "url"])
            topics_dict[text] = topic_list
        else:
            count1 += 1
    else:
        count2 += 1


count = 0
count1 = 0
count2 = 0
for i in range(ht2.shape[0]):
    text = ht2.loc[i, "text"]
    if ((isinstance(text, float) == False) and (len(text) != 0)):
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("'", "")
        text = text.replace("-", " ")
        text = re.sub("[^abcdefghijklmnopqrstuvwxyzABCDEFHIJKLMNOPQRSTUVWXZ ]", " ", text)
        text = text.lower()
        text = re.sub("\\s+", " ", text)
        text = text.strip()

        if (text in topics_dict.keys()):
            count += 1
            topic_list = topics_dict[text]
            topic_list.append(ht2.loc[i, "url"])
            topics_dict[text] = topic_list
        else:
            count1 += 1
    else:
        count2 += 1


new_topics_dict = {}
for key, val in topics_dict.items():
    old_key = key
    old_val = val
    new_val = old_val[0:22] # 22 for IE, 21 for HT
    new_key = old_val[22:]
    #(new_val)
    #print(new_key)
    for i in new_key:
        new_topics_dict[i] = new_val

col_type = {"article_title": str, "URL": str, "cluster_id" : int}
combined = []
for i in range(1, 13):
    for j in range(1, 4):
        combined.append(pd.read_csv("../ie/ie_combined_mo" + str(i) + "p" + str(j) + ".csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type))

combined = pd.concat(combined, ignore_index = True)

combined["Topic1"] = ""
combined["Topic2"] = ""
for i in range(1, 21):
    combined["T" + str(i)] = 0

print(combined.head())
unmatched_urls = []
count = 0
for i in range(combined.shape[0]):
    if ((str(combined.loc[i, "URL"]) + "\n") in new_topics_dict.keys()):
        top_list = new_topics_dict[combined.loc[i, "URL"] + "\n"]
        combined.loc[i, "Topic1" : "T20"] = top_list
    elif (str(combined.loc[i, "URL"]) in new_topics_dict.keys()):
        top_list = new_topics_dict[combined.loc[i, "URL"]]
        combined.loc[i, "Topic1": "T20"] = top_list
        print("GOT HERE")
    else:
        count += 1
        unmatched_urls.append(combined.loc[i, "URL"])
        print("OH NOOOOOOOO")

print(count)
print(combined.head())
combined.to_csv("ie_combined.csv")

with open('unmatched_urls.csv','w') as result_file:
    wr = csv.writer(result_file, dialect='excel')
    wr.writerows(unmatched_urls)

exit(1)

topic_names = ["article_title", "URL", "cluster_id", "Topic1", "Topic2"]
topic_dist = ["T" + str(i) for i in range(1, 20)]
topic_names = topic_names + topic_dist
topic_values = [str, str, int, str, str]
topic_values = topic_values + [np.float64 for i in range(1, 20)]
col_dict = {k : v for k, v in zip(topic_names, topic_values)}
combined = pd.read_csv("ht_combined.csv", usecols = topic_names , dtype = col_dict)

combined_dict = {}
for i in range(combined.shape[0]):
        combined_dict[combined.loc[i, "URL"]] = [combined.loc[i, "Topic1"], combined.loc[i, "Topic2"],
                                combined.loc[i, "T1"], combined.loc[i, "T2"], combined.loc[i, "T3"], combined.loc[i, "T4"],
                               combined.loc[i, "T5"], combined.loc[i, "T6"], combined.loc[i, "T7"], combined.loc[i, "T8"],
                               combined.loc[i, "T9"], combined.loc[i, "T10"], combined.loc[i, "T11"], combined.loc[i, "T12"],
                               combined.loc[i, "T13"], combined.loc[i, "T14"], combined.loc[i, "T15"], combined.loc[i, "T16"],
                               combined.loc[i, "T17"], combined.loc[i, "T18"], combined.loc[i, "T19"]]

topic_names = ["storytime", "id", "url", "cluster_id", "lmviews", "seq"]
topic_values = [str, int, str, int, np.float64, int]
col_dict = {k : v for k, v in zip(topic_names, topic_values)}
mina = pd.read_csv("../mina_IE.csv", usecols = topic_names, dtype = col_dict)

mina_dict = {}
for i in range(mina.shape[0]):
    cluster_id = mina.loc[i, "cluster_id"]
    if cluster_id in mina_dict.keys():
        print("got here")
        dict_list = mina_dict[cluster_id]
        url_dict = {}
        top_list = combined_dict[mina.loc[i, "url"]]
        url_dict[mina.loc[i, "url"]] = top_list
        dict_list.append(url_dict)
        mina_dict[cluster_id] = dict_list
    else:
        url_dict = {}
        top_list = combined_dict[mina.loc[i, "url"]]
        url_dict[mina.loc[i, "url"]] = top_list
        mina_dict[cluster_id] = [url_dict]

print(len(mina_dict))

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

save_obj(mina_dict, "mina_dict_ie")

















