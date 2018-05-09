import { Distribution } from '../model/model'

export function count(map, newkey) : {}
{
    let result = {}
    for (var key in map) {
        const resultkey = newkey(map[key])
        result[resultkey] = result[resultkey]+1 || 1
    }        
    return result
}

export function group(map, newkey) : {}
{
    let result = {}
    for (var key in map) {
        const resultkey = newkey(map[key])
        result[resultkey] = result[resultkey] || []
        result[resultkey].push(map[key].id)
    }        
    return result
}

/*
index: {
    id:      { key:PostId, values:PostId[] }[] 
    created: { key:Date, values:PostId[] }[]
    size:    { key:number, values:PostId[] }[]
}  
*/

export function index<K, V>(map, newkey) : { key:K, values:V[] }[]
{
    return Object.entries(group(map, newkey))        
        .map(v=> ({ key:(<any>v[0]), values:<V[]>v[1] }))    
}

export function distribution<T>(countmap, idextract, bins) : Distribution<T>
{
    return count(countmap, idextract)
}