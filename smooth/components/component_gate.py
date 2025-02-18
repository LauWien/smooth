"""
A gate component is created to transform a specific bus into a more
general bus.

*****
Scope
*****
The gate component is a virtual component, so would not be found in a real life
energy system, but is used in the framework as a means of transforming a
specific bus into a more general bus. As an example, it could be useful in an
energy system to initially differentiate between the electricity buses coming
out of each renewable energy source, but at some point in the system it could
become more useful to have only one generic electricity bus defined.

*******
Concept
*******
An oemof Transformer component is used to convert the chosen input bus into the
chosen output bus, with a limitation on the value that can be transformed
per timestep by the defined maximum input parameter. Applying an efficiency
to the conversion of the input bus to the output bus is optional, with the
default value set to 100%.
"""

import oemof.solph as solph
from .component import Component


class Gate(Component):
    """
    :param name: unique name given to the gate component
    :type name: str
    :param max_input: maximum value that the gate can intake per timestep
    :type max_input: numerical
    :param bus_in: bus that enters the gate component
    :type bus_in: str
    :param bus_out: bus that leaves the gate component
    :type bus_out: str
    :param efficiency: efficiency of the gate component
    :type efficiency: numerical
    :param set_parameters(params): updates parameter default values (see generic Component class)
    :type set_parameters(params): function
    """

    def __init__(self, params):
        """Constructor method
        """
        # Call the init function of the mother class.
        Component.__init__(self)

        # ------------------- PARAMETERS -------------------
        self.name = 'Gate_default_name'
        self.max_input = 1e6
        # Busses
        self.bus_in = None
        self.bus_out = None
        self.efficiency = 1

        # ------------------- UPDATE PARAMETER DEFAULT VALUES -------------------
        self.set_parameters(params)

        if self.max_input <= 0:
            raise ValueError("The maximum input of the component must be greater than zero!")

    def add_to_oemof_model(self, busses, model):
        """Creates an oemof Transformer component from information given in
        the Gate class, to be used in the oemof model

        :param busses: virtual buses used in the energy system
        :type busses: dict
        :param model: current oemof model
        :type model: oemof model
        :return: oemof component
        """
        gate = solph.Transformer(
            label=self.name,
            inputs={busses[self.bus_in]: solph.Flow(variable_costs=self.artificial_costs,
                                                    nominal_value=self.max_input)},
            outputs={busses[self.bus_out]: solph.Flow()},
            conversion_factors={busses[self.bus_out]: self.efficiency}
        )

        model.add(gate)
        return gate
