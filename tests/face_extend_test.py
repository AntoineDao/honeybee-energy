"""Tests for features add to honeybee by honeybee_energy."""
from honeybee.face import Face
from honeybee.facetype import Wall
from honeybee_energy.properties import EnergyProperties


face = Face.from_vertices('wall_face', [[0, 0, 0], [10, 0, 0], [10, 0, 10], [0, 0, 10]])


def test_energy_properties():
    assert hasattr(face.properties, 'energy')
    assert isinstance(face.properties.energy, EnergyProperties)
    assert face.properties.energy.construction.name == 'generic_wall'

def test_writer_to_idf():
    assert hasattr(face.to, 'energy')
    idf_string = face.to.energy(face)
    assert 'wall_face,' in idf_string
    assert 'BuildingSurface:Detailed,' in idf_string
