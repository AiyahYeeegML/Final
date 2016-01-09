from UserClass import *
from enroll_course import *
import cPickle as pickle
import sys


enrolls = init_enrollments()
users = init_users()
courses = init_courses()

with open('./enroll.pkl', 'wb') as f:
    pickle.dump(enrolls, f)
with open('./users.pkl', 'wb') as f:
    pickle.dump(user, f)
with open('./courses.pkl', 'wb') as f:
    pickle.dump(courses, f)

# def main(argv):
    # classes = ['enroll', 'user', 'course', 'all']
    # if len(argv) < 2 or not argv[1] in classes:
        # exit('python dump_classes.py <enroll|users|courses|all>')
    
    # # if argv[1] == classes[0]:
        


# if __name__ == '__main__':
    # main(sys.argv)
