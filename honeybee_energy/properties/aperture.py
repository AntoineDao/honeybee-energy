# coding=utf-8
"""Aperture Energy Properties."""
from ..construction import WindowConstruction
from ..lib.default.room import generic_costruction_set


class ApertureEnergyProperties(object):
    """Energy Properties for Honeybee Aperture.

    Properties:
        construction
        is_construction_set_by_user
    """

    __slots__ = ('_host', '_construction')

    def __init__(self, host, construction=None):
        """Initialize Aperture energy properties.

        Args:
            host: A honeybee_core Aperture object that hosts these properties.
            construction: An optional Honeybee WindowConstruction object for
                the aperture. If None, it will be set by the parent Room ConstructionSet
                or the the Honeybee default generic ConstructionSet.
        """
        self._host = host
        self.construction = construction

    @property
    def host(self):
        """Get the Aperture object hosting these properties."""
        return self._host

    @property
    def construction(self):
        """Get or set Aperture Construction.

        If the Construction is not set on the aperture-level, then it will be assigned
        based on the ConstructionSet assigned to the parent Room.  If there is no
        parent Room or the the parent Room's ConstructionSet has no construction for
        the aperture, it will be assigned using the honeybee default generic
        construction set.
        """
        if self._construction:  # set by user
            return self._construction
        elif self._host.has_parent and self._host.parent.has_parent:  # set by zone
            constr_set = self._host.parent.parent.properties.energy.construction_set
            return constr_set.get_aperture_construction(
                self._host.boundary_condition.name, self._host.type.name,
                self._host.parent.type.name)
        elif self._host.has_parent:  # generic but influenced by parent face
            return generic_costruction_set.get_aperture_construction(
                self._host.boundary_condition.name, self._host.type.name,
                self._host.parent.type.name)
        else:
            return generic_costruction_set.get_aperture_construction(
                self._host.boundary_condition.name, self._host.type.name, 'Wall')

    @construction.setter
    def construction(self, value):
        if value is not None:
            assert isinstance(value, WindowConstruction), \
                'Expected Window Construction for aperture. Got {}'.format(type(value))
            value.lock()  # lock editing in case construction has multiple references
        self._construction = value

    @property
    def is_construction_set_by_user(self):
        """Check if construction is set by user."""
        return self._construction is not None

    def to_dict(self, abridged=False):
        """Return energy properties as a dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
        """
        base = {'energy': {}}
        base['energy']['type'] = 'ApertureEnergyProperties' if not \
            abridged else 'ApertureEnergyPropertiesAbridged'
        if self._construction is not None:
            base['energy']['construction'] = \
                self._construction.name if abridged else self._construction.to_dict()
        return base

    def duplicate(self, new_host=None):
        """Get a copy of this object.

        new_host: A new Aperture object that hosts these properties.
            If None, the properties will be duplicated with the same host.
        """
        _host = new_host or self._host
        return ApertureEnergyProperties(_host, self._construction)

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return 'Aperture Energy Properties:\n Construction:{}'.format(
            self.construction.name)
