import logging
import os
from typing import Optional

from flask_cors import CORS
from flask_script import Manager

from .commands import init_cli
from .flaskapp import App
from .graphene_boilerplate.ext import db


def create_app(test_config: Optional[dict] = None) -> App:
    app = App("kostik_study")

    # load config
    configure(app=app, test_config=test_config)

    # extensions
    CORS(app)
    configure_database(app)

    # CLI
    manager = Manager(app)
    init_cli(app, manager)

    return app