from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.neighbors import NearestNeighbors

import pickle
import json
import logging
import os.path

class NLPCalculator:
    def __init__(self, training_data):
        path = os.path.normpath(os.path.join(os.path.dirname(__file__),"../Assets/swedishStopWords.txt"))
        stopwords = list(set([t[:-1] for t in open(path).readlines()]))
        #print stopwords
        self.training_data = training_data.values()
        self.ids = training_data.keys()
        #print(training_data)
        self.tfidf = TfidfVectorizer(stop_words=stopwords)
        self.clf = NearestNeighbors()
        self.setup_model()

    #
    # Constructor
    # Startup script - setting up Models
    #
    def setup_model(self):
        #  ---- Redundant --- db loads training data
        # if not os.path.exists("./jobListings.pickle"):
        #     print("No previous data found - setting up Models")
        #     pickle.dump(self.training_data, open("./jobListings.pickle", "w"), protocol=2)
        # else:
        #     print("Pre-trained Models found - accessing content and IDs")
        #     self.training_data = pickle.load(open("./jobListings.pickle", "r"))

        if not os.path.exists("./tfidfVectorizer.pickle"):
            print("No previous Tf-Idf Models found - setting up matrix")
            self.inp_bow = self.train_vector_model([obj.location_desc for obj in self.training_data])
            pickle.dump(self.tfidf, open("./tfidfVectorizer.pickle", "w"), protocol=2)
            pickle.dump(self.inp_bow, open("./bow.pickle", "w"), protocol=2)
        else:
            print("Pre-trained Tf-Idf Models found - accessing matrix")
            self.tfidf = pickle.load(open("./tfidfVectorizer.pickle", "r"))
            self.inp_bow = pickle.load(open("./bow.pickle", "r"))

        if not os.path.exists("./nearestNeighbor.pickle"):
            print("No previous NN-Algorithm found - training Models")
            self.train_nearest_neighbor(self.inp_bow)
            pickle.dump(self.clf, open("./nearestNeighbor.pickle", "w"), protocol=2)
        else:
            print("NN-Algorithm found - setting up Models")
            self.clf = pickle.load(open("./nearestNeighbor.pickle", "r"))

    #
    # Training and storing the Tf-Idf vectorization matrix - storing result using pickle
    #
    def train_vector_model(self, jobs):
        logging.info("training Tf-Idf-vectorizer")
        inp_bow = self.tfidf.fit_transform(jobs)
        logging.info("tfidf - BOW shape")
        return inp_bow

    #
    # Training and storing the NearestNeighbors algorithm - storing result using pickle
    #
    def train_nearest_neighbor(self, inp_bow):
        logging.info("training NN")
        self.clf.fit(inp_bow)
        logging.info("Fit done")

    #
    # Main method; returns
    #
    def match_text(self, text_input, return_count):
        self.setup_model()
        inp_bow = self.tfidf.transform([text_input])
        ans = self.clf.kneighbors(inp_bow, n_neighbors=return_count)
        res = []
        for id, score in zip(ans[1][0],ans[0][0]):
            if score > 0:
                self.training_data[id].score = float(score)
                res.append(self.training_data[id])
        return res


#
# Test-run
#
#tmp = NLPcalculator()
#res = tmp.match_text("jag vill jobba med djur och hastar. kanske hovslagare.", 2)
#print(res)
