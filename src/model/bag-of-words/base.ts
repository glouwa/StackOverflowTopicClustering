
export type PostId = string
export type Ref = string
export type Hash = string
export type Char = string

export type Text = string[] // weil beim parsen von p schon getrennt wird
export type BagOfWords = string[]

export type Distribution<E> = { [key:string]:number }
//type Distribution<E> = Map<E, number>
export interface TextDistributions {    
    sizeDistribution: Distribution<number>
    letterDistribution: Distribution<Char>
    sentencesCountDistribution: Distribution<number>
    sentencesSizeDistribution: Distribution<number>    
}
export interface TermDistributions extends TextDistributions {
    distribution: Distribution<string>    
}

export interface Post {
    id: PostId
    created: Date    
    size: number    
    
    terms: { [key:string]:BagOfWords }
    text: { [key:string]:Text }    
}
export interface StackOverflowPost extends Post {
    isAnswered: boolean
    answerCount: number
    score: number
    
    terms: { 
        tags: BagOfWords
    }
    sentences?: {
        title: Text        
        body: Text
    }
    text: {
        title: Text
        body: Text
        inlinecode: Text
        code: Text
    }
}
export type Dataset = { [key:string]:Post }

export interface Meta {
    data: {
        file: Ref
        hash: Hash    
        size: number
    }    
    datasource: {
        hash: Hash    
        size: number
    }
    //size: number
    //postcount: number
    index: {
        id:      { id:PostId, values:PostId[] }[] 
        created: { date:Date, values:PostId[] }[]
        sizes: {
            post:       { size:number, values:PostId[] }[]
            title:      { size:number, values:PostId[] }[]
            body:       { size:number, values:PostId[] }[]
            inlinecode: { size:number, values:PostId[] }[]            
            code:       { size:number, values:PostId[] }[]
        }        
    }    
    distributions: {
        terms:{ [key:string]: TermDistributions }
        sentences:{ [key:string]: TextDistributions }
        texts:{ [key:string]: TextDistributions }
    }
}
export interface StackOverflowMeta extends Meta {
    datasource: {
        hash: Hash,
        size: number
        filecount: number
        rawquestions: number
        errquestions: number
        dupquestions: number
    }   
    distributions: {
        size: Distribution<boolean>
        isAnswered: Distribution<boolean>
        answerCount: Distribution<number>
        score: Distribution<number>
        
        terms: {  
            tags: TermDistributions
            title: TermDistributions
            body: TermDistributions
            code: TermDistributions
        }
        sentences: {}
        texts: { 
            title: TextDistributions
            body: TextDistributions
            code: TextDistributions
        }                
    }
}

