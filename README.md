# KDDM2

## Stackexchange Access
https://api.stackexchange.com/docs

User Authorized with account id = 11442814, 
got access token = 7pv4lwwEzDqZsT5Z3ucn2g))

## 
sudo apt-get install node python3
npm install
pip install nlpk -u


## Pipeline:
Use root folder as working path:
- JS: node src/webget.js
- PY: python3 src/lemmatizing.py

| Module            | Input                 | Output              |
| ----------------- | --------------------- | -----------------:  |
| 1. webget.js      |   -                   |  #.json[]
| 2. merge.js       |   #.json[]            |  merge.json
| 3. htmlclean.py   |   merge.json          |  htmlclean.json
| 4. stemming.py    |   htmlclean.json      |  stemming.json
| 5. lemmatizing.py |   htmlclean.json      |  lemmatizing.json
| 6. tfidf.py       |   lemmatizing.json    |  itf.json, docvecs.json
| 7. ngram.py       |   ngrams.json         |  ngramitf.json, docngrams.json


### htmlclean.json:
```json
{
    "8800": "So I been poking around with C# a bit"
}
```

```json
#### stemmed.json, lemmatizing.json:
{
    "8800": ["So", "I", "been", "poking"]
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

read write functions
htmlclean