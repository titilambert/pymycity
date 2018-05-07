from io import StringIO
import asyncio
import sys

import pytest

from pymycity.__main__ import main



class TestMascouche(object):

    @pytest.mark.order1
    def test_taxes(self, capsys, event_loop):
        # pymycity -c 1 mascouche taxes -t municipal
        sys.argv = ['pymycity', '-c', '1', 'mascouche', 'taxes', '-t', 'municipale']
        main()
        out, err = capsys.readouterr()
        assert 'Next municipale taxes for' in out
        assert '' == err

    @pytest.mark.order2
    def test_garbage(self, capsys, event_loop):
        # pymycity -a garbage_collection taxes -t waste
        sys.argv = ['pymycity', '-a', 'mascouche', 'garbage_collection', '-t', 'déchets' ]
        main()
        out, err = capsys.readouterr()
        assert 'Next déchets collection for' in out
        assert '' == err

    @pytest.mark.order3
    def test_event(self, capsys, event_loop):
        # pymycity garbage_collection events
        sys.argv = ['pymycity', 'mascouche', 'events']
        main()
        out, err = capsys.readouterr()
        assert 'Next all events for' in out
        assert '' == err
        # pymycity garbage_collection events
        sys.argv = ['pymycity', 'mascouche', 'events', '-t', 'Bibliothèque']
        main()
        out, err = capsys.readouterr()
        assert 'Next Bibliothèque events for' in out
        assert '' == err
