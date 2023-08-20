#!/usr/bin/env python
# coding: utf-8

# # NY 2015 Street Tree Census - Tree Data

# In[1]:


#import libraries
import pandas as pd
import numpy as np


# In[3]:


df = pd.read_csv('2015-street-tree-census-tree-data.csv')
df.head()


# In[4]:


df.shape


# In[8]:


df.info()


# In[10]:


df.describe()


# In[11]:


df.columns


# ### Selecting important columns

# In[12]:


df= df[['tree_id',  'tree_dbh', 'stump_diam',
       'curb_loc', 'status', 'health', 'spc_latin', 'steward',
       'sidewalk', 'problems', 'root_stone',
       'root_grate', 'root_other', 'trunk_wire', 'trnk_light', 'trnk_other',
       'brch_light', 'brch_shoe', 'brch_other',]]
df


# In[13]:


df.dtypes


# In[14]:


df.hist(bins=60, figsize=(20,10))


# ### Checking for null values

# In[15]:


df.isna().sum()


# In[16]:


df[df['health'].isna()]


# ### Handling outliers
# 
# if stamp dbh higher then 50 In this we have option to do groupby function group them by species and filter with average dbh of all specific species

# In[17]:


big_tree = df[df['tree_dbh']>50]
big_tree


# In[18]:


# We Saw there are some out liers in the data set near to 450
big_tree[['tree_id','tree_dbh']].plot(kind='scatter',x='tree_id',y='tree_dbh',figsize=(20,10))


# In[22]:


#in this we have Common and uncommon species
pd.DataFrame(df['spc_latin'].value_counts()).plot(kind='bar',figsize=(20,10))


# In[23]:


#value counts
df['steward'].value_counts()


# In[24]:


df['curb_loc'].value_counts()


# In[25]:


#make a stump variable to see how many status of tree has a stump 
stumps = df[df['status']=='Stump']
stumps


# In[26]:


#count the values in health column
df['health'].value_counts()


# In[27]:


#make a deads variable to see how many status of tree is dead
deads = stumps = df[df['status']=='Dead']
deads


# In[28]:


#to see how many tree have a problem or not
tree_problems = df[['root_stone','root_grate', 'root_other', 'trunk_wire', 'trnk_light', 'trnk_other',
       'brch_light', 'brch_shoe', 'brch_other',]]
tree_problems


# In[29]:


tree_problems.apply(pd.Series.value_counts)


# ### Data Cleaning Part

# In[30]:


#make a varible of a mask name and store a stump and deads tree in it
mask = ((df['status']=='Stump') | (df['status']=='Dead'))


# In[31]:


#fill nan values of stump and deads with not applicable Because the Stumped or Dead Tree has 
# Because of that health is not to apply on them.
df.loc[mask]= df.loc[mask].fillna('Not Applicable')


# In[32]:


#to see nan values are replace with not applicable
 # nan values are successfully replaced with not applicable
df[df['status']=='Stump']


# In[33]:


#to check how many null values are there in the dataset
df.isna().sum()


# In[34]:


#to see null values in a specific column
df[df['health'].isna()]


# In[35]:


# We can fiil it with the most common value because we not want to remove rows of other columns

#fill nan values of health column with good health
df['health'].fillna('Good',inplace=True)

#fill nan values of spc_latin column with no observation
df['spc_latin'].fillna('No observation',inplace=True)

#fill nan values of sidewalk column with no damage
df['sidewalk'].fillna('NoDamage',inplace=True)

#fill nan values of problem column with None
df['problems'].fillna('None',inplace=True)


# In[36]:


#again check null values in the dataset
 ## but now we completely deals with null values
df.isna().sum()


# In[37]:


big_tree = df[(df['tree_dbh']>60) | (df['stump_diam']>60)]

big_tree


# In[38]:


df = df[(df['tree_dbh']<=60) | (df['stump_diam']<=60)]
df


# ### Dealing with unexpected data

# In[39]:


tree_census_subset_alive = df[df['status']=='Alive']
tree_census_subset_dead_or_stump = df[(df['status']=='Dead')|(df['status']=='Stump')]


# In[40]:


stats_alive = tree_census_subset_alive.groupby('spc_latin')['tree_dbh'].describe().reset_index()[['spc_latin','25%','75%']]
stats_alive


# In[41]:


#We want ot merge the two tables

tree_census_subset_alive=tree_census_subset_alive.merge(stats_alive, on='spc_latin',how='left')
tree_census_subset_alive


# In[42]:


# for remove th outlier we fix the range of tree_dbh between 25% and 75% of the tree_dbh
mask =tree_census_subset_alive['tree_dbh']<tree_census_subset_alive['25%']
tree_census_subset_alive.loc[mask,'tree_dbh']= tree_census_subset_alive['25%']

mask = tree_census_subset_alive['tree_dbh']>tree_census_subset_alive['75%']
tree_census_subset_alive.loc[mask,'tree_dbh']=tree_census_subset_alive['75%']


# In[43]:


tree_census_subset_alive


# In[44]:


# Saving The Wrangled Dataset
tree_census_subset_alive.to_csv('Wrangled DataSet of Street Tree Census')


# In[ ]:





# In[ ]:




