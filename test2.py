
import re
import zipfile
from collections import Counter, OrderedDict
from math import log2,sqrt
from nltk.corpus import wordnet
from bs4 import BeautifulSoup, Comment

archive= zipfile.ZipFile('Jan.zip','r')

files= archive.namelist()

N = len(files)

# terms = Counter()
documents= {}
positions= {}
terms ={}
df= {} #document frequency
tfidf = {}
doc_len= {}
title_desc={}
for i in files:
    file_contents = archive.read(i).decode('utf-8')
    soup = BeautifulSoup(file_contents, 'html.parser')



    title_desc[i]= [soup.find('title').text, ""]

    for s in soup.find_all(['style', 'script']):
        s.extract()
    for comment in soup(text=lambda it: isinstance(it, Comment)):
        comment.extract()
    # pull titles and description
    # print(soup.title.text)
    # remove all non-alphanumeric but keep '
    wordlist = re.sub('[^A-Za-z\']', " ", soup.text.lower()).split()
    title_desc[i][1]=wordlist.copy()
    stopwords = {"about", "above", "after", "again", "against", "ain", "all", "and", "any", "are", "aren", "aren't",
                 "because", "been", "before", "being", "below", "between", "both", "but", "can", "couldn", "couldn't",
                 "did", "didn", "didn't", "does", "doesn", "doesn't", "doing", "don", "don't", "down", "during", "each",
                 "few", "for", "from", "further", "had", "hadn", "hadn't", "has", "hasn", "hasn't", "have", "haven",
                 "haven't", "having", "her", "here", "hers", "herself", "him", "himself", "his", "how", "into", "isn",
                 "isn't", "it's", "its", "itself", "just", "mightn", "mightn't", "more", "most", "mustn", "mustn't",
                 "myself", "needn", "needn't", "nor", "not", "now", "off", "once", "only", "other", "our", "ours",
                 "ourselves", "out", "over", "own", "same", "shan", "shan't", "she", "she's", "should", "should've",
                 "shouldn", "shouldn't", "some", "such", "than", "that", "that'll", "the", "their", "theirs", "them",
                 "themselves", "then", "there", "these", "they", "this", "those", "through", "too", "under", "until",
                 "very", "was", "wasn", "wasn't", "were", "weren", "weren't", "what", "when", "where", "which", "while",
                 "who", "whom", "why", "will", "with", "won", "won't", "wouldn", "wouldn't", "you", "you'd", "you'll",
                 "you're", "you've", "your", "yours", "yourself", "yourselves", "could", "he'd", "he'll", "he's",
                 "here's", "how's", "i'd", "i'll", "i'm", "i've", "let's", "ought", "she'd", "she'll", "that's",
                 "there's", "they'd", "they'll", "they're", "they've", "we'd", "we'll", "we're", "we've", "what's",
                 "when's", "where's", "who's", "why's", "would", "able", "abst", "accordance", "according",
                 "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects",
                 "afterwards", "almost", "alone", "along", "already", "also", "although", "always", "among", "amongst",
                 "announce", "another", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways",
                 "anywhere", "apparently", "approximately", "arent", "arise", "around", "aside", "ask", "asking",
                 "auth", "available", "away", "awfully", "back", "became", "become", "becomes", "becoming",
                 "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "believe", "beside", "besides",
                 "beyond", "biol", "brief", "briefly", "came", "cannot", "can't", "cause", "causes", "certain",
                 "certainly", "com", "come", "comes", "contain", "containing", "contains", "couldnt", "date",
                 "different", "done", "downwards", "due", "edu", "effect", "eight", "eighty", "either", "else",
                 "elsewhere", "end", "ending", "enough", "especially", "etc", "even", "ever", "every", "everybody",
                 "everyone", "everything", "everywhere", "except", "far", "fifth", "first", "five", "fix", "followed",
                 "following", "follows", "former", "formerly", "forth", "found", "four", "furthermore", "gave", "get",
                 "gets", "getting", "give", "given", "gives", "giving", "goes", "gone", "got", "gotten", "happens",
                 "hardly", "hed", "hence", "hereafter", "hereby", "herein", "heres", "hereupon", "hes", "hid", "hither",
                 "home", "howbeit", "however", "hundred", "immediate", "immediately", "importance", "important", "inc",
                 "indeed", "index", "information", "instead", "invention", "inward", "itd", "it'll", "keep", "keeps",
                 "kept", "know", "known", "knows", "largely", "last", "lately", "later", "latter", "latterly", "least",
                 "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking",
                 "looks", "ltd", "made", "mainly", "make", "makes", "many", "may", "maybe", "mean", "means", "meantime",
                 "meanwhile", "merely", "might", "million", "miss", "moreover", "mostly", "mrs", "much", "mug", "must",
                 "name", "namely", "nay", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither",
                 "never", "nevertheless", "new", "next", "nine", "ninety", "nobody", "non", "none", "nonetheless",
                 "noone", "normally", "nos", "noted", "nothing", "nowhere", "obtain", "obtained", "obviously", "often",
                 "okay", "old", "omitted", "one", "ones", "onto", "ord", "others", "otherwise", "outside", "overall",
                 "owing", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed",
                 "please", "plus", "poorly", "possible", "possibly", "potentially", "predominantly", "present",
                 "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "que", "quickly",
                 "quite", "ran", "rather", "readily", "really", "recent", "recently", "ref", "refs", "regarding",
                 "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting",
                 "results", "right", "run", "said", "saw", "say", "saying", "says", "sec", "section", "see", "seeing",
                 "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall",
                 "shed", "shes", "show", "showed", "shown", "showns", "shows", "significant", "significantly",
                 "similar", "similarly", "since", "six", "slightly", "somebody", "somehow", "someone", "somethan",
                 "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically",
                 "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially",
                 "successfully", "sufficiently", "suggest", "sup", "sure", "take", "taken", "taking", "tell", "tends",
                 "thank", "thanks", "thanx", "thats", "that've", "thence", "thereafter", "thereby", "thered",
                 "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've",
                 "theyd", "theyre", "think", "thou", "though", "thoughh", "thousand", "throug", "throughout", "thru",
                 "thus", "til", "tip", "together", "took", "toward", "towards", "tried", "tries", "truly", "try",
                 "trying", "twice", "two", "unfortunately", "unless", "unlike", "unlikely", "unto", "upon", "ups",
                 "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "value", "various",
                 "'ve", "via", "viz", "vol", "vols", "want", "wants", "wasnt", "way", "wed", "welcome", "went",
                 "werent", "whatever", "what'll", "whats", "whence", "whenever", "whereafter", "whereas", "whereby",
                 "wherein", "wheres", "whereupon", "wherever", "whether", "whim", "whither", "whod", "whoever", "whole",
                 "who'll", "whomever", "whos", "whose", "widely", "willing", "wish", "within", "without", "wont",
                 "words", "world", "wouldnt", "www", "yes", "yet", "youd", "youre", "zero", "a's", "ain't", "allow",
                 "allows", "apart", "appear", "appreciate", "appropriate", "associated", "best", "better", "c'mon",
                 "c's", "cant", "changes", "clearly", "concerning", "consequently", "consider", "considering",
                 "corresponding", "course", "currently", "definitely", "described", "despite", "entirely", "exactly",
                 "example", "going", "greetings", "hello", "help", "hopefully", "ignored", "inasmuch", "indicate",
                 "indicated", "indicates", "inner", "insofar", "it'd", "novel", "presumably", "reasonably", "second",
                 "secondly", "sensible", "serious", "seriously", "t's", "third", "thorough", "thoroughly", "three",
                 "well", "wonder", "amoungst", "amount", "bill", "bottom", "call", "con", "cry", "describe", "detail",
                 "eleven", "empty", "fifteen", "fify", "fill", "find", "fire", "forty", "front", "full", "hasnt",
                 "interest", "mill", "mine", "move", "side", "sincere", "sixty", "system", "ten", "thickv", "thin",
                 "top", "twelve", "twenty", "research-articl", "pagecount", "cit", "ibid", "les", "est", "pas", "los",
                 "u201d", "well-b", "http", "volumtype", "par"}
    # Testing purposes
    # stopwords = {}
    wordlist = [word for word in wordlist if len(word) > 2 and word not in stopwords]  # remove stop words and 2 chars
    # terms = []
    terms ={}

    #index = position w= word
    for index, word in enumerate(wordlist):
        if(word in terms):
            terms[word][0] +=1
            terms[word][1].append(index)
        else:
            terms[word]= [1,[index]]
            if word in df:
                df[word].append(i)
            else:
                df[word] = []
                df[word].append(i)

    documents[i]= terms

