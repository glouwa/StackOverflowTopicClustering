import { bb } from 'billboard.js'

export class BillboardBar
{
    private args
    private chart

    constructor(args)
    {
        this.args = args
        this.chart = bb.generate({
            bindto: this.args.parent,
            padding: {    
                left: 70,
                right: 70, 
            },  
            legend: {
                //show: false
            },             
            size: {
                height: this.args.height||200,                    
            },
            data: {         
                order: "asc",       
                columns: [],
                groups: this.args.groups, 
                //bar: { width: { ratio: .5 }}, 
                color: this.args.color               
            },
            bar: { width: { ratio: .65 }},
            axis: {
                x: {                    
                    label: {
                        text: 'Post size',
                        //position: "outer-center"
                    },
                    tick: {
                        count: this.args.tickcount,
                        //fit: true,                    
                        multiline: false,
                        format: x=> Math.pow(2, x.toFixed(0))-1+'Chars' 
                    }, 
                },
                y: {
                    max: 2100,
                    label: {
                         text: 'Posts',
                         //position: "outer-middle"
                    },                    
                    tick: { 
                        count: 2, 
                        format: x=> x.toFixed(0)+'#' 
                    }
                }
            }            
        })  
    }

    public update(data) {
        console.log(data)
        this.chart.load(data)        
    }
}
