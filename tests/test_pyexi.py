from pyexi.pyexi import ExiEncoder

def test_can_instantiate():
    encoder = ExiEncoder()
    assert encoder is not None
