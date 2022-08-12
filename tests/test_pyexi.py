from pyexi.parser import ExiHandler
from xml import sax
import xmlschema

def test_can_instantiate():
    encoder = ExiHandler()
    assert encoder is not None

def test_can_use_handler():
    handler = ExiHandler()
    sax.parse("tests/fixtures/notebook.xml", handler)
    print(handler.events)
