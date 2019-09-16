# coding=utf-8
from honeybee_energy.programtype import ProgramType
from honeybee_energy.load.people import People
from honeybee_energy.load.lighting import Lighting
from honeybee_energy.load.equipment import ElectricEquipment
from honeybee_energy.load.infiltration import Infiltration
from honeybee_energy.load.ventilation import Ventilation
from honeybee_energy.load.setpoint import Setpoint

from honeybee_energy.schedule.day import ScheduleDay
from honeybee_energy.schedule.ruleset import ScheduleRuleset

import honeybee_energy.lib.scheduletypelimits as schedule_types

from ladybug.dt import Time

import json
import pytest


def test_program_type_init():
    """Test the initialization of ProgramType and basic properties."""
    simple_office = ScheduleDay('Simple Weekday Occupancy', [0, 1, 0],
                                [Time(0, 0), Time(9, 0), Time(17, 0)])
    occ_schedule = ScheduleRuleset('Office Occupancy Schedule', simple_office,
                                   None, schedule_types.fractional)
    light_schedule = occ_schedule.duplicate()
    light_schedule.name = 'Office Lighting-Equip Schedule'
    light_schedule.default_day_schedule.values = [0.25, 1, 0.25]
    equip_schedule = light_schedule.duplicate()
    inf_schedule = ScheduleRuleset.from_constant_value(
        'Infiltration Schedule', 1, schedule_types.fractional)
    heat_setpt = ScheduleRuleset.from_constant_value(
        'Office Heating Schedule', 21, schedule_types.temperature)
    cool_setpt = ScheduleRuleset.from_constant_value(
        'Office Cooling Schedule', 24, schedule_types.temperature)

    people = People('Open Office People', 0.05, occ_schedule)
    lighting = Lighting('Open Office Lighting', 10, light_schedule)
    equipment = ElectricEquipment('Open Office Equipment', 10, equip_schedule)
    infiltration = Infiltration('Office Infiltration', 0.00015, inf_schedule)
    ventilation = Ventilation('Office Ventilation', 0.0025, 0.0003)
    setpoint = Setpoint('Office Setpoints', heat_setpt, cool_setpt)
    office_program = ProgramType('Open Office Program', people, lighting, equipment,
                                 None, infiltration, ventilation, setpoint)

    str(office_program)  # test the string representation

    assert office_program.name == 'Open Office Program'
    assert isinstance(office_program.people, People)
    assert office_program.people == people
    assert isinstance(office_program.lighting, Lighting)
    assert office_program.lighting == lighting
    assert isinstance(office_program.electric_equipment, ElectricEquipment)
    assert office_program.electric_equipment == equipment
    assert office_program.gas_equipment is None
    assert isinstance(office_program.infiltration, Infiltration)
    assert office_program.infiltration == infiltration
    assert isinstance(office_program.ventilation, Ventilation)
    assert office_program.ventilation == ventilation
    assert isinstance(office_program.setpoint, Setpoint)
    assert office_program.setpoint == setpoint
    assert len(office_program.schedules) == 7
    assert len(office_program.schedules_unique) == 6


