import * as d3 from 'd3'
import { BillboardCounter } from '../components/bb-counter/bb-counter'
import { TagDistribution } from '../components/tagdistribution/tagdistribution'

document.body.onload = function init()
{
    // stackoverflow dataset
    const scores = new BillboardCounter({
        parent: document.querySelector("#SCOChart"),         
        height: 120,
        //tickcount: 20,
        data: [],
    })

    const ansercount = new BillboardCounter({
        parent: document.querySelector("#ANCChart"),         
        height: 120,
        data: [],
    })

    const isanswered = new BillboardCounter({
        parent: document.querySelector("#ISAChart"),         
        height: 120,
        data: [],
    })

    const tags = new TagDistribution({
        parent: document.body,
        name: 'Tag',
        data: {},
    })

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

    d3.json("tasks/bag-of-sentences/merge-meta.json")
        .then((mergemeta:any)=> {             
            document.querySelector<HTMLElement>("#downloadheader").innerText = `Stackoverflow: ${mergemeta.files} Files, ${mergemeta.rawquestions} Raw-Questions, ${mergemeta.dupquestions} duplicate, ${mergemeta.errquestions} invalid`
            document.querySelector<HTMLElement>("#mergeheader").innerText = `Merged: ${(mergemeta.size/1024/1024).toFixed(0)}MB, ${mergemeta.questions} Valid-Questions, ${mergemeta.tagcount} Tags`        

            scores.update({
                parent: document.querySelector("#SCOChart"),         
                height: 120,
                tickcount: 20,
                data: Object.entries(mergemeta.scodist)
                    .sort((a:any, b:any)=> a[0] - b[0])
                    .slice(0, 35),        
            })
            ansercount.update({
                parent: document.querySelector("#ANCChart"),         
                height: 120,
                data: Object.entries(mergemeta.ancdist)
                    .sort((a:any, b:any)=> a[0] - b[0]),        
            })
            isanswered.update({
                parent: document.querySelector("#ISAChart"),         
                height: 120,
                data: Object.entries(mergemeta.isadist)
                    .sort((a:any, b:any)=> b[1] - a[1]),        
            })
            tags.update({
                parent: document.body,
                name: 'Tag',
                data: mergemeta.tagdist,        
            })            
        })    

    d3.json("tasks/bag-of-sentences/htmlcleaned-meta.json")
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

    d3.json("tasks/bag-of-words/stemmed-meta.json")
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

    d3.json("tasks/bag-of-words/lemmatized-meta.json")
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
