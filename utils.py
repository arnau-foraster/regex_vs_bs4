# -*- coding: utf-8 -*-
import os


def load_html(path: str) -> str:  #Encoding for cross-compatibility with windows
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', path), encoding="utf8") as html_file:
        return html_file.read()
