"""Unit tests for checking whether or not depictions are written properly.
"""


import json
import os
import defusedxml.ElementTree as ET

import pytest
from pdbeccdutils.core import ccd_reader
from pdbeccdutils.core.component import Component
from pdbeccdutils.helpers.drawing import save_no_image, svg_namespace
from pdbeccdutils.core.depictions import DepictionManager, DepictionSource
from pdbeccdutils.tests.tst_utilities import cif_filename

collision_free_templates = [
    ("hem", ["HEM", "HEA", "HEB", "HEC", "HDD", "HEG"]),
    ("porphycene", ["HNN", "HME"]),
    ("ru_complex", ["11R"]),
    ("ru_complex", ["11R"]),
    ("phorbine", ["G2O"]),
]

collision_templates = [("cube", ["SF4", "0KA", "1CL"]), ("adamantane", ["ADM"])]

depictions = DepictionManager()


def load_molecule(id_):
    c = ccd_reader.read_pdb_cif_file(cif_filename(id_)).component
    c.compute_2d(depictions)

    return c


class TestWriteImg:
    @staticmethod
    def test_file_generated(tmpdir):  # tmpdir is a fixture with temporary directory
        mol = load_molecule("ATP")
        path = str(tmpdir.join("atp_test.svg"))
        mol.export_2d_svg(path)

        assert os.path.isfile(path)

    @staticmethod
    @pytest.mark.parametrize(
        "ccd_id,expected,names",
        [
            ("NAG", "C8", True),
            ("ATP", "C5&apos;", True),
            ("08T", "BE", True),
            ("BCD", "C66", True),
            ("ATP", "<rect", False),
            ("08T", "<rect", False),
            ("10R", "<rect", False),
            ("0OD", "<rect", False),
        ],
    )
    def test_image_generation_with_names(tmpdir, ccd_id, expected, names):
        mol = load_molecule(ccd_id)
        path = str(tmpdir.join(f"{ccd_id}_{'names' if names else 'no_names'}.svg"))
        mol.export_2d_svg(path, names=names)

        with open(path, "r") as f:
            content = f.readlines()
        assert any(expected in i for i in content)

    @staticmethod
    @pytest.mark.parametrize("expected_template,names", collision_free_templates)
    def test_collision_free_template_picked(expected_template, names):
        """Test if expected templates are picked for certain compounds

        Args:
            expected_template (str): template name.
            names (list of str): list of ids matching this template.
        """
        d = DepictionManager()

        for ccd_id in names:
            mol = load_molecule(ccd_id)
            response = mol.compute_2d(d)

            assert response.source == DepictionSource.Template
            assert response.score == 0
            assert response.template_name == expected_template

    @staticmethod
    @pytest.mark.parametrize("expected_template,names", collision_templates)
    def test_collision_template_picked(expected_template, names):
        """Test if expected templates are picked for certain compounds

        Args:
            expected_template (str): template name.
            names (list of str): list of ids matching this template.
        """
        d = DepictionManager()

        for ccd_id in names:
            mol = load_molecule(ccd_id)
            response = mol.compute_2d(d)

            assert response.source == DepictionSource.Template
            assert response.score > 0
            assert response.template_name == expected_template

    @staticmethod
    def test_svg_annotation(component: Component, tmpdir_factory):
        if not component.atoms_ids:
            return

        json_obj = None
        wd = tmpdir_factory.mktemp("svg_json_test")
        out_file = os.path.join(wd, f"{component.id}.json")
        component.compute_2d(depictions)
        component.export_2d_annotation(out_file)

        assert os.path.isfile(out_file)
        assert os.path.getsize(out_file) > 0

        with open(out_file, "r") as fp:
            json_obj = json.load(fp)

        assert json_obj["ccd_id"] == component.id
        assert json_obj["resolution"]["x"] >= 0
        assert json_obj["resolution"]["y"] >= 0

        atom_names = [atom["name"] for atom in json_obj["atoms"]]
        assert len(json_obj["atoms"]) == component.mol_no_h.GetNumAtoms()
        assert len(json_obj["bonds"]) >= component.mol_no_h.GetNumBonds()
        assert all(atom["name"] for atom in json_obj["atoms"])  # do we have atom names?

        for atom in json_obj["atoms"]:
            for l in atom["labels"]:
                h_tspans = sum(1 for x in l["tspans"] if x == "H")
                assert h_tspans < len(
                    l["tspans"]
                )  # we do not have bare H labels, because we dont have links to them.

        assert all(
            bond["bgn"] in atom_names and bond["end"] in atom_names
            for bond in json_obj["bonds"]
        )  # are all the atoms defined?
        assert all(
            bond["coords"] for bond in json_obj["bonds"]
        )  # do we have coordinates?
        assert all(bond["style"] for bond in json_obj["bonds"])  # and its stylling?

    @staticmethod
    def test_no_image_svg(tmpdir):
        value = "foo"
        svg = str(tmpdir.join("test.svg"))

        save_no_image(svg, default_msg="foo")

        assert os.path.isfile(svg)

        xml = ET.parse(svg)
        text = xml.find("svg:text", svg_namespace)
        assert text.text.strip() == value

    @staticmethod
    def test_no_image_png(tmpdir):
        png = str(tmpdir.join("test.png"))
        save_no_image(png)

        assert os.path.join(png)
