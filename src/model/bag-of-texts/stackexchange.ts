import * as fs from 'fs'
import * as request from 'request'
import { JSDOM } from 'jsdom'
import { PostId } from '../model'
import { StackOverflowPost } from '../model'
import { StackOverflowMeta } from '../model'
import { counts } from '../stats-frequency'

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


export function parseAndMerge(source:string)
{    
    return ((resolve, reject)=> {
        convert_(source)       
        resolve()
    })
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
