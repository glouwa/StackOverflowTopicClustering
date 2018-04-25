var gulp        = require('gulp')

var ts          = require('gulp-typescript')
//var sass        = require('gulp-sass')
//var concat      = require('gulp-concat')
var plumber     = require('gulp-plumber')
var debug       = require('gulp-debug')
var merge       = require('merge2')
//var del         = require('del');
//var wp          = require('webpack')
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
        .pipe(browserSync.stream())
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
        .pipe(browserSync.stream())
}

const build = gulp.parallel(html, gulp.series(tsc, web))

function watch() {
    browserSync.init({
        index: files.mainhtml,
        server: { baseDir: paths.dist }
    })
        
    gulp.watch(paths.src + '**/*.ts',   build)
    gulp.watch(paths.src + '**/*.html', html)
}

exports.html = html
exports.tsc = tsc
exports.web = web
exports.watch = watch
exports.default = watch

// ---------------------------------------------------------------------------------------------
/*
var argv        = require('yargs').argv
var through2    = require('through2')
var fs          = require('fs')
*/