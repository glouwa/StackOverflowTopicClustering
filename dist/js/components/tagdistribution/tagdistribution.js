"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cloud_1 = require("../cloud/cloud");
const bb_counter_1 = require("../bb-counter/bb-counter");
const html_1 = require("../../tools/html");
const vecstats_1 = require("../../model/vecstats");
const html = `
    <div>
        <div class="header">
            <span class="title"></span>
            <span class="desc"></span>
        </div>    
        <br>
        <div>          
            <div class="tfcloud"><div id="XTTFChart"></div></div>
            <div class="cloud" id="XTTFcloud"></div>
        </div>
    </div>`;
class TagDistribution {
    constructor(args) {
        this.args = args;
        const keyvaluepairs = Object.entries(this.args.data)
            .sort((a, b) => b[1] - a[1]);
        const keyvector = keyvaluepairs.map(e => e[0]);
        const valuevector = keyvaluepairs.map(e => e[1]);
        this.stats = new vecstats_1.Stats(valuevector);
        const view = html_1.HTML.parse(html)();
        args.parent.appendChild(view);
        view.querySelector(".header > .title").innerText = args.name;
        view.querySelector(".header > .desc").innerText = this.stats;
        new bb_counter_1.BillboardCounter({
            parent: view.querySelector("#XTTFChart"),
            data: keyvaluepairs.slice(0, 100),
            title: "Tag frequency"
        });
        new cloud_1.TagCloud({
            parent: view.querySelector('#XTTFcloud'),
            words: keyvaluepairs
                .slice(0, 75)
                .map(e => ({ text: e[0], size: 9 + e[1] / this.stats.max * 20 }))
        });
    }
}
exports.TagDistribution = TagDistribution;
