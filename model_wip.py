"""
Python model 'model_wip.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Delay, Integ
from pysd.py_backend.lookups import HardcodedLookups
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 1,
    "final_time": lambda: 24,
    "time_step": lambda: 0.25,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Quarter", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Quarter", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Quarter",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Quarter",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Constrained Defence Spending",
    units="billionEuro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "willingness_to_spend_lookup": 1,
        "defence_spending_rate": 1,
        "stress_to_willingness": 1,
    },
)
def constrained_defence_spending():
    return (
        willingness_to_spend_lookup()
        * defence_spending_rate()
        / stress_to_willingness()
    )


@component.add(
    name="critical metals lookup",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "critical_metals_rate": 1},
)
def critical_metals_lookup():
    return critical_metals_rate(time())


@component.add(
    name="critical metals rate",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_critical_metals_rate"},
)
def critical_metals_rate(x, final_subs=None):
    return _hardcodedlookup_critical_metals_rate(x, final_subs)


_hardcodedlookup_critical_metals_rate = HardcodedLookups(
    [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 12.0, 16.0, 20.0, 24.0, 25.0],
    [
        0.06,
        0.07968,
        0.083787,
        0.082347,
        0.12,
        0.12,
        0.12,
        0.12,
        0.12,
        0.092373,
        0.100053,
        0.1056,
        0.1,
        0.1,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_critical_metals_rate",
)


@component.add(
    name="Order Backlog",
    units="billionEuro",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_order_backlog": 1},
    other_deps={
        "_integ_order_backlog": {
            "initial": {},
            "step": {"rate_of_new_orders": 1, "rate_of_orders_fulfilled": 1},
        }
    },
)
def order_backlog():
    return _integ_order_backlog()


_integ_order_backlog = Integ(
    lambda: rate_of_new_orders() - rate_of_orders_fulfilled(),
    lambda: 63,
    "_integ_order_backlog",
)


@component.add(
    name="Cumulative Earnings",
    units="billionEuro",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_earnings": 1},
    other_deps={
        "_integ_cumulative_earnings": {
            "initial": {},
            "step": {
                "rate_of_orders_fulfilled": 1,
                "rate_of_expenses": 1,
                "tax_rate": 1,
            },
        }
    },
)
def cumulative_earnings():
    return _integ_cumulative_earnings()


_integ_cumulative_earnings = Integ(
    lambda: (rate_of_orders_fulfilled() - rate_of_expenses()) * (1 - tax_rate()),
    lambda: 2,
    "_integ_cumulative_earnings",
)


@component.add(
    name="energy rate",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_energy_rate"},
)
def energy_rate(x, final_subs=None):
    return _hardcodedlookup_energy_rate(x, final_subs)


_hardcodedlookup_energy_rate = HardcodedLookups(
    [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0,
        12.0,
        16.0,
        20.0,
        24.0,
        25.0,
    ],
    [
        0.08,
        0.084446,
        0.085477,
        0.097252,
        0.102741,
        0.087448,
        0.092568,
        0.100637,
        0.102526,
        0.086366,
        0.090696,
        0.095644,
        0.085999,
        0.08947,
        0.087719,
        0.087719,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_energy_rate",
)


@component.add(
    name="rate of orders fulfilled",
    units="billionEuro",
    comp_type="Stateful",
    comp_subtype="Delay",
    depends_on={"_delay_rate_of_orders_fulfilled": 1},
    other_deps={
        "_delay_rate_of_orders_fulfilled": {
            "initial": {
                "delivery_lookup": 1,
                "order_backlog": 1,
                "delay_in_delivery": 1,
            },
            "step": {"delivery_lookup": 1, "order_backlog": 1, "delay_in_delivery": 1},
        }
    },
)
def rate_of_orders_fulfilled():
    return _delay_rate_of_orders_fulfilled()


_delay_rate_of_orders_fulfilled = Delay(
    lambda: delivery_lookup() * order_backlog(),
    lambda: delay_in_delivery(),
    lambda: delivery_lookup() * order_backlog(),
    lambda: 1,
    time_step,
    "_delay_rate_of_orders_fulfilled",
)


@component.add(
    name="shock to feedstock",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 2, "geopolitical_shock_probability": 1},
)
def shock_to_feedstock():
    """
    seed is 42
    """
    return if_then_else(
        float(np.random.uniform(0, 1, size=())) < geopolitical_shock_probability(),
        lambda: float(np.random.uniform(1, 3, size=())),
        lambda: 1,
    )


@component.add(
    name="stress to willingness",
    units="Dmnl",
    limits=(1.0, 3.0, 0.5),
    comp_type="Constant",
    comp_subtype="Normal",
)
def stress_to_willingness():
    return 1


@component.add(
    name="structural metals lookup",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "structural_metals_rate": 1},
)
def structural_metals_lookup():
    return structural_metals_rate(time())


@component.add(
    name="energy costs lookup",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "energy_rate": 1},
)
def energy_costs_lookup():
    return energy_rate(time())


@component.add(
    name="geopolitical shock probability",
    units="Dmnl",
    limits=(0.1, 1.0, 0.2),
    comp_type="Constant",
    comp_subtype="Normal",
)
def geopolitical_shock_probability():
    """
    10% chance per quarter of a geopolitical shock
    """
    return 0.1


@component.add(
    name="rate of expenses",
    units="billionEuro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "rate_of_orders_fulfilled": 1,
        "critical_metals_lookup": 1,
        "energy_costs_lookup": 1,
        "shock_to_feedstock": 1,
        "fixed_costs": 1,
        "structural_metals_lookup": 1,
    },
)
def rate_of_expenses():
    return rate_of_orders_fulfilled() * (
        (critical_metals_lookup() + energy_costs_lookup() + structural_metals_lookup())
        * shock_to_feedstock()
        + fixed_costs()
    )


@component.add(
    name="structural metals rate",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_structural_metals_rate"},
)
def structural_metals_rate(x, final_subs=None):
    return _hardcodedlookup_structural_metals_rate(x, final_subs)


_hardcodedlookup_structural_metals_rate = HardcodedLookups(
    [1.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 25.0],
    [0.12, 0.1276, 0.1352, 0.1382, 0.1446, 0.1488, 0.153, 0.153],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_structural_metals_rate",
)


@component.add(
    name="willingness to spend lookup",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"cumulative_defence_spending": 1},
)
def willingness_to_spend_lookup():
    return np.interp(
        cumulative_defence_spending(),
        [0.0, 200.0, 400.0, 600.0, 800.0, 1000.0],
        [1.0, 0.9, 0.85, 0.8, 0.75, 0.7],
    )


@component.add(
    name="Cumulative Defence Spending",
    units="billionEuro",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_cumulative_defence_spending": 1},
    other_deps={
        "_integ_cumulative_defence_spending": {
            "initial": {},
            "step": {"defence_spending_rate": 1},
        }
    },
)
def cumulative_defence_spending():
    return _integ_cumulative_defence_spending()


_integ_cumulative_defence_spending = Integ(
    lambda: defence_spending_rate(), lambda: 0, "_integ_cumulative_defence_spending"
)


@component.add(
    name="Defence Spending",
    units="billionEuro",
    comp_type="Auxiliary",
    comp_subtype="with Lookup",
    depends_on={"time": 1},
)
def defence_spending():
    return np.interp(
        time(),
        [
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
            11.0,
            12.0,
            13.0,
            14.0,
            15.0,
            16.0,
            17.0,
            18.0,
            19.0,
            20.0,
            21.0,
            22.0,
            23.0,
            24.0,
        ],
        [
            43.03,
            43.03,
            43.03,
            43.03,
            43.68,
            43.68,
            43.68,
            43.68,
            44.33,
            44.33,
            44.33,
            44.33,
            45.0,
            45.0,
            45.0,
            45.0,
            45.67,
            45.67,
            45.67,
            45.67,
            46.36,
            46.36,
            46.36,
            46.36,
        ],
    )


@component.add(
    name="defence spending rate",
    units="billionEuro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"defence_spending": 1},
)
def defence_spending_rate():
    return defence_spending()


@component.add(
    name="delay in delivery",
    units="Dmnl",
    limits=(1.0, 20.0, 0.25),
    comp_type="Constant",
    comp_subtype="Normal",
)
def delay_in_delivery():
    return 1


@component.add(
    name="delivery lookup",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time": 1, "delivery_rate": 1},
)
def delivery_lookup():
    return delivery_rate(time())


@component.add(
    name="tax rate", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def tax_rate():
    return 0.3


@component.add(
    name="fixed costs",
    units="Dmnl",
    limits=(0.3, 0.57, 0.2),
    comp_type="Constant",
    comp_subtype="Normal",
)
def fixed_costs():
    """
    these are inflation dependent and with a 2% inflation can be assumed constant
    """
    return 0.57


@component.add(
    name="rate of new orders",
    units="billionEuro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"constrained_defence_spending": 1, "market_share": 1},
)
def rate_of_new_orders():
    return constrained_defence_spending() * market_share()


@component.add(
    name="market share", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def market_share():
    """
    Rheinmettal's market share
    """
    return 0.15


@component.add(
    name="delivery rate",
    units="Dmnl",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_delivery_rate"},
)
def delivery_rate(x, final_subs=None):
    return _hardcodedlookup_delivery_rate(x, final_subs)


_hardcodedlookup_delivery_rate = HardcodedLookups(
    [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
        8.0,
        9.0,
        10.0,
        11.0,
        12.0,
        13.0,
        14.0,
        15.0,
        16.0,
        17.0,
        18.0,
        19.0,
        20.0,
        21.0,
        22.0,
        23.0,
        24.0,
    ],
    [
        0.04,
        0.04,
        0.04,
        0.04,
        0.042,
        0.042,
        0.042,
        0.042,
        0.0441,
        0.0441,
        0.0441,
        0.0441,
        0.0463,
        0.0463,
        0.0463,
        0.0463,
        0.0486,
        0.0486,
        0.0486,
        0.0486,
        0.051,
        0.051,
        0.051,
        0.051,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_delivery_rate",
)
