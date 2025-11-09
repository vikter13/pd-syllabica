# app/db.py
import re
from flask import g
import flask_migrate
from sqlalchemy import text
import app.mod.models as models

# База данных из Flask-SQLAlchemy
PDB = models.db


class SAProxy:
    """
    Промежуточный класс, чтобы старый код (на sqlite) работал с PostgreSQL.
    Поддерживает старые методы .execute() и .commit().
    """

    def __init__(self, sa_db):
        self.sa_db = sa_db

    def _qmarks_to_named(self, sql: str, params):
        """
        Заменяет знаки вопроса ? на именованные параметры (:p0, :p1, ...),
        чтобы запросы корректно работали через SQLAlchemy.
        """
        if not params:
            return sql, {}

        qcount = sql.count('?')
        if qcount != len(params):
            raise ValueError(f"Количество ? не совпадает с числом параметров: {qcount} vs {len(params)}")

        named = {}

        def repl(m, counter=[0]):
            i = counter[0]
            counter[0] += 1
            key = f"p{i}"
            named[key] = params[i]
            return f":{key}"

        sql_named = re.sub(r'\?', repl, sql)
        return sql_named, named

    def _ddl_sql_fixups(self, sql: str) -> str:
        """
        Подгоняет синтаксис SQL под PostgreSQL:
        заменяет 'INTEGER PRIMARY KEY AUTOINCREMENT' на 'SERIAL PRIMARY KEY' и т.п.
        """
        s = sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        s = s.replace('AUTOINCREMENT', '')
        return s

    def execute(self, sql: str, params=None):
        """
        Выполняет SQL-запрос (через session.execute()).
        Старый код может вызывать: db.execute('SELECT * FROM ...', (a, b))
        """
        sql = self._ddl_sql_fixups(sql)

        if params is not None and not isinstance(params, (list, tuple)):
            params = tuple(params)

        if params:
            sql_named, bind = self._qmarks_to_named(sql, params)
            res = self.sa_db.session.execute(text(sql_named), bind)
        else:
            res = self.sa_db.session.execute(text(sql))

        return res

    def commit(self):
        """Фиксирует изменения в базе."""
        self.sa_db.session.commit()


def get_db():
    """
    Возвращает объект для работы с БД.
    Теперь это не sqlite3 connection, а SAProxy поверх SQLAlchemy.
    """
    if 'db' not in g:
        g.db = SAProxy(PDB)
    return g.db


def init_app(app):
    """Инициализация базы и миграций при старте Flask-приложения."""
    PDB.init_app(app)
    app.MIGRATE = flask_migrate.Migrate(app, PDB)
