
from collections import defaultdict 
from collections import namedtuple

from nltk.stem import PorterStemmer 

import math

Posting = namedtuple("Posting", "docid tfidf")

def search_results(query: str, doc_len_loaded: list, data_dict: str, pos_dict_loaded: dict, doc_ids: dict, num_of_doc: int) -> list:
    ps = PorterStemmer()
    scores = defaultdict(int)
    read_stream = open(data_dict, "r")
    docids_used = set()
    for word in query.lower().split():
        word = ps.stem(word)
        if word not in pos_dict_loaded:
            wtq = 0
        else:
            read_stream.seek(pos_dict_loaded[word])
            term_postings_tuple = eval(read_stream.readline()) #this is a tuple (term, postings list)
            wtq = (1 + math.log10(query.lower().count(word.lower()))) * math.log10(num_of_doc/len(term_postings_tuple[1]))
            for posting in term_postings_tuple[1]:
                scores[posting.docid] += posting.tfidf * wtq
                docids_used.add(posting.docid)
    for x in docids_used:
        if doc_len_loaded[x] != 0:
            scores[x] = scores[x]/doc_len_loaded[x]
        else:
            scores[x] = 0
    sorted_score_tuples = sorted(scores.items(), key = lambda x: x[1], reverse = True)
    top_5 = []
    if len(sorted_score_tuples):
        # print()
        # print("Top 10 results:")
        for x in sorted_score_tuples[0:5]:
            top_5.append(x[0]) #add the URL portion of tuple to list
        return top_5
    else:
        # print()
        # print("No results are available.")
        return top_5
        