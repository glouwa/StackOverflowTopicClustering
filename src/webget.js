'use strict'
const request = require('request')
const fs = require('fs')
 
const site = 'stackoverflow.com'
const client_id = '12241'
const client_secret = 'fARiV63SIlUxr*tpsrFXDw(('
const client_key = 'iBKWVDJ4ZBz4LF7EvTdLKA(('


//https://stackexchange.com/oauth/dialog?client_id=12241&scope=no_expiry&redirect_uri=https://stackoverflow.com/oauth/login_success
const access_token = 'ss7QVLkuuRE6NZ77M(3B(A))'

//scope: no_expiry
//redirect_uri: site

function requestone(page)
{    
    request({
        url: `https://api.stackexchange.com/2.2/questions?page=${page}&order=desc&sort=activity&site=stackoverflow&filter=!9Z(-wwK0y`,
        gzip: true,
        auth: {
            'bearer': access_token
        }
    }, 
    (err, res)=> {
        console.log('got response')
        const formated_body = JSON.stringify(JSON.parse(res.body), null, 4)                 
        fs.writeFileSync(`./res/download/${page}.json`, formated_body)
    })
}

var begin = 240
for (var page = begin; page < begin+30; ++page)
    requestone(page)