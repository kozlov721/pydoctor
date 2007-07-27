import py
from pydoctor import model, astbuilder
from pydoctor.test import test_astbuilder

def processPackage(packname, buildercls=None,
                   systemcls=model.System):
    testpackage = py.magic.autopath().dirpath().join(packname)
    system = systemcls()
    if buildercls is None:
        buildercls = system.defaultBuilder
    builder = buildercls(system)
    system.packages.append(testpackage.strpath)
    system.addDirectory(testpackage.strpath)
    builder.processDirectory(None)
    return system

def test_local_import():
    system = processPackage("localimporttest")
    cls = system.allobjects['localimporttest.mod1.C']
    assert len(system.warnings['local import']) > 0
    assert cls.bases == ['localimporttest.mod2.B']

def test_package_docstring():
    system = processPackage("localimporttest")
    assert (system.allobjects['localimporttest.__init__'].docstring ==
            "DOCSTRING")

def test_modnamedafterbuiltin():
    # well, basically the test is that this doesn't explode:
    system = processPackage("modnamedafterbuiltin")
    # but let's test _something_
    assert system.allobjects['modnamedafterbuiltin.mod.Dict'].baseobjects == [None]

def test_package_docstring():
    system = processPackage("localimporttest")
    assert (system.allobjects['localimporttest.__init__'].docstring ==
            "DOCSTRING")

def test_nestedconfusion():
    system = processPackage("nestedconfusion")
    A = system.allobjects['nestedconfusion.mod.nestedconfusion.A']
    C = system.allobjects['nestedconfusion.mod.C']
    assert A.baseobjects[0] is C

def test_moresystems():
    system = processPackage("basic")
    system2 = model.System()
    system2.moresystems.append(system)
    mod = test_astbuilder.fromText("""
    from basic import mod
    class E(mod.C):
        pass
    """, system=system2)
    E = mod.contents["E"]
    assert E.baseobjects[0] is not None
