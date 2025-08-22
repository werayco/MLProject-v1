from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle as pkl
from nltk.stem import PorterStemmer
import os
from nltk.corpus import stopwords
import string

stopwords_set = set(stopwords.words("english"))
stemmer = PorterStemmer()  

def pickle_loader(path_of_pickle_file: str):
    with open(path_of_pickle_file, "rb") as model_obj:
        output = pkl.load(model_obj)
    return output

vectorizer = pickle_loader("/app/models/vectorizer.pkl")
model = pickle_loader("/app/models/multinomial_naive_bayess.pkl")
encoder = pickle_loader("/app/models/encoder.pkl")
def second_workflow(text):
    email_text = (
        text.lower().translate(str.maketrans("", "", string.punctuation)).split()
    )
    email_text = [
        stemmer.stem(word) for word in email_text if word not in stopwords_set
    ]
    email_text = " ".join(email_text)
    email_corpus = [email_text]
    x_email = vectorizer.transform(email_corpus)

    predicted_probabilities = model.predict_proba(x_email)
    predicted_class = predicted_probabilities.argmax(axis=1)
    confidence = predicted_probabilities[0][predicted_class[0]]
    actual_label = encoder.inverse_transform(predicted_class)
    return actual_label[0], confidence

