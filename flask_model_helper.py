'''
Contains helper functions that's called by flask_model.py
'''

from __future__ import print_function

import os
import re
import numpy as np
import nltk
import json
import random
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize, PorterStemmer
from nltk.corpus import stopwords
stop_w = stopwords.words('english')

stop_w += ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]


def encode_phrases(comments, word_encoding=None, add_pos_tags_flag=False):
    '''
    Encodes comments into a vectorized list

    INPUTS:
    :param comments: Array of strings containig contents of comments
    :param word_encoding: Prior hashmap containing mapping of encodings 
    :param add_pos_tags_flag: Flag to add parts-of-speach tags after each word

    RETURNS:
    :return encoded_comments: Comments in a vectorized list of lists
                              words and punctuation vectorized.
    :return word_encoding: hashmap of the word to embeded value
    :return word_decoding: hashmap of the embedded value to word
    '''

    word_decoding = { ' ': 0}     # will store a has to reviews words
    count = 1
    encoded_comments = []

    if word_encoding == None:
        word_encoding = { 0: ' '} # will store a hash of words
    else:
        # Will preload word_decoding if word_encoding exists
        for word in word_encoding:
            word_decoding[word_encoding[word]] = word
        
    max_tokens = 0
    for comment in comments:
        encoded_comment = []

        comment = nltk.word_tokenize(comment)

        # Create a POS sentence: word POS_tag word POS_tag, etc.
        if add_pos_tags_flag:
            comment = nltk.pos_tag(comment)
            comment = [ele for word_tuple in comment for ele in word_tuple]
        ps = PorterStemmer()
        for word in comment:
            word = word.lower() # Lowercase word for mapping
            #added
            #stem  = ps.stem(word)
            #if word in stop_w or stem in stop_w:
            #    continue
            #word = stem
            #END of ADDED
            if word not in word_encoding:
                word_encoding[word] = count
                count += 1
                
            if word not in word_decoding:
                word_decoding[word_encoding[word]] = word
                
            encoded_comment.append(word_encoding[word])
            if len(encoded_comment) > max_tokens:
                max_tokens = len(encoded_comment)
        encoded_comments.append(encoded_comment)
    print('MAX Word tokens among encoded comments is', max_tokens)
    return encoded_comments, word_encoding, word_decoding

def decode_phrases(encoded_comments, word_decoding):
    '''
    Decodes comments to an array of words

    INPUTS:
    :param encoded_comments: Vectorized list of embedded words 
                             and punctiuation. Created by the
                             encode_phrases function
    :param word_decoding: Mapping from word embedding to words.

    RETURNS:
    :return dencoded_comments: Comments in english words (still in list)
    '''
    
    decoded_comments = []
    
    for encoded_comment in encoded_comments:
        decoded_comment = []
        for encoded_word in encoded_comment:
            word = word_decoding[encoded_word]
            decoded_comment.append(word)
        decoded_comments.append(" ".join(decoded_comment))
        
    return decoded_comments

def get_custom_test_comments():
    '''
    Returns a sample test which is easy to manually validates
    '''
    print('\nCreating Manual Test...')
    
    test_comments = [
        "This is a stupid example.",
        "This is another statement, perhaps this will trick the network",
        "I don't understand",
        "What's up",
        "open the app",
        "This is another example",
        "Do what I tell you",
        "come over here and listen",
        "how do you know what to look for",
        "Remember how good the concert was",
        "Who is the greatest basketball player of all time",
        "Eat your cereal.",
        "Usually the prior sentence is not classified properly.",
        "Don't forget about your homework!",
        "Can the model identify a sentence without a question mark",
        "Everything speculated here is VC money and financial bubble with unrelaible financial values. Zomato, uber, paytm, flipkart throw discounts at the rate of losses. May be few can survive at the end. This hurts a lot for SMB too.",
        "I am trying to keep tabs on electric two-wheeler startup industry in India. Ather energy is emerging as a big name. Anyone knows how they are doing",
        "generally a pretty intuitive way to accomplish a task. Want to trash an app Drag it to the trash Want to print a PDF",
        "Make sure ownership is clear and minimizing opportunities for such problematic outcomes in the second place",
        "Stop the video and walk away."
    ]
    
    test_comments_category = [
        "statement",
        "statement",
        "statement",
        "question",
        "command",
        "statement",
        "command",
        "command",
        "question",
        "question",
        "question",
        "command",
        "statement",
        "command",
        "question",
        "statement",
        "question",
        "question",
        "statement",
        "command"
    ]

    return test_comments, test_comments_category

