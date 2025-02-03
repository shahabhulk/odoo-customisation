from odoo import api, models, fields
import requests


class WeatherCity(models.Model):
    _name = "weather.city"
    _description = "Weather Information"

    name = fields.Char(string="City Name", required=True)
    temperature = fields.Float(string="Temperature (°C)")
    weather_description = fields.Char(string="Weather Description")
    last_updated = fields.Datetime(string="Last Updated", readonly=True)

    @api.model
    def fetch_weather(self, city_name):
        api_key = "e3d3159525bd69d2375107f9add7e6b7"  # Replace with a real API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            weather_data = {
                "temperature": data["main"]["temp"],
                "weather_description": data["weather"][0]["description"],
                "last_updated": fields.Datetime.now(),
            }
            return weather_data
        else:
            return {"error": "City not found or API error"}

    def update_weather(self):
        for record in self:
            weather_data = self.fetch_weather(record.name)
            if "error" not in weather_data:
                record.write(weather_data)
