//import * as d3 from 'd3'
import { bb } from 'billboard.js'

document.body.onload = function init()
{
    function write(divid, text){
        document.querySelector(divid).innerText = text
    }

    write("#downloadheader",     `Downloaded: ${mergemeta.files} Files, ${mergemeta.rawquestions} Raw-Questions, ${mergemeta.dupquestions} duplicate, ${mergemeta.errquestions} invalid`)
    write("#mergeheader",        `Merged: ${(mergemeta.size/1024/1024).toFixed(0)}MB, ${mergemeta.questions} Valid-Questions, ${mergemeta.tagcount} Tags`)
    plot("#SCOChart",            mergemeta.scodist, "Question Score distribution", 0, true)
    plot("#ANCChart",            mergemeta.ancdist, "Answer Count distribution", 0, true)
    plot("#ISAChart",            mergemeta.isadist, "Is Answered distribution", 0, true)
    plot("#TTFChart",            mergemeta.tagdist, "Tag frequency", 50)

    write("#t-cleanedheader",    `Title Cleaned: ${htmlcleanedmeta.titletermcount} Terms`)
    write("#t-stemmedheader",    `Title Stemmed: ${Object.keys(stemmeta.title_terms).length} stemmed Terms`)
    write("#t-lemmatizedheader", `Title Lemmatized: ${Object.keys(lemmmeta.title_terms).length} lemmed Terms`)
    plot("#T-TFChart",            htmlcleanedmeta.titletermdist, "Title Term frequency (cleaned)", 100)
    plot("#T-STFChart",           stemmeta.title_terms, "Title Term frequency (stemmed)", 200)
    plot("#T-LTFChart",           lemmmeta.title_terms, "Title Term frequency (lemmed)", 200)

    write("#b-cleanedheader",    `Body Cleaned: ${htmlcleanedmeta.termcount} Terms`)
    write("#b-stemmedheader",    `Body Stemmed: ${Object.keys(stemmeta.body_terms).length} stemmed Terms`)
    write("#b-lemmatizedheader", `Body Lemmatized: ${Object.keys(lemmmeta.body_terms).length} lemmed Terms`)
    plot("#BTFChart",            htmlcleanedmeta.termdist, "Body terms frequency (cleaned)", 800)        
    plot("#STFChart",            stemmeta.body_terms, "Body terms frequency (stemmed)", 1200)        
    plot("#LTFChart",            lemmmeta.body_terms, "Body terms frequency (lemmed)", 1200)
}

export function plot(divid, data, xlabel, min, small) {
    var entries = Object.entries(data)
    entries = entries.sort((a:any, b:any)=> b[1] - a[1])
    
    //entries = entries.filter(e=> e[1] > min)
    entries = entries.slice(0, 100)

    var numbers = entries.map(e=> e[1])
    var labels = entries.map(e=> e[0])

    var chart = bb.generate({
        size: {
            height: small?120:200,                    
        },
        data: {
            columns: [[xlabel].concat(numbers)],
            type: "bar"
        },
        bar: { width: { ratio: 1 }},
        axis: {
            x: {
                type: "category",
                categories: labels,                       
                tick: {
                    count: small?10:undefined,       
                    fit: true,                     
                    rotate: 90, 
                    multiline: false,
                },
            },
            y: {
                tick: { count:2, format:x=> x.toFixed(0) },                            
            },
            y2: {
                label: {
                    text: xlabel,
                    position: "outer-middle"
                }
            }
        },
        padding: {    
            left: 70,
            right: 70,
        },  
        legend: {
            show: false
        }, 
        //zoom: { enabled: true },
        bindto: divid
    })
}

