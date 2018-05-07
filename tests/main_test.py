from io import StringIO
import sys

import pytest

from pymycity.__main__ import main


class TestCli(object):

    @pytest.mark.order1
    def test_help(self, capsys):
        # pymycity
        sys.argv = ['pymycity']
        main()
        out, err = capsys.readouterr()
        assert 'usage: ' in out
        assert '' == err
        # pymycity --help
        sys.argv = ['pymycity', '--help']
        with pytest.raises(SystemExit):
            main()
        out, err = capsys.readouterr()
        assert 'usage: ' in out
        assert '' == err
        # pymycity mascouche
        sys.argv = ['pymycity', 'mascouche']
        main()
        out, err = capsys.readouterr()
        assert 'usage:' in out
        assert '' == err
