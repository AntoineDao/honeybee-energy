# coding=utf-8
from honeybee_energy.schedule.typelimit import ScheduleTypeLimit
from ladybug.datatype import fraction

import json
import pytest


def test_schedule_typelimit_init():
    """Test the initialization of ScheduleTypeLimit and basic properties."""
    fractional = ScheduleTypeLimit('Fractional', 0, 1, 'Continuous', 'Dimensionless')
    str(fractional)  # test the string representation

    assert fractional.name == 'Fractional'
    assert fractional.lower_limit == 0
    assert fractional.upper_limit == 1
    assert fractional.numeric_type == 'Continuous'
    assert fractional.unit_type == 'Dimensionless'
    assert isinstance(fractional.data_type, fraction.Fraction)
    assert fractional.unit == 'fraction'


def test_schedule_typelimit_equality():
    """Test the equality of ScheduleTypeLimit objects."""
    fractional = ScheduleTypeLimit('Fractional', 0, 1, 'Continuous', 'Dimensionless')
    fract_dup = fractional.duplicate()
    temperature = ScheduleTypeLimit('Temperature', -273.15, None, 'Continuous', 'Temperature')

    assert fractional == fract_dup
    assert fractional != temperature


def test_schedule_typelimit_to_from_idf():
    """Test the ScheduleTypeLimit to_idf and from_idf methods."""
    temperature = ScheduleTypeLimit('Temperature', -273.15, None, 'Continuous', 'Temperature')

    temp_string = temperature.to_idf()
    rebuilt_temperature = ScheduleTypeLimit.from_idf(temp_string)
    rebuilt_temp_string = rebuilt_temperature.to_idf()

    assert rebuilt_temperature == temperature
    assert rebuilt_temp_string == temp_string


def test_schedule_ruleset_dict_methods():
    """Test the ScheduleRuleset to/from dict methods."""
    temperature = ScheduleTypeLimit('Temperature', -273.15, None, 'Continuous', 'Temperature')

    temp_dict = temperature.to_dict()
    new_temperature = ScheduleTypeLimit.from_dict(temp_dict)
    assert new_temperature == temperature
    assert temp_dict == new_temperature.to_dict()

    """
    f_dir = 'C:/Users/chris/Documents/GitHub/energy-model-schema/app/models/samples/json'
    dest_file = f_dir + '/scheduletypelimit_temperature.json'
    with open(dest_file, 'w') as fp:
        json.dump(temp_dict, fp, indent=4)
    """
