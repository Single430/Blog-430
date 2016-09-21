# -*- coding: utf-8 -*-
# !/usr/bin/env python

# from datetime import datetime

from datetime import datetime

from flask import render_template, request, abort, redirect, url_for, current_app
from .models import Article, Tag, create_article, PostForm
from .utils import markdown2html, load_content
from . import app
from .database import db


@app.errorhandler(404)
def page_not_found(error):
    title = unicode(error)
    message = error.description
    return render_template('errors.html',
                           title=title,
                           message=message)


@app.errorhandler(500)
def internal_server_error(error):
    title = unicode(error)
    message = error.description
    return render_template('errors.html',
                           title=title,
                           message=message)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    page = request.args.get('page', 1, type=int)
    pagination = Article.query.order_by(Article.id.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@app.route('/show', methods=['POST'])
def show():
    if request.method == 'POST':
        title = request.form.get('article_title', 'None')
        body = request.form.get('article_body', 'None')
        body_des = request.form.get('article_summary', 'None')
        author = request.form.get('article_author', 'None')
        updb = Article(title=title, body=body, author=author,
                           create_time=datetime.now(), summary=body_des)
        print '''
            ======================
            =========%s===========
            ========================
        ''' % title
        updb.save()
    return redirect(url_for('index'))


@app.route('/article/create')
def add_article():
    return render_template('add_article.html')


@app.route('/article/<id>')
def show_article(id):
    article = Article.query.get_or_404(id)
    return render_template('content.html',
                           id=id,
                           title=article.title,
                           author=article.author,
                           body=article.body.replace('\n', '<br/>').replace(' ', '&nbsp;'),
                           create_time=article.create_time,
                           tags=article.tags)


@app.route('/delete/<id>')
def delete_article(id):
    return redirect(url_for('index'))


@app.route('/edit/<id>')
def edit_article(id):
    return redirect(url_for('index'))