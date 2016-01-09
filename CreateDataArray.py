
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
import sys

# In[18]:

def create(train=1):
    if train:
        enrollf = './enroll.pkl'
        userf = './users.pkl'
        coursesf = './courses.pkl'
    else:
        enrollf = './enroll_test.pkl'
        userf = './users_test.pkl'
        coursesf = './courses_test.pkl'

    with open(enrollf, 'r') as f:
        enrolls = pickle.load(f)
    with open(userf, 'r') as f:
        users = pickle.load(f)
    with open(coursesf, 'r') as f:
        courses = pickle.load(f)

    if not (enrolls and users and courses):
        exit('load data fail.'+ 
                str([(i, i != None) for i in [enrolls, users, courses]]))


    # In[24]:

    if train:
        df = pandas.read_csv('./enrollment_train.csv')
        tadf = pandas.read_csv('./sample_train_x.csv')
    else:
        df = pandas.read_csv('./enrollment_test.csv')
        tadf = pandas.read_csv('./sample_test_x.csv')


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
        avgAction = float(enroll.course_log_num) / enroll.take_user_num
        activeActions = enroll.log_num - (float(enroll.course_log_num) / enroll.take_user_num)
        dropRate = float(user.dropcourseNum) / enroll.take_course_num

        tafeats = tadf.iloc[i].tolist()

        data.append(tafeats + [avgNonRepeatVideo,avgRepeatVideo,v2,v3,firstTime,lastTime,avgLog,avgAction,activeActions,dropRate])

        if i % 1000 == 0:
            print i

    data = np.array(data)
    if train:
        data.dump('./data.np')
    else:
        data.dump('./data_test.np')
    print ('Saveing Features Sucessfully.')

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        create(train=0)
    else:
        create(train=1)
    

