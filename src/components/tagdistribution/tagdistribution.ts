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

    constructor(args)
    {   
        this.args = args
         
        const keyvaluepairs = Object.entries(this.args.data)
            .sort((a:any, b:any)=> b[1] - a[1])

        const keyvector = keyvaluepairs.map(e=> e[0])
        const valuevector = keyvaluepairs.map(e=> e[1])        

        this.stats = new Stats(valuevector)

        const view = HTML.parse(html)()
        args.parent.appendChild(view)
        
        view.querySelector(".header > .title").innerText = args.name
        view.querySelector(".header > .desc").innerText = this.stats

        new BillboardCounter({
            parent: view.querySelector("#XTTFChart"), 
            data: keyvaluepairs.slice(0, 100)
            title: "Tag frequency" 
        })
        
        new TagCloud({ 
            parent: view.querySelector('#XTTFcloud'),
            words: keyvaluepairs
                .slice(0, 75)
                .map(e=> ({ text:e[0], size:9+e[1]/this.stats.max*20 }))
        })
    }
}