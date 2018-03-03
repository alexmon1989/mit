const gulp = require('gulp'), // Gulp
    gutil = require('gulp-util'),
    sass = require('gulp-sass'), // SASS,
    browserSync = require('browser-sync'),
    concat = require('gulp-concat'),
    uglify = require('gulp-uglify'),
    cleanCSS = require('gulp-clean-css'),
    rename = require('gulp-rename'),
    del = require('del'),
    imagemin = require('gulp-imagemin'),
    cache = require('gulp-cache'),
    autoprefixer = require('gulp-autoprefixer'), // Add the desired vendor prefixes and remove unnecessary in SASS-files
    notify = require("gulp-notify"),
    babel = require('gulp-babel'),
    browserify = require('gulp-browserify'),
    njkRender = require('gulp-nunjucks-render'),
    htmlbeautify = require('gulp-html-beautify');

//
// Fonts
//
gulp.task('fonts', function () {
    return gulp.src([
        './app/vendor/icon-awesome/fonts/*.*',
        './app/vendor/icon-hs/fonts/*.*',
    ]).pipe(gulp.dest('./app/fonts/'));
});

//
// CSS
//

gulp.task('sass', ['fonts'], function () {
    return gulp.src('./app/scss/main.scss')
        .pipe(sass({outputStyle: 'expand'}).on("error", notify.onError()))
        .pipe(autoprefixer(['last 15 versions']))
        .pipe(gulp.dest('./app/css/'))
});

gulp.task('css', ['sass'], function () {
    return gulp.src([
        './app/vendor/bootstrap/bootstrap.css',
        './app/vendor/bootstrap/offcanvas.css',
        './app/vendor/hamburgers/hamburgers.css',
        './app/vendor/hs-megamenu/src/hs.megamenu.css',
        './app/vendor/icon-hs/style.css',
        './app/vendor/dzsparallaxer/dzsparallaxer.css',
        './app/vendor/dzsparallaxer/dzsscroller/scroller.css',
        './app/vendor/dzsparallaxer/advancedscroller/plugin.css',
        './app/vendor/fancybox/jquery.fancybox.min.css',
        './app/vendor/slick-carousel/slick/slick.css',
        './app/vendor/animate.css',
        './app/css/main.css',
    ])
        .pipe(concat('styles.min.css'))
        .pipe(gulp.dest('./app/css'))
        .pipe(browserSync.reload({stream: true}));
});

//
// JS
//

gulp.task('vueify', function () {
    return gulp.src('./app/js/main.js')
        .pipe(browserify({
            transform: [
                [{_flags: {debug: false}}, 'vueify'],
                'babelify',
                [{NODE_ENV: process.env.NODE_ENV === 'production' ? 'production' : 'development'}, 'envify'],
            ]
        }))
        .pipe(concat('bundle.min.js'))
        .pipe(gulp.dest('./app/js'));
});