def get_transcript_sentences(dialogue_str):
    dialogue_str = dialogue_str.strip()
    dialogue_str = dialogue_str.replace("\n", " ")
    sentences = sent_tokenize(dialogue_str)
    if len(sentences) == 1:
        print('NO PUNCTUATIONS!')
        from deepsegment import DeepSegment
        segmenter = DeepSegment('en')
        sentences = segmenter.segment_long(sentences[0])
    return sentences


def encode_transcript(test_comments,data_split=1.0, embedding_name=None, add_pos_tags_flag=False):
    
    print("Encoding Data...")
    
    # Import prior mapping
    word_encoding = None
    if embedding_name:
        word_encoding, _  = import_embedding(embedding_name)

    # Encode comments word + punc, using prior mapping or make new
    encoded_comments, word_encoding, \
        word_decoding = encode_phrases(test_comments, word_encoding,
                                       add_pos_tags_flag=add_pos_tags_flag)
    
    print("Embedding Name", embedding_name)
     
    training_sample = int(len(encoded_comments) * data_split)
    
    
    x_test  = np.array(encoded_comments[training_sample:])

    return x_test 


    
def gen_test_comments(max_samples=999999999):

    """    
    Generates sample dataset from parsing
    the SQuAD dataset and combining it 
    with the SPAADIA dataset. 

    The data is then shuffled, and two 
    arrays are returned. One contains
    comments the other categories. 

    The indexes for classification 
    in both arrays match, such that
    comment[i] correlates with category[i].

    Types of sentences:

        Statement (Declarative Sentence)
        Question (Interrogative Sentence)
        Exclamation (Exclamatory Sentence)
        Command (Imperative Sentence)

    Current Counts:

         Command: 1264
         Statement: 81104
         Question: 131219

    Ideally, we will improve the command and 
    exclamation data samples to be at least 
    10% of the overall dataset.
    """
    
    
    tagged_comments = {}
    
    with open('sentence-classification/data/train-v2.0.json', 'r') as qa:
        parsed = json.load(qa)

    statement_count = 0
    question_count  = 0
    command_count   = 0
        
    # Pulls all data from the SQuAD 2.0 Dataset, adds to our dataset
    for i in range(len(parsed["data"])):
        for j in range(len(parsed["data"][i]["paragraphs"])):
            statements = parsed["data"][i]["paragraphs"][j]["context"]
            if random.randint(0,9) % 4 == 0:                
                statement = statements                
                if statement_count < max_samples and statement not in tagged_comments:
                    tagged_comments[statement] = "statement"
                    statement_count += 1                    
            else:
                
                for statement in statements.split("."):
                    if len(statement) <= 2:
                        continue
                    if random.randint(0,9) % 3 == 0:                        
                        statement += "."
                    if statement_count < max_samples and statement not in tagged_comments:
                        tagged_comments[statement] = "statement"
                        statement_count += 1
                        
            for k in range(len(parsed["data"][i]["paragraphs"][j]["qas"])):
            
                question = parsed["data"][i]["paragraphs"][j]["qas"][k]["question"]
            
                if random.randint(0,9) % 2 == 0:
                    question = question.replace("?", "")
                    
                if random.randint(0,9) % 2 == 0:
                    question = statements.split(".")[0]+". "+question
                    
                if question_count < max_samples and question not in tagged_comments:
                    tagged_comments[question] = "question"                
                    question_count += 1

    # Pulls all data from the SPAADIA dataset, adds to our dataset
    for doc in os.listdir('sentence-classification/data/SPAADIA'):
        with open('sentence-classification/data/SPAADIA/' + doc, 'r') as handle:
            conversations = BeautifulSoup(handle, features="xml")
            for imperative in conversations.findAll("imp"):
                    imperative = imperative.get_text().replace("\n", "")
                    if command_count < max_samples and imperative not in tagged_comments:
                        tagged_comments[imperative] = "command"
                        command_count += 1
            for declarative in conversations.findAll("decl"):
                    declarative = declarative.get_text().replace("\n", "")
                    if statement_count < max_samples and declarative not in tagged_comments:
                        tagged_comments[declarative] = "statement"
                        statement_count += 1
            for question in conversations.findAll("q-yn"):
                    question = question.get_text().replace("\n", "")
                    if question_count < max_samples and question not in tagged_comments:
                        tagged_comments[question] = "question"
                        question_count += 1
            for question in conversations.findAll("q-wh"):
                    question = question.get_text().replace("\n", "")
                    if question_count < max_samples and question not in tagged_comments:
                        tagged_comments[question] = "question"
                        question_count += 1

    # Pulls all the data from the manually generated imparatives dataset
    with open('sentence-classification/data/imperatives.csv', 'r') as imperative_file:
        for row in imperative_file:
            imperative = row.replace("\n", "")
            if command_count < max_samples and imperative not in tagged_comments:
                tagged_comments[imperative] = "command"
                command_count += 1

            # Also add without punctuation
            imperative = re.sub('[^a-zA-Z0-9 \.]', '', row)
            if command_count < max_samples and imperative not in tagged_comments:
                tagged_comments[imperative] = "command"
                command_count += 1
        
    test_comments          = []
    test_comments_category = []

    # Ensure random ordering
    comments = list(tagged_comments.items())
    random.shuffle(comments)

    ###
    ### Balance the dataset
    ###
    local_statement_count = 0
    local_question_count  = 0
    local_command_count   = 0
    
    min_count = min([question_count, statement_count, command_count])

    for comment, category in comments:

        '''
        if category is "statement":
            if local_statement_count > min_count:
                continue
            local_statement_count += 1
        elif category is "question":
            if local_question_count > min_count:
                continue
            local_question_count += 1
        elif category is "command":
            if local_command_count > min_count:
                continue
            local_command_count += 1
        '''
        test_comments.append(comment.rstrip())
        test_comments_category.append(category)

    print("\n-------------------------")
    print("command", command_count)
    print("statement", statement_count)
    print("question", question_count)
    print("-------------------------\n")
        
    return test_comments, test_comments_category


