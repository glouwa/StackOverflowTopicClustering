export class Stats
{
    name
    elementtype
    count
    min
    max
    mean
    median
    variance
    entropy

    constructor(v:[])
    {
        this.count = v.length
        this.elementtype = this.count ? typeof v[0] : undefined
        //v.forEach(e=> console.assert(typeof e === this.elementtype, e, typeof e))
        v = v.filter(e=> typeof e === this.elementtype)

        const E = (v, f)=> v.reduce((a, v)=> a+f(v)/this.count, 0)

        this.min = v.reduce((a, v)=> (a<v ? a:v ))
        this.max = v.reduce((a, v)=> (a>v ? a:v ))
        this.median = v[~~(this.count/2)]
        this.mean = E(v, ve=> ve)
        //this.variance = E(v.map(e=> (e-this.mean)*(e-this.mean)), de=> de)
        this.variance = E(v, ve=> (ve-this.mean)*(ve-this.mean))
        this.entropy = E(v, ve=> Math.log2(ve))
    }

    public toString()
    {
        return `${this.count}#, [${this.min} - ${this.max}], ~${this.mean.toFixed(2)}, Ø${this.median}, σ${this.variance.toExponential(2)}, H${this.entropy.toExponential(2)}`
    }
}