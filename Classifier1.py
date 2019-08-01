import cv2
import os
import numpy as np
from sklearn.svm import SVC
from sklearn.cluster import KMeans

if __name__ == '__main__':
    o_path1 = './trainset/0_book'
    o_path2 = './trainset/0_hand'

    count = 0
    features_hand = []
    features_book = []
    for files in os.listdir(o_path2):
        count = count + 1
        print(count)

        img = cv2.imread(o_path2 + '/' + files)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        descriptor = cv2.xfeatures2d.SIFT_create()
        kps, features = descriptor.detectAndCompute(gray, None)
        if features is None:
            continue

        if np.shape(features)[0] < 10:
            continue
        print(np.shape(features))

        k = 10
        kmeans = KMeans(n_clusters=k, random_state=0).fit(features)
        center = kmeans.cluster_centers_

        print(np.shape(center))
        center = np.reshape(center,(1,-1))
        features_hand.append(center.T)
        #features = np.reshape(features,(1,-1))
    #img = cv2.drawKeypoints(gray, kps, outImage=np.array([]))

    for files in os.listdir(o_path1):
        count = count + 1
        print(count)

        img = cv2.imread(o_path1 + '/' + files)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        descriptor = cv2.xfeatures2d.SIFT_create()
        kps, features = descriptor.detectAndCompute(gray, None)
        if features is None:
            continue

        if np.shape(features)[0] < 10:	
            continue
        print(np.shape(features))

        k = 10
        kmeans = KMeans(n_clusters=k, random_state=0).fit(features)
        center = kmeans.cluster_centers_

        print(np.shape(center))
        center = center.ravel()
        features_book.append(center.T)


    features_hand = np.reshape(features_hand,(-1,1280))
    features_book = np.reshape(features_book,(-1, 1280))
    len1 = np.shape(features_book)[0]
    len2 = np.shape(features_hand)[0]
    print(np.shape(features_book))
    print(np.shape(features_hand))

    X = np.concatenate((features_book,features_hand), axis=0)
    y = np.concatenate((np.zeros(len1),np.ones(len2)), axis=0)
    print(np.shape(y))

    clf = SVC(gamma='auto')
    clf.fit(X, y)
    #print(clf.coef_)

    #cv2.imwrite('trainset/sift/sift_keypoints.jpg', img)
    img = cv2.imread('D:/MakeData/venv/trainset/0_book/43_5b9fa59e498ca47ccdc7a13e.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    descriptor = cv2.xfeatures2d.SIFT_create()
    kps, features = descriptor.detectAndCompute(gray, None)
    
    print(np.shape(features))

    k = 10
    kmeans = KMeans(n_clusters=k, random_state=0).fit(features)
    center = kmeans.cluster_centers_
    print(clf.predict(center))