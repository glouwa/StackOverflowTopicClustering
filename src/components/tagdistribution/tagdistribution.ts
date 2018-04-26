import { TagCloud } from '../cloud/cloud'
import { BillboardCounter } from '../bb-counter/bb-counter'
import { HTML } from '../../tools/html'
import { Stats } from '../../model/vecstats'

const html = `
    <div>
        <div class="header">
            <span class="title"></span>
            <span class="desc"></span>
        </div>    
        <br>
        <div>          
            <div class="tfcloud"><div id="XTTFChart"></div></div>
            <div class="cloud" id="XTTFcloud"></div>
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

        const keyvaluepairs = Object.entries(this.args.data)
            .sort((a:any, b:any)=> b[1] - a[1])

        const keyvector = keyvaluepairs.map(e=> e[0])
        const valuevector = keyvaluepairs.map(e=> e[1])        

        this.stats = new Stats(valuevector)

        this.view.querySelector<HTMLElement>(".header > .title").innerText = args.name
        this.view.querySelector<HTMLElement>(".header > .desc").innerText = this.stats
        
        this.bb = new BillboardCounter({
            parent: this.view.querySelector("#XTTFChart"), 
            data: keyvaluepairs.slice(0, 100),
            title: "Tag frequency" 
        })
        
        this.tc = new TagCloud({ 
            parent: this.view.querySelector('#XTTFcloud'),
            words: keyvaluepairs
                .slice(0, 75)
                .map((e:any)=> ({ text:e[0], size:9+e[1]/this.stats.max*23 }))
        })
    }
}