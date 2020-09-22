import pandas as pd
import numpy as np
import re

topic_file = "../ht_topics.csv"
topic_names = ["T" + str(i) for i in range(1, 20)]
topic_values = [np.float64 for i in range(1, 20)]
topic_dict = {k : v for k, v in zip(topic_names, topic_values)}
topic_dict["url"] = str
topic_dict["article_text"] = str
topic_dict["Topic1"] = str
topic_dict["Topic2"] = str
col_names = ["url", "article_text", "Topic1", "Topic2"] + topic_names
topics = pd.read_csv(topic_file, usecols = col_names, dtype = topic_dict)

ht_directory_1 = "../ht/ht1-6monthsscrapedinfo.csv"
ht_directory_2 = "../ht/ht7-12monthsscrapedinfo.csv"
ht1 = pd.read_csv(ht_directory_1, usecols = ["article_text", "url"])
ht2 = pd.read_csv(ht_directory_2, usecols = ["article_text", "url"])

print(ht1.shape[0])
print(ht2.shape[0])

topic_text = []
temp_df = topics.loc[:, 'article_text']
for i in range(temp_df.shape[0]):
    topic_text.append(temp_df.iloc[i])

topic_vals = []
temp_df = topics.loc[:, 'Topic1' : 'T19']
for i in range(temp_df.shape[0]):
    topic_vals.append(list(temp_df.iloc[i, :]))

topics_dict = {k : v for k, v in zip(topic_text, topic_vals)}

count = 0
for i in range(ht1.shape[0]):
    text = ht1.loc[i, "article_text"]
    if ((isinstance(text, float) == False) and (len(text) != 0)):
        text = text.replace("\n", " ")
        text = text.replace("\r", " ")
        text = text.replace("'", "")
        text = text.replace("-", " ")
        text = re.sub("[^abcdefghijklmnopqrstuvwxyzABCDEFHIJKLMNOPQRSTUVWXZ ]", " ", text)
        text = text.lower()
        text = re.sub("\\s+", " ", text)
        text = text.strip()

        # 9 ARTICLES THAT WERE NOT FOUND
        if (text in topics_dict.keys()):
            count += 1
            topic_list = topics_dict[text]
            topic_list.append(ht1.loc[i, "url"])
            topics_dict[text] = topic_list

print(count)

count = 0
for i in range(ht2.shape[0]):
    text = ht2.loc[i, "article_text"]
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

print(count)

#
# new_topics_dict = {}
# for key, val in topics_dict.items():
#     old_key = key
#     old_val = val
#     new_val = old_val[0:21]
#     new_key = old_val[21:]
#     print(new_val)
#     print(new_key)
#     for i in new_key:
#         new_topics_dict[i] = new_val

# col_type = {"article_title": str, "URL": str, "cluster_id" : int}
# combined1 = pd.read_csv("../ht/ht_combined_mo1.csv", usecols = ["article_title", "URL", "cluster_id"] , dtype = col_type)
# combined2 = pd.read_csv("../ht/ht_combined_mo2.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined3 = pd.read_csv("../ht/ht_combined_mo3.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined4 = pd.read_csv("../ht/ht_combined_mo4.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined5 = pd.read_csv("../ht/ht_combined_mo5.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined6 = pd.read_csv("../ht/ht_combined_mo6.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined7 = pd.read_csv("../ht/ht_combined_mo7.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined8 = pd.read_csv("../ht/ht_combined_mo8.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined9 = pd.read_csv("../ht/ht_combined_mo9.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined10 = pd.read_csv("../ht/ht_combined_mo10.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined11 = pd.read_csv("../ht/ht_combined_mo11.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)
# combined12 = pd.read_csv("../ht/ht_combined_mo12.csv", usecols = ["article_title", "URL", "cluster_id"], dtype = col_type)

