import numpy as np
import math
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier

# load train and test data
train = np.loadtxt('new_train_x.csv')
train_label = np.loadtxt('ML_final_project/truth_train.csv', dtype = int, delimiter = ',')
test = np.loadtxt('new_test_x.csv')

print 'load done'

clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=350)
#clf = ExtraTreesClassifier(n_estimators=2000, n_jobs=-1)
#clf = GradientBoostingClassifier(n_estimators=3000, loss='exponential')
#clf = RandomForestClassifier(n_estimators=2000)

print 'tree done'

clf.fit(train[:, 1:], train_label[:, 1])

print 'fit done'

result = clf.predict(test[:, 1:])

print 'predict done'

f = open('predict_y_new.csv', 'w')
for i in xrange(len(result)):
    f.write(str(test[i, 0]) + ',' + str(result[i]) + '\n')
f.close()
