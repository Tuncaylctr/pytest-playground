import pytest


# Mock the decorator before importing Weather because decorators are applied
# at import time (when the module is loaded). If we import Weather at the top
# of the file, the real decorator would run before we have a chance to mock it.
# By mocking first and then importing inside the fixture, we ensure our mock
# is in place when the decorator is applied to the Weather class.
@pytest.fixture()
def weather_class(mocker):
    mocker.patch(
        "src.decorators.report",
        side_effect=lambda f: f,

    )
    from src.weather import Weather
    return  Weather


def test_temperature(mocker, weather_class):
    from src.analytics import report_event
    mock_get_temperature = mocker.patch(
        "src.weather_source.get_temperature",
        return_value=1
    )
    # useful when  we need reuse the same mock across multiple patches
    shared = mocker.create_autospec(
        report_event,
        spec_set=True,
        return_value=None,
    )

    m1 = mocker.patch(
        "src.weather.report_event",
        new=shared,
    )
    m2 = mocker.patch(
        "src.weather_source.report_event",
         new=shared,
    )

    weather = weather_class()
    assert weather.temperature() == 1
    mock_get_temperature.assert_called_once()

    assert shared.call_count == 3