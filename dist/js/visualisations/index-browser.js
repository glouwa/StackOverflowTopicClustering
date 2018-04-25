"use strict";
//import * as d3 from 'd3'
Object.defineProperty(exports, "__esModule", { value: true });
const bb_counter_1 = require("../components/bb-counter/bb-counter");
const tagdistribution_1 = require("../components/tagdistribution/tagdistribution");
document.body.onload = function init() {
    function write(divid, text) {
        document.querySelector(divid).innerText = text;
    }
    write("#downloadheader", `Downloaded: ${mergemeta.files} Files, ${mergemeta.rawquestions} Raw-Questions, ${mergemeta.dupquestions} duplicate, ${mergemeta.errquestions} invalid`);
    write("#mergeheader", `Merged: ${(mergemeta.size / 1024 / 1024).toFixed(0)}MB, ${mergemeta.questions} Valid-Questions, ${mergemeta.tagcount} Tags`);
    bb_counter_1.plot("#SCOChart", mergemeta.scodist, "Question Score distribution", 0, true);
    bb_counter_1.plot("#ANCChart", mergemeta.ancdist, "Answer Count distribution", 0, true);
    bb_counter_1.plot("#ISAChart", mergemeta.isadist, "Is Answered distribution", 0, true);
    // Tags
    new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Tag',
        data: mergemeta.tagdist
    });
    // Title
    new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Title plain',
        data: htmlcleanedmeta.titletermdist
    });
    new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Title stemmed',
        data: stemmeta.title_terms
    });
    new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Title lemmed',
        data: lemmmeta.title_terms
    });
    // Body
    new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Body plain',
        data: htmlcleanedmeta.termdist
    });
    new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Body stemmed',
        data: stemmeta.body_terms
    });
    new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Body lemmed',
        data: lemmmeta.body_terms
    });
};
