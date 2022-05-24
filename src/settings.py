"""
Creating and maintaining base application settings.
"""

# Python built-in modules
import datetime
import os
from configparser import ConfigParser, ExtendedInterpolation


class Settings:
    """Reads and writes settings."""

    parser = ConfigParser(interpolation=ExtendedInterpolation())
    base_dir = os.path.realpath(os.path.dirname(__file__))
    ini_file = f"{os.path.join(base_dir, 'config.ini')}"

    def __init__(self):
        """Call 'create_ini_file'-method on initialization."""
        self.read_ini_file()

    def read_ini_file(self):
        """Read settings in config-parser object."""
        try:
            self.parser.read(self.ini_file)
        except Exception:
            raise

    def dataset_properties(self, dataset: str) -> dict:
        """Returns a tuple of dataset properties."""
        abbr = self.parser[dataset]["abbr"]
        file_path = self.parser[dataset]["path"]
        full_path = f"{self.base_dir}{file_path}"
        fields_string = self.parser[dataset]["fields"]
        fields = fields_string.split(",")
        the_dict = {"abbr": abbr, "path": full_path, "fields": fields}
        return the_dict

    def app_files_dir(self) -> str:
        """Returns the path for application's csv files."""
        partial_path = self.parser.get("dirs", "app_files")
        the_path = f"{self.base_dir}{partial_path}/"
        return the_path

    def reports_dir(self) -> str:
        """Returns the path for 'reports'."""
        partial_path = self.parser.get("dirs", "reports")
        the_path = f"{self.base_dir}{partial_path}/"
        return the_path

    def set_days_advanced(self, days: int):
        """Set amount of days from current day. Where 0 is today."""
        if not type(days) is int:
            raise TypeError
        self.parser["dates"]["advanced"] = str(days)
        with open(self.ini_file, "w") as file:
            self.parser.write(file)

    def application_date(self, long_date=False) -> str:
        """Get the 'current' application date as ISO standard date or long date notation."""
        days = self.parser.get("dates", "advanced")
        app_date = datetime.date.today() + datetime.timedelta(days=float(days))
        if long_date:
            return app_date.strftime("%d %B %Y")
        else:
            return app_date.strftime("%Y-%m-%d")

    def csv_delimiter(self) -> str:
        """Returns de delimiter in use for csv files."""
        delimiter = self.parser["csv"]["delimiter"]
        return delimiter

    def text_colors(self) -> dict:
        """Returns a dictionary of colors to be used with the Rich module."""
        the_dict = {}
        for key, value in self.parser["text_colors"].items():
            the_dict[key] = value
        return the_dict

    def emojis(self) -> dict:
        """Returns a dictionary of emojis to be used with the Rich module."""
        the_dict = {}
        for key, value in self.parser["emojis"].items():
            the_dict[key] = value
        return the_dict
