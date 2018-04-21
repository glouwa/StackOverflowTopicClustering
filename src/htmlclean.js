const jsdom = require("jsdom")
const { JSDOM } = jsdom;
const fs = require('fs')
const merge = JSON.parse(fs.readFileSync(`./res/merge.json`))
const extract = require('./tools/ttf-extract')

const cleaned = {}
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

for (var qid in merge) {
    cleaned[qid] = clean(merge[qid].body)
    const count = Object.keys(cleaned).length
    if (count % 100 === 1) console.log(count)
    if (count > 5000) break;
}

fs.writeFileSync(`./res/htmlcleaned.json`, JSON.stringify(cleaned, null, 4))
meta.termdist = extract.bodyterm_dist(cleaned)
meta.termcount = Object.keys(meta.termdist).length
const metajson = JSON.stringify(meta)
fs.writeFileSync(`./res/htmlcleaned-meta.json`, metajson)
fs.writeFileSync(`./res/htmlcleaned-meta.js`, 'var htmlcleanedmeta = ' + metajson)


