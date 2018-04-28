import { bb } from 'billboard.js'

export class BillboardTimeline
{
    private args

    constructor(args)
    {        
        this.update(args)
    }

    public update(args) {
        this.args = args 
        console.log(args.labels.map(e=> new Date(Number(e))), args.numbers)
        bb.generate({
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
                    ["x"]    .concat(args.labels), //.map(e=> new Date(e))),
                    ["Posts per day"].concat(args.numbers)
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
                        format:x=> Math.pow(10, x).toFixed(0)
                    },
                }                
            }
        })  
    }
}