# combined = pd.concat([combined1, combined2, combined3, combined4, combined5, combined6,
#                       combined7, combined8, combined9, combined10, combined11, combined12],
#                      ignore_index = True)
#
# combined["Topic1"] = ""
# combined["Topic2"] = ""
# for i in range(1, 20):
#     combined["T" + str(i)] = 0
#
# for i in range(combined.shape[0]):
#     if (combined.loc[i, "URL"] in new_topics_dict.keys()):
#         top_list = new_topics_dict[combined.loc[i, "URL"]]
#         combined.loc[i, "Topic1" : "T19"] = top_list
#
# print(combined.head())
# combined.to_csv("ht_combined.csv")

topic_names = ["article_title", "URL", "cluster_id", "Topic1", "Topic2"]
topic_dist = ["T" + str(i) for i in range(1, 20)]
topic_names = topic_names + topic_dist
topic_values = [str, str, int, str, str]
topic_values = topic_values + [np.float64 for i in range(1, 20)]
col_dict = {k : v for k, v in zip(topic_names, topic_values)}

combined = pd.read_csv("ht_combined.csv", usecols = topic_names , dtype = col_dict)

# Split combined dataframe into 12 separate dataframes
ht_combined = []
start_index = 0
for i in range(1, combined.shape[0]):
    if (i == (combined.shape[0] - 1)):
        ht_combined.append(combined.iloc[start_index: i, :])
    if (combined.loc[i, "cluster_id"] == 0 and combined.loc[i - 1, "cluster_id"] != 0):
        ht_combined.append(combined.iloc[start_index : i, :])
        start_index = i

for data in ht_combined:
    data.index = np.arange(len(data))

orig_dict = {}
original_file = ht_combined[0]
for i in range(original_file.shape[0]):
    cluster_id = original_file.loc[i, "cluster_id"]
    if cluster_id in orig_dict.keys():
        url_list = orig_dict[cluster_id]
        url_dict = {}
        url_dict[original_file.loc[i, "URL"]] = [original_file.loc[i, "Topic1"], original_file.loc[i, "Topic2"],
                                original_file.loc[i, "T1"], original_file.loc[i, "T2"], original_file.loc[i, "T3"], original_file.loc[i, "T4"],
                               original_file.loc[i, "T5"], original_file.loc[i, "T6"], original_file.loc[i, "T7"], original_file.loc[i, "T8"],
                               original_file.loc[i, "T9"], original_file.loc[i, "T10"], original_file.loc[i, "T11"], original_file.loc[i, "T12"],
                               original_file.loc[i, "T13"], original_file.loc[i, "T14"], original_file.loc[i, "T15"], original_file.loc[i, "T16"],
                               original_file.loc[i, "T17"], original_file.loc[i, "T18"], original_file.loc[i, "T19"]]
        url_list.append(url_dict)
        orig_dict[cluster_id] = url_list
    else:
        url_dict = {}
        url_dict[original_file.loc[i, "URL"]] = [original_file.loc[i, "Topic1"], original_file.loc[i, "Topic2"],
                               original_file.loc[i, "T1"], original_file.loc[i, "T2"], original_file.loc[i, "T3"], original_file.loc[i, "T4"],
                               original_file.loc[i, "T5"], original_file.loc[i, "T6"], original_file.loc[i, "T7"], original_file.loc[i, "T8"],
                               original_file.loc[i, "T9"], original_file.loc[i, "T10"], original_file.loc[i, "T11"], original_file.loc[i, "T12"],
                               original_file.loc[i, "T13"], original_file.loc[i, "T14"], original_file.loc[i, "T15"], original_file.loc[i, "T16"],
                               original_file.loc[i, "T17"], original_file.loc[i, "T18"], original_file.loc[i, "T19"]]
        orig_dict[cluster_id] = [url_dict]


cluster_id_counter = len(orig_dict)
for ht_index in range(1, len(ht_combined)):
    print(ht_index)
    adjacent_file = ht_combined[ht_index]
    adjacent_dict = {}
    for i in range(adjacent_file.shape[0]):
        cluster_id = adjacent_file.loc[i, "cluster_id"]
        if cluster_id in adjacent_dict.keys():
            url_list = adjacent_dict[cluster_id]
            url_dict = {}
            url_dict[adjacent_file.loc[i, "URL"]] = [adjacent_file.loc[i, "Topic1"], adjacent_file.loc[i, "Topic2"],
                                                     adjacent_file.loc[i, "T1"], adjacent_file.loc[i, "T2"],
                                                     adjacent_file.loc[i, "T3"], adjacent_file.loc[i, "T4"],
                                                     adjacent_file.loc[i, "T5"], adjacent_file.loc[i, "T6"],
                                                     adjacent_file.loc[i, "T7"], adjacent_file.loc[i, "T8"],
                                                     adjacent_file.loc[i, "T9"], adjacent_file.loc[i, "T10"],
                                                     adjacent_file.loc[i, "T11"], adjacent_file.loc[i, "T12"],
                                                     adjacent_file.loc[i, "T13"], adjacent_file.loc[i, "T14"],
                                                     adjacent_file.loc[i, "T15"], adjacent_file.loc[i, "T16"],
                                                     adjacent_file.loc[i, "T17"], adjacent_file.loc[i, "T18"],
                                                     adjacent_file.loc[i, "T19"]]
            url_list.append(url_dict)
            adjacent_dict[cluster_id] = url_list
        else:
            url_dict = {}
            url_dict[adjacent_file.loc[i, "URL"]] = [adjacent_file.loc[i, "Topic1"], adjacent_file.loc[i, "Topic2"],
                                                     adjacent_file.loc[i, "T1"], adjacent_file.loc[i, "T2"],
                                                     adjacent_file.loc[i, "T3"], adjacent_file.loc[i, "T4"],
                                                     adjacent_file.loc[i, "T5"], adjacent_file.loc[i, "T6"],
                                                     adjacent_file.loc[i, "T7"], adjacent_file.loc[i, "T8"],
                                                     adjacent_file.loc[i, "T9"], adjacent_file.loc[i, "T10"],
                                                     adjacent_file.loc[i, "T11"], adjacent_file.loc[i, "T12"],
                                                     adjacent_file.loc[i, "T13"], adjacent_file.loc[i, "T14"],
                                                     adjacent_file.loc[i, "T15"], adjacent_file.loc[i, "T16"],
                                                     adjacent_file.loc[i, "T17"], adjacent_file.loc[i, "T18"],
                                                     adjacent_file.loc[i, "T19"]]
            adjacent_dict[cluster_id] = [url_dict]

    print("created adjacent dict")

    for key, value in adjacent_dict.items():
        flag = 0
        url_value = []
        for i in value:
            url_value += i.keys()
        for key2, value2 in orig_dict.items():
            url_value2 = []
            for i in value2:
                url_value2 += i.keys()
            #print(url_value2)
            #print(url_value)
            if (not set(url_value).isdisjoint(url_value2)):
                #print("match")
                no_dup_list = url_value + url_value2
                no_dup_list = list(set(no_dup_list))
                for url in no_dup_list:
                    if url in url_value:
                        url_index = url_value.index(url)
                        orig_list = orig_dict[key2]
                        orig_list.append(value[url_index])
                        orig_dict[key2] = orig_list
                    else:
                        url_index = url_value2.index(url)
                        orig_list = orig_dict[key2]
                        orig_list.append(value2[url_index])
                        orig_dict[key2] = orig_list
                flag = 1
                break
        if (flag == 0):
            #print("no match")
            #print(value)
            orig_dict[cluster_id_counter] = value
            cluster_id_counter += 1

    print("compared adjacent dict to original dict")

print(len(orig_dict))
for key, val in orig_dict.items():
    print(key)
    print(val)




