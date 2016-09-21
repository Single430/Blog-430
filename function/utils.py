# coding=utf8

import markdown
# from datetime import datetime
from . import app


def format_date(date_obj):
    return date_obj.strftime(
        '%b %d,%Y')


def format_date_weekday(date_obj):
    return date_obj.strftime(
        '%A %b %d,%Y')


def format_datetime(date_obj):
    return date_obj.strftime(
        '%A %b %d,%Y %H:%M:%S')


app.jinja_env.globals['format_date'] = format_date
app.jinja_env.globals['format_date_weekday'] = format_date_weekday
app.jinja_env.globals['format_datetime'] = format_datetime


def markdown2html(md_text):
    return markdown.markdown(md_text)


def load_content(name):
    with open('{}.md'.format(name)) as f:
        md_text = f.read().decode('utf8', 'ignore')
    return markdown2html(md_text)
