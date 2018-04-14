from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm
import pickle
import json
import logging
import os.path


class NLPcalculator:
    def __init__(self):
        self.tfidf = TfidfVectorizer(min_df=5, max_df=75)
        self.clf = NearestNeighbors()
        self.setup_model()

    #
    # Constructor
    # Startup script - setting up model
    #
    def setup_model(self):
        if not os.path.exists("./jobListings.pickle"):
            print("No previous data found - setting up model")
            jobs, ids = get_jobs()
            self.ids = ids
            self.jobs = jobs
        else:
            print("Pre-trained model found - accessing content and IDs")
            self.jobs = pickle.load(open("./jobListings.pickle", "r"))
            self.ids = pickle.load(open("./jobListingsIds.pickle", "r"))

        if not os.path.exists("./tfidfVectorizer.pickle"):
            print("No previous Tf-Idf model found - setting up matrix")
            inp_bow = self.train_vector_model(self.jobs)
        else:
            print("Pre-trained Tf-Idf model found - accessing matrix")
            self.tfidf = pickle.load(open("./tfidfVectorizer.pickle", "r"))
            inp_bow = self.tfidf.transform(self.jobs)

        if not os.path.exists("./nearestNeighbor.pickle"):
            print("No previous NN-Algorithm found - training model")
            self.train_nearest_neighbor(inp_bow)
        else:
            print("NN-Algorithm found - setting up model")
            self.clf = pickle.load(open("./nearestNeighbor.pickle", "r"))

    #
    # Training and storing the Tf-Idf vectorization matrix - storing result using pickle
    #
    def train_vector_model(self, jobs):
        logging.info("training Tf-Idf-vectorizer")
        inp_bow = self.tfidf.fit_transform(jobs)
        pickle.dump(self.tfidf, open("./tfidfVectorizer.pickle", "w"), protocol=2)
        logging.info("tfidf - BOW shape")
        return inp_bow

    #
    # Training and storing the NearestNeighbors algorithm - storing result using pickle
    #
    def train_nearest_neighbor(self, inp_bow):
        logging.info("training NN")
        self.clf.fit(inp_bow)
        pickle.dump(self.clf, open("./nearestNeighbor.pickle", "w"), protocol=2)
        logging.info("Fit done")

    #
    # Matching IDS with the main database ID-list
    #
    def match_id_with_custom_id(self, id_inp):
        return self.ids[id_inp]

    #
    # Main method; returns
    #
    def match_text(self, text_input, return_count):
        inp_bow = self.tfidf.transform([text_input])
        ans = self.clf.kneighbors(inp_bow, n_neighbors=return_count)
        res = {"id": [self.match_id_with_custom_id(t) for t in ans[1][0]],
               "score": ans[0][0]}
        return res

#
# Mocking function - get jobDescr. and IDs
#
#def get_jobs():
#    txt = ["test sadasd sad", "inget spec", "asd asas dsa dsasd", "asd ada sad a sda", "seconde"]
#    ids = [1231, 12312, 122]
#    return txt, ids

#
# Test-run
#
#tmp = NLPcalculator()
#res = tmp.match_text("jag vill jobba med djur och hastar. kanske hovslagare.", 2)
#print res
