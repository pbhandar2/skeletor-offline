import sys, os, math
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn import svm
import matplotlib.pyplot as plt
from tabulate import tabulate
from scipy.stats import describe
from sklearn.linear_model import LogisticRegression


def run_random_forest(trainx, trainy, testx, testy, mode):

    print("RUNNING RANDOM FOREST")
    regr_1 = RandomForestRegressor(
        max_depth=50,
        random_state=0,
        n_estimators=100)
    regr_1.fit(trainx[:, 1:], trainy)
    pred = regr_1.predict(testx[:, 1:].astype('float'))

    process_error(testx, testy, pred, mode)


def run_tree(trainx, trainy, testx, testy, mode):

    print("RUNNING TREE")
    regr_1 = DecisionTreeRegressor(max_depth=4)
    regr_1.fit(trainx[:, 1:], trainy)

    pred = regr_1.predict(testx[:, 1:].astype('float'))

    process_error(testx, testy, pred, mode)


def run_svm(trainx, trainy, testx, testy):
    print("RUNNING SVM")
    regr_1 = svm.SVC(gamma='scale', kernel="sigmoid")
    regr_1.fit(trainx[:, 1:], trainy)
    pred = regr_1.predict(testx[:, 1:].astype('float'))
    process_error(testx, testy, pred)


def process_error(testx, testy, pred, mode):
    err_arr = []

    error_handle = open("error.csv", "w+")
    error_table = []
    diff_array = []
    for file_name, real, p in zip(testx[:, 0], testy.astype('float'), pred.astype('float')):
        diff = abs(abs(p) - abs(real))
        rel_err = diff / abs(real)
        diff_array.append((p-real)/real)
        error_handle.write("{},{},{},{},{}\n".format(file_name, real, p, diff, rel_err))
        error_table.append([file_name, real, p, p-real, rel_err])
        # print("File: {} Real: {}, Predicted: {}, Difference: {} = {}MB, Error = {}".format(file_name, real, p, diff,
        #                                                                                    (diff * 4 / 1024), rel_err))
        err_arr.append(rel_err)

    labels=["name", "real", "pred", "diff", "relative"]
    print(tabulate(sorted(error_table, key=lambda k: k[3]), headers=labels))

    mean_err = np.mean(err_arr)

    if mode == 1:
        title_string = "Error vs test cases \n trained on " \
                       "CachePhysics and tested on MSR for random forest " \
                       "\nAverage Error: {}".format(mean_err)
    else:
        title_string = "Error vs test cases \n trained on " \
                       "CachePhysics and tested on CachePhysics for random forest " \
                       "\nAverage Error: {}".format(mean_err)

    plot_rel_error(err_arr, title_string)

    real_vs_error = list(zip(testy.astype('float'), err_arr))
    sort_real_vs_error = sorted(real_vs_error, key=lambda k: k[0])
    x, y = zip(*sort_real_vs_error)

    if mode == 1:
        title_string = "Error vs true value \n trained of CachePhysics and tested on MSR for random forest " \
                        " \n Average Error: {}".format(mean_err)
    else:
        title_string = "Error vs true value \n trained of CachePhysics and tested on CachePhysics for random forest " \
                        " \n Average Error: {}".format(mean_err)

    plot_with_threshold(x, y, h=0.2, v=262144, hlabel="20% error threshold", vlabel="1GB minimum cache threshold", title=title_string)

    filtered_real_vs_error = list(filter(lambda k: k[0] > 262144, real_vs_error))
    x, y = zip(*filtered_real_vs_error)
    if mode == 1:
        title_string = "Error vs test cases \n for threshold data trained on \n " \
                       "CachePhysics and tested on MSR for random forest " \
                       "\nAverage Error: {}".format(np.mean(y))
    else:
        title_string = "Error vs test cases \n for threshold data trained on \n " \
                       "CachePhysics and tested on CachePhysics for random forest " \
                       "\nAverage Error: {}".format(np.mean(y))
    plot_rel_error_filtered(y, title_string)

    if mode == 1:
        title_string = "Error vs test cases \n trained on " \
                       "CachePhysics and tested on MSR for random forest " \
                       "\nAverage Error: {}".format(np.mean(diff_array))
    else:
        title_string = "Error vs test cases \n trained on " \
                       "CachePhysics and tested on CachePhysics for random forest " \
                       "\nAverage Error: {}".format(np.mean(diff_array))
    plot_diff(diff_array, title_string)

    real_vs_error = list(zip(testy.astype('float'), diff_array))
    sort_real_vs_error = sorted(real_vs_error, key=lambda k: k[0])
    x, y = zip(*sort_real_vs_error)

    if mode == 1:
        title_string = "Error vs true value \n trained of CachePhysics and tested on MSR for random forest " \
                        " \n Average Error: {}".format(mean_err)
    else:
        title_string = "Error vs true value \n trained of CachePhysics and tested on CachePhysics for random forest " \
                        " \n Average Error: {}".format(mean_err)

    plot_diff_with_threshold(x, y, h=0.2, v=262144, hlabel="20% error threshold", vlabel="1GB minimum cache threshold", title=title_string)

def plot_rel_error(err_arr, title):
    mean_arr = np.mean(err_arr)
    plt.plot(err_arr, label="relative error")
    plt.ylabel("Relative Error")
    plt.xlabel("Workloads")
    plt.title(title)
    plt.axhline(y=mean_arr, color='g', linestyle='--', label="avg.error")
    plt.legend()
    plt.tight_layout()
    plt.savefig("error_test_msr_cp_msr.png")
    plt.close()


def plot_diff(err_arr, title):
    mean_arr = np.mean(err_arr)
    plt.plot(err_arr, label="relative error")
    plt.ylabel("Relative Error")
    plt.xlabel("Workloads")
    plt.title(title)
    plt.axhline(y=mean_arr, color='g', linestyle='--', label="avg.error")
    plt.legend()
    plt.tight_layout()
    plt.savefig("diff_test_msr_cp_msr.png")
    plt.close()


def plot_rel_error_filtered(y, title):
    mean_arr = np.mean(y)
    plt.plot(y, label="relative error")
    plt.ylabel("Relative Error")
    plt.xlabel("Workloads")
    plt.title(title)
    plt.axhline(y=mean_arr, color='g', linestyle='--', label="avg.error")
    plt.legend()
    plt.tight_layout()
    plt.savefig("error_test_msr_cp_msr_filtered.png")
    plt.close()


def plot_with_threshold(x,y, h=0, v=0, hlabel=None, vlabel=None, title=None):
    plt.figure()
    plt.plot(x,y, 'ro', markersize=2)
    plt.axhline(y=h, color='g', linestyle='--', label=hlabel)
    plt.axvline(x=v, color='b', linestyle='--', label=vlabel)
    plt.legend()
    plt.title(title)
    plt.xlabel("Real cache size")
    plt.ylabel("Relative Error")
    plt.tight_layout()
    plt.savefig("error_real_size_cp_msr.png")
    plt.close()


def plot_diff_with_threshold(x,y, h=0, v=0, hlabel=None, vlabel=None, title=None):
    plt.figure()
    plt.plot(x,y, 'ro', markersize=2)
    plt.axhline(y=h, color='g', linestyle='--', label=hlabel)
    plt.axvline(x=v, color='b', linestyle='--', label=vlabel)
    plt.legend()
    plt.title(title)
    plt.xlabel("Real cache size")
    plt.ylabel("Relative Error")
    plt.tight_layout()
    plt.savefig("diff_real_size_cp_msr.png")
    plt.close()

def get_raw_data(file_name):
    raw_data = []

    f = open(file_name)
    line = f.readline()
    while line:
        line_split = line.split(",")

        name = line_split[0]
        mean = float(line_split[2])
        variance = float(line_split[3])
        skew = float(line_split[4])
        kurtosis = float(line_split[5])
        size = math.ceil(float(line_split[6]))
        unique_object_ratio = float(line_split[9])

        raw_data.append([name, unique_object_ratio, mean, variance, skew, kurtosis, size])

        line = f.readline()

    return raw_data


