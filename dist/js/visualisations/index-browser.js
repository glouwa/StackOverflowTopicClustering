"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const d3 = require("d3");
const tagdistribution_1 = require("../components/tagdistribution/tagdistribution");
const stackexchange_view_1 = require("../components/stackexchange/stackexchange-view");
document.body.onload = function init() {
    const dataset = new stackexchange_view_1.StackoverflowDatasetView({
        parent: document.body
    });
    d3.json("data/bag-of-texts/stackoverflow-meta.json")
        .then((datasetmeta) => dataset.update(datasetmeta));
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
    d3.json("data/bag-of-words/htmlcleaned-meta.json")
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
