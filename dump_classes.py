from UserClass import *
from enroll_course import *
import cPickle as pickle
import sys

def dump_train():
    print 'dumping train'
    enrolls = init_enrollments()
    with open('./enroll.pkl', 'wb') as f:
        pickle.dump(enrolls, f)

    users = init_users()
    with open('./users.pkl', 'wb') as f:
        pickle.dump(users, f)

    courses = init_courses()
    with open('./courses.pkl', 'wb') as f:
        pickle.dump(courses, f)

def dump_test():
    print 'dumping test'
    enrolls = init_enrollments(train=0)
    with open('./enroll_test.pkl', 'wb') as f:
        pickle.dump(enrolls, f)

    users = init_users_test()
    with open('./users_test.pkl', 'wb') as f:
        pickle.dump(users, f)

    courses = init_courses(train=0)
    with open('./courses_test.pkl', 'wb') as f:
        pickle.dump(courses, f)


def main(argv):
    if argv[1] == 'test':
        dump_test()
    else:
        dump_train()


if __name__ == '__main__':
    main(sys.argv)
