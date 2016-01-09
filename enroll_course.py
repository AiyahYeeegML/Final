# coding: utf-8
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

class Course:
    def __init__(self, course_id=''):
        self.first_release_time = 0. # epoch seconds
        self.last_release_time = 0.  # epoch seconds
        self.video_num = 0
    
    def get_first_release_time(self):
        return self.first_release_time
    
    def get_last_release_time(self):
        return self.last_release_time
    
    def get_video_num(self):
        return self.video_num
    
def init_courses():
    df = pandas.read_csv('./object.csv')
    # get the ocurse_id of the first row: 
    #    data.iloc[0]['course_id']
    courses = {}
    course_ids = df['course_id'].unique()
    epoch = datetime.utcfromtimestamp(0)

    for cid in course_ids:
        course = Course(cid)
        
        # time
        starts = df.loc[df['course_id'] == cid]['start']
        dates = []
        for s in starts:
            if s == 'null': continue
            dates.append(datetime.strptime(s, '%Y-%m-%dT%H:%M:%S'))
        dates = sorted(dates)
        course.first_release_time = (dates[0] - epoch).total_seconds()
        course.last_release_time = (dates[-1] - epoch).total_seconds()
        
        # video num
        category_df = df.loc[df['course_id'] == cid]['category']
        course.video_num = len(category_df[category_df == 'video'])
        
        courses[cid] = course

    print 'init_enrollments done.'
    return courses


class Enrollment:
    def __init__(self, enrollment_id=''):
        self.enrollment_id = enrollment_id
        self.first_access_time = 0.
        self.last_access_time = 0.
        self.video_count_unique = 0
        
        self.user_log_num = 0
        self.course_log_num = 0
        self.take_course_num = 0
        self.take_user_num = 0
        
        self.server_navi = 0
        self.server_access = 0
        self.video_count = 0
        
    def __str__(self):
        s = 'Enrollment ' + self.enrollment_id + '\n'
        s += ', '.join('%s: %s\n' % item for item in vars(self).items())
        return s
        

def init_enrollments():
    epoch = datetime.utcfromtimestamp(0)
    enrolls = {}
    
    df = pandas.read_csv('./sample_train_x.csv')
    logdf = pandas.read_csv('./log_train.csv')
    logs = {}


    print 'read enrollment csv done'
    print '#enrollments:', len(df)
    
    print 'reading logs'

    lasteid = None
    lastlog = None
    for i in xrange(len(logdf)):
        log = logdf.iloc[i]
        eid = log['enrollment_id']
        if eid != lasteid:
            enrolls[eid] = Enrollment(eid)
            enrolls[eid].first_access_time = log['time']
            lasteid = eid

        enrolls[eid].last_access_time = log['time']
        lastlog = log 

        if i % 5000 == 0:
            print i

    print logs[logdf.iloc[0]['enrollment_id']]
    

    print 'reading enrollments'

    for i in xrange(len(df)):
        row = df.iloc[i]
        eid = row['ID']
        e = enrolls[e]
        e.user_log_num = row['user_log_num']
        e.course_log_num = row['course_log_num']
        e.take_course_num = row['take_course_num']
        e.take_user_num = row['take_user_num']
        e.server_navi = row['server_nagivate']
        e.server_access = row['server_access']
        e.video_count = row['video_count']
        
        ## first,last time
        # logs = logdf.loc[logdf['enrollment_id'] == eid]
        logsthis = logs[eid]
        # print logs.iloc[0]
        firstdate = datetime.strptime(logsthis.iloc[0]['time'], '%Y-%m-%dT%H:%M:%S')
        firsttime = (firstdate - epoch).total_seconds()
        lastdate = datetime.strptime(logsthis.iloc[-1]['time'], '%Y-%m-%dT%H:%M:%S')
        lasttime = (lastdate - epoch).total_seconds()
        e.first_access_time = firsttime
        e.last_access_time = lasttime
        
        ## videos unique counts
        e.video_count_unique = len(logsthis.loc[logsthis['event'] == 'video']['object'].unique())
        
    
        if i % 2000 == 0:
            print i


    print 'init_courses done.'
    return enrolls



def main():
    init_courses()
    init_enrollments()
    
if __name__ == '__main__':
    main()
