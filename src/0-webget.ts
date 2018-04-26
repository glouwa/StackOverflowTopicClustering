import * as request from 'request'
import * as fs from 'fs'
 
const source = 'stackoverflow'

const site = `${source}.com`
const client_id = '12241'
const client_secret = 'fARiV63SIlUxr*tpsrFXDw(('
const client_key = 'iBKWVDJ4ZBz4LF7EvTdLKA(('


//https://stackexchange.com/oauth/dialog?client_id=12241&scope=no_expiry&redirect_uri=https://stackoverflow.com/oauth/login_success
const access_token = 'ss7QVLkuuRE6NZ77M(3B(A))'

//scope: no_expiry
//redirect_uri: site
let result = { written:0, err:0 }
function requestone(page)
{    
    request({
        url: `https://api.stackexchange.com/2.2/questions?page=${page}&order=desc&sort=activity&site=${source}&filter=!9Z(-wwK0y`,
        gzip: true,
        auth: {
            'bearer': access_token
        }
    }, 
    (err, res)=> {
        if (!res.body.error_id) {
            result.written++
            const formated_body = JSON.stringify(JSON.parse(res.body), null, 4)                 
            fs.writeFileSync(`./res/${source}/html/${page}.json`, formated_body)
        }
        else {
            result.err++
        }
 
        if (result.err + result.written === amount - 1)
            console.log(`${result.written} OK, ${result.err} failed`)
    })
}

var begin = 1000
var amount = 10
for (var page = begin; page < begin+amount; ++page)
    requestone(page)

