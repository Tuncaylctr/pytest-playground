from src.analytics import report_event
from src.decorators import report
from src.weather_source import WeatherAPI


class Weather(object):
    @report
    def temperature(self):
        report_event("Started")
        weather_api = WeatherAPI()
        temperature = weather_api.run()
        report_event("Finished")
        return temperature