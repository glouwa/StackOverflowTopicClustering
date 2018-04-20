'use strict'
const fs = require('fs')

const merge = {}
for (var i = 1; i < 540; i++) 
{   
    const filen = `./res/download/${i}.json`    
    const dlstr = fs.readFileSync(filen)
    const dlobj = JSON.parse(dlstr)
        
    dlobj.items.forEach(q=> merge[q.question_id] = q)
    console.log(filen, dlobj.items.length)
}

fs.writeFileSync(`./res/merge.json`, JSON.stringify(merge, null, 4))