#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import re
import string
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random


# In[37]:


nltk.download('punkt')#an error message in clean_txt() asked for it


# # reading the stories

# In[5]:


story_path = 'C:/Users/benha/Desktop/archive/sherlock/'


# In[7]:


for files in os.walk(story_path):
    print(files)


# In[16]:


for _, _, files in os.walk(story_path):
        for file in files:
            with open(story_path + file) as f:
#                 data = f.readlines()
#                 print(data[0:20])
                for line in f[0:20]:
                    print(line)
                break


# In[21]:


for _, _, files in os.walk(story_path):
        for file in files:
            with open(story_path + file) as f:
#                 data = f.readlines()
#                 print(data[0:20])
                for line in f:
                    print(line)
                break


# In[23]:


help(line.strip)


# In[19]:


for _, _, files in os.walk(story_path):
        for file in files:
            with open(story_path + file) as f:
#                 data = f.readlines()
#                 print(data[0:20])
                for line in f:
                    line = line.strip()
                    print(line)
                break


# In[26]:


for _, _, files in os.walk(story_path):
        for file in files:
            with open(story_path + file) as f:
#                 data = f.readlines()
#                 print(data[0:20])
                for line in f:
                    line = line.strip()
                    if line != '':
                        print(line)
                break


# In[27]:


for _, _, files in os.walk(story_path):
        for file in files:
            with open(story_path + file) as f:
#                 data = f.readlines()
#                 print(data[0:20])
                for line in f:
                    line = line.strip()
                    if line == '----------':break
                    if line != '':
                        print(line)
                break


# In[32]:


def read_all_stories(story_path):
    text = []
    
    for _, _, files in os.walk(story_path):
        for file in files:
            with open(story_path + file) as f:
                for line in f:
                    line = line.strip()
                    if line == '----------' : break
                    if line != '': text.append(line)
    return text

stories = read_all_stories(story_path)
print('total number of lines = ', len(stories))


# In[33]:


stories


# In[43]:


def clean_txt(txt):
    cleaned_txt = []
    
    for line in txt:
        line = line.lower()
        line = re.sub(r"[,.\"\'!@#$%^&*(){}?/;`~:<>+=-\\]", "", line)
        
        tokens = word_tokenize(line)
        words = [token for token in tokens if token.isalpha()]
        
        cleaned_txt += words

    return cleaned_txt

cleaned_stories = clean_txt(stories)
cleaned_stories


# In[46]:


print('number of words: ', len(cleaned_stories))


# # Creating the markov model

# In[60]:


def make_markov_model(cleaned_stories, n_grams = 2):
    markov_model = {}
    
    for i in range(10000):#len(cleaned_stories)- n_grams -1):
        curr_state = ''
        next_state = ''
        
        for j in range(n_grams):
            curr_state += cleaned_stories[i+j] + ' '
            next_state += cleaned_stories[i+j+n_grams]+ ' '
            
#         print(curr_state, next_state, sep = '\t')
        curr_state_2 = curr_state[:-3]
        next_state_2 = next_state[:-3]
#         print(curr_state, next_state, sep = '\t')
        if curr_state not in markov_model:
            markov_model[curr_state] = {}
            markov_model[curr_state][next_state] = 1
        elif next_state not in markov_model[curr_state]:
            markov_model[curr_state][next_state] = 1
        else:
            markov_model[curr_state][next_state] +=1
    return markov_model
    
        
print(make_markov_model(cleaned_stories) )  


# In[108]:


def make_markov_model(cleaned_stories, n_grams = 2):
    markov_model = {}
    
    for i in range(len(cleaned_stories)- (2 * n_grams - 1)):#n_grams -(n_grams -1)
        curr_state = ''
        next_state = ''
        
        for j in range(n_grams):
            curr_state += cleaned_stories[i+j] + ' '
            next_state += cleaned_stories[i+j+n_grams]+ ' '
            
        curr_state = curr_state[:-1]
        next_state = next_state[:-1]
        
        if curr_state not in markov_model:
            markov_model[curr_state] = {}
            markov_model[curr_state][next_state] = 1
        elif next_state not in markov_model[curr_state]:
            markov_model[curr_state][next_state] = 1
        else:
            markov_model[curr_state][next_state] += 1
            
    for curr_state, transition in markov_model.items():
        total = sum(transition.values())
        for state, count in transition.items():
            markov_model[curr_state][state] = count/total

    return markov_model 


# In[85]:


markov_model = make_markov_model(cleaned_stories)


# In[86]:


markov_model


# In[80]:


markov_model


# In[87]:


len(markov_model.keys())


# In[88]:


markov_model['dear watson']


# In[104]:


def generate_story(markov_model, limit = 100, start = 'dear watson'):
    n = 0
    curr_state = start
#     next_state = None
    story = ''
    story += curr_state + ' '
    
    while n<limit:
        next_state = random.choices(list(markov_model[curr_state].keys()),
                                   list(markov_model[curr_state].values()))
        curr_state = next_state[0]
        story += curr_state + ' '
        
        n += 1
    
    return story[:-1]


# In[99]:


help(random.choices)


# In[105]:


generate_story(markov_model = markov_model)


# In[103]:


generate_story(markov_model = markov_model)


# In[101]:


generate_story(markov_model = markov_model)


# In[109]:


markov_model_3grams = make_markov_model(cleaned_stories, n_grams = 3)


# In[111]:


generate_story(markov_model = markov_model_3grams, start = 'my dear watson')


# In[112]:


generate_story(markov_model = markov_model_3grams, limit = 12, start = 'my dear watson')


# In[113]:


generate_story(markov_model = markov_model_3grams, limit = 12, start = 'my dear watson')


# In[114]:


markov_model_4grams = make_markov_model(cleaned_stories, n_grams = 4)


# In[115]:


generate_story(markov_model = markov_model_3grams, limit = 12, start = 'my dear watson')


# In[120]:


generate_story(markov_model = markov_model_4grams, limit = 100, start = 'my dear watson you')


# In[122]:


markov_model_10grams = make_markov_model(cleaned_stories, n_grams = 10)


# In[124]:


markov_model_20grams = make_markov_model(cleaned_stories, n_grams = 20)


# In[125]:


generate_story(markov_model = markov_model_20grams, limit = 10, start = 'my dear watson you must play your cards as best you can when such a stake is on the table')


# In[126]:


markov_model_5grams = make_markov_model(cleaned_stories, n_grams = 5)


# In[127]:


generate_story(markov_model = markov_model_5grams, limit = 100, start = 'my dear watson you must')


# In[119]:


generate_story(markov_model = markov_model_4grams, limit = 12, start = 'my dear watson you')


# In[123]:


generate_story(markov_model = markov_model_10grams, limit = 10, start = 'my dear watson you must play your cards as best')


# In[138]:


generate_story(markov_model = markov_model_4grams, limit = 20, start = 'i dont think that')


# In[142]:


generate_story(markov_model = markov_model_3grams, limit = 20, start = 'who did it')


# In[149]:


generate_story(markov_model = markov_model_3grams, limit = 60, start = 'the curse of')


# In[151]:


generate_story(markov_model = markov_model_4grams, limit = 50, start = 'if he had not')


# In[152]:


generate_story(markov_model = markov_model_4grams, limit = 50, start = 'disappointed in his conclusions')


# In[ ]:




