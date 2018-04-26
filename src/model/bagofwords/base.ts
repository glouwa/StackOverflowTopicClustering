
type PostId = string
type Ref = string
type Hash = string
type Char = string

type Text = string[] // weil beim parsen von p schon getrennt wird
type BagOfWords = string[]

type Distribution<E> = { [key:string]:number }
//type Distribution<E> = Map<E, number>
interface TextDistributions {
    sizeDistribution: Distribution<number>
    sentencesizeDistribution: Distribution<number>
    letterDistribution: Distribution<Char>
}
interface TermDistributions extends TextDistributions {
    distribution: Distribution<string>    
}

interface Post {
    id: PostId
    created: Date    
    size: number    
    
    terms: { [key:string]:BagOfWords }
    text: { [key:string]:Text }    
}
interface StackOverflowPost extends Post {
    isAnswered: boolean
    answerCount: number
    score: number
    
    terms: { 
        tags: BagOfWords
    }
    sentences: {
        title: Text        
        body: Text
    }
    text: {
        title: Text
        body: Text
        code: Text
    }
}

interface Meta {
    datafile: Ref
    datafileHash: Hash
    datasource: {}
    idindex: { PostId:PostId } 
    timeindex: { Date:PostId }
    sizeindex: { number:PostId }
    
    distributions: {
        terms:{ [key:string]: TermDistributions }
        sentences:{ [key:string]: TextDistributions }
        texts:{ [key:string]: TextDistributions }
    }
}
interface StackOverflowMeta {
    datasource: {        
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
        texts: { 
            title: TextDistributions
            body: TextDistributions
            code: TextDistributions
        }                
    }
}

export type Dataset = { [key:string]:Post }