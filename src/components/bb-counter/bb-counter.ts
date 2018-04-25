import { bb } from 'billboard.js'

export class BillboardCounter
{
    constructor(args)
    {
        var numbers = args.data.map(e=> e[1])
        var labels = args.data.map(e=> e[0])
        bb.generate({
            size: {
                height: 200,                    
            },
            data: {
                columns: [[args.title].concat(numbers)],
                type: "bar"
            },
            bar: { width: { ratio: 1 }},
            axis: {
                x: {
                    type: "category",
                    categories: labels,                       
                    tick: {
                        //count: small?10:undefined,       
                        fit: true,                     
                        rotate: 90, 
                        multiline: false,
                    }, 
                },
                y: {
                    tick: { count:2, format:x=> x.toFixed(0) },                            
                },
                y2: {
                    label: {
                        text: args.title, 
                        position: "outer-middle"
                    } 
                }
            },
            padding: {    
                left: 70,
                right: 70, 
            },  
            legend: {
                show: false
            }, 
            //zoom: { enabled: true },
            bindto: args.parent
        })  
    }
}

export function plot(divid, data, xlabel, min, small) {
    var entries = Object.entries(data)
    entries = entries.sort((a:any, b:any)=> b[1] - a[1])
    
    //entries = entries.filter(e=> e[1] > min)
    entries = entries.slice(0, 50)

    var numbers = entries.map(e=> e[1])
    var labels = entries.map(e=> e[0])

    var chart = bb.generate({
        size: {
            height: small?120:200,                    
        },
        data: {
            columns: [[xlabel].concat(numbers)],
            type: "bar"
        },
        bar: { width: { ratio: 1 }},
        axis: {
            x: {
                type: "category",
                categories: labels,                       
                tick: {
                    count: small?10:undefined,       
                    fit: true,                     
                    rotate: 90, 
                    multiline: false,
                },
            },
            y: {
                tick: { count:2, format:x=> x.toFixed(0) },                            
            },
            y2: {
                label: {
                    text: xlabel,
                    position: "outer-middle"
                }
            }
        },
        padding: {    
            left: 70,
            right: 70,
        },  
        legend: {
            show: false
        }, 
        //zoom: { enabled: true },
        bindto: divid
    })    
}

