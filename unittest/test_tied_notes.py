import sys
sys.path += ["../"]

from mingus.containers.Bar import Bar
from mingus.containers.Note import Note, NotesNotTieable
from mingus.containers.NoteContainer import NoteContainer
from mingus.containers.mt_exceptions import MeterFormatError
import unittest

class test_tied_notes(unittest.TestCase):

    def setUp(self):
        self.bar1 = Bar()
        self.bar2 = Bar()

    def test_tie_note(self):
        n = Note('G')
        m = Note('G', tie_note=n)
        self.bar1.place_notes('C', 2)
        self.bar1.place_notes('G', 4)
        self.bar1.place_notes(n, 4)
        self.bar2.place_notes(m, 4)
        self.bar2.place_notes('C', 2)

        self.assertEqual(m.tie_note(), n)
        self.assertEqual(n.next_note(), m)
        self.assertTrue(n.is_tied())
        self.assertTrue(m.is_last_tied())

    def test_tie_together(self):
        n = Note('G')
        m = Note('G')
        m.tie_together(n)
        self.bar1.place_notes('C', 2)
        self.bar1.place_notes('G', 4)
        self.bar1.place_notes(n, 4)
        self.bar2.place_notes(m, 4)
        self.bar2.place_notes('C', 2)

        self.assertEqual(m.tie_note(), n)
        self.assertEqual(n.next_note(), m)
        self.assertTrue(n.is_tied())
        self.assertTrue(m.is_last_tied())

    def test_not_tieable(self):
        def different_note():
            n = Note('G')
            m = Note('C')
            m.tie_together(n)
        def different_channel():
            n = Note('G')
            m = Note('G', dynamics={'channel': n.channel+1})
            m.tie_together(n)
        self.assertRaises(NotesNotTieable, different_note)
        self.assertRaises(NotesNotTieable, different_channel)

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(test_tied_notes)
