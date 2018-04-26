import { JSDOM } from 'jsdom'
import * as fs from 'fs'
import * as extract from './tools/ttf-extract'


const merge = JSON.parse(fs.readFileSync(`./dist/merge.json`))
const cleaned = fs.existsSync(`./dist/htmlcleaned.json`) 
    ? JSON.parse(fs.readFileSync(`./dist/htmlcleaned.json`))
    : {}

const meta = {
    termcount: 0,
    termdist: {}
} 

function splitsentences(text) {
    return text
        .replace('e.g.', '')
        .replace(/(\r\n\t|\n|\r\t)/gm, "")
        .split(/\.|\?|\!/)
        .map(e=> e.trim())
        .filter(s=> s.length > 0)
        .map(e=> e.toLowerCase())    
} 

function clean(html)
{
    const dom = new JSDOM(html)
    dom.window.document.body.querySelectorAll('code').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('pre').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('a').forEach(e=> e.innerHTML = '')    
    return splitsentences(dom.window.document.body.textContent)
}

const qids = Object.keys(merge)
const begin = 15000
const batch = qids.slice(begin, begin+5000)

for (var qid of batch) {  
    cleaned[qid] = {
        title: splitsentences(merge[qid].title),
        body: clean(merge[qid].body)
    }
}

const outfile = 'htmlcleaned'
fs.writeFileSync(`./dist/${outfile}.json`, JSON.stringify(cleaned, null, 4))
meta.termdist = extract.bodyterm_dist(cleaned)
meta.termcount = Object.keys(meta.termdist).length
meta.titletermdist = extract.titleterm_dist(cleaned)
meta.titletermcount = Object.keys(meta.titletermdist).length
const metajson = JSON.stringify(meta, null, 4)
fs.writeFileSync(`./dist/${outfile}-meta.json`, metajson)
fs.writeFileSync(`./dist/${outfile}-meta.js`, 'var htmlcleanedmeta = ' + metajson)


