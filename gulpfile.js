var gulp        = require('gulp')

var ts          = require('gulp-typescript')
//var sass        = require('gulp-sass')
//var concat      = require('gulp-concat')
var plumber     = require('gulp-plumber')
var debug       = require('gulp-debug')
var merge       = require('merge2')
//var del         = require('del')
var webpack     = require('webpack-stream')
var browserSync = require('browser-sync').create()

var paths = {
    src:  './src/',
    dist: './dist/',
    res:  './res/'    
}

var files = {   
    mainjs:   'visualisations/index-browser.js',
    mainhtml: 'visualisations/index.html'
}

function html() {
    return gulp.src(paths.src + '**/*.html')
        .pipe(plumber()) 
        .pipe(gulp.dest(paths.dist))
}

function tsc() {
    var tsResult = gulp.src(paths.src + '**/*.ts')
        .pipe(plumber())
        .pipe(debug())
        .pipe(ts.createProject(require('./tsconfig').compilerOptions)())

    return merge([
        tsResult.dts.pipe(gulp.dest(paths.dist + 'd/')),
        tsResult.js.pipe(gulp.dest(paths.dist + 'js/'))
    ])
}

function web() {
    return gulp.src(paths.dist + 'js/' + files.mainjs)
        .pipe(plumber())
        .pipe(debug())
        .pipe(webpack({
            output: { filename:files.mainjs },
            devtool: 'source-map',
            plugins: []
        }))
        .pipe(gulp.dest(paths.dist))
}

function bs() {
    return gulp.src(paths.dist + '**/*.html')        
        .pipe(browserSync.stream())        
}

const build = gulp.series(gulp.parallel(html, gulp.series(tsc, web)), bs)

function watch() {
    browserSync.init({
        index: files.mainhtml,
        server: { baseDir: paths.dist }
    })
        
    gulp.watch(paths.src + '**/*.ts',   build)
    gulp.watch(paths.src + '**/*.html', html)

    gulp.watch(paths.res + 'stackoverflow/meta.json', exports.convert)
    gulp.watch(paths.dist + 'data/ngrams/*', bs)
}

exports.html = html
exports.tsc = tsc
exports.web = web
exports.watch = gulp.series(build, watch)
exports.default = exports.watch

// ---------------------------------------------------------------------------------------------
/*
var argv        = require('yargs').argv
var through2    = require('through2')
var fs          = require('fs')
*/


const stackexchange = require('./dist/js/model/bag-of-texts/stackexchange')
const stats = require('./dist/js/model/stats-frequency')
var exec = require('child_process').exec

function run(cmd) {
    return function run_(cb) {
        exec(cmd, function (err, stdout, stderr) {
            console.log(stdout)
            console.log(stderr)
            cb(err)
        })
    }
}

exports.stackoverflow = stackexchange.download('stackoverflow', 10)
exports.text =          gulp.series(
                            stackexchange.parseAndMerge('stackoverflow'),
                            //stats.calc('stackoverflow'),
                        )
exports.sentence =      gulp.series(
                            run('python3 src/model/bag-of-sentences/sentences.py'),
                            //stats.calc('stackoverflow'),
                        )
exports.word =          gulp.series(
                            //run('python3 src/model/bag-of-sentences/sentences.py'),
                            gulp.parallel(
                                run('python3 src/model/bag-of-words/stemming.py'),
                                run('python3 src/model/bag-of-words/lemming.py'),
                                run('python3 src/model/bag-of-words/terms.py')
                            ),
                            //stats.calc('stackoverflow')
                        )
exports.ngram =         gulp.series(
                            /*gulp.parallel(
                                run('python3 src/model/bag-of-words/stemming.py'),
                                run('python3 src/model/bag-of-words/lemming.py'),
                                run('python3 src/model/bag-of-words/terms.py')
                            ),*/
                            gulp.parallel(
                                run('python3 src/model/ngrams/ngram.py 2'),
                                run('python3 src/model/ngrams/ngram.py 3')
                            ),
                            //stats.calc('stackoverflow')
                        )
exports.stats =         stats.calc('stackoverflow')

exports.all =           gulp.series(exports.text, exports.sentence, exports.word, exports.ngram, exports.stats)

exports.classify =      gulp.series(
                            run('python3 src/algo/main.py'),
                            //stats.calc('stackoverflow'),
                        )

exports.pip =           gulp.series(
                            run('pip3 install sklearn'),
                            run('pip3 install nltk'),
                            run(`python3 >>> "import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
nltk.download('wordnet')"`),
                            run('pip3 install --upgrade mathplotlib'),
                            //stats.calc('stackoverflow'),
                        )
