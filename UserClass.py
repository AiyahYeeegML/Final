# coding: utf-8

import glob
import pandas as pd 
import numpy as np

class User:
    def __init__(self,name):
        self.username = name
        self.course_id = []
        self.enrollment_id = [] 
        self.courseNum = 0
        self.dropcourseNum = 0
        self.dropRate = 0
    def addCourse(self,courseID,drop):
        self.course_id.append(courseID)
        self.courseNum += 1
        if drop == 1:
            self.dropcourseNum += 1
        
    def addEnrollment(self,enrollment_id):
        self.enrollment_id.append(enrollment_id)

    def getDropRate(self):
        return (self.dropcourseNum/self.courseNum)


def init_users():
    data = pd.read_csv('./enrollment_train.csv')
    label = pd.read_csv('./truth_train.csv',header=None)

    print 'Data Length: ' + str(len(data))
    print data.iloc[0][0]
    print data.iloc[0]['course_id']

    addedList = []
    userList = []
    users = {}
    for i in xrange(len(data)):
        if (data.iloc[i]['username'] in addedList) == False:
            if i%2000 == 0:
                print 'Fin. ' + str(i)
            #print 'Add'
            addedList.append(data.iloc[i]['username'])
            user = User(data.iloc[i]['username'])
            #print data.iloc[i]['username']
            user.addEnrollment (User(data.iloc[i]['enrollment_id']))
            #print User(data.iloc[i]['enrollment_id'])
            user.addCourse (data.iloc[i]['course_id'],label.iloc[i][1])
            #print data.iloc[i]['course_id']
            users[data.iloc[i]['username']] = user
            #print len(userList)
            #break
    print 'Fin.'



    print 'User Num: ' + str(len(users))
    print 'Avg Drop Rate' + str(sum([x.getDropRate() for x in users.values()])/float(len(users)))

    return users