def test_program_type_setability():
    """Test the setting of properties of ProgramType."""
    simple_office = ScheduleDay('Simple Weekday Occupancy', [0, 1, 0],
                                [Time(0, 0), Time(9, 0), Time(17, 0)])
    occ_schedule = ScheduleRuleset('Office Occupancy Schedule', simple_office,
                                   None, schedule_types.fractional)
    light_schedule = occ_schedule.duplicate()
    light_schedule.name = 'Office Lighting-Equip Schedule'
    light_schedule.default_day_schedule.values = [0.25, 1, 0.25]
    equip_schedule = light_schedule.duplicate()
    inf_schedule = ScheduleRuleset.from_constant_value(
        'Infiltration Schedule', 1, schedule_types.fractional)
    heat_setpt = ScheduleRuleset.from_constant_value(
        'Office Heating Schedule', 21, schedule_types.temperature)
    cool_setpt = ScheduleRuleset.from_constant_value(
        'Office Cooling Schedule', 24, schedule_types.temperature)

    people = People('Open Office People', 0.05, occ_schedule)
    lighting = Lighting('Open Office Lighting', 10, light_schedule)
    equipment = ElectricEquipment('Open Office Equipment', 10, equip_schedule)
    infiltration = Infiltration('Office Infiltration', 0.00015, inf_schedule)
    ventilation = Ventilation('Office Ventilation', 0.0025, 0.0003)
    setpoint = Setpoint('Office Setpoints', heat_setpt, cool_setpt)
    office_program = ProgramType('Open Office Program')

    assert office_program.name == 'Open Office Program'
    office_program.name = 'Office Program'
    assert office_program.name == 'Office Program'
    assert office_program.people is None
    office_program.people = people
    assert office_program.people == people
    assert office_program.lighting is None
    office_program.lighting = lighting
    assert office_program.lighting == lighting
    assert office_program.electric_equipment is None
    office_program.electric_equipment = equipment
    assert office_program.electric_equipment == equipment
    assert office_program.infiltration is None
    office_program.infiltration = infiltration
    assert office_program.infiltration == infiltration
    assert office_program.ventilation is None
    office_program.ventilation = ventilation
    assert office_program.ventilation == ventilation
    assert office_program.setpoint is None
    office_program.setpoint = setpoint
    assert office_program.setpoint == setpoint

    with pytest.raises(AssertionError):
        office_program.people = lighting
    with pytest.raises(AssertionError):
        office_program.lighting = equipment
    with pytest.raises(AssertionError):
        office_program.electric_equipment = people
    with pytest.raises(AssertionError):
        office_program.infiltration = people
    with pytest.raises(AssertionError):
        office_program.ventilation = setpoint
    with pytest.raises(AssertionError):
        office_program.setpoint = ventilation


def test_program_type_equality():
    """Test the equality of ProgramType objects."""
    simple_office = ScheduleDay('Simple Weekday Occupancy', [0, 1, 0],
                                [Time(0, 0), Time(9, 0), Time(17, 0)])
    occ_schedule = ScheduleRuleset('Office Occupancy Schedule', simple_office,
                                   None, schedule_types.fractional)
    light_schedule = occ_schedule.duplicate()
    light_schedule.name = 'Office Lighting-Equip Schedule'
    light_schedule.default_day_schedule.values = [0.25, 1, 0.25]
    equip_schedule = light_schedule.duplicate()
    inf_schedule = ScheduleRuleset.from_constant_value(
        'Infiltration Schedule', 1, schedule_types.fractional)
    heat_setpt = ScheduleRuleset.from_constant_value(
        'Office Heating Schedule', 21, schedule_types.temperature)
    cool_setpt = ScheduleRuleset.from_constant_value(
        'Office Cooling Schedule', 24, schedule_types.temperature)

    people = People('Open Office People', 0.05, occ_schedule)
    lighting = Lighting('Open Office Lighting', 10, light_schedule)
    led_lighting = Lighting('LED Office Lighting', 5, light_schedule)
    equipment = ElectricEquipment('Open Office Equipment', 10, equip_schedule)
    infiltration = Infiltration('Office Infiltration', 0.00015, inf_schedule)
    ventilation = Ventilation('Office Ventilation', 0.0025, 0.0003)
    setpoint = Setpoint('Office Setpoints', heat_setpt, cool_setpt)
    office_program = ProgramType('Open Office Program', people, lighting, equipment,
                                 None, infiltration, ventilation, setpoint)
    office_program_dup = office_program.duplicate()
    office_program_alt = ProgramType(
        'Open Office Program', people, led_lighting, equipment,
        None, infiltration, ventilation, setpoint)

    assert office_program is office_program
    assert office_program is not office_program_dup
    assert office_program == office_program_dup
    office_program_dup.people.people_per_area = 0.1
    assert office_program != office_program_dup
    assert office_program != office_program_alt


