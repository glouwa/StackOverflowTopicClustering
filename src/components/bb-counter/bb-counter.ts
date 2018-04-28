import { bb } from 'billboard.js'

export class BillboardCounter
{
    private args

    constructor(args)
    {        
        this.update(args)
    }

    public update(args) {
        this.args = args
        
        var numbers = this.args.data.map(e=> e[1])
        var labels = this.args.data.map(e=> e[0])
        //console.log('update bb', args, numbers, labels)
        bb.generate({
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
                columns: [[this.args.title].concat(numbers)],
                type: "bar"
            },
            bar: { width: { ratio: 1 }},
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
                    tick: { count:2, format:x=> x.toFixed(0) },                            
                }
            }            
        })  
    }
}
