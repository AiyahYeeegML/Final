from UserClass import *
from enroll_course import *
import cPickle as pickle


def main():
    with open('./enroll.pkl', 'r') as f:
        enrolls = pickle.load(f)
    with open('./users.pkl', 'r') as f:
        users = pickle.load(f)
    with open('./courses.pkl', 'r') as f:
        courses = pickle.load(f)

    if not (enrolls and users and courses):
        exit('load data fail.'+ 
                str([(i, i != None) for i in [enrolls, users, courses]]))


if __name__ == '__main__':
    main()


