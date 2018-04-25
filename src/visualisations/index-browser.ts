//import * as d3 from 'd3'

import { TagCloud } from '../components/cloud/cloud'
import { plot } from '../components/bb-counter/bb-counter'
import { BillboardCounter } from '../components/bb-counter/bb-counter'
import { TagDistribution } from '../components/tagdistribution/tagdistribution'

document.body.onload = function init()
{
    function write(divid, text){
        document.querySelector(divid).innerText = text
    }

    write("#downloadheader",     `Downloaded: ${mergemeta.files} Files, ${mergemeta.rawquestions} Raw-Questions, ${mergemeta.dupquestions} duplicate, ${mergemeta.errquestions} invalid`)
    write("#mergeheader",        `Merged: ${(mergemeta.size/1024/1024).toFixed(0)}MB, ${mergemeta.questions} Valid-Questions, ${mergemeta.tagcount} Tags`)
    plot("#SCOChart",            mergemeta.scodist, "Question Score distribution", 0, true)
    plot("#ANCChart",            mergemeta.ancdist, "Answer Count distribution", 0, true)
    plot("#ISAChart",            mergemeta.isadist, "Is Answered distribution", 0, true)
     
    // Tags
    new TagDistribution({
        parent: document.body,
        name: 'Tag',
        data: mergemeta.tagdist
    })

    // Title
    new TagDistribution({
        parent: document.body,
        name: 'Title plain',
        data: htmlcleanedmeta.titletermdist
    })

    new TagDistribution({
        parent: document.body,
        name: 'Title stemmed',
        data: stemmeta.title_terms
    })

    new TagDistribution({
        parent: document.body,
        name: 'Title lemmed',
        data: lemmmeta.title_terms
    })

    // Body
    new TagDistribution({
        parent: document.body,
        name: 'Body plain',
        data: htmlcleanedmeta.termdist
    })

    new TagDistribution({
        parent: document.body,
        name: 'Body stemmed',
        data: stemmeta.body_terms
    })

    new TagDistribution({
        parent: document.body,
        name: 'Body lemmed',
        data: lemmmeta.body_terms        
    })
}
