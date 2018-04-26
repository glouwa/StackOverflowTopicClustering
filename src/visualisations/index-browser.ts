import * as d3 from 'd3'
import { BillboardCounter } from '../components/bb-counter/bb-counter'
import { TagDistribution } from '../components/tagdistribution/tagdistribution'

var mergemeta

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

    // Tags
    const tags = new TagDistribution({
        parent: document.body,
        name: 'Tag',
        data: {},
    })

    // Title
    const plaintitle = new TagDistribution({
        parent: document.body,
        name: 'Title plain',
        data: {}
    })

    const stemmedtitle = new TagDistribution({
        parent: document.body,
        name: 'Title stemmed',
        data: {}
    })

    const lemmedtitle = new TagDistribution({
        parent: document.body,
        name: 'Title lemmed',
        data: {}
    })

    // Body
    const plainbody = new TagDistribution({ 
        parent: document.body,
        name: 'Body plain',
        data: {}
    })

    const stemmedbody = new TagDistribution({
        parent: document.body,
        name: 'Body stemmed',
        data: {}
    })

    const lemmedbody = new TagDistribution({
        parent: document.body,
        name: 'Body lemmed',
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
                name: 'Title plain',
                data: htmlcleanedmeta.titletermdist,        
            })
            plainbody.update({
                name: 'Body plain',
                data: htmlcleanedmeta.termdist
            })
        }) 

    d3.json("tasks/bag-of-words/stemmed-meta.json")
        .then((stemmeta:any)=> { 
            stemmedtitle.update({
                name: 'Title stemmed',
                data: stemmeta.title_terms,        
            })
            stemmedbody.update({
                name: 'Body stemmed',
                data: stemmeta.body_terms
            })
        }) 

    d3.json("tasks/bag-of-words/lemmatized-meta.json")
        .then((lemmmeta:any)=> { 
            lemmedtitle.update({
                name: 'Title lemmed',
                data: lemmmeta.title_terms,        
            })
            lemmedbody.update({
                name: 'Body lemmed',
                data: lemmmeta.body_terms
            })
        })
}
