"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const billboard_js_1 = require("billboard.js");
class BillboardCounter {
    constructor(args) {
        this.update(args);
    }
    update(args) {
        this.args = args;
        var numbers = this.args.data.map(e => e[1]);
        var labels = this.args.data.map(e => e[0]);
        //console.log('update bb', args, numbers, labels)
        billboard_js_1.bb.generate({
            size: {
                height: this.args.height || 200,
            },
            data: {
                columns: [[this.args.title].concat(numbers)],
                type: "bar"
            },
            bar: { width: { ratio: 1 } },
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
                    tick: { count: 2, format: x => x.toFixed(0) },
                },
                y2: {
                    label: {
                        text: this.args.title,
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
            bindto: this.args.parent
        });
    }
}
exports.BillboardCounter = BillboardCounter;
