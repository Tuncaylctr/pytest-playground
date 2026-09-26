from hypothesis import given, strategies as st

from uc.converter import ConversionGraph, Quantity


@given(
    from_value=st.floats(),
    from_unit=st.sampled_from(["m", "cm", "mm", "km"]),
    to_unit=st.sampled_from(["m", "cm", "mm", "km"]),
)
def test_linear_conversion(from_value, from_unit, to_unit):
    print(f"{from_value=} {from_unit=} {to_unit=}")
    unit_registry = ConversionGraph()

    unit_registry.add_unit(name="km", dimension="Length")
    unit_registry.add_unit(name="m", dimension="Length")
    unit_registry.add_unit(name="cm", dimension="Length")
    unit_registry.add_unit(name="mm", dimension="Length")

    unit_registry.add_linear(u_from="m", u_to="cm", scale=100.0)
    unit_registry.add_linear(u_from="cm", u_to="mm", scale=10.0)
    unit_registry.add_linear(u_from="km", u_to="m", scale=1000000)

    from_quantity = Quantity(from_value, unit=from_unit)
    unit_registry.convert(from_quantity, to_unit=to_unit)