for i in files:
    fterms = documents[i]
    tmax = max(fterms.values())[0]

    #added doc_sum
    doc_sum = 0
    for term,value in fterms.items():
        tf = value[0]/tmax  #freq of term in doc/max freq
        idf = log2(N/(len(df[term])+1)) + 1 #Smoothed idf
        tfidf[i,term] = tf*idf
        #doc_sum hold all tfidf for a document and squares them
        doc_sum = doc_sum + ((tf*idf) ** 2)
        #doc_length is the sqrt of the document sum
    doc_len[i] = sqrt(doc_sum)

def queryExp(keyword):
    synonyms =[]
    for syn in wordnet.synsets(keyword):
        for l in syn.lemmas():
            synonyms.append(l.name())

    return synonyms


#Parse Query and get documents belonging to all the keywords
def queryParser(query):
    str = query
    docs = []
    operator = ""

    #Check for and or and but
    if "and" in str:
        operator = "and"
        str = list(filter(("and").__ne__, str)) #revoming the word and from the list.
    elif "or" in str:
        operator = "or"
        str = list(filter(("or").__ne__, str))
    elif "but" in str:
        operator = "but"
        str = list(filter(("but").__ne__, str))
    else:
        operator = "none"


    #Testing Query Expansion Code.
    #newstr=[]
    #for q in str:
    #    newstr.extend(queryExp(q))



    #Do Query operations and retrieve list of documents belong to the keywords.
    if str:
        if str[0] in df.keys():
            docs = df[str[0]]
        for d in str:
            if d in df.keys() and operator == "none":
                docs = list(set(df[d]).union(set(docs)))
            elif d in df.keys() and operator == "and":
                docs = list(set(df[d]) & set(docs))
            elif d in df.keys() and operator == "or":
                docs = list(set(df[d]).union(set(docs)))
            elif d in df.keys() and operator == "but":
                if docs != df[d]:
                    docs = list(set(docs).difference(set(df[d])))



    return docs