def import_embedding(embedding_name="data/default"):
    '''
    Import word embedding to a giant json document
    '''
    if not embedding_name:
        return None, None
    
    file_flag = os.path.isfile(embedding_name+"_word_encoding.json")
    file_flag &= os.path.isfile(embedding_name+"_cat_encoding.json")
    
    if not file_flag:
        return None, None

    word_encoding = {}
    with open(embedding_name+"_word_encoding.json") as word_embedding:
        word_encoding = json.load(word_embedding)

    category_encoding = {}
    with open(embedding_name+"_cat_encoding.json") as cat_embedding:
        category_encoding = json.load(cat_embedding)
    
    return word_encoding, category_encoding
    

def export_embedding(word_encoding, category_encoding,
                     embedding_name="data/default"):
    '''
    Export word embedding to a giant json document
    '''
    if not embedding_name \
       or (not word_encoding) or 2 > len(word_encoding) \
       or (not category_encoding) or 2 > len(category_encoding):
        return
    
    with open("sentence-classification"+embedding_name+"_word_encoding.json", "w") as embedding:
        embedding.write(json.dumps(word_encoding))

    with open("sentence-classification"+embedding_name+"_cat_encoding.json", "w") as embedding:
        embedding.write(json.dumps(category_encoding))
    
    
