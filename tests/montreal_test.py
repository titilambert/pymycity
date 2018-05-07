from io import StringIO
import asyncio
import sys

import pytest

from pymycity.__main__ import main



class TestMontreal(object):

    @pytest.mark.order1
    def test_taxes(self, capsys, event_loop):
        # --help
        sys.argv = ['fake', 'montreal', 'taxes', '-t', 'municipal']

        main()
        out, err = capsys.readouterr()

        assert 'Next municipal taxes for' in out
        assert '' == err
