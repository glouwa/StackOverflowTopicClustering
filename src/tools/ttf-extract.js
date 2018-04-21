'use strict'
const fs = require('fs')

exports.tag_tf = function tag_tf(merge) {
    let result = {}
    for (var qid in merge)             
        merge[qid].tags
            .filter(t=> t !== 'constructor')
            .forEach(tag=> result[tag] = result[tag]+1 || 1)
    //fs.writeFileSync(`./res/ttf.js`, 'var ttf='+JSON.stringify(result, null, 4))
    return result
}

exports.anc_dist = function anc_dist(merge) {
    let result = {}
    for (var qid in merge) 
        result[merge[qid].answer_count] = result[merge[qid].answer_count ]+1 || 1            
    //fs.writeFileSync(`./res/anc.js`, 'var anc='+JSON.stringify(result, null, 4))
    return result
}

exports.isa_dist = function isa_dist(merge) {
    let result = {}
    for (var qid in merge) 
        result[merge[qid].is_answered] = result[merge[qid].is_answered]+1 || 1
    //fs.writeFileSync(`./res/isa.js`, 'var isa='+JSON.stringify(result, null, 4))
    return result
}

exports.sco_dist = function sco_dist(merge) {
    let result = {}
    for (var qid in merge)         
        result[merge[qid].score] = result[merge[qid].score]+1 || 1    
    
    //sort---
    return result
}

exports.bodyterm_dist = function bodyterm_dist(merge) {
    let result = {}
    for (var qid in merge)             
        merge[qid]            
            .forEach(sentence=> {
                const terms = sentence.split(' ')
                terms.forEach(t=> {
                    if(t.length > 5) 
                        result[t] = result[t]+1 || 1
                })                
            })
    
    return result
}