# coding=utf-8

from datetime import datetime

from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required
from flask_wtf import Form

from .database import db


articles_tags = db.Table(
    'articles_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id')))


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(100))
    summary = db.Column(db.String(512))
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    tags = db.relationship('Tag',
                           secondary=articles_tags,
                           backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, author, summary, body, create_time=None):
        self.title = title
        self.author = author
        self.summary = summary
        self.body = body
        if create_time:
            self.create_time = create_time

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class PostForm(Form):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


def _get_tag(name):
    name = name.lower()
    tag = db.session.query(Tag).filter(Tag.name == name).first()
    if not tag:
        tag = Tag(name)
        tag.save()
    return tag


def create_article(title, author, summary, body, create_time=None, tagnames=[]):
    article = Article(title, author, summary, body, create_time)
    for tagname in tagnames:
        tag = _get_tag(tagname.lower())
        article.tags.append(tag)
    article.save()
    return article