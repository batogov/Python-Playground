from keras.datasets import cifar10
from scipy.misc import toimage
from matplotlib import pyplot


def get_data(train_size=50000, test_size=10000):
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()
    return (X_train[:train_size], y_train[:train_size]), (X_test[:test_size], y_test[:test_size])


def visualize_data(X):
    for i in range(0, 9):
        pyplot.subplot(330 + 1 + i)
        pyplot.imshow(toimage(X[i]))
    pyplot.show()
