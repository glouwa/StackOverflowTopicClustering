
# Machine Learning
    
- Task: Automatic tagging of resources, using either an unsupervised or a supervised approach. The goal is to apply tags to an unseen resource.
- Approach: For this project the approach may vary widely. A supervised approach requires a training dataset and may include classification algorithms. Unsupervised approaches may either look at a set of resources or a single resource at a time.
- Suggested data-sets:
    - Stack Exchange:
        One example for tagged data are the stack exchange pages, which can be downloaded at Stack Exchange Website
    - Last.fm
        The Million Song Dataset, which contains tracks, similar tracks as well as tags. The dataset is already split into a training and testing dataset and can be accessed at Last.fm website
- Advanced: Implement an unsupervised and a supervised approach, and then compare the two approaches. Measure their differences in accuracy as well as discuss their individual strengths and weaknesses.
 
## Stemmer Algorithms Differences:

The three major stemming algorithms in use today are Porter, Snowball(Porter2), and Lancaster (Paice-Husk), with the aggressiveness continuum basically following along those same lines.

- Porter: Most commonly used stemmer without a doubt, also one of the most gentle stemmers. One of the few stemmers that actually has Java support which is a plus, though it is also the most computationally intensive of the algorithms(Granted not by a very significant margin). It is also the oldest stemming algorithm by a large margin.

- Snowball (=Porter2): Nearly universally regarded as an improvement over porter, and for good reason. Porter himself in fact admits that it is better than his original algorithm. Slightly faster computation time than porter, with a fairly large community around it.

- Lancaster: Very aggressive stemming algorithm, sometimes to a fault. With porter and snowball, the stemmed representations are usually fairly intuitive to a reader, not so with Lancaster, as many shorter words will become totally obfuscated. The fastest algorithm here, and will reduce your working set of words hugely, but if you want more distinction, not the tool you would want.



## Pipeline:
```
1- webget.js       ()                  -> #.json[]
2- merge.js        (#.json[])          -> merge.json                  // one file. contains map qid->q
3- htmlclean.py    (merge.json)        -> htmlclean.json              // one file. contains map qid->
4- stemming.py     (htmlclean.json)    -> stemming.json               // 
5- lemmatizing.py  (stemming.json)     -> lemmatizing.json            // 
6- tfidf.py        (lemmatizing.json)  -> (itf.json, docvecs.json)    // 
6- ngram.py        (ngrams.json)       -> (ngramitf.json, docngrams.json)    // 
```

### Example Jsons:
```json
htmlclean.json:
{
    "8800": "So I been poking around with C# a bit"
}
```
```json
stemmed.json, lemmatizing.json:
{
    "8800": ["So", "I", "been", "poking"]
}
```
```json
docvec.json:
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
```json
idf.json:
{
    "So":.2, 
    "I":.14,
    "been": .23,
    "bla": .1,
}
```