def encode_data(test_comments, test_comments_category,
                data_split=0.8, embedding_name=None, add_pos_tags_flag=False):
    
    print("Encoding Data...")
    
    # Import prior mapping
    word_encoding, category_encoding = None, None
    if embedding_name:
        word_encoding, category_encoding = import_embedding(embedding_name)

    # Encode comments word + punc, using prior mapping or make new
    encoded_comments, word_encoding, \
        word_decoding = encode_phrases(test_comments, word_encoding,
                                       add_pos_tags_flag=add_pos_tags_flag)
    
    encoded_categories, categories_encoding, \
        categories_decoding = encode_phrases([" ".join(test_comments_category)],
                                             category_encoding,
                                             add_pos_tags_flag=False)

    print("Embedding Name", embedding_name)
    if embedding_name:
        export_embedding(word_encoding, categories_encoding,
                         embedding_name=embedding_name)
    
    training_sample = int(len(encoded_comments) * data_split)
    
    print(np.array(encoded_categories[0]))

    x_train = np.array(encoded_comments[:training_sample])
    x_test  = np.array(encoded_comments[training_sample:])
    y_train = np.array(encoded_categories[0][:training_sample])
    y_test  = np.array(encoded_categories[0][training_sample:])

    print(len(x_train), 'train sequences')
    print(len(x_test), 'test sequences')

    return x_train, x_test, y_train, y_test


def load_encoded_data(data_split=0.8, embedding_name="data/default", pos_tags=False):
    '''
    Loads and encodes embeddings
    If data has already been encoded, uses the pre-encoded data
    If data has not been encoded, encodes, then saves for future use
    returns split training and testing data
    '''

    file_name = embedding_name+"_pre_encoded_comments.csv"
    if pos_tags:
        file_name = embedding_name+"_pre_encoded_pos_tagged_comments.csv"

    encoded_comments   = []
    encoded_categories = []

    # If the encoded results are not available for quick load,
    # create a cache in the data folder of encoded data to pull quickly
    if not os.path.isfile(file_name):

        print("No Cached Data Found...")
        print("Loading Data...")
        
        test_comments, test_comments_category = gen_test_comments()        
        x_train, x_test, y_train, y_test = encode_data(test_comments,
                                                       test_comments_category,
		                                       data_split=data_split,
                                                       embedding_name="data/default",
                                                       add_pos_tags_flag=pos_tags)
        for i in range(len(y_train)):
            encoded_comments.append([y_train[i], x_train[i]])
        for i in range(len(y_test)):
            encoded_comments.append([y_test[i], x_test[i]])

        with open(file_name, 'w') as encoding_file:
            for row in encoded_comments:
                encoding_file.write(str(row[0]) + "|||||" + str(row[1]))
                encoding_file.write('\n')
    else:
        print("Loading Data...")
                
    encoded_comments   = []
    encoded_categories = []
    with open(file_name, 'r') as encoding_file:
        for row in encoding_file:
            row = row.split("|||||")
            row[0] = int(row[0])
            row[1] = row[1].replace("\n", "").replace("[", "").replace("]", "")
            row[1] = np.array(row[1].split(",")).astype('int').tolist()
            encoded_categories.append(row[0])
            encoded_comments.append(row[1])
                
    training_sample = int(len(encoded_comments) * data_split)

    x_train = np.array(encoded_comments[:training_sample])
    x_test  = np.array(encoded_comments[training_sample:])
    y_train = np.array(encoded_categories[:training_sample])
    y_test  = np.array(encoded_categories[training_sample:])

    print(len(x_train), 'train sequences')
    print(len(x_test), 'test sequences')

    return x_train, x_test, y_train, y_test

