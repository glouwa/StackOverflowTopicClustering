import { bb } from 'billboard.js'

export class BillboardTimeline
{
    private args
    private chart

    constructor(args)
    {   
        this.args = args         
        this.chart = bb.generate({
            bindto: this.args.parent,
            size: {
                height: this.args.height,                    
            },
            padding: {    
                left: 70,
                right: 70, 
            },  
            legend: {
                show: false
            }, 
            data: {
                x:"x",
                columns: [
                    ["x"],            
                    ["Posts per day"]
                ]     
            },            
            axis: {
                x: {                    
                    tick: {
                        count: 10,
                        format:x=> new Date(x)
                    }
                },
                y: {                    
                    tick: { 
                        count: 5, 
                        format:x=> Math.pow(10, x).toFixed(0)+'#'
                    },
                }                
            }
        })        
    }

    public update(args) {
        this.chart.load({
            columns: [
                ["x"]            .concat(args.labels), //.map(e=> new Date(e))),
                ["Posts per Day"].concat(args.numbers)
            ] 
        })      
    }
}
