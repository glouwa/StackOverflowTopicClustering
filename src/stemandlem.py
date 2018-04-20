import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tag import pos_tag
#nltk.download() to download further packages/modules for nltk
'''Extract words from each sentence, tokenize and pos_tag it. Afterwards stemming and lemmatization happens'''

def convert_tagset(tag):
    '''Convert Universal tagset to wordnet tagset, default is 'NOUN' '''
    if tag == "ADJ":
        return wordnet.ADJ
    elif tag == "VERB":
        return wordnet.VERB
    elif tag == "ADV":
        return wordnet.ADV
    else:
        return wordnet.NOUN

sentences = ["Cats are paid much money","The quick brown fox jumped quickly over the lazy dog","He studies a lot of different technologies","The boys' room is dirty", "The boy's dirty"]

snow_stemmer = SnowballStemmer("english", ignore_stopwords=False)
lemmatizer = WordNetLemmatizer()

words = []
stems = []
lemmas = []

for sentence in sentences:
    print("Sentence:\t"+sentence)
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens,tagset='universal')
    tmp_words = list(sentence.lower().split(" "))
    words += (tmp_words)
    for word in tmp_words:
        stems.append(snow_stemmer.stem(word))
    for i in range(len(tmp_words)):
        lemmas.append(lemmatizer.lemmatize(tmp_words[i],convert_tagset(tagged[i][1])))
print("")
for i in range(len(words)):
    print("Original:\t"+words[i].ljust(15)+"\tStem: "+stems[i].ljust(15)+"\tLemma: "+lemmas[i].ljust(15))
