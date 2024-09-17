from flask_appbuilder import AppBuilder, expose, BaseView
import nbformat
from nbconvert import HTMLExporter


def convert_notebook_to_html(path_to_notebook):
    with open(path_to_notebook) as f:
        nb = nbformat.read(f, as_version=4)
    exporter = HTMLExporter()
    body, _ = exporter.from_notebook_node(nb)
    return body

