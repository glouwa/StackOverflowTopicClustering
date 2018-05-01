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

function convert_(source:string)
{
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
                                tags: [q.tags]
                            },
                            text:{
                                title: parse(q.title).body,
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

    const jsonmeta = JSON.stringify(datasourcemeta, null, 4)
    fs.writeFileSync(datametapath, jsonmeta)

    console.log("merged and converted")
}

function stats_(source:string, tokenformat:string)
{   
    const inputtextspath = `./dist/data/bag-of-texts/${source}.json`
    const inputmetapath =  `./dist/data/bag-of-texts/${source}-meta.json`    
    const inputwordspath = `./dist/data/bag-of-words/${source}-${tokenformat}.json`    
    const datametapath =   `./dist/data/bag-of-words/${source}-${tokenformat}-meta.json` 

    const datasourcemeta = JSON.parse(fs.readFileSync(inputmetapath, 'utf8'))
    const merge = JSON.parse(fs.readFileSync(inputtextspath, 'utf8'))
    const words = JSON.parse(fs.readFileSync(inputwordspath, 'utf8'))
    
    const meta : StackOverflowMeta =  {
        data:{
            file: inputwordspath,
            hash: '',
            size: 12345,
        },
        datasource: datasourcemeta,
        //size: '??',
        //postcount: Object.keys(merge).length,
        index: {
            id:             m.index<PostId, PostId>(merge, e=> e.id),
            created:        m.index<number, PostId>(merge, e=> rounddate(e.created).getTime()),
            sizes: {
                post:       m.index<number, PostId>(merge, e=> Math.log2(1+e.size).toFixed(1)), 
                title:      m.index<number, PostId>(merge, e=> Math.log2(1+e.text.title.reduce((a, s)=> s.length, 0)).toFixed(1)), 
                inlinecode: m.index<number, PostId>(merge, e=> Math.log2(1+e.text.inlinecode.reduce((a, s)=> s.length, 0)).toFixed(1)), 
                body:       m.index<number, PostId>(merge, e=> Math.log2(1+e.text.body.reduce((a, s)=> s.length, 0)).toFixed(1)),                     
                code:       m.index<number, PostId>(merge, e=> Math.log2(1+e.text.code.reduce((a, s)=> s.length, 0)).toFixed(1)), 
            }
        },
        distributions: {
            size:           m.distribution(merge, e=> e.size, null),
            isAnswered:     m.distribution(merge, e=> e.isAnswered, null),
            answerCount:    m.distribution(merge, e=> e.answerCount, null),
            score:          m.distribution(merge, e=> e.score, null),
            terms:{ 
                tags:       bla(words, q=> q.terms.tags),
                title:      bla(words, q=> q.terms.title),
                body:       bla(words, q=> q.terms.body),
                inlinecode: bla(words, q=> q.terms.inlinecode),
                code:       bla(words, q=> q.terms.code),
            },            
            texts:{
                title:      null,
                body:       null,
                inlinecode: null,
                code:       null
            }
        }
    }

    const metajson = JSON.stringify(meta, null, 4)
    fs.writeFileSync(datametapath, metajson)
}

export function convert(source:string)
{    
    return ((resolve, reject)=> {
        convert_(source)
        stats_(source, 'raw')
        stats_(source, 'stem')
        stats_(source, 'lemma')
        resolve()
    })
}

function bla(merge, who) {
    return {
        key: tag_tf(merge, who, term=> term),
        //size: tag_tf(merge, who, t=> t.length),
        chars: char_tf(merge, who),
        sentencecount: sent_tf(merge, who, sent=> sent.length),
        sentencelength: sent_tf(merge, who, sent=> sent.reduce((a, s)=> a+=s.length, 0)),
    }
}

export function sent_tf(merge, who, t) {
    let result = {}
    for (var qid in merge)             
        who(merge[qid])
            .filter(sent=> sent !== 'constructor')
            .forEach(sent=> result[t(sent)] = result[t(sent)]+1 || 1)                
    return result
}

export function tag_tf(merge, who, t) {
    let result = {}
    for (var qid in merge)             
        who(merge[qid])
            .filter(sent=> sent !== 'constructor')
            .forEach(sent=> sent
                .filter(term=> term !== 'constructor')
                .forEach(term=> result[t(term)] = result[t(term)]+1 || 1))
    return result
}

export function char_tf(merge, who) {
    let result = {}
    for (var qid in merge)             
        who(merge[qid])
            .filter(sent=> sent !== 'constructor')
            .forEach(sent=> sent
                .filter(term=> term !== 'constructor')
                .forEach(term=> term
                    .split('')
                    .forEach(char=> result[char] = result[char]+1 || 1)))
    return result
}

function rounddate(din) {
    var d = new Date(din);
    //d.setDate(1)
    d.setHours(0)
    d.setMinutes(0)
    d.setSeconds(0)
    d.setMilliseconds(0)
    return d
}

const dom = new JSDOM('')    
function parse(html)
{
    dom.window.document.body.innerHTML = html

    const result = {
        body: [],
        code: [],
        inlinecode: []
    }
    dom.window.document.body.querySelectorAll('pre').forEach(e=> {
        result.code.push(e.textContent) 
        e.innerHTML = ''
    })
    dom.window.document.body.querySelectorAll('code').forEach(e=> {
         result.inlinecode.push(e.textContent) 
         e.innerHTML = ''
    })
    
    dom.window.document.body.querySelectorAll('a').forEach(e=> e.innerHTML = '')    

    result.body = [dom.window.document.body.textContent]
    return result
}
