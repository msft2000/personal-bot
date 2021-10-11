import nltk
import math
import os
import string
from listen import listen
from talk import talk

FILE_MATCHES = 1
SENTENCE_MATCHES = 1
def answer_questions():
    corpus=listen("What is the name of the corpus where the information is?")
    RIGTH_CORPUS=False
    while not RIGTH_CORPUS:
        try:
            files = load_files(corpus.lower())
            talk("Wait a minute i am going to think")
            RIGTH_CORPUS=True
        except:
            corpus=listen("Sorry can you repeat the name of the corpus, i can not find it")
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)
    KEPP_ASKING=True
    while KEPP_ASKING:
        query = set(tokenize(listen("Which are your question?")))
        filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
        sentences = dict()
        for filename in filenames:
            for passage in files[filename].split("\n"):
                for sentence in nltk.sent_tokenize(passage):
                    tokens = tokenize(sentence)
                    if tokens:
                        sentences[sentence] = tokens
        idfs = compute_idfs(sentences)
        matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
        for match in matches:
            talk(match)
        if (listen("Do you want to keep asking? ").lower()) != "yes": KEPP_ASKING=False
def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dic=dict()
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                file_string = file.read()
                dic[filename] = file_string
    return dic


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    final_tokens = []
    tokens = nltk.tokenize.word_tokenize(document.lower())
    for token in tokens:
        if token in nltk.corpus.stopwords.words('english'):
            continue
        else:
            all_punct = True
            for char in token:
                if char not in string.punctuation:
                    all_punct = False
                    break
            if not all_punct:
                final_tokens.append(token)
    return final_tokens

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.    
    """
    D=len(documents)
    words_idf=dict()
    words_df=dict()
    for doc in documents:
        for w in set(documents[doc]):
            if w in words_idf:
                words_df[w]+=1
            else:
                words_idf[w]=0
                words_df[w]=1
    for w in words_idf:
        words_idf[w]=math.log(D/words_df[w])
    return words_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    files_scores = {filename:0 for filename in files}
    for word in query:
        words_tf=dict()
        for file in files:
            words_tf[word]=file.count(word)
            files_scores[file]+=words_tf[word]+idfs[word]
    sorted_files_scores = sorted([filename for filename in files], key = lambda x : files_scores[x], reverse=True)
    return sorted_files_scores[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = {sentence:{'idf_score': 0, 'length':0, 'query_words':0, 'qtd_score':0} for sentence in sentences}
    for sentence in sentences:
        s = sentence_score[sentence]
        s['length'] = len(nltk.word_tokenize(sentence))
        for word in query:
            if word in sentences[sentence]:
                s['idf_score'] += idfs[word]
                s['query_words'] += sentences[sentence].count(word)
        s['qtd_score'] = s['query_words'] / s['length']
    sorted_sentences = sorted([sentence for sentence in sentences], key= lambda x: (sentence_score[x]['idf_score'], sentence_score[x]['qtd_score']), reverse=True)
    return sorted_sentences[:n]