def test_program_type_lockability():
    """Test the lockability of ProgramType objects."""
    simple_office = ScheduleDay('Simple Weekday Occupancy', [0, 1, 0],
                                [Time(0, 0), Time(9, 0), Time(17, 0)])
    light_schedule = ScheduleRuleset('Office Lighting-Equip Schedule', simple_office,
                                     None, schedule_types.fractional)
    lighting = Lighting('Open Office Lighting', 10, light_schedule)
    led_lighting = Lighting('LED Office Lighting', 5, light_schedule)
    office_program = ProgramType('Open Office Program', lighting=lighting)

    office_program.lighting.watts_per_area = 6
    office_program.lock()
    with pytest.raises(AttributeError):
        office_program.lighting.watts_per_area = 8
    with pytest.raises(AttributeError):
        office_program.lighting = led_lighting
    office_program.unlock()
    office_program.lighting.watts_per_area = 8
    office_program.lighting = led_lighting


def test_program_type_from_standards_dict():
    """Test the from_standards_dict methods."""
    filename = './tests/standards/OpenStudio_Standards_schedules.json'
    if filename:
        with open(filename, 'r') as f:
            data_store = json.load(f)
    program_dict = {
        "template": "90.1-2013",
        "building_type": "Office",
        "space_type": "MediumOffice - OpenOffice",
        "lighting_standard": "ASHRAE 90.1-2013",
        "lighting_per_area": 0.98,
        "lighting_per_person": None,
        "additional_lighting_per_area": None,
        "lighting_fraction_to_return_air": 0.0,
        "lighting_fraction_radiant": 0.7,
        "lighting_fraction_visible": 0.2,
        "lighting_schedule": "OfficeMedium BLDG_LIGHT_SCH_2013",
        "ventilation_standard": "ASHRAE 62.1-2007",
        "ventilation_primary_space_type": "Office Buildings",
        "ventilation_secondary_space_type": "Office space",
        "ventilation_per_area": 0.06,
        "ventilation_per_person": 5.0,
        "ventilation_air_changes": None,
        "minimum_total_air_changes": None,
        "occupancy_per_area": 5.25,
        "occupancy_schedule": "OfficeMedium BLDG_OCC_SCH",
        "occupancy_activity_schedule": "OfficeMedium ACTIVITY_SCH",
        "infiltration_per_exterior_area": 0.0446,
        "infiltration_schedule": "OfficeMedium INFIL_SCH_PNNL",
        "gas_equipment_per_area": None,
        "gas_equipment_fraction_latent": None,
        "gas_equipment_fraction_radiant": None,
        "gas_equipment_fraction_lost": None,
        "gas_equipment_schedule": None,
        "electric_equipment_per_area": 0.96,
        "electric_equipment_fraction_latent": 0.0,
        "electric_equipment_fraction_radiant": 0.5,
        "electric_equipment_fraction_lost": 0.0,
        "electric_equipment_schedule": "OfficeMedium BLDG_EQUIP_SCH_2013",
        "heating_setpoint_schedule": "OfficeMedium HTGSETP_SCH_YES_OPTIMUM",
        "cooling_setpoint_schedule": "OfficeMedium CLGSETP_SCH_YES_OPTIMUM"
    }
    office_program = ProgramType.from_standards_dict(program_dict, data_store)

    assert office_program.name == 'MediumOffice - OpenOffice'
    assert office_program.people.people_per_area == pytest.approx(0.05651, rel=1e-3)
    assert office_program.people.occupancy_schedule.name == 'OfficeMedium BLDG_OCC_SCH'
    assert office_program.people.activity_schedule.name == 'OfficeMedium ACTIVITY_SCH'
    assert office_program.lighting.watts_per_area == pytest.approx(10.548, rel=1e-3)
    assert office_program.lighting.schedule.name == 'OfficeMedium BLDG_LIGHT_SCH_2013'
    assert office_program.lighting.return_air_fraction == pytest.approx(0.0, rel=1e-3)
    assert office_program.lighting.radiant_fraction == pytest.approx(0.7, rel=1e-3)
    assert office_program.lighting.visible_fraction == pytest.approx(0.2, rel=1e-3)
    assert office_program.electric_equipment.watts_per_area == pytest.approx(10.3333, rel=1e-3)
    assert office_program.electric_equipment.schedule.name == 'OfficeMedium BLDG_EQUIP_SCH_2013'
    assert office_program.electric_equipment.latent_fraction == pytest.approx(0.0, rel=1e-3)
    assert office_program.electric_equipment.radiant_fraction == pytest.approx(0.5, rel=1e-3)
    assert office_program.electric_equipment.lost_fraction == pytest.approx(0.0, rel=1e-3)
    assert office_program.gas_equipment is None
    assert office_program.infiltration.flow_per_exterior_area == pytest.approx(0.000226568, rel=1e-3)
    assert office_program.infiltration.schedule.name == 'OfficeMedium INFIL_SCH_PNNL'
    assert office_program.ventilation.flow_per_person == pytest.approx(0.0023597, rel=1e-3)
    assert office_program.ventilation.flow_per_area == pytest.approx(0.0003048, rel=1e-3)
    assert office_program.ventilation.flow_per_zone == pytest.approx(0.0, rel=1e-3)
    assert office_program.ventilation.air_changes_per_hour == pytest.approx(0.0, rel=1e-3)
    assert office_program.setpoint.heating_schedule.name == 'OfficeMedium HTGSETP_SCH_YES_OPTIMUM'
    assert office_program.setpoint.heating_setpoint == pytest.approx(21.0, rel=1e-3)
    assert office_program.setpoint.heating_setback == pytest.approx(15.6, rel=1e-3)
    assert office_program.setpoint.cooling_schedule.name == 'OfficeMedium CLGSETP_SCH_YES_OPTIMUM'
    assert office_program.setpoint.cooling_setpoint == pytest.approx(24.0, rel=1e-3)
    assert office_program.setpoint.cooling_setback == pytest.approx(26.7, rel=1e-3)


def test_program_type_dict_methods():
    """Test the to/from dict methods."""
    simple_office = ScheduleDay('Simple Weekday Occupancy', [0, 1, 0],
                                [Time(0, 0), Time(9, 0), Time(17, 0)])
    occ_schedule = ScheduleRuleset('Office Occupancy Schedule', simple_office,
                                   None, schedule_types.fractional)
    light_schedule = occ_schedule.duplicate()
    light_schedule.name = 'Office Lighting-Equip Schedule'
    light_schedule.default_day_schedule.values = [0.25, 1, 0.25]
    equip_schedule = light_schedule.duplicate()
    inf_schedule = ScheduleRuleset.from_constant_value(
        'Infiltration Schedule', 1, schedule_types.fractional)
    heat_setpt = ScheduleRuleset.from_constant_value(
        'Office Heating Schedule', 21, schedule_types.temperature)
    cool_setpt = ScheduleRuleset.from_constant_value(
        'Office Cooling Schedule', 24, schedule_types.temperature)

    people = People('Open Office People', 0.05, occ_schedule)
    lighting = Lighting('Open Office Lighting', 10, light_schedule)
    equipment = ElectricEquipment('Open Office Equipment', 10, equip_schedule)
    infiltration = Infiltration('Office Infiltration', 0.00015, inf_schedule)
    ventilation = Ventilation('Office Ventilation', 0.0025, 0.0003)
    setpoint = Setpoint('Office Setpoints', heat_setpt, cool_setpt)
    office_program = ProgramType('Open Office Program', people, lighting, equipment,
                                 None, infiltration, ventilation, setpoint)

    prog_dict = office_program.to_dict()
    new_office_program = ProgramType.from_dict(prog_dict)
    assert new_office_program == office_program
    assert prog_dict == new_office_program.to_dict()


def test_program_type_average():
    """Test the ProgramType.average method."""
    simple_office = ScheduleDay('Simple Weekday Occupancy', [0, 1, 0],
                                [Time(0, 0), Time(9, 0), Time(17, 0)])
    occ_schedule = ScheduleRuleset('Office Occupancy Schedule', simple_office,
                                   None, schedule_types.fractional)
    light_schedule = occ_schedule.duplicate()
    light_schedule.name = 'Office Lighting-Equip Schedule'
    light_schedule.default_day_schedule.values = [0.25, 1, 0.25]
    equip_schedule = light_schedule.duplicate()
    inf_schedule = ScheduleRuleset.from_constant_value(
        'Infiltration Schedule', 1, schedule_types.fractional)
    heat_setpt = ScheduleRuleset.from_constant_value(
        'Office Heating Schedule', 21, schedule_types.temperature)
    cool_setpt = ScheduleRuleset.from_constant_value(
        'Office Cooling Schedule', 24, schedule_types.temperature)

    people = People('Open Office People', 0.05, occ_schedule)
    lighting = Lighting('Open Office Lighting', 10, light_schedule)
    equipment = ElectricEquipment('Open Office Equipment', 10, equip_schedule)
    infiltration = Infiltration('Office Infiltration', 0.0002, inf_schedule)
    ventilation = Ventilation('Office Ventilation', 0.005, 0.0003)
    setpoint = Setpoint('Office Setpoints', heat_setpt, cool_setpt)
    office_program = ProgramType('Open Office Program', people, lighting, equipment,
                                 None, infiltration, ventilation, setpoint)
    plenum_program = ProgramType('Plenum Program')

    office_avg = ProgramType.average(
        'Office Average Program', [office_program, plenum_program])

    assert office_avg.people.people_per_area == pytest.approx(0.025, rel=1e-3)
    assert office_avg.people.occupancy_schedule.default_day_schedule.values == \
        office_program.people.occupancy_schedule.default_day_schedule.values
    assert office_avg.people.latent_fraction == \
        office_program.people.latent_fraction
    assert office_avg.people.radiant_fraction == \
        office_program.people.radiant_fraction

    assert office_avg.lighting.watts_per_area == pytest.approx(5, rel=1e-3)
    assert office_avg.lighting.schedule.default_day_schedule.values == \
        office_program.lighting.schedule.default_day_schedule.values
    assert office_avg.lighting.return_air_fraction == \
        office_program.lighting.return_air_fraction
    assert office_avg.lighting.radiant_fraction == \
        office_program.lighting.radiant_fraction
    assert office_avg.lighting.visible_fraction == \
        office_program.lighting.visible_fraction

    assert office_avg.electric_equipment.watts_per_area == pytest.approx(5, rel=1e-3)
    assert office_avg.electric_equipment.schedule.default_day_schedule.values == \
        office_program.electric_equipment.schedule.default_day_schedule.values
    assert office_avg.electric_equipment.radiant_fraction == \
        office_program.electric_equipment.radiant_fraction
    assert office_avg.electric_equipment.latent_fraction == \
        office_program.electric_equipment.latent_fraction
    assert office_avg.electric_equipment.lost_fraction == \
        office_program.electric_equipment.lost_fraction

    assert office_avg.gas_equipment is None

    assert office_avg.infiltration.flow_per_exterior_area == \
        pytest.approx(0.0001, rel=1e-3)
    assert office_avg.infiltration.schedule.default_day_schedule.values == \
        office_program.infiltration.schedule.default_day_schedule.values
    assert office_avg.infiltration.constant_coefficient == \
        office_program.infiltration.constant_coefficient
    assert office_avg.infiltration.temperature_coefficient == \
        office_program.infiltration.temperature_coefficient
    assert office_avg.infiltration.velocity_coefficient == \
        office_program.infiltration.velocity_coefficient

    assert office_avg.ventilation.flow_per_person == pytest.approx(0.0025, rel=1e-3)
    assert office_avg.ventilation.flow_per_area == pytest.approx(0.00015, rel=1e-3)
    assert office_avg.ventilation.flow_per_zone == pytest.approx(0, rel=1e-3)
    assert office_avg.ventilation.air_changes_per_hour == pytest.approx(0, rel=1e-3)
    assert office_avg.ventilation.schedule is None

    assert office_avg.setpoint.heating_setpoint == pytest.approx(21, rel=1e-3)
    assert office_avg.setpoint.cooling_setpoint == pytest.approx(24, rel=1e-3)
