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
        <br>                
        <div id="SCOChart" style="width:44%;float:left;"></div>
        <div id="ANCChart" style="width:44%;float:left;"></div>    
        <div id="ISAChart" style="width:12%;float:left;"></div>
        <br>        
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
            height: 150,
        })
        this.datasize = new BillboardBar({
            parent: document.querySelector("#SizeChart"),   
            title: 'Post Size',      
            height: 120,
            labels: [],
            numbers: []
        })

        this.scores = new BillboardCounter({
            parent: document.querySelector("#SCOChart"),         
            height: 120,
            //tickcount: 20,
            data: [],
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
        this.datasize.update({
            parent: document.querySelector("#SizeChart"),         
            height: 120,
            tickcount: 10,
            labels: datasetmeta.index.sizes.post
                .map(e=> e.key),
            numbers: datasetmeta.index.sizes.post
                .map(e=> e.values.length), // count of posts
        })

        this.scores.update({
            parent: document.querySelector("#SCOChart"),         
            height: 120,
            tickcount: 20,
            data: Object.entries(datasetmeta.distributions.score)
                .sort((a:any, b:any)=> a[0] - b[0])
                .slice(0, 35),        
        })
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