def get_class_from_data(trainy, testy, numbins):

    full_array = trainy + testy

    print(describe(full_array))

    bin_edges = [0, 100000, 500000, 1000000, math.inf]

    train_y_class = np.digitize(trainy, bin_edges)
    test_y_class = np.digitize(testy, bin_edges)
    # print(train_y_class)
    #
    # train_y_class = []
    # for y in trainy:
    #     cur_bucket = -1
    #     for i in range(len(bin_edges) -1):
    #         if y >= bin_edges[i] and y<bin_edges[i+1]:
    #             cur_bucket = i
    #
    #     if cur_bucket == -1:
    #         cur_bucket = len(bin_edges) - 1
    #
    #     train_y_class.append(cur_bucket)
    #
    # test_y_class = []
    # for y in testy:
    #     cur_bucket = -1
    #     for i in range(len(bin_edges) - 1):
    #         if y >= bin_edges[i] and y < bin_edges[i + 1]:
    #             cur_bucket = i
    #
    #     if cur_bucket == -1:
    #         cur_bucket = len(bin_edges) - 1
    #
    #     test_y_class.append(cur_bucket)

    from collections import Counter
    c = Counter(train_y_class)
    print(c)
    c = Counter(test_y_class)
    print(c)


    # hist, bin_edges = np.histogram(full_array, bins=numbins)
    #
    # train_y_class = np.digitize(trainy, bin_edges)
    # test_y_class = np.digitize(testy, bin_edges)
    #
    # from collections import Counter
    # c = Counter(train_y_class)
    # print(c)
    # c = Counter(test_y_class)
    # print(c)

    return np.array(train_y_class), np.array(test_y_class)


def run_classifier(trainx, trainy, testx, testy, numbins):
    trainy, testy = get_class_from_data([int(s) for s in trainy], [int(s) for s in testy], numbins)

    from sklearn.tree import DecisionTreeClassifier, plot_tree
    regr_1 = DecisionTreeClassifier(random_state=0)

    #regr_1 = LogisticRegression()
    regr_1.fit(trainx[:, 1:], trainy)
    pred = regr_1.predict(testx[:, 1:].astype('float'))

    from sklearn.metrics import accuracy_score, classification_report
    from sklearn import tree
    score = accuracy_score(testy, pred)
    print(score)
    print(classification_report(testy, pred))
    from IPython.display import Image
    from sklearn import tree
    import pydotplus

    for i, y in enumerate(pred):
        if testy[i] != y:
            print("{},{},{}\n".format(testx[i][0], testy[i], y))


    # Create DOT data
    dot_data = tree.export_graphviz(regr_1, out_file=None,
                                    feature_names=["unique_obj", "mean", "variance", "skew", "kurtosis"])

    # Draw graph
    tree.export_graphviz(regr_1, out_file="tree_class.dot")

    plot_tree(regr_1, feature_names=["unique_obj", "mean", "variance", "skew", "kurtosis"], filled=True)
    plt.savefig("tree_class.png", dpi=100)

    # Show graph
    #Image(graph.create_png())


def main(mode, train_data, test_data):

    raw_data = get_raw_data(train_data)
    data = np.array(raw_data).reshape(-1, len(raw_data[0]))

    if mode == 0:
        np.random.shuffle(raw_data)
        trainx, testx, trainy, testy = train_test_split(data[:, :-1], data[:, -1], test_size=0.1, random_state=42)
    else:
        trainx = data[:, :-1]
        trainy = data[:, -1]
        raw_data = get_raw_data(test_data)
        data = np.array(raw_data).reshape(-1, len(raw_data[0]))
        testx = data[:, :-1]
        testy = data[:, -1]


    #run_random_forest(trainx, trainy, testx, testy, mode)
    #run_svm(trainx, trainy, testx, testy)

    run_classifier(trainx, trainy, testx, testy, 5)


if __name__ == "__main__":
    mode = int(sys.argv[1])
    train_data = sys.argv[2]
    test_data = -1

    if mode == 1:
        test_data = sys.argv[3]

    process_style = 0

    main(mode, train_data, test_data)
