# KDDM2

For a summary see [Info Poster](https://drive.google.com/file/d/1MVLcjVWxoR1Gj3BeBN4GMhDpZ4QqUS--/view?usp=sharing)

## Stackexchange Data Crawling
https://api.stackexchange.com/docs

User Authorized with account id = USER_ID, 
got access token = ACCESS_TOKEN

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
| 6. tfidf.py       |  lemmatizing.json     | itf.json,         doc-vecs.json
| 7. ngram.py       |  ngrams.json          | ngram-itf.json,   doc-ngrams.json
| 8. classification |  
| 9. clusterning    |

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

## Stemmer Algorithms Differences:

The three major stemming algorithms in use today are Porter, Snowball(Porter2), and Lancaster (Paice-Husk), with the aggressiveness continuum basically following along those same lines.

- Porter: Most commonly used stemmer without a doubt, also one of the most gentle stemmers. One of the few stemmers that actually has Java support which is a plus, though it is also the most computationally intensive of the algorithms(Granted not by a very significant margin). It is also the oldest stemming algorithm by a large margin.

- Snowball (=Porter2): Nearly universally regarded as an improvement over porter, and for good reason. Porter himself in fact admits that it is better than his original algorithm. Slightly faster computation time than porter, with a fairly large community around it.

- Lancaster: Very aggressive stemming algorithm, sometimes to a fault. With porter and snowball, the stemmed representations are usually fairly intuitive to a reader, not so with Lancaster, as many shorter words will become totally obfuscated. The fastest algorithm here, and will reduce your working set of words hugely, but if you want more distinction, not the tool you would want.

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
