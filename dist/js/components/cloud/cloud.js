"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const d3 = require("d3");
const cloud = require("d3-cloud");
class TagCloud {
    constructor(args) {
        this.fill = d3.scaleOrdinal(d3.schemeCategory10);
        this.layout = null;
        this.args = args;
        this.layout = cloud()
            .size([420, 280])
            .words(this.args.words)
            .padding(3)
            //.rotate(()=> ~~(Math.random() * 2 ) * 90)
            .rotate(() => ~~(Math.random() * 2) * 40 - 20)
            .font("Impact")
            .fontSize(d => d.size)
            .on("end", (w) => this.draw(w));
        this.layout.start();
    }
    draw(words) {
        d3.select(this.args.parent).select('svg').remove();
        d3.select(this.args.parent).append("svg")
            .attr("width", this.layout.size()[0])
            .attr("height", this.layout.size()[1])
            .append("g")
            .attr("transform", "translate(" + this.layout.size()[0] / 2 + "," + this.layout.size()[1] / 2 + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", (d) => d.size + "px")
            .style("font-family", "Impact")
            .style("fill", (d, i) => this.fill('' + i))
            .attr("text-anchor", "middle")
            .attr("transform", (d) => "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")")
            .text((d) => d.text);
    }
}
exports.TagCloud = TagCloud;
