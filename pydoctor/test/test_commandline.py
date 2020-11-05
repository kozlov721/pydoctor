from io import StringIO
import sys

from pydoctor import driver

from . import CapSys


def geterrtext(*options: str) -> str:
    """
    Run CLI with options and return the output triggered by system exit.
    """
    se = sys.stderr
    f = StringIO()
    print(options)
    sys.stderr = f
    try:
        try:
            driver.main(list(options))
        except SystemExit:
            pass
        else:
            assert False, "did not fail"
    finally:
        sys.stderr = se
    return f.getvalue()

def test_invalid_option() -> None:
    err = geterrtext('--no-such-option')
    assert 'no such option' in err

def test_cannot_advance_blank_system() -> None:
    err = geterrtext('--make-html')
    assert 'forget an --add-package?' in err

def test_no_systemclasses_py3() -> None:
    err = geterrtext('--system-class')
    assert 'requires 1 argument' in err

def test_invalid_systemclasses() -> None:
    err = geterrtext('--system-class=notdotted')
    assert 'dotted name' in err
    err = geterrtext('--system-class=no-such-module.System')
    assert 'could not import module' in err
    err = geterrtext('--system-class=pydoctor.model.Class')
    assert 'is not a subclass' in err


def test_projectbasedir() -> None:
    """
    The --project-base-dir option should set the projectbasedirectory attribute
    on the options object.
    """
    value = "projbasedirvalue"
    options, args = driver.parse_args([
            "--project-base-dir", value])
    assert str(options.projectbasedirectory) == value


def test_cache_disabled_by_default() -> None:
    """
    Intersphinx object caching is disabled by default.
    """
    parser = driver.getparser()
    (options, _) = parser.parse_args([])
    assert not options.enable_intersphinx_cache


def test_cli_warnings_on_error() -> None:
    """
    The --warnings-as-errors option is disabled by default.
    This is the test for the long form of the CLI option.
    """
    options, args = driver.parse_args([])
    assert options.warnings_as_errors == False

    options, args = driver.parse_args(['--warnings-as-errors'])
    assert options.warnings_as_errors == True


def test_main_return_zero_on_warnings(capsys: CapSys) -> None:
    """
    By default it will return 0 as exit code even when there are warnings.
    """
    exit_code = driver.main(args=[
        '-v', '--testing',
        'pydoctor/test/testpackages/basic/'
        ])

    assert exit_code == 0
    assert '. guessing "basic" for project name' in capsys.readouterr().out


def test_main_return_non_zero_on_warnings(capsys: CapSys) -> None:
    """
    When `-W` is used it returns 3 as exit code even when there are warnings.
    """
    exit_code = driver.main(args=[
        '-W',
        '-v', '--testing',
        'pydoctor/test/testpackages/basic/'
        ])

    assert exit_code == 3
    assert '. guessing "basic" for project name' in capsys.readouterr().out
