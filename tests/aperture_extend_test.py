"""Tests the features that honeybee_energy adds to honeybee_core Aperture."""
from honeybee.aperture import Aperture
from honeybee.aperturetype import aperture_types

from honeybee_energy.properties.aperture import ApertureEnergyProperties
from honeybee_energy.construction import WindowConstruction
from honeybee_energy.material.glazing import EnergyWindowMaterialGlazing
from honeybee_energy.material.gas import EnergyWindowMaterialGas

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D

import pytest


def test_energy_properties():
    """Test the existence of the Aperture energy properties."""
    aperture = Aperture.from_vertices(
        'wall_aperture', [[0, 0, 1], [10, 0, 1], [10, 0, 2], [0, 0, 2]])
    assert hasattr(aperture.properties, 'energy')
    assert isinstance(aperture.properties.energy, ApertureEnergyProperties)
    assert isinstance(aperture.properties.energy.construction, WindowConstruction)
    assert not aperture.properties.energy.is_construction_set_by_user


def test_default_constructions():
    """Test the auto-assigning of constructions by boundary condition."""
    vertices_wall = [[0, 0, 0], [0, 10, 0], [0, 10, 3], [0, 0, 3]]
    vertices_wall_2 = list(reversed(vertices_wall))
    vertices_floor = [[0, 0, 0], [0, 10, 0], [10, 10, 0], [10, 0, 0]]
    vertices_roof = [[10, 0, 3], [10, 10, 3], [0, 10, 3], [0, 0, 3]]

    wa = Aperture.from_vertices('wall window', vertices_wall)
    assert wa.properties.energy.construction.name == 'Generic Double Pane Window'

    wa2 = Aperture.from_vertices('wall window2', vertices_wall_2)
    wa.set_adjacency(wa2)
    assert wa.properties.energy.construction.name == 'Generic Single Pane Window'

    ra = Aperture.from_vertices('roof window', vertices_roof)
    assert ra.properties.energy.construction.name == 'Generic Double Pane Window'
    fa = Aperture.from_vertices('floor window', vertices_floor)
    assert fa.properties.energy.construction.name == 'Generic Double Pane Window'


def test_set_construction():
    """Test the setting of a construction on an Aperture."""
    vertices_wall = [[0, 0, 0], [0, 10, 0], [0, 10, 3], [0, 0, 3]]
    clear_glass = EnergyWindowMaterialGlazing(
        'Clear Glass', 0.005715, 0.770675, 0.07, 0.8836, 0.0804,
        0, 0.84, 0.84, 1.0)
    gap = EnergyWindowMaterialGas('air gap', thickness=0.0127)
    triple_pane = WindowConstruction(
        'Triple Pane', [clear_glass, gap, clear_glass, gap, clear_glass])

    aperture = Aperture.from_vertices('wall window', vertices_wall)
    aperture.properties.energy.construction = triple_pane

    assert aperture.properties.energy.construction == triple_pane
    assert aperture.properties.energy.is_construction_set_by_user

    with pytest.raises(AttributeError):
        aperture.properties.energy.construction[0].thickness = 0.1


def test_duplicate():
    """Test what happens to energy properties when duplicating an Aperture."""
    verts = [Point3D(0, 0, 0), Point3D(10, 0, 0), Point3D(10, 0, 10), Point3D(0, 0, 10)]
    clear_glass = EnergyWindowMaterialGlazing(
        'Clear Glass', 0.005715, 0.770675, 0.07, 0.8836, 0.0804,
        0, 0.84, 0.84, 1.0)
    gap = EnergyWindowMaterialGas('air gap', thickness=0.0127)
    triple_pane = WindowConstruction(
        'Triple Pane', [clear_glass, gap, clear_glass, gap, clear_glass])

    aperture_original = Aperture('wall window', Face3D(verts))
    aperture_dup_1 = aperture_original.duplicate()

    assert aperture_original.properties.energy.host is aperture_original
    assert aperture_dup_1.properties.energy.host is aperture_dup_1
    assert aperture_original.properties.energy.host is not \
        aperture_dup_1.properties.energy.host

    assert aperture_original.properties.energy.construction == \
        aperture_dup_1.properties.energy.construction
    aperture_dup_1.properties.energy.construction = triple_pane
    assert aperture_original.properties.energy.construction != \
        aperture_dup_1.properties.energy.construction

    aperture_dup_2 = aperture_dup_1.duplicate()

    assert aperture_dup_1.properties.energy.construction == \
        aperture_dup_2.properties.energy.construction
    aperture_dup_2.properties.energy.construction = None
    assert aperture_dup_1.properties.energy.construction != \
        aperture_dup_2.properties.energy.construction


def test_to_dict():
    """Test the Aperture to_dict method with energy properties."""
    aperture = Aperture.from_vertices(
        'wall_window', [[0, 0, 0], [10, 0, 0], [10, 0, 10], [0, 0, 10]])
    clear_glass = EnergyWindowMaterialGlazing(
        'Clear Glass', 0.005715, 0.770675, 0.07, 0.8836, 0.0804,
        0, 0.84, 0.84, 1.0)
    gap = EnergyWindowMaterialGas('air gap', thickness=0.0127)
    triple_pane = WindowConstruction(
        'Triple Pane', [clear_glass, gap, clear_glass, gap, clear_glass])

    ad = aperture.to_dict()
    assert 'properties' in ad
    assert ad['properties']['type'] == 'ApertureProperties'
    assert 'energy' in ad['properties']
    assert ad['properties']['energy']['type'] == 'ApertureEnergyProperties'

    aperture.properties.energy.construction = triple_pane
    ad = aperture.to_dict()
    assert 'construction' in ad['properties']['energy']
    assert ad['properties']['energy']['construction'] is not None


def test_aperture_type():
    """Test the assigning of aperture type."""
    vertices_wall = [[0, 0, 0], [0, 10, 0], [0, 10, 3], [0, 0, 3]]
    wa = Aperture.from_vertices('wall window', vertices_wall)

    assert wa.type == aperture_types.window
    wa.type = aperture_types.operable_window()
    assert wa.type == aperture_types.operable_window()
    wa.type = aperture_types.glass_door
    assert wa.type == aperture_types.glass_door
