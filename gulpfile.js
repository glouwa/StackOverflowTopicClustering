var gulp        = require('gulp')
var ts          = require('gulp-typescript')
var sass        = require('gulp-sass')
var concat      = require('gulp-concat')
var plumber     = require('gulp-plumber')
var debug       = require('gulp-debug')
var merge       = require('merge2')
var del         = require('del');
var wp          = require('webpack')
var webpack     = require('webpack-stream')
var browserSync = require('browser-sync').create()

var paths = {
    src:  './src/',
    dist: './dist/',
    res:  './res/'    
}

var files = {   
    mainjs:   'index.js',
    mainhtml: 'visualisations/index.html'
}

var html = ()=> gulp.src(paths.src + '**/*.html')
    .pipe(plumber())
    //.pipe(debug())
    .pipe(gulp.dest(paths.dist))

// ---------------------------------------------------------------------------------------------

gulp.task('html',    ()=> html())
gulp.task('html+bs', ()=> html().pipe(browserSync.stream()))
gulp.task('watch',    ['build'], () => {
    browserSync.init({
        index: files.mainhtml,
        server: { baseDir: paths.dist }
    })
    var d3hDist = './dist/' 
    gulp.watch(d3hDist   + 'index.js',  ['build'])
    gulp.watch(paths.src + '**/*.html', ['html+bs'])
})

gulp.task('build',   ['html'])
gulp.task('default', ['watch'])

// ---------------------------------------------------------------------------------------------

var argv        = require('yargs').argv
var through2    = require('through2')
var fs          = require('fs')
