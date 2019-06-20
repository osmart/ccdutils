"""Unit tests for checking whether or not depictions are written properly.
"""


import os

import pytest

from pdbeccdutils.core import ccd_reader
from pdbeccdutils.core.depictions import DepictionManager
from pdbeccdutils.tests.tst_utilities import cif_filename


def load_molecule(id_):
    depiction = DepictionManager()
    c = ccd_reader.read_pdb_cif_file(cif_filename(id_)).component
    c.compute_2d(depiction)

    return c


class TestWriteImg:

    @staticmethod
    def test_file_generated(tmpdir):  # tmpdir is a fixture with temporary directory
        mol = load_molecule('ATP')
        path = str(tmpdir.join('atp_test.svg'))
        mol.export_2d_svg(path)

        assert os.path.isfile(path)

    @staticmethod
    @pytest.mark.parametrize("ccd_id,expected,names", [
        ("NAG", 'C8', True),
        ("ATP", 'C5&apos;', True),
        ("08T", 'BE', True),
        ("BCD", 'C66', True),
        ("ATP", '<rect', False),
        ("08T", '<rect', False),
        ("10R", '<rect', False),
        ("0OD", '<rect', False),
    ])
    def test_image_generation_with_names(tmpdir, ccd_id, expected, names):
        mol = load_molecule(ccd_id)
        path = str(tmpdir.join('{}_{}.svg'.format(ccd_id, 'names' if names else 'no_names')))
        mol.export_2d_svg(path, names=names)

        with open(path, 'r') as f:
            content = f.readlines()
        assert any(expected in i for i in content)
