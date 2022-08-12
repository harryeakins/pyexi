from pyexi.parser import ExiHandler
from xml import sax
import xmlschema

def test_can_instantiate():
    encoder = ExiHandler()
    assert encoder is not None

def test_can_use_handler():
    handler = ExiHandler()
    sax.parse("tests/fixtures/notebook.xml", handler)
    bitstream = ''.join([item for sublist in handler.output for item in sublist])
    hexstream = [format(int(bitstream[i:i+8], 2), "02x") for i in range(0, len(bitstream), 8)]
    print(handler.events)
