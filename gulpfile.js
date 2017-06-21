const gulp = require('gulp');
const htmlmin = require('gulp-htmlmin');
const pug = require('gulp-pug');
const webserver = require('gulp-webserver');

gulp.task('default', ['html', 'webserver', 'watch']);

gulp.task('build', ['html']);

gulp.task('html', () => {
  gulp.src('index.pug')
    .pipe(pug({}))
    .pipe(htmlmin({ collapseWhitespace: true }))
    .pipe(gulp.dest('dist'));
});

gulp.task('webserver', () => {
  const port = parseInt(process.env.port || '8080', 10);
  gulp.src('dist')
    .pipe(webserver({ livereload: true, open: true, port, host: '0.0.0.0' }));
});

gulp.task('watch', () => {
  gulp.watch('index.pug', ['html']);
});
