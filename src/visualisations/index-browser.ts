import * as d3 from 'd3'
import { BillboardCounter } from '../components/bb-counter/bb-counter'
import { TagDistribution } from '../components/tagdistribution/tagdistribution'
import { StackOverflowMeta } from '../model/bag-of-words/base'
import { StackoverflowDataset } from '../components/stackexchange/stackexchange-view'

document.body.onload = function init()
{
    const dataset = new StackoverflowDataset({
        parent: document.body
    })
    d3.json("data/bag-of-texts/stackoverflow-meta.json")
      .then((datasetmeta:StackOverflowMeta)=> dataset.update(datasetmeta))

    // Plain
    const plaintitle = new TagDistribution({
        parent: document.body,
        name: 'Plain Title',
        data: {}
    })
    const plainbody = new TagDistribution({ 
        parent: document.body,
        name: 'Plain Body',
        data: {}
    })
    d3.json("data/bag-of-words/htmlcleaned-meta.json")
        .then((htmlcleanedmeta:any)=> { 
            plaintitle.update({
                name: 'Plain Title',
                data: htmlcleanedmeta.titletermdist,        
            })
            plainbody.update({
                name: 'Plain Body',
                data: htmlcleanedmeta.termdist
            })
        }) 
        
    // Stemmed
    const stemmedtitle = new TagDistribution({
        parent: document.body,
        name: 'Stemmed Title',
        data: {}
    })
    const stemmedbody = new TagDistribution({
        parent: document.body,
        name: 'Stemmed Body',
        data: {}
    })
    d3.json("data/bag-of-words/stemmed-meta.json")
        .then((stemmeta:any)=> { 
            stemmedtitle.update({
                name: 'Stemmed Title',
                data: stemmeta.title_terms,        
            })
            stemmedbody.update({
                name: 'Stemmed Body',
                data: stemmeta.body_terms
            })
        }) 

    // Lemmed
    const lemmedtitle = new TagDistribution({
        parent: document.body,
        name: 'Lemmed Title',
        data: {}
    })
    const lemmedbody = new TagDistribution({
        parent: document.body,
        name: 'Lemmed Body',
        data: {}
    })
    d3.json("data/bag-of-words/lemmatized-meta.json")
        .then((lemmmeta:any)=> { 
            lemmedtitle.update({
                name: 'Lemmed Title',
                data: lemmmeta.title_terms,        
            })
            lemmedbody.update({
                name: 'Lemmed Body',
                data: lemmmeta.body_terms
            })
        })
}
