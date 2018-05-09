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
| 2. merge.js       |  #.json[]             | merge.json,       merge-meta.json
| 3. htmlclean.py   |  merge.json           | htmlcleaned.json, htmlcleaned-meta.json
| 4. stemming.py    |  htmlcleaned.json     | stemming.json,    stemming-meta.json
| 5. lemmatizing.py |  htmlcleaned.json     | lemmatizing.json, lemmatizing-meta.json

### Next Steps
| Module            | Input                 | Output              |
| ----------------- | --------------------- | -----------------:  |
| 6. tfidf.py       |  lemmatizing.json     | itf.json,         doc-vecs.json
| 7. ngram.py       |  ngrams.json          | ngram-itf.json,   doc-ngrams.json
| 8. classification |
| 9. evauation      |

- Machine Learning Algorithms
- Evaluation methods (especially for multi-classification)

### merge
```json
{  
    "8800": {
        "score": 123,
        "title": ["So I been poking around",  "with C# a bit"],
        "body": ["So I been poking around",  "with C# a bit"],
        "code": ["So I been poking around",  "with C# a bit"]
    }
}
{
    "files": 1000,
    "rawquestions": 26460,  //raw_question
    "errquestions": 117,    //err_question
    "dupquestions": 8319,  //dup_question
    "questions": 18141,
    "size": 78717106,
    "tagdist": {},      // tag_dist
    "tagcount": 8655,   // tag_count
    ...
}

```

### clean
```json
{  
    "8800": {
        "title": ["accessing post variables using java servlets"],
        "body": ["what is the java equivalent of php's","after searching the web for an hour, i'm still"]
    }
}

{
    "termdist": {},   // body_term_dist
    "titletermdist": {}  // title_term_dist
}
```

### stem & lem
```json
{      
    "10012019": {
        "body": ["i", "need", "to", "see"...],
        "title": [ "how", "to", ...]
    }
}

{
    "body_terms": {},  // body_term_dist
    "title_terms": {}  // title_term_dist
}
```


### TODO

Michi:
gulp
tagcloud
cleaning fertig machen: documentieren 
 -encoding 


Veri:
remove stopword, change stemming tokenizer
clean tokenizer(remove all single special characters)
reaserch: was is a besserer lemma input: mit oder ohne stopwords
what to do for evaluation? (precision, recall, accuracy)


gulp download
gulp convert
python3 src/sentences.py
python3 src/terms.py
python3 src/stemming.py
python3 src/lemming.py
python3 src/ngram.py 
// change n
python3 src/ngram.py
gulp convert