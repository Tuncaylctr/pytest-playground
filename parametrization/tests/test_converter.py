import pytest

from uc.converter import ConversionGraph, Quantity

#  parametrizing fixtures
@pytest.fixture(scope="session",
                params=["bfs","dfs"],)
def unit_registry(request):
    unit_registry = ConversionGraph(search_algo=request.param)

    unit_registry.add_unit(name="m", dimension="Length")
    unit_registry.add_unit(name="cm", dimension="Length")
    unit_registry.add_unit(name="mm", dimension="Length")

    unit_registry.add_linear(u_from="m", u_to="cm", scale=100.0)
    unit_registry.add_linear(u_from="cm", u_to="mm", scale=10.0)
    return unit_registry

# factories as fixtures
@pytest.fixture()
def convert_value(unit_registry):

    def _convert(from_value, from_unit, to_unit) -> float:
        from_quantity = Quantity(from_value, from_unit)
        to_quantity = unit_registry.convert(from_quantity, to_unit)
        return to_quantity.value

    return _convert

# parametrizing tests
@pytest.mark.parametrize(
    "from_unit, from_value, to_unit, expected_value",
    [
        ("m", 1, "mm", 1000.0),
        ("m", 0.5, "mm", 500.0),
        ("m", 5000, "mm", 5000000.0),
    ]
)
def test_conversions_calculation_combined(
        unit_registry, from_unit, from_value, to_unit, expected_value
):
    from_quantity = Quantity(value=from_value, unit=from_unit)
    to_quantity = unit_registry.convert(from_quantity, to_unit)

    assert to_quantity.value == pytest.approx(expected_value)




@pytest.mark.parametrize(
    "from_value, from_unit, to_unit, expected_to_value",
    [
        (1, "m", "mm", 1000.0),
        (0.5, "m", "mm", 500.0),
        (5000, "m", "mm", 5000000.0),
    ]
)
def test_conversions_calculation(
    from_value, from_unit, to_unit, expected_to_value, convert_value):
    to_value = convert_value(from_value, from_unit, to_unit)
    assert to_value == pytest.approx(expected_to_value)



def test_conversion_unknown_units_fails(unit_registry, convert_value):
    from_value = 1
    from_unit = "unknown_unit"
    to_unit = "mm"

    with pytest.raises(KeyError):
        convert_value(from_value, from_unit, to_unit)


def test_conversion_no_conv_path_fails(unit_registry, convert_value):
    from_value = 1
    from_unit = "mi"
    to_unit = "mm"

    with pytest.raises(ValueError):
        convert_value(from_value, from_unit, to_unit)




# didnt implement dynamic parametrization but it has more complex functionalities.
