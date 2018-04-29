import * as d3 from 'd3'
import { TagCloud } from '../cloud/cloud'
import { BillboardCounter } from '../billboardjs/bb-counter'
import { BillboardBar } from '../billboardjs/bb-bar'
import { BillboardTimeline } from '../billboardjs/bb-timeline'
import { HTML } from '../../tools/html'
import { Stats } from '../../model/vecstats'
import { StackOverflowMeta } from '../../model/bag-of-words/base'
import { TagDistribution } from '../tagdistribution/tagdistribution'

const html = `
    <div>
        <div id="downloadheader" class="header">Stackoverflow</div>     
        <div id="mergeheader" class="header">Merged</div>    
        <br>        
        <div id="TimeChart"></div>
        <br><br>                
        <div id="SCOChart" style="width:42%;float:left;"></div>
        <div id="ANCChart" style="width:42%;float:left;"></div>    
        <div id="ISAChart" style="width:16%;float:left;"></div>
        <br><br>        
        <div id="SizeChart"></div>        
    </div>`

export class StackoverflowDatasetView
{
    private args    
    private view : HTMLElement
    private timeline
    private datasize
    private scores
    private ansercount 
    private isanswered
    private tags
    
    constructor(args)
    {   
        this.view = HTML.parse(html)()
        args.parent.appendChild(this.view)
        this.args = args
     
        this.timeline = new BillboardTimeline({
            parent: document.querySelector("#TimeChart"),         
            height: 140,
        })
        this.datasize = new BillboardBar({
            parent: document.querySelector("#SizeChart"),   
            title: 'Post Size',      
            tickcount: 20,
            height: 140,
            groups: [[ "Body size", "Title size", "Inline code size", "Code size" ]],
        })

        this.scores = new BillboardBar({
            parent: document.querySelector("#SCOChart"),         
            height: 120,  
            tickcount: 10,   
            color: function (color, d) {                
                if (d.x < 0) return  d3.schemeCategory10[3] 
                if (d.x > 0) return  d3.schemeCategory10[2] 
                return color
            }       
        })
    
        this.ansercount = new BillboardCounter({
            parent: document.querySelector("#ANCChart"),         
            height: 120,
            data: [],
        })
    
        this.isanswered = new BillboardCounter({
            parent: document.querySelector("#ISAChart"),         
            height: 120,
            data: [],
        })
    
        this.tags = new TagDistribution({
            parent: document.body,
            name: 'Tag',
            data: {},
        })
    }

    public update(datasetmeta:StackOverflowMeta) {
        document.querySelector<HTMLElement>("#downloadheader").innerText = 
            `Stackoverflow: ${(datasetmeta.datasource.size/1024/1024).toFixed(0)}MB, ${datasetmeta.datasource.filecount} Files, ${datasetmeta.datasource.rawquestions} Raw-Questions, ${datasetmeta.datasource.dupquestions} duplicate, ${datasetmeta.datasource.errquestions} invalid`
        document.querySelector<HTMLElement>("#mergeheader").innerText = 
            `Merged: ${(datasetmeta.data.size/1024/1024).toFixed(0)}MB, ${datasetmeta.index.id.length} Valid-Questions,` // ${mergemeta.tagcount} Tags`        

        this.timeline.update({
            labels: datasetmeta.index.created
                .map(e=> e.key),
            numbers: datasetmeta.index.created
                .map(e=> Math.log10(e.values.length)), // count of posts
        })

        const s = datasetmeta.index.sizes
        this.datasize.update({           
            type: "bar",
            xs: {                
                'Title size':       'x1',
                'Body size':        'x2',
                'Inline code size': 'x3', 
                'Code size':        'x4',                
            },
            order: "asc",
            columns: [
                ['x1']              .concat(s.title.map(e=> e.key)),                
                ['x2']              .concat(s.body.map(e=> e.key)),                
                ['x3']              .concat(s.inlinecode.map(e=> e.key)),                
                ['x4']              .concat(s.code.map(e=> e.key)),
                ['Inline code size'].concat(s.inlinecode.map(e=> e.values.length)),
                ['Title size']      .concat(s.title.map(e=> e.values.length)),
                ['Body size']       .concat(s.body.map(e=> e.values.length)),                
                ['Code size']       .concat(s.code.map(e=> e.values.length)),
            ],            
        })

        this.scores.update({           
            type: "bar",
            xs: {                
                '#Posts':       'x1',                
            },
            columns: [
                ['x1']              .concat(Object.entries(datasetmeta.distributions.score)
                    .sort((a:any, b:any)=> a[0] - b[0])
                    .slice(0, 35)
                    .map(e=> e[0])),                
                
                ['#Posts'].concat(Object.entries(datasetmeta.distributions.score)
                    .sort((a:any, b:any)=> a[0] - b[0])
                    .slice(0, 35)
                    .map(e=> e[1])),
            ],
            
        })

        /*this.scores.update({            
            data: Object.entries(datasetmeta.distributions.score)
                .sort((a:any, b:any)=> a[0] - b[0])
                .slice(0, 35),        
        })*/
        this.ansercount.update({
            parent: document.querySelector("#ANCChart"),         
            height: 120,
            data: Object.entries(datasetmeta.distributions.answerCount)
                .sort((a:any, b:any)=> a[0] - b[0]),        
        })
        this.isanswered.update({
            parent: document.querySelector("#ISAChart"),         
            height: 120,
            data: Object.entries(datasetmeta.distributions.isAnswered)
                .sort((a:any, b:any)=> b[1] - a[1]),        
        })
        this.tags.update({
            parent: document.body,
            name: 'Tag',
            data: datasetmeta.distributions.terms.tags,        
        })        
    }
}