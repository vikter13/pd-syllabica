# app/db_view.py
# coding: utf-8

import os
from flask import Blueprint, render_template, g, request

import app.mod.models as models

BP = Blueprint(
    "db_view",
    __name__,
    url_prefix="/db",
)


@BP.url_value_preprocessor
def bp_url_value_preprocessor(endpoint, values):
    g.url_prefix = "auth"


@BP.route("/list", methods=["GET"], endpoint="list")
def list_page():
    q = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 20

    base_query = models.Text.query

    if q:
        like = f"%{q}%"
        filters = []
        if hasattr(models.Text, "title"):
            filters.append(models.Text.title.ilike(like))
        if hasattr(models.Text, "text"):
            filters.append(models.Text.text.ilike(like))
        if hasattr(models.Text, "author"):
            filters.append(models.Text.author.ilike(like))
        if filters:
            from sqlalchemy import or_
            base_query = base_query.filter(or_(*filters))

    total = base_query.count()
    page_count = (total + per_page - 1) // per_page or 1
    if page < 1:
        page = 1
    if page > page_count:
        page = page_count

    offset = (page - 1) * per_page
    rows_orm = base_query.order_by(models.Text.id).offset(offset).limit(per_page).all()

    columns = []
    for name in ("id", "user_id", "date_id", "genre_id", "author_id", "author", "title", "text"):
        if hasattr(models.Text, name):
            columns.append(name)

    rows = []
    for t in rows_orm:
        d = {}
        for col in columns:
            d[col] = getattr(t, col, None)
        rows.append(d)

    window = 5
    start = max(1, page - window)
    end = min(page_count, page + window)
    page_numbers = list(range(start, end + 1))

    return render_template(
        "db/list.html",
        rows=rows,
        columns=columns,
        q=q,
        total=total,
        page=page,
        page_count=page_count,
        page_numbers=page_numbers,
    )