# coding: utf-8

import glob
import pandas as pd 
import numpy as np
import cPickle as pickle

class User:
    def __init__(self,name):
        self.username = name
        self.course_id = []
        self.enrollment_id = [] 
        self.courseNum = 0
        self.dropcourseNum = 0
        self.dropRate = 0
    def addCourse(self,courseID,drop=-1):
        self.course_id.append(courseID)
        self.courseNum += 1
        if drop == 1:
            self.dropcourseNum += 1
        
    def addEnrollment(self,enrollment_id):
        self.enrollment_id.append(enrollment_id)
        
    def getCourseNum(self):
        return self.courseNum
    
    def getDropCourseNum(self):
        return self.dropcourseNum

    def getDropRate(self):
        return (self.dropcourseNum/self.courseNum)


def init_users():
    data = pd.read_csv('./enrollment_train.csv')
    label = pd.read_csv('./truth_train.csv',header=None)

    print 'Data Length: ' + str(len(data))
    print data.iloc[0][0]
    print data.iloc[0]['course_id']

    addedList = set()
    userList = []
    users = {}
    for i in xrange(len(data)):
        if not (data.iloc[i]['username'] in addedList):
            addedList.add(data.iloc[i]['username'])
            user = User(data.iloc[i]['username'])
            users[data.iloc[i]['username']] = user
        else:
            user = users[data.iloc[i]['username']]

        if i%2000 == 0:
            print 'Fin. ' + str(i)
        #print 'Add'
        #print data.iloc[i]['username']
        user.addEnrollment (User(data.iloc[i]['enrollment_id']))
        #print User(data.iloc[i]['enrollment_id'])
        user.addCourse (data.iloc[i]['course_id'],label.iloc[i][1])
        #print data.iloc[i]['course_id']
        #print len(userList)
        #break
    print 'Fin.'



    print 'User Num: ' + str(len(users))
    print 'Avg Drop Rate' + str(sum([x.getDropCourseNum() for x in users.values()])/float(len(users)))

    return users

def init_users_test():
    data = pd.read_csv('./enrollment_test.csv')
    with open('./users.pkl', 'rb') as f:
        train_users = pickle.load(f)

    print 'Data Length: ' + str(len(data))
    print data.iloc[0][0]
    print data.iloc[0]['course_id']

    addedList = set()
    userList = []
    users = {}
    for i in xrange(len(data)):
        if not (data.iloc[i]['username'] in addedList):
            addedList.add(data.iloc[i]['username'])
            user = User(data.iloc[i]['username'])
            users[data.iloc[i]['username']] = user
        else:
            user = users[data.iloc[i]['username']]
        if i%2000 == 0:
            print 'Fin. ' + str(i)
        #print 'Add'
        #print data.iloc[i]['username']
        user.addEnrollment (User(data.iloc[i]['enrollment_id']))
        #print User(data.iloc[i]['enrollment_id'])
        user.addCourse (data.iloc[i]['course_id'])
        #print data.iloc[i]['course_id']

        if user.username in train_users:
            user.dropcourseNum = train_users[user.username].dropcourseNum
        else:
            user.dropcourseNum = 1.1377

        #print len(userList)
        #break

    print 'Fin.'
    return users
