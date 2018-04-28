import { TagCloud } from '../cloud/cloud'
import { BillboardCounter } from '../bb-counter/bb-counter'
import { BillboardTimeline } from '../bb-counter/bb-timeline'
import { HTML } from '../../tools/html'
import { Stats } from '../../model/vecstats'
import { StackOverflowMeta } from '../../model/bag-of-words/base'
import { TagDistribution } from '../tagdistribution/tagdistribution'

const html = `
    <div>
        <div id="downloadheader" class="header"></div>     
        <div id="mergeheader" class="header"></div>    
        <br>        
        <div id="TimeChart"></div>
        <br>        
        <div id="SizeChart"></div>
        <div id="SCOChart" style="width:42%;float:left;"></div>
        <div id="ANCChart" style="width:42%;float:left;"></div>    
        <div id="ISAChart" style="width:16%;float:left;"></div>    
    </div>`

export class StackoverflowDataset
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
            height: 200,
            labels: [],
            numbers: []
        })
        this.datasize = new BillboardCounter({
            parent: document.querySelector("#SizeChart"),         
            height: 80,
            data: [],
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
            parent: document.querySelector("#TimeChart"),         
            height: 200,
            tickcount: 20,
            labels: datasetmeta.index.created
                .map(e=> e.key),
            numbers: datasetmeta.index.created
                .map(e=> Math.log10(e.values.length)), // count of 
        })
        this.datasize.update({
            parent: document.querySelector("#SizeChart"),         
            height: 80,
            data: [],
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