def titleDesc(document,query):
    title =title_desc[document][0]
    for keyword in query.split():
        try:
            tmp = title_desc[document][1].index(keyword)
            desc = title_desc[document][1][index: index+40]
            break
        except :
            pass
    desc= ' '.join([str(elem) for elem in desc])
    return [title,desc]

def cosine(keywords):
    cosine_sim = {}
    str = keywords.lower().split()
    docs = queryParser(str)
            
    inner = Counter()
    for x in docs:
        for tf in str:
            try:
                inner[x] += tfidf[x,tf]
            except:
                pass
        cosine_sim[x]= inner[x] /(doc_len[x]*sqrt(len(str)))
    return cosine_sim
    

def phrasal_search(keywords):
    keywords = re.sub('"','', keywords)
    k = keywords.lower().split( )
    searchterm = ''
    for x in k[0:-1]:
        searchterm += x + ' and '
    searchterm+=k[-1]

    and_docs = list(cosine(searchterm).keys())
    R = {}

    for doc in and_docs:
        current_doc_terms = documents[doc]
        # Positions of k0
        g = current_doc_terms[k[0]]
        # For each position p of keyword k_0 in P_0(g)
        match_found = 1
        for p in g[1]:
            # For each keyword k_j, 1≤j ≤m
            for idx, j in enumerate(k[1:]):
                # Check whether p+|k_(j-1) |+1∈P_j
                if(j in current_doc_terms.keys()):
                    pj_doc = current_doc_terms[j]
                    pj = pj_doc[1]
                    # p + len(k[idx]) + 1
                    if (p + idx+ 1) not in pj:
                        match_found = 0
                else:
                    match_found = 0
        if(match_found == 1):
            R[doc] = 1
    return R


    #Test print
    #print(i,":",sqrt(doc_sum))
    #print(i,":",doc_length)        
    
#added his print from his example here
# print("Now the search begins:")
#
# c= "none"
# while c != "":
#     c = input("enter a search key=>")
#     arr= []
#     for doc in documents:
#         if c in documents[doc]:
#             arr.append(doc)
#     if len(arr)>0:
#         print("found a match:")
#         print(arr)
#     else:
#         if c!="":
#             print("no match")
#         else:
#             print("Bye")
