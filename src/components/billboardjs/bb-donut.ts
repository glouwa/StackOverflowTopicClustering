import { bb } from 'billboard.js'

export class BillboardDonut
{
    private args
    private chart

    constructor(args) 
    {
        this.args = args
        this.chart = bb.generate({
            bindto: this.args.parent,
            padding: {    
                left: 0,
                right: 0, 
            },                        
            legend: {
                show: false
            },             
            size: {
                height: this.args.height||200,                    
            },
            data: {         
                columns: [],
                type: "donut",
            },
        })
    }

    public update(data) {
        console.log(data)
        this.chart.load(data)        
    }
}
