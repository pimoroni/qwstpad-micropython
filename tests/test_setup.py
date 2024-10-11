def test_setup(machine, micropython):
    import qwstpad
    qwstpad.QwSTPad(machine.I2C())


def test_version():
    import qwstpad
    assert qwstpad.__version__ == '0.0.1'