gulp.task('custom-js', function () {
    return gulp.src([
        './app/js/custom.js',
    ])
        .pipe(babel({
            presets: ['env']
        }))
        .pipe(concat('custom.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('app/js'));
});

gulp.task('js', ['vueify', 'custom-js'], function () {
    return gulp.src([
        './app/vendor/jquery/jquery.min.js',
        './app/vendor/jquery-migrate/jquery-migrate.min.js',
        './app/vendor/popper.min.js',
        //'./app/vendor/jquery.easing/js/jquery.easing.js',
        './app/vendor/bootstrap/bootstrap.min.js',
        './app/vendor/bootstrap/offcanvas.js',
        './app/vendor/hs-megamenu/src/hs.megamenu.js',
        './app/vendor/dzsparallaxer/dzsparallaxer.js',
        './app/vendor/dzsparallaxer/dzsscroller/scroller.js',
        './app/vendor/dzsparallaxer/advancedscroller/plugin.js',
        './app/vendor/fancybox/jquery.fancybox.min.js',
        './app/vendor/slick-carousel/slick/slick.js',
        './app/vendor/imagesloaded/imagesloaded.pkgd.min.js',
        './app/vendor/masonry/dist/masonry.pkgd.min.js',
        './app/js/hs.core.js',
        './app/js/components/hs.header.js',
        './app/js/helpers/hs.hamburgers.js',
        './app/js/components/hs.popup.js',
        './app/js/components/hs.carousel.js',
        './app/js/components/hs.go-to.js',
        './app/js/components/hs.dropdown.js',
        './app/js/bundle.min.js',
        './app/js/custom.min.js', // Всегда в конце
    ])
        .pipe(concat('scripts.min.js'))
        .pipe(gulp.dest('./app/js'))
        .pipe(browserSync.reload({stream: true}));
});


//
// Images
//

gulp.task('imagemin', function () {
    return gulp.src([
        './app/img/**/*',
        './app/img-temp/**/*'
    ])
        .pipe(cache(imagemin())) // Cache Images
        .pipe(gulp.dest('./dist/img'));
});

//
// Browser Sync
//

gulp.task('browser-sync', function () {
    browserSync({
        server: {
            baseDir: 'app'
        },
        notify: false,
        // tunnel: true,
        // tunnel: "projectmane", //Demonstration page: http://projectmane.localtunnel.me
    });
});

//
// Nunjucks
//

gulp.task('nunjucks', function () {
    return gulp.src([
        './app/nunjucks/pages/home/index.njk',
        './app/nunjucks/pages/news/list/news_list.njk',
        './app/nunjucks/pages/news/detail/news_detail.njk',
        './app/nunjucks/pages/about/about.njk',
        './app/nunjucks/pages/contacts/contacts.njk',
    ])
        .pipe(njkRender())
        .pipe(htmlbeautify({
            indent_size : 4 // размер отступа - 4 пробела
        }))
        .pipe(gulp.dest('./app'))
        .pipe(browserSync.reload({stream: true}));
});

//
// Build
//

gulp.task('build', ['set-prod-node-env', 'clearcache', 'removedist', 'js', 'css', 'imagemin', 'nunjucks'], function () {

    const buildFiles = gulp.src([
        './app/*.html'
    ]).pipe(gulp.dest('dist'));

    const buildCss = gulp.src([
        'app/css/styles.min.css',
    ])
        .pipe(cleanCSS({level: {1: {specialComments: 0}}})) // Опционально, закомментировать при отладке
        .pipe(gulp.dest('dist/css'));

    const buildJs = gulp.src([
        'app/js/scripts.min.js',
    ])
        .pipe(uglify()) // Минимизировать весь js (на выбор)
        .pipe(gulp.dest('dist/js'));

    const buildFonts = gulp.src([
        'app/fonts/*.*',
    ]).pipe(gulp.dest('dist/fonts'));

});


//
// ENVs
//

gulp.task('set-dev-node-env', function () {
    return process.env.NODE_ENV = 'development';
});

gulp.task('set-prod-node-env', function () {
    return process.env.NODE_ENV = 'production';
});


gulp.task('removedist', function () {
    return del.sync('dist');
});
gulp.task('clearcache', function () {
    return cache.clearAll();
});

//
// Watch
//

gulp.task('watch', ['set-dev-node-env', 'css', 'js', 'nunjucks', 'browser-sync'], function () {
    gulp.watch([
        './app/scss/**/*.scss',
        './app/vendor/**/*.scss',
        './app/vendor/**/*.css'
    ], ['css']);
    gulp.watch([
        './app/js/blocks/**/*.js',
        './app/js/components/**/*.js',
        './app/js/helpers/**/*.js',
        './app/js/vue-components/**/*.vue',
        './app/js/custom.js',
        './app/js/main.js',
        './app/js/placemark.js'
    ], ['js']);
    gulp.watch('./app/nunjucks/**/*.njk', ['nunjucks']);
});

//
// Default
//

gulp.task('default', ['watch']);
