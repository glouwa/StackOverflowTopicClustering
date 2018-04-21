const jsdom = require("jsdom")
const { JSDOM } = jsdom;
const fs = require('fs')
const extract = require('./tools/ttf-extract')


const merge = JSON.parse(fs.readFileSync(`./res/merge.json`))
const cleaned = JSON.parse(fs.readFileSync(`./res/htmlcleaned.json`))

const meta = {
    termcount: 0,
    termdist: {}
}

function clean(html)
{
    const dom = new JSDOM(html)
    dom.window.document.body.querySelectorAll('code').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('pre').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('a').forEach(e=> e.innerHTML = '')

    const plainline = dom.window.document.body.textContent.replace('e.g.', '').replace(/(\r\n\t|\n|\r\t)/gm, "")
    const sentences = plainline.split(/\.|\?|\!/).filter(s=> s.length > 0)
    return sentences
}

const qids = Object.keys(merge)
const begin = 15000
const batch = qids.slice(begin, begin+5000)

for (var qid of batch) {    
    cleaned[qid] = clean(merge[qid].body)

    const count = Object.keys(cleaned).length    
    if (count % 1000 === 1)
        console.log(count)    
}

const outfile = 'htmlcleaned'
fs.writeFileSync(`./res/${outfile}.json`, JSON.stringify(cleaned, null, 4))
meta.termdist = extract.bodyterm_dist(cleaned)
meta.termcount = Object.keys(meta.termdist).length
const metajson = JSON.stringify(meta)
fs.writeFileSync(`./res/${outfile}-meta.json`, metajson)
fs.writeFileSync(`./res/${outfile}-meta.js`, 'var htmlcleanedmeta = ' + metajson)


