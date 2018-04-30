"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const d3 = require("d3");
const tagdistribution_1 = require("../components/tagdistribution/tagdistribution");
const stackexchange_view_1 = require("../components/stackexchange/stackexchange-view");
document.body.onload = function init() {
    const dataset = new stackexchange_view_1.StackoverflowDatasetView({
        parent: document.body
    });
    const plaintitle = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Plain Title',
    });
    const plainbody = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Plain Body',
    });
    const plaininlinecode = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Plain inline Code',
    });
    const plaincode = new tagdistribution_1.TagDistribution({
        parent: document.body,
        name: 'Plain Code',
    });
    d3.json("data/bag-of-words/stackoverflow-raw-meta.json")
        .then((datasetmeta) => {
        dataset.update(datasetmeta);
        plaintitle.update({
            name: 'Plain Title',
            data: datasetmeta.distributions.terms.title
        });
        plainbody.update({
            name: 'Plain Body',
            data: datasetmeta.distributions.terms.body
        });
        plaininlinecode.update({
            name: 'Plain inline Code',
            data: datasetmeta.distributions.terms.inlinecode
        });
        plaincode.update({
            name: 'Plain Code',
            data: datasetmeta.distributions.terms.code
        });
    });
    // Plain    
    /*
    const plainbody = new TagDistribution({
        parent: document.body,
        name: 'Plain Body',
    })
    
    d3.json("data/bag-of-words/htmlcleaned-meta.json")
        .then((htmlcleanedmeta:any)=> {
            plaintitle.update({
                name: 'Plain Title',
                data: htmlcleanedmeta.titletermdist,
            })
            plainbody.update({
                name: 'Plain Body',
                data: htmlcleanedmeta.termdist
            })
        })
        
    // Stemmed
    const stemmedtitle = new TagDistribution({
        parent: document.body,
        name: 'Stemmed Title',
    })
    const stemmedbody = new TagDistribution({
        parent: document.body,
        name: 'Stemmed Body',
    })
    d3.json("data/bag-of-words/stemmed-meta.json")
        .then((stemmeta:any)=> {
            stemmedtitle.update({
                name: 'Stemmed Title',
                data: stemmeta.title_terms,
            })
            stemmedbody.update({
                name: 'Stemmed Body',
                data: stemmeta.body_terms
            })
        })

    // Lemmed
    const lemmedtitle = new TagDistribution({
        parent: document.body,
        name: 'Lemmed Title',
    })
    const lemmedbody = new TagDistribution({
        parent: document.body,
        name: 'Lemmed Body',
    })
    d3.json("data/bag-of-words/lemmatized-meta.json")
        .then((lemmmeta:any)=> {
            lemmedtitle.update({
                name: 'Lemmed Title',
                data: lemmmeta.title_terms,
            })
            lemmedbody.update({
                name: 'Lemmed Body',
                data: lemmmeta.body_terms
            })
        })
        */
};
