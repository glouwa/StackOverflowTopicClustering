# KDDM2

## Stackexchange Access
https://api.stackexchange.com/docs

User Authorized with account id = 11442814, 
got access token = 7pv4lwwEzDqZsT5Z3ucn2g))

##
``` 
sudo apt-get install node npm python3
npm install
pip install -U nltk 
python3 
> import nltk
> nltk.download('stopwords')
> nltk.download('punkt')
> nltk.download('averaged_perceptron_tagger')
> nltk.download('universal_tagset')
> nltk.download('wordnet')
install all and more
```

## Pipeline:
Use root folder as working path:
- JS: node src/webget.js
- PY: python3 src/lemmatizing.py

| Module            | Input                 | Output              |
| ----------------- | --------------------- | -----------------:  |
| 1. webget.js      |  -                    | #.json[]
| 2. merge.js       |  #.json[]             | merge.json
| 3. htmlclean.py   |  merge.json           | htmlclean.json
| 4. stemming.py    |  htmlclean.json       | stemming.json
| 5. lemmatizing.py |  htmlclean.json       | lemmatizing.json
| 6. tfidf.py       |  lemmatizing.json     | itf.json, doc-vecs.json
| 7. ngram.py       |  ngrams.json          | ngram-itf.json, doc-ngrams.json
| 8. classification |
| 9. evauation      |


### htmlclean.json:
```json
{  
    "8800": {
        "score": 123,
        "title": ["So I been poking around",  "with C# a bit"],
        "body": ["So I been poking around",  "with C# a bit"],
        "code": ["So I been poking around",  "with C# a bit"]
    }
}
```

### stemmed.json, lemmatizing.json:
```json
{
    "8800": ["I", "be", "poke", "be", "C#", "bit"]
}
```

### docvec.json:
```json
{
    "8800":{
        "So":.3, 
        "I":.4,
        "been": .3
    },
    "3800":{
        "bla":.3,         
    }
}
```

### idf.json:
```json
{
    "So":.2, 
    "I":.14,
    "been": .23,
    "bla": .1,
}
```

### todo

Michi:
gulp
tagcloud
cleaning fertig machen: documentieren 
 -encoding
 -sonderzeichen
 -min word len, 
zusammenfügen (file format) 


Veri:
remove stopweord
stemming lemming refac
zusammenfügen
reaserch: was is a besserer lemma input: mit oder ohne stopwords
