import { TagCloud } from '../cloud/cloud'
import { BillboardCounter } from '../billboardjs/bb-counter'
import { HTML } from '../../tools/html'
import { Stats } from '../../model/vecstats'

const html = `
    <div>
        <div class="header">
            <span class="title"></span>
            <span class="desc"></span>
        </div>    
        <br>                
        <div class="cloud" id="XTTFcloud"></div>
        <div class="right">                      
            <div id="tagdist" class="alphadist"></div>
            <div class="tfcloud"><div id="chardist"></div></div>                        
            <div class="tfcloud2"><div id="textsize"></div></div>            
            <div class="tfcloud2"><div id="sentencecount"></div></div>            
            <!--<div class="tfcloud"><div id="sentencesize"></div></div>-->
        </div>
    </div>`

export class TagDistribution
{
    private args
    private stats
    private view : HTMLElement
    private bb
    private tc

    constructor(args)
    {   
        this.view = HTML.parse(html)()
        args.parent.appendChild(this.view)
     
        this.update(args)
    }

    public update(args) {
        this.args = args

        if (!this.args.data) return
        const keyvaluepairs = this.convert(this.args.data.key)
          
        this.stats = new Stats(keyvaluepairs.map(e=> e[1]))
        this.view.querySelector<HTMLElement>(".header > .title").innerText = args.name
        this.view.querySelector<HTMLElement>(".header > .desc").innerText = this.stats
        
        this.bb = new BillboardCounter({
            parent: this.view.querySelector("#tagdist"), 
            data: keyvaluepairs.slice(0, 120),
            title: "Tag frequency" 
        })

        this.bb = new BillboardCounter({
            parent: this.view.querySelector("#chardist"), 
            data: this.convert(this.args.data.chars).slice(0, 60),
            title: "Char frequency",
            height: 100,
        })

        this.bb = new BillboardCounter({
            parent: this.view.querySelector("#textsize"), 
            data: Object.entries(this.args.data.sentencecount).slice(0, 100),
            title: "Sentence count frequency",
            height: 100,
            tickcount: 20,
        })

        this.bb = new BillboardCounter({
            parent: this.view.querySelector("#sentencecount"), 
            data: Object.entries(this.args.data.sentencelength).slice(0, 100),
            title: "Sentence length frequency",
            height: 100,
            tickcount: 20,
        })

        this.tc = new TagCloud({ 
            parent: this.view.querySelector('#XTTFcloud'),
            words: keyvaluepairs
                .slice(0, 120)
                .map((e:any)=> ({ text:e[0], size:9+e[1]/this.stats.max*23 }))
        })
    }

    private convert(d) {
        return Object.entries(d)
            .sort((a:any, b:any)=> b[1] - a[1])
    }
}