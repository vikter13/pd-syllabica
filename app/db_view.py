# app/db_view.py
# coding: utf-8
"""
Страница «Базы данных» на PostgreSQL.
"""

from flask import Blueprint, render_template, g

import app.mod.models as models

__all__ = ["BP"]

BP = Blueprint(
    "db_view",
    __name__,
    url_prefix="/db",
)


@BP.url_value_preprocessor
def bp_url_value_preprocessor(endpoint, values):
    # чтобы header.html подключил auth/header_links.html
    g.url_prefix = "auth"


@BP.route("/list", methods=["GET"], endpoint="list")
def list_page():
    """
    Простая страница, которая показывает немного содержимого
    из нескольких таблиц PostgreSQL.
    """
    # users2: там ключ vk_id, а не id
    users = models.User.query.order_by(models.User.vk_id).limit(50).all()

    texts = models.Text.query.order_by(models.Text.id).limit(50).all()
    authors = models.Author.query.order_by(models.Author.id).limit(50).all()
    dictionary = models.Dictionary.query.order_by(models.Dictionary.word).limit(50).all()

    stats = {
        "users": models.User.query.count(),
        "texts": models.Text.query.count(),
        "authors": models.Author.query.count(),
        "dictionary": models.Dictionary.query.count(),
    }

    return render_template(
        "db/list.html",
        stats=stats,
        users=users,
        texts=texts,
        authors=authors,
        dictionary=dictionary,
    )