def test_setup(machine, micropython):
    import boilerplate
    boilerplate.Boilerplate(machine.I2C())


def test_version():
    import boilerplate
    assert boilerplate.__version__ == '0.0.1'