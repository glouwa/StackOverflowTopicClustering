"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const cloud_1 = require("../cloud/cloud");
const bb_counter_1 = require("../billboardjs/bb-counter");
const tools_1 = require("../../visualisations/tools");
const stats_vector_1 = require("../../model/stats-vector");
const html = `
    <div>
        <div class="header">
            <span class="title"></span>
            <span class="desc"></span>
        </div>    
        <br>                
        <div class="cloud" id="XTTFcloud"></div>
        <div class="right">                      
            <div id="tagdist" class="alphadist"></div>
            <div class="tfcloud"><div id="chardist"></div></div>                        
            <div class="tfcloud2"><div id="textsize"></div></div>            
            <div class="tfcloud2"><div id="sentencecount"></div></div>            
            <!--<div class="tfcloud"><div id="sentencesize"></div></div>-->
        </div>
    </div>`;
class TagDistribution {
    constructor(args) {
        this.view = tools_1.HTML.parse(html)();
        args.parent.appendChild(this.view);
        this.update(args);
    }
    update(args) {
        this.args = args;
        if (!this.args.data)
            return;
        const keyvaluepairs = this.convert(this.args.data.key);
        this.stats = new stats_vector_1.Stats(keyvaluepairs.map(e => e[1]));
        this.view.querySelector(".header > .title").innerText = args.name;
        this.view.querySelector(".header > .desc").innerText = this.stats;
        this.bb = new bb_counter_1.BillboardCounter({
            parent: this.view.querySelector("#tagdist"),
            data: keyvaluepairs.slice(0, 120),
            title: "Tag frequency"
        });
        this.bb = new bb_counter_1.BillboardCounter({
            parent: this.view.querySelector("#chardist"),
            data: this.convert(this.args.data.chars).slice(0, 60),
            title: "Char frequency",
            height: 100,
        });
        this.bb = new bb_counter_1.BillboardCounter({
            parent: this.view.querySelector("#textsize"),
            data: Object.entries(this.args.data.sentencecount).slice(0, 100),
            title: "Sentence count frequency",
            height: 100,
            tickcount: 20,
        });
        this.bb = new bb_counter_1.BillboardCounter({
            parent: this.view.querySelector("#sentencecount"),
            data: Object.entries(this.args.data.sentencelength).slice(0, 100),
            title: "Sentence length frequency",
            height: 100,
            tickcount: 20,
        });
        const tagclouddata = keyvaluepairs.slice(0, 150);
        const min = tagclouddata[tagclouddata.length - 1][1];
        this.tc = new cloud_1.TagCloud({
            parent: this.view.querySelector('#XTTFcloud'),
            words: tagclouddata
                .map((e) => ({ text: e[0], size: 9 + (e[1] - min) / (this.stats.max - min) * 23 }))
        });
    }
    convert(d) {
        return Object.entries(d)
            .sort((a, b) => b[1] - a[1]);
    }
}
exports.TagDistribution = TagDistribution;
