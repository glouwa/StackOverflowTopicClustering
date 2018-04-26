"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const d3 = require("d3");
const bb_counter_1 = require("../components/bb-counter/bb-counter");
const tagdistribution_1 = require("../components/tagdistribution/tagdistribution");
var mergemeta;
document.body.onload = function init() {
    // stackoverflow dataset
    const scores = new bb_counter_1.BillboardCounter({
        parent: document.querySelector("#SCOChart"),
        height: 120,
        //tickcount: 20,
        data: [],
    });
    const ansercount = new bb_counter_1.BillboardCounter({
        parent: document.querySelector("#ANCChart"),
        height: 120,
        data: [],
    });
    const isanswered = new bb_counter_1.BillboardCounter({
        parent: document.querySelector("#ISAChart"),
        height: 120,
        data: [],
    });
    // Tags
    const tags = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Tag',
        data: {},
    });
    // Title
    const plaintitle = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Title plain',
        data: {}
    });
    const stemmedtitle = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Title stemmed',
        data: {}
    });
    const lemmedtitle = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Title lemmed',
        data: {}
    });
    // Body
    const plainbody = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Body plain',
        data: {}
    });
    const stemmedbody = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Body stemmed',
        data: {}
    });
    const lemmedbody = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Body lemmed',
        data: {}
    });
    d3.json("tasks/bag-of-sentences/merge-meta.json")
        .then((mergemeta) => {
        document.querySelector("#downloadheader").innerText = `Stackoverflow: ${mergemeta.files} Files, ${mergemeta.rawquestions} Raw-Questions, ${mergemeta.dupquestions} duplicate, ${mergemeta.errquestions} invalid`;
        document.querySelector("#mergeheader").innerText = `Merged: ${(mergemeta.size / 1024 / 1024).toFixed(0)}MB, ${mergemeta.questions} Valid-Questions, ${mergemeta.tagcount} Tags`;
        scores.update({
            parent: document.querySelector("#SCOChart"),
            height: 120,
            tickcount: 20,
            data: Object.entries(mergemeta.scodist)
                .sort((a, b) => a[0] - b[0])
                .slice(0, 35),
        });
        ansercount.update({
            parent: document.querySelector("#ANCChart"),
            height: 120,
            data: Object.entries(mergemeta.ancdist)
                .sort((a, b) => a[0] - b[0]),
        });
        isanswered.update({
            parent: document.querySelector("#ISAChart"),
            height: 120,
            data: Object.entries(mergemeta.isadist)
                .sort((a, b) => b[1] - a[1]),
        });
        tags.update({
            parent: document.body,
            name: 'Tag',
            data: mergemeta.tagdist,
        });
    });
    d3.json("tasks/bag-of-sentences/htmlcleaned-meta.json")
        .then((htmlcleanedmeta) => {
        plaintitle.update({
            name: 'Title plain',
            data: htmlcleanedmeta.titletermdist,
        });
        plainbody.update({
            name: 'Body plain',
            data: htmlcleanedmeta.termdist
        });
    });
    d3.json("tasks/bag-of-words/stemmed-meta.json")
        .then((stemmeta) => {
        stemmedtitle.update({
            name: 'Title stemmed',
            data: stemmeta.title_terms,
        });
        stemmedbody.update({
            name: 'Body stemmed',
            data: stemmeta.body_terms
        });
    });
    d3.json("tasks/bag-of-words/lemmatized-meta.json")
        .then((lemmmeta) => {
        lemmedtitle.update({
            name: 'Title lemmed',
            data: lemmmeta.title_terms,
        });
        lemmedbody.update({
            name: 'Body lemmed',
            data: lemmmeta.body_terms
        });
    });
};
