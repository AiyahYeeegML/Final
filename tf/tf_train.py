import tensorflow as tf
import numpy as np
import random

print 'load data'
datax = np.load('../data.np')[:,1:-1]
testx = np.load('../data_test.np')[:,1:-1]
datay = np.load('../labels.np')
test_eids = np.array(np.load('../data_test.np')[:,0], dtype='int')
print 'load data done'

#normalizatioa
x_mean = np.mean(datax, axis=0)
x_std = np.std(datax, axis=0)
datax = (datax - x_mean) / x_std
testx = (testx - x_mean) / x_std

datay_tmp = np.zeros((len(datay), 2))
for i in range(len(datay)):
    datay_tmp[i, datay[i]] = 1
datay = datay_tmp


n = len(datay)
idxs = range(n)
random.shuffle(idxs)
datax,datay = datax[idxs], datay[idxs]
trainx,trainy = datax[:n*0.9, :], datay[:n*0.9, :]
valx,valy = datax[n*0.9:, :], datay[n*0.9:, :]

print datax.shape
print datay.shape
print trainx.shape, trainy.shape
print valx.shape, valy.shape
print trainy

n = n*0.9


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# START
sess = tf.InteractiveSession()

x = tf.placeholder('float', shape=[None, 26])
y_ = tf.placeholder('float', shape=[None, 2])

W_fc1 = weight_variable([26, 256])
b_fc1 = bias_variable([256])
h_fc1 = tf.nn.relu(tf.matmul(x, W_fc1) + b_fc1)
keep_prob = tf.placeholder('float')
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([256, 256])
b_fc2 = bias_variable([256])
h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
h_fc2_drop = tf.nn.dropout(h_fc2, keep_prob)

W_fc3 = weight_variable([256, 2])
b_fc3 = bias_variable([2])
y = tf.nn.softmax(tf.matmul(h_fc2_drop, W_fc3) + b_fc3)
cross_entropy = -tf.reduce_sum(y_*tf.log(y))


sess.run(tf.initialize_all_variables())


train_step = tf.train.GradientDescentOptimizer(0.0001).minimize(cross_entropy)

batch_size = 100
cnt = 0
for i in range(12000):
    batchx = trainx[cnt*batch_size : (cnt+1)*batch_size]
    batchy = trainy[cnt*batch_size : (cnt+1)*batch_size]
    train_step.run(feed_dict={x: batchx, y_:batchy, keep_prob: 0.5})
    
    if i % 500 == 0:
        print i
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))

        print accuracy.eval(feed_dict={x: valx, y_:valy, keep_prob: 0.5})

    cnt += 1
    if (cnt+1)*batch_size > n:
        cnt = 0


correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))

print accuracy.eval(feed_dict={x: valx, y_:valy, keep_prob: 0.5})

# print tf.argmax(y,1).eval(feed_dict={x: valx, y_:valy})

