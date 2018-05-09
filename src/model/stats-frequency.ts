import * as fs from 'fs'
import { PostId } from '../model/model'
import { StackOverflowPost } from '../model/model'
import { StackOverflowMeta } from '../model/model'
import * as m from '../model/stats-index'

export function calc(source:string)
{    
    return ((resolve, reject)=> {        
        stats_(source, 'bag-of-words', 'raw')
        stats_(source, 'bag-of-words', 'stem')
        stats_(source, 'bag-of-words', 'lemma')
        stats_(source, 'ngrams', '2gram-stem')
        stats_(source, 'ngrams', '3gram-stem')
        resolve()
    })
}

function stats_(source:string, folder:string, tokenformat:string)
{   
    const inputtextspath = `./dist/data/bag-of-texts/${source}.json`
    const inputmetapath =  `./dist/data/bag-of-texts/${source}-meta.json`    
    const inputwordspath = `./dist/data/${folder}/${source}-${tokenformat}.json`    
    const datametapath =   `./dist/data/${folder}/${source}-${tokenformat}-meta.json` 

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
    console.log(`${folder} ${tokenformat} done`)
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

export function bla(merge, who) {
    return {
        key: tag_tf(merge, who, term=> term),
        //size: tag_tf(merge, who, t=> t.length),
        chars: char_tf(merge, who),
        sentencecount: sent_tf(merge, who, sent=> sent.length),
        sentencelength: sent_tf(merge, who, sent=> sent.reduce((a, s)=> a+=s.length, 0)),
    }
}

const minoccurrences = 3

export function sent_tf(merge, who, t) {
    let result = {}
    for (var qid in merge)             
        who(merge[qid])
            .filter(sent=> sent !== 'constructor')
            .forEach(sent=> result[t(sent)] = result[t(sent)]+1 || 1)                
    for (var key in result) 
            if (result[key] < minoccurrences) delete result[key]
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
    for (var key in result) 
        if (result[key] < minoccurrences) delete result[key]
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
    for (var key in result) 
        if (result[key] < minoccurrences) delete result[key]
    return result
}
