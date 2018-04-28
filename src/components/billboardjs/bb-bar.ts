import { bb } from 'billboard.js'

export class BillboardBar
{
    private args
    private chart

    constructor(args)
    {        
        this.update(args)
    }

    public update(args) {
        this.args = args
        
        var numbers = this.args.numbers
        var labels = this.args.labels
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
                columns: [
                    ['data1'].concat(numbers),
                    ['data2'].concat(numbers)
                ],             
                type: "bar",
                groups: [
                    [ "data1", "data2" ]
                ]
            },
            bar: { width: { ratio: .8 }},
            axis: {
                x: {
                    type: "category", 
                    categories: labels,                       
                    tick: {
                        count: this.args.tickcount,
                        fit: true,                     
                        //rotate: 90, 
                        multiline: false,
                        format: x=> x.toFixed(0)+'KB' 
                    }, 
                },
                y: {
                    //center: 0,
                    tick: { 
                        count: 2, 
                        format: x=> x.toFixed(0)+'#' 
                    }
                }
            }            
        })  
    }
}
