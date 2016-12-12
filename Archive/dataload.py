# This tells matplotlib not to try opening a new window for each plot.
%matplotlib inline

import pandas as pd
import numpy as np
import copy
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

# load original gansta versions of the data
# DO NOT OVERWRITE THESE
clicks_train_og = pd.read_csv("../input/clicks_train.csv")
clicks_test_og = pd.read_csv("../input/clicks_test.csv")
promoted_content_og = pd.read_csv("../input/promoted_content.csv")
doc_cats_og = pd.read_csv("../input/documents_categories.csv")
doc_ents_og = pd.read_csv("../input/documents_entities.csv")
doc_meta_og = pd.read_csv("../input/documents_meta.csv")
doc_topics_og = pd.read_csv("../input/documents_topics.csv")
events_og = pd.read_csv("../input/events.csv")
page_views_og = pd.read_csv("../input/page_views_sample.csv")

# FOR TESTING WITH MINI DATASET

doc_ids = set(page_views_og['document_id']) & set(promoted_content_og['document_id'])
# pull in the content that is in both page_views and promoted_content

events = events_og[events_og['document_id'].isin(doc_ids)]
clicks_train = clicks_train_og[clicks_train_og['display_id'].isin(events['display_id'])]
clicks_test = clicks_test_og[clicks_test_og['display_id'].isin(events['display_id'])]

events = events[events['display_id'].isin(clicks_train['display_id'])]

promoted_content = promoted_content_og[promoted_content_og['ad_id'].isin(clicks_train['ad_id'])]
doc_cats = doc_cats_og[doc_cats_og['document_id'].isin(promoted_content['document_id'])]
doc_ents = doc_ents_og[doc_ents_og['document_id'].isin(promoted_content['document_id'])]
doc_meta = doc_meta_og[doc_meta_og['document_id'].isin(promoted_content['document_id'])]
doc_topics = doc_topics_og[doc_topics_og['document_id'].isin(promoted_content['document_id'])]
page_views = page_views_og[page_views_og['document_id'].isin(events['document_id'])]

# # FOR FULL DATASET ON AWS

# display_sample = np.random.choice(clicks_train_og["display_id"].unique(), 10000) # change this if too many rows
# clicks_train = clicks_train_og[clicks_train_og["display_id"].isin(display_sample)]
# # select 4000 random display id's and grab all rows in click_train with that display
# # every display has multiple ads and only 1 ad in every display is clicked
# promoted_content = promoted_content_og[promoted_content_og["ad_id"].isin(clicks_train["ad_id"])]
# # same ad can show up in multiple displays, so length of unique ads < length of unique displays
# doc_cats = doc_cats_og[doc_cats_og["document_id"].isin(promoted_content["document_id"])]
# doc_ents = doc_ents_og[doc_ents_og["document_id"].isin(promoted_content["document_id"])]
# doc_meta = doc_meta_og[doc_meta_og["document_id"].isin(promoted_content["document_id"])]
# doc_topics = doc_topics_og[doc_topics_og["document_id"].isin(promoted_content["document_id"])]
# events = events_og[events_og["display_id"].isin(clicks_train_og["display_id"])]
# page_views = page_views_og[page_views_og["document_id"].isin(promoted_content["document_id"])]
# # platform & traffic source need to be either all integers or all strings (right now its mixed)

# Merging information aout the displays to master dataset

data = clicks_train.merge(events, on='display_id', how='left')
# joins information about the display that the user saw
# each display has a unique user id, doc id, and timestamp
# events has the information about the display (who the user is, which site (document_id) it was on, when it was seen, from where, etc.)

# Identifying which documents the ads refer to (aka destination documents)

data = data.merge(promoted_content, on='ad_id', how='left')
data.head()

# Gather/bin data about the documents the ads refer to

sparsetop = doc_topics.pivot(index='document_id', columns='topic_id', values='confidence_level')
sparsetop.columns = ['top_' + str(col) for col in sparsetop.columns]

sparsecat = doc_cats.pivot(index='document_id', columns='category_id', values='confidence_level')
sparsecat.columns = ['cat_' + str(col) for col in sparsecat.columns]

sparse = sparsetop.join(sparsecat, how='outer')
sparse.fillna(0, inplace=True)

sparse.reset_index(level=0, inplace=True)
sparse.head()

print(len(sparse['document_id'].unique()), len(data['document_id_y'].unique()))
data = data.merge(sparse, left_on='document_id_y', right_on='document_id', how='left')
data.head()

# Adding meta data about the advertiser and campaign successes

advr_success = dict(zip(data.advertiser_id.unique(), [sum(data[data['advertiser_id']==x]['clicked'])/len(data[data['advertiser_id']==x]) for x in data['advertiser_id'].unique()]))
camp_success = dict(zip(data.campaign_id.unique(), [sum(data[data['campaign_id']==x]['clicked'])/len(data[data['campaign_id']==x]) for x in data['campaign_id'].unique()]))

data['campaign_perc'] = data['campaign_id'].map(camp_success)
data['advertiser_perc'] = data['advertiser_id'].map(advr_success)

data.head()

doc_view_freq = dict(zip(page_views.document_id.unique(), [len(page_views[page_views.document_id==x]) for x in page_views.document_id.unique()]))
data['docx_view_freq'] = data['document_id_x'].map(doc_view_freq)
data.head()

# Splitting dataset into data and labels

labels = data['clicked']
labels = labels.values.reshape(-1,1) # check this please! my python is 3.5 and told me to use values.reshape
del data['clicked']

print 'Labels length:', len(labels)
print 'data length:', data.shape

# Making training and test sets

train_data = data[:int(.7*len(data))]
test_data = data[int(.7*len(data)):]

train_labels = labels[:int(.7*len(data))]
test_labels = labels[int(.7*len(data)):]

print 'training label shape:', train_labels.shape
print 'training data shape:', train_data.shape
print 'test label shape:', test_labels.shape
print 'test data shape:', test_data.shape