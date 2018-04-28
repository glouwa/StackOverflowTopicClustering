import * as fs from 'fs'
import * as request from 'request'
import { JSDOM } from 'jsdom'
import * as extract from '../tools/ttf-extract'
import { PostId } from './bag-of-words/base'
import { StackOverflowPost } from './bag-of-words/base'
import { StackOverflowMeta } from './bag-of-words/base'
import * as m from './meta'

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
            size: 0,
            hash: '',
            filecount: report.filecount,
            rawquestions: 0,
            errquestions: 0,
            dupquestions: 0    
        }

        const merge : { [key:string]:StackOverflowPost } = {}
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
                                created: new Date(q.creation_date*1000),
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
        console.log("merged and converted")

        function rounddate(din) {
            var d = new Date(din);
            d.setHours(0);
            d.setMinutes(0);
            d.setSeconds(0);
            d.setMilliseconds(0);
            return d
        }
        const meta : StackOverflowMeta =  {
            data:{
                file: datapath,
                hash: '',
                size: json.length,
            },
            datasource: datasourcemeta,
            //size: '??',
            //postcount: Object.keys(merge).length,
            index: {
                id:      m.index<PostId, PostId>(merge, e=> e.id),
                created: m.index<number, PostId>(merge, e=> rounddate(e.created).getTime()),
                sizes: {
                    post:       m.index<number, PostId>(merge, e=> (e.size/1000).toFixed()), 
                    title:      m.index<number, PostId>(merge, e=> (e.text.itle.length).toFixed()), 
                    body:       m.index<number, PostId>(merge, e=> (e.text.body.length/1000).toFixed()), 
                    inlinecode: m.index<number, PostId>(merge, e=> (e.text.inlinecode.length/1000).toFixed()), 
                    code:       m.index<number, PostId>(merge, e=> (e.text.code/1000).toFixed()), 
                }
            },
            distributions: {
                size:        m.distribution(merge, e=> e.size, null),
                isAnswered:  m.distribution(merge, e=> e.isAnswered, null),
                answerCount: m.distribution(merge, e=> e.answerCount, null),
                score:       m.distribution(merge, e=> e.score, null),
                terms:{ 
                    tags:    tag_tf(merge)
                },
                sentences: {},
                texts:{ 
                    title: null,
                    body: null,
                    inlinecode: null,
                    code: null
                }
            }
        }

        const metajson = JSON.stringify(meta, null, 4)
        fs.writeFileSync(datametapath, metajson)
        resolve()
    })
}

export function tag_tf(merge) {
    let result = {}
    for (var qid in merge)             
        merge[qid].terms.tags
            .filter(t=> t !== 'constructor')
            .forEach(tag=> result[tag] = result[tag]+1 || 1)
    return result
}
/*
function splitsentences(text) {
    return text
        .replace('e.g.', '')
        .replace(/(\r\n\t|\n|\r\t)/gm, "")
        .split(/\.|\?|\!/)
        .map(e=> e.trim())
        .filter(s=> s.length > 0)
        .map(e=> e.toLowerCase())    
} */

const dom = new JSDOM('')    
function parse(html)
{
    dom.window.document.body.innerHTML = html
    dom.window.document.body.querySelectorAll('code').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('pre').forEach(e=> e.innerHTML = '')
    dom.window.document.body.querySelectorAll('a').forEach(e=> e.innerHTML = '')    
    return {
        body: dom.window.document.body.textContent,
        code: '',
        inlinecode: ''
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