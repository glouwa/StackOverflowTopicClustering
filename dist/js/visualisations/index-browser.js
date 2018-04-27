"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const d3 = require("d3");
const bb_counter_1 = require("../components/bb-counter/bb-counter");
const tagdistribution_1 = require("../components/tagdistribution/tagdistribution");
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
    const tags = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Tag',
        data: {},
    });
    // Plain
    const plaintitle = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Plain Title',
        data: {}
    });
    const plainbody = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Plain Body',
        data: {}
    });
    // Stemmed
    const stemmedtitle = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Stemmed Title',
        data: {}
    });
    const stemmedbody = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Stemmed Body',
        data: {}
    });
    // Lemmed
    const lemmedtitle = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Lemmed Title',
        data: {}
    });
    const lemmedbody = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Lemmed Body',
        data: {}
    });
    d3.json("data/bag-of-texts/merge-meta.json")
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
    d3.json("data/bag-of-texts/htmlcleaned-meta.json")
        .then((htmlcleanedmeta) => {
        plaintitle.update({
            name: 'Plain Title',
            data: htmlcleanedmeta.titletermdist,
        });
        plainbody.update({
            name: 'Plain Body',
            data: htmlcleanedmeta.termdist
        });
    });
    d3.json("data/bag-of-words/stemmed-meta.json")
        .then((stemmeta) => {
        stemmedtitle.update({
            name: 'Stemmed Title',
            data: stemmeta.title_terms,
        });
        stemmedbody.update({
            name: 'Stemmed Body',
            data: stemmeta.body_terms
        });
    });
    d3.json("data/bag-of-words/lemmatized-meta.json")
        .then((lemmmeta) => {
        lemmedtitle.update({
            name: 'Lemmed Title',
            data: lemmmeta.title_terms,
        });
        lemmedbody.update({
            name: 'Lemmed Body',
            data: lemmmeta.body_terms
        });
    });
};
