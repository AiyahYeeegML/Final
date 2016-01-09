
# coding: utf-8

# In[17]:


from sklearn import datasets
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score


# COURSE的video數
# course第一次release的時間
# course最後release的時間

import pandas
from datetime import datetime
import pprint

from UserClass import *
from enroll_course import *
import cPickle as pickle


# In[18]:

with open('./enroll.pkl', 'r') as f:
    enrolls = pickle.load(f)
with open('./users.pkl', 'r') as f:
    users = pickle.load(f)
with open('./courses.pkl', 'r') as f:
    courses = pickle.load(f)

if not (enrolls and users and courses):
    exit('load data fail.'+ 
            str([(i, i != None) for i in [enrolls, users, courses]]))


# In[24]:

df = pandas.read_csv('./enrollment_train.csv')
tadf = pandas.read_csv('./sample_train_x.csv')

data = []
for i in xrange(len(df)):
    log = df.iloc[i]
    eid = log['enrollment_id']
    cid = log['course_id']
    uid = log['username']
    course = courses[cid]
    enroll = enrolls[eid]
    user = users[uid]
    
    #course's video num
    v1 = course.video_num
    #non-repeated video nums
    v2 = enroll.video_count_unique
    #total videos nums
    v3 = enroll.video_count
    
    avgNonRepeatVideo = v2/float(v1)
    avgRepeatVideo = v3/float(v1)
    
    firstTime = float(enroll.first_access_time) - course.first_release_time
    lastTime = enroll.last_access_time - course.last_release_time
    avgLog = enroll.user_log_num - course.video_num
    avgAction = enroll.course_log_num / enroll.take_user_num
    activeActions = tadf.loc[tadf['ID'] == 20]['log_num'][1] - (enroll.course_log_num / enroll.take_user_num)
    dropRate = user.dropcourseNum / enroll.take_course_num
    data.append([avgNonRepeatVideo,avgRepeatVideo,v2,v3,firstTime,lastTime,avgLog,avgAction,activeActions,dropRate])

data = np.append(data)
with open('./data.pkl', 'wb') as f:
    pickle.dump(data, f)
print ('Saveing Features Sucessfully.')


# In[ ]:



