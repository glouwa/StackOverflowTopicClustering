"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const d3 = require("d3");
const tagdistribution_1 = require("../components/tagdistribution/tagdistribution");
const stackexchange_view_1 = require("../components/stackexchange/stackexchange-view");
class TermformatView {
    constructor(args) {
        this.args = args;
        this.plaintitle = new tagdistribution_1.TagDistribution({
            parent: document.body,
            name: `${this.args.format} Title`,
        });
        this.plainbody = new tagdistribution_1.TagDistribution({
            parent: document.body,
            name: `${this.args.format} Body`,
        });
    }
    update(data) {
        this.plaintitle.update({
            name: `${this.args.format} Title`,
            data: data.title
        });
        this.plainbody.update({
            name: `${this.args.format} Body`,
            data: data.body
        });
    }
}
document.body.onload = function init() {
    const dataset = new stackexchange_view_1.StackoverflowDatasetView({
        parent: document.body
    });
    const plaininlinecode = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: `Inline Code`,
    });
    const plaincode = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: `Code`,
    });
    const termsraw = new TermformatView({ format: 'Plain' });
    const termsstem = new TermformatView({ format: 'Stem' });
    const termslem = new TermformatView({ format: 'Lemma' });
    const ngram2 = new TermformatView({ format: '2Grams' });
    const ngram3 = new TermformatView({ format: '3Grams' });
    d3.json("data/bag-of-words/stackoverflow-raw-meta.json")
        .then((datasetmeta) => {
        dataset.update(datasetmeta);
        termsraw.update(datasetmeta.distributions.terms);
        plaininlinecode.update({
            name: `Inline Code`,
            data: datasetmeta.distributions.terms.inlinecode
        });
        plaincode.update({
            name: `Code`,
            data: datasetmeta.distributions.terms.code
        });
    });
    d3.json("data/bag-of-words/stackoverflow-stem-meta.json")
        .then((datasetmeta) => {
        termsstem.update(datasetmeta.distributions.terms);
    });
    d3.json("data/bag-of-words/stackoverflow-lemma-meta.json")
        .then((datasetmeta) => {
        termslem.update(datasetmeta.distributions.terms);
    });
    d3.json("data/ngrams/stackoverflow-2gram-stem-meta.json")
        .then((datasetmeta) => {
        ngram2.update(datasetmeta.distributions.terms);
    });
    d3.json("data/ngrams/stackoverflow-3gram-stem-meta.json")
        .then((datasetmeta) => {
        ngram3.update(datasetmeta.distributions.terms);
    });
};
