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
        self.object_num = 0
    
def init_courses(train=1):
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
        coursedf = df.loc[df['course_id'] == cid]
        category_df = coursedf['category']
        course.video_num = len(category_df[category_df == 'video'])
        
        # object num
        course.object_num = len(coursedf)

        courses[cid] = course

    print 'init_courses done.'
    return courses


class Enrollment:
    def __init__(self, enrollment_id=''):
        self.enrollment_id = enrollment_id
        self.userid = ''
        self.courseid = ''

        self.first_access_time = 0.
        self.last_access_time = 0.
        self.video_count_unique = 0
        
        self.user_log_num = 0
        self.course_log_num = 0
        self.take_course_num = 0
        self.take_user_num = 0
        self.log_num = 0
        
        self.server_navi = 0
        self.server_access = 0
        self.video_count = 0
        
    def __str__(self):
        s = 'Enrollment ' + self.enrollment_id + '\n'
        s += ', '.join('%s: %s\n' % item for item in vars(self).items())
        return s
        
def date2sec(datestr):
    epoch = datetime.utcfromtimestamp(0)
    date = datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
    return (date - epoch).total_seconds()
    

def init_enrollments(train=1):
    epoch = datetime.utcfromtimestamp(0)
    enrolls = {}
    
    if train:
        df = pandas.read_csv('./sample_train_x.csv')
        logdf = pandas.read_csv('./log_train.csv')
        mapdf = pandas.read_csv('./enrollment_train.csv')
    else:
        df = pandas.read_csv('./sample_test_x.csv')
        logdf = pandas.read_csv('./log_test.csv')
        mapdf = pandas.read_csv('./enrollment_test.csv')

    logs = {}


    print 'read enrollment csv done'
    print '#enrollments:', len(df)
    
    print 'reading logs'

    lasteid = None
    lastlog = None
    sawvideos = set()
    for i in xrange(len(logdf)):
        log = logdf.iloc[i]
        eid = log['enrollment_id']
        if eid != lasteid:
            enrolls[eid] = Enrollment(eid)
            enrolls[eid].first_access_time = date2sec(log['time'])
            if lasteid:
                enrolls[lasteid].video_count_unique = len(sawvideos)
            sawvideos = set()
            lasteid = eid

        enrolls[eid].last_access_time = date2sec(log['time'])

        if log['event'] == 'video':
            sawvideos.add(log['object'])

        lastlog = log 

        if i % 5000 == 0:
            print i

    enrolls[eid].video_count_unique = len(sawvideos)

    print 'reading enrollments'

    for i in xrange(len(df)):
        row = df.iloc[i]
        eid = row['ID']
        if eid not in enrolls:
            print str(eid) + ' not in'
            break
        e = enrolls[eid]
        e.user_log_num = row['user_log_num']
        e.course_log_num = row['course_log_num']
        e.take_course_num = row['take_course_num']
        e.take_user_num = row['take_user_num']
        e.log_num = row['log_num']
        e.server_navi = row['server_nagivate']
        e.server_access = row['server_access']
        e.video_count = row['video_count']
        
        if i % 2000 == 0:
            print i

    
    ## read course user map
    print 'reading maps'

    for i in xrange(len(mapdf)):
        m = mapdf.iloc[i]
        eid = m['enrollment_id']
        enrolls[eid].userid = m['username']
        enrolls[eid].courseid = m['course_id']

    print 'init_courses done.'
    return enrolls


def main():
    init_enrollments()
    init_courses()
    
if __name__ == '__main__':
    main()
