import * as d3 from 'd3'
import { StackOverflowMeta } from '../model/model'
import { TagDistribution } from '../components/tagdistribution/tagdistribution'
import { StackoverflowDatasetView } from '../components/stackexchange/stackexchange-view'

class TermformatView 
{
    private args
    private plaintitle
    private plainbody
    
    constructor(args)
    {
        this.args = args
        this.plaintitle = new TagDistribution({
            parent: document.body,
            name: `${this.args.format} Title`,
        })
        this.plainbody = new TagDistribution({
            parent: document.body,
            name: `${this.args.format} Body`,
        })        
    }

    public update(data) 
    {
        this.plaintitle.update({             
            name: `${this.args.format} Title`,
            data: data.title 
        })
        this.plainbody.update({             
            name: `${this.args.format} Body`,
            data: data.body 
        })        
    }
}

window.d3 = d3
window.TagDistribution = TagDistribution
window.StackoverflowDatasetView = StackoverflowDatasetView
window.showAll = function()
{
    const dataset = new StackoverflowDatasetView({
        parent: document.body
    })

    const plaininlinecode = new TagDistribution({
        parent: document.body,
        name: `Inline Code`,
    })
    const plaincode = new TagDistribution({
        parent: document.body,
        name: `Code`,
    })
 
    //const termsraw = new TermformatView({ format:'Plain' })
    //const termsstem = new TermformatView({ format:'Stem' })
    const termslem = new TermformatView({ format:'Lemma' })
    const ngram2 = new TermformatView({ format:'2Grams' })
    //const ngram3 = new TermformatView({ format:'3Grams' })
    
    d3.json("/dist/data/bag-of-words/stackoverflow-raw-meta.json")
      .then((datasetmeta:StackOverflowMeta)=> { 
            dataset.update(datasetmeta)
            //termsraw.update(datasetmeta.distributions.terms)            
            plaininlinecode.update({             
                name: `Inline Code`,
                data: datasetmeta.distributions.terms.inlinecode
            })
            plaincode.update({             
                name: `Code`,
                data: datasetmeta.distributions.terms.code
            })
      })
/*
    d3.json("data/bag-of-words/stackoverflow-stem-meta.json")
      .then((datasetmeta:StackOverflowMeta)=> { 
            termsstem.update(datasetmeta.distributions.terms)
      })*/
    d3.json("/dist/data/bag-of-words/stackoverflow-lemma-meta.json")
      .then((datasetmeta:StackOverflowMeta)=> { 
            termslem.update(datasetmeta.distributions.terms)
      })
    d3.json("/dist/data/ngrams/stackoverflow-2gram-stem-meta.json")
      .then((datasetmeta:StackOverflowMeta)=> { 
            ngram2.update(datasetmeta.distributions.terms)
      })/*
    d3.json("data/ngrams/stackoverflow-3gram-stem-meta.json")
      .then((datasetmeta:StackOverflowMeta)=> { 
            ngram3.update(datasetmeta.distributions.terms)
      })*/
}
