import * as fs from 'fs'
import * as request from 'request'
import { JSDOM } from 'jsdom'
import * as extract from '../tools/ttf-extract'
import { StackOverflowPost } from './bag-of-words/base'
import { StackOverflowMeta } from './bag-of-words/base'

export function download(source, amount) 
{    
    return ((resolve, reject)=> 
    {
        const respath = page=> `./res/${source}/html/${page}.json`
        const resmetapath =    `./res/${source}/meta.json`

        const site = `${source}.com`
        const client_id = '12241'
        const client_secret = 'fARiV63SIlUxr*tpsrFXDw(('
        const client_key = 'iBKWVDJ4ZBz4LF7EvTdLKA(('

        //https://stackexchange.com/oauth/dialog?client_id=12241&scope=no_expiry&redirect_uri=https://stackoverflow.com/oauth/login_success
        const access_token = 'ss7QVLkuuRE6NZ77M(3B(A))'

        //scope: no_expiry
        //redirect_uri: site
        let result = { written:0, err:0 }
        function requestone(page)
        {    
            request({
                url: `https://api.stackexchange.com/2.2/questions?page=${page}&order=desc&sort=activity&site=${source}&filter=!9Z(-wwK0y`,
                gzip: true,
                auth: {
                    'bearer': access_token
                }
            }, 
            (err, res)=> {
                if (!res.body.error_id) {
                    result.written++
                    const formated_body = JSON.stringify(JSON.parse(res.body), null, 4)                 
                    fs.writeFileSync(respath(page), formated_body)
                }
                else {
                    result.err++
                }
        
                if (result.err + result.written === amount - 1) {
                    console.log(`${result.written} OK, ${result.err} failed`)
                    resolve()
                }
            })
        }

        const report = JSON.parse(fs.readFileSync(resmetapath, 'utf8'))    
        var nextfile = report.filecount + amount

        for (var page = report.filecount; page < nextfile; ++page)
            requestone(page)

        const newreport = {
            source: source,
            filecount: nextfile    
        }
        fs.writeFileSync(resmetapath, JSON.stringify(newreport, null, 4))
    })
}

export function convert(source:string)
{    
    return ((resolve, reject)=> {
        const respath = page=> `./res/stackoverflow/html/${page}.json`
        const resmetapath =    `./res/${source}/meta.json`
        const datapath =       `./dist/data/bag-of-texts/${source}.json`
        const datametapath =   `./dist/data/bag-of-texts/${source}-meta.json` 

        const report = JSON.parse(fs.readFileSync(resmetapath, 'utf8'))
        const datasourcemeta = {
            filecount: report.filecount,
            size: 0,
            rawquestions: 0,
            errquestions: 0,
            dupquestions: 0    
        }

        const merge : {[key:string]:StackOverflowPost} = {}
        for (var i = 1; i < datasourcemeta.filecount; i++) {    
            const dlstr = fs.readFileSync(respath(i), 'utf8')
            const dlobj = JSON.parse(dlstr)        
            datasourcemeta.size += dlstr.length

            if (!dlobj.error_id)
                dlobj.items.forEach(q=> {
                    datasourcemeta.rawquestions++   
                    if (!merge[q.question_id]) 
                        if (q.body.length > 10) {
                            const parsed = parse(q.body)
                            merge[q.question_id] = {
                                id: q.question_id,
                                created: new Date(1523544518),
                                size: dlstr.length,
                                isAnswered: q.is_answered,
                                answerCount: q.answer_count,
                                score: q.score,
                                terms: {
                                    tags: q.tags
                                },
                                text:{
                                    title: q.title,
                                    inlinecode: parsed.inlinecode,
                                    body: parsed.body,                            
                                    code: parsed.code,                            
                                }
                            }
                        }
                        else
                            datasourcemeta.errquestions++
                    else
                        datasourcemeta.dupquestions++
                })
            else
                datasourcemeta.errquestions++
        }
        const json = JSON.stringify(merge, null, 4)
        fs.writeFileSync(datapath, json)

        const meta : StackOverflowMeta =  {
            datafile: datapath,
            datafileHash: '',
            datafileSize: json.length,
            datasource: datasourcemeta,
            postcount: Object.keys(merge).length,
            idindex: null,
            timeindex: null,
            sizeindex: null,
            distributions: {
                size:null,
                isAnswered:null,
                answerCount:null,
                score:null,
                terms:{ 
                    tags: null 
                },
                sentences: {},
                texts:{ 
                    title:null,
                    body:null,
                    inlinecode:null,
                    code:null
                }
            }
        }

        const metajson = JSON.stringify(meta, null, 4)
        fs.writeFileSync(datametapath, metajson)
        resolve()
    })
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

const dom = new JSDOM('')    
function parse(html)
{
    dom.window.document.body.innerHTML = html
    dom.window.document.body.querySelectorAll('code').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('pre').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('a').forEach(e=> e.innerHTML = '')    
    return {
        body: splitsentences(dom.window.document.body.textContent),
        code: [],
        inlinecode: []
    }
}

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