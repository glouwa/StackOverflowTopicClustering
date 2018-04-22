'use strict'
const fs = require('fs')
const extract = require('./tools/ttf-extract')

const filecount = 1000

const merge = {}
const meta = {
    files: filecount,        
    rawquestions: 0,
    errquestions: 0,
    dupquestions: 0,
    questions: 0,    
    size: '?',  
    tagdist: {},
    tagcount: 0,

    isadist: {},
    isacount: 0,    
    ancdist: {},
    anccount: 0,
    ancmax: 0,
    ancmin: 0,
    scodist: {},
    scocount: 0,
    scomax: 0,
    scomin: 0,
}

for (var i = 1; i < filecount; i++) {    
    const dlstr = fs.readFileSync(`./res/download/${i}.json`)
    const dlobj = JSON.parse(dlstr)
    
    if (dlobj.error_id) 
        meta.errquestions++
        
    else 
        dlobj.items.forEach(q=> {
            meta.rawquestions++   
            if (!merge[q.question_id]) 
                if (q.body.length > 10)
                    merge[q.question_id] = q                    
                else
                    meta.errquestions++
            else
                meta.dupquestions++
        })            
}
const json = JSON.stringify(merge, null, 4)
meta.questions =  Object.keys(merge).length        
meta.size = json.length
fs.writeFileSync(`./dist/merge.json`, json)

meta.tagdist  = extract.tag_tf(merge)
meta.tagcount = Object.keys(meta.tagdist).length
meta.titletermdist  = extract.title_tf(merge)
meta.titletermcount = Object.keys(meta.titletermdist).length
meta.isadist  = extract.isa_dist(merge)
meta.isacount = Object.keys(meta.isadist).length
meta.ancdist  = extract.anc_dist(merge)
meta.anccount = Object.keys(meta.ancdist).length
meta.scodist  = extract.sco_dist(merge)
meta.scocount = Object.keys(meta.scodist).length
const metajson = JSON.stringify(meta, null, 4)
fs.writeFileSync(`./dist/merge-meta.json`, metajson)
fs.writeFileSync(`./dist/merge-meta.js`, 'var mergemeta = ' + metajson)

//console.log(`${meta.filecount} Files, 
//${metaerr_count} Invalid, ${raw_count}, ${meta}`)
/*
    "files": 540,
    "size": 69490361,
    "questions": 15967,
    "tagcount": 8091,



    "files": 540,
    "size": 69490361,
    "rawquestions": 16170,
    "errquestions": 0,
    "questions": 15967,
    "tagcount": 8091,


    "files": 540,
    "size": 69467085,
    "rawquestions": 16170,
    "errquestions": 0,
    "dupquestions": 203,
    "questions": 15967,
    "tagcount": 8091,

    "files": 640,
    "size": 69511211,
    "rawquestions": 18570,
    "errquestions": 20,
    "dupquestions": 2595,
    "questions": 15975,
    "tagcount": 8093,


    Downloaded: 900 Files, 26460 Raw-Questions, 8319 duplicate, 17 invalid
    Merged: 75MB, 18141 Valid-Questions, 8655 Tags
*/