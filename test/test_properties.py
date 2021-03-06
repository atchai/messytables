# -*- coding: utf-8 -*-

import unittest
from . import horror_fobj
from messytables.any import any_tableset
from nose.tools import (
    assert_equal,
    assert_false,
    assert_raises,
    assert_true)
import lxml.html

try:
    # Python 2.6 doesn't provide assert_is_instance
    from nose.tools import assert_is_instance, assert_greater_equal
except ImportError:
    from shim26 import assert_is_instance, assert_greater_equal


class TestCellProperties(unittest.TestCase):
    def test_core_properties(self):
        csv = any_tableset(horror_fobj('simple.csv'), extension="csv")
        for table in csv.tables:
            for row in table:
                for cell in row:
                    cell.properties  # vague existence
                    assert_false('anything' in cell.properties)


class TestCoreProperties(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = any_tableset(horror_fobj('rowcolspan.html'),
                                extension="html")
        cls.first_row = list(list(cls.html.tables)[0])[0]
        cls.real_cell = cls.first_row[1]

    def test_properties_implements_in(self):
        assert_true('html' in self.real_cell.properties)
        assert_false('invalid' in self.real_cell.properties)

    def test_properties_implements_keys(self):
        assert_equal(list, type(self.real_cell.properties.keys()))

    def test_properties_implements_items(self):
        self.real_cell.properties.items()

    def test_properties_implements_get(self):
        assert_equal('default', self.real_cell.properties.get(
            'not_in_properties', 'default'))
        assert_equal(None, self.real_cell.properties.get('not_in_properties'))


class TestHtmlProperties(unittest.TestCase):
    # <td colspan='2'> would create one 'real' and one 'fake' cell
    @classmethod
    def setUpClass(cls):
        cls.html = any_tableset(horror_fobj('rowcolspan.html'),
                                extension="html")
        cls.first_row = list(list(cls.html.tables)[0])[0]
        cls.real_cell = cls.first_row[1]
        cls.fake_cell = cls.first_row[2]

    def test_real_cells_have_properties(self):
        assert_greater_equal(
            set(self.real_cell.properties.keys()),
            set(['_lxml', 'html'])
            )

    def test_real_cells_have_lxml_property(self):
        lxml_element = self.real_cell.properties['_lxml']
        assert_is_instance(lxml_element, lxml.etree._Element)
        assert_equal('<td colspan="2">06</td>',
                     lxml.html.tostring(lxml_element))

    def test_real_cell_has_a_colspan(self):
        assert_equal(self.real_cell.properties['colspan'], 2)

    def test_fake_cells_have_no_lxml_property(self):
        assert_raises(KeyError, lambda: self.fake_cell.properties['_lxml'])

    def test_real_cells_have_html_property(self):
        html = self.real_cell.properties['html']
        assert_is_instance(html, basestring)
        assert_equal('<td colspan="2">06</td>', html)

    def test_fake_cells_have_no_html_property(self):
        assert_raises(KeyError, lambda: self.fake_cell.properties['html'])

class TestBrokenColspans(unittest.TestCase):
    def setUp(self):
        self.html = any_tableset(horror_fobj("badcolspan.html"),
                                 extension="html")

    def test_first_row(self):
        first_row = list(list(self.html.tables)[0])[0]
        self.assertEqual([cell.properties['colspan'] for cell in first_row],
                         [1, 1, 1, 1])

    def test_second_row(self):
        second_row = list(list(self.html.tables)[0])[1]
        self.assertEqual([cell.properties['colspan'] for cell in second_row],
                         [1, 1, 1, 1])

    def test_third_row(self):
        third_row = list(list(self.html.tables)[0])[2]
        self.assertEqual([cell.properties['colspan'] for cell in third_row],
                         [1, 1, 1, 1])

    def test_fourth_row(self):
        fourth_row = list(list(self.html.tables)[0])[3]
        self.assertEqual([cell.properties['colspan'] for cell in fourth_row],
                         [1, 1, 1, 1])
