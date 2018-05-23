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
                left: 45,
                right: 10, 
            },  
            legend: {
                show: false
            }, 
            data: {
                x:"x",
                type: "bar",
                //point: false,
                columns: [
                    ["x"],            
                    ["Posts per day"]
                ]     
            },            
            axis: {                
                x: {                    
                    label: 'Time',
                    tick: {
                        count: 10,
                        format:x=> new Date(x)
                    }
                },
                y: {              
                    label: '#Posts',      
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
