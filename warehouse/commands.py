import click
from warehouse import db


def initdb():
    db.create_all()
