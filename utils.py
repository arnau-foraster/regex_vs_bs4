# -*- coding: utf-8 -*-
import os


def load_html(path: str) -> str:
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', path)) as html_file:
        return html_file.read()
