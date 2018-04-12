'use strict'
const fs = require('fs')

const mergestr = fs.readFileSync(`./res/merge.json`)
const mergeobj = JSON.parse(mergestr)

const ttf = {}
const anc = {}
const isa = {}
const sco = {}

for (var qid in mergeobj) {
    const q = mergeobj[qid]
    q.tags.forEach(tag=> ttf[tag] = ttf[tag]+1 || 1)

    anc[q.answer_count] = anc[q.answer_count ]+1 || 1
    isa[q.is_answered] = isa[q.is_answered]+1 || 1
    sco[q.score] = sco[q.score]+1 || 1
}

fs.writeFileSync(`./res/ttf.js`, 'var ttf='+JSON.stringify(ttf, null, 4))
fs.writeFileSync(`./res/anc.js`, 'var anc='+JSON.stringify(anc, null, 4))
fs.writeFileSync(`./res/isa.js`, 'var isa='+JSON.stringify(isa, null, 4))
fs.writeFileSync(`./res/sco.js`, 'var sco='+JSON.stringify(sco, null, 4))

