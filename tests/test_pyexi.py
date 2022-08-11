from pyexi.pyexi import ExiEncoder, ExiSchemaHandler
from xml import sax
import xmlschema

def test_can_instantiate():
    encoder = ExiEncoder()
    assert encoder is not None

def test_can_use_handler():
    # sax.parse("tests/fixtures/notebook.xsd", ExiSchemaHandler())
    schema = xmlschema.XMLSchema("tests/fixtures/notebook.xsd")
    for name in schema.elements:
        element = schema.elements[name]
        print(element)
        print(element.type)