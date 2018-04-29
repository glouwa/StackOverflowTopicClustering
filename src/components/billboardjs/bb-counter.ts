import { bb } from 'billboard.js'
import * as d3 from 'd3'

export class BillboardCounter
{
    private args
    private chart

    constructor(args)
    {        
        this.update(args)
    }

    public update(args) {
        this.args = args
        
        var numbers = this.args.data.map(e=> e[1])
        var labels = this.args.data.map(e=> e[0])
        console.log('update bb', args, numbers, labels)
        this.chart = bb.generate({
            bindto: this.args.parent,
            padding: {    
                left: 70,
                right: 70, 
            },  
            legend: {
                show: false
            },             
            size: {
                height: this.args.height||200,                    
            },
            data: {
                type: "bar",
                bar: { width: { ratio: .1 }},
                //bar: { padding:.01 },
                columns: [
                    [this.args.title].concat(numbers)
                ],                
                color: function (color, d) {                    
                    return (d.x == '0' || d.x == '0') 
                        ? d3.schemeCategory10[3] 
                        : d3.schemeCategory10[2]
                }
            },
            bar: { width: { ratio: .8 }},
            axis: {
                x: {
                    type: "category", 
                    categories: labels,                       
                    tick: {
                        count: this.args.tickcount,
                        //fit: true,                     
                        rotate: 90, 
                        multiline: false,
                    }, 
                },
                y: {
                    //center: 0,
                    tick: { 
                        count:2, 
                        format:x=> x.toFixed(0)+'#' 
                    }
                }
            }            
        })  
    }
}