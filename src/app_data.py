"""Creating, Reading and Updating of csv files."""

# Python built-in modules:
import csv
import os.path

# Local modules:
import settings


class ReadWriteCSV:
    """Read and write csv files."""

    def __init__(self, dataset_properties: dict):
        """Create needed variables and call create_csv_file method."""
        self.abbr = dataset_properties["abbr"]
        self.path = dataset_properties["path"]
        self.fields = dataset_properties["fields"]
        self.cfg = settings.Settings()
        self.delimiter = self.cfg.csv_delimiter()
        self.create_csv_file()

    def create_csv_file(self):
        """Create new csv file with header row if it doesn't exist."""
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self.fields, delimiter=self.delimiter)
                writer.writeheader()

    def read_all_from_csv(self) -> list:
        """Read all data of a csv file in a list (dictionary per row)."""
        data_list = []
        with open(self.path, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=self.delimiter)
            for row in reader:
                data_list.append(row)
        return data_list

    def write_all_to_csv(self, new_rows: list):
        """Write all data from a list (dictionary per row) to a csv file."""
        if not type(new_rows) is list:
            raise TypeError
        with open(self.path, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fields, delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(new_rows)

    def read_record(self, record_id: str) -> dict:
        """Read record (row) from csv file by id."""
        data_set = self.read_all_from_csv()
        if not type(record_id) is str:
            raise TypeError
        for row in data_set:
            if row["id"] == record_id:
                return row
        # If for some reason no record id is found.
        raise ValueError("Couldn't find record-id!")

    def append_record(self, new_row: dict):
        """Add a new record (row) to CSV file."""
        if not type(new_row) is dict:
            raise TypeError
        with open(self.path, "a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fields, delimiter=self.delimiter)
            writer.writerow(new_row)

    def update_record(self, new_row: dict):
        """Update a record (row) in csv file."""
        if not type(new_row) is dict:
            raise TypeError
        new_list = []
        old_list = self.read_all_from_csv()
        for row in old_list:
            if row["id"] == new_row["id"]:
                row = new_row
            new_list.append(row)
        self.write_all_to_csv(new_list)

    def create_record_id(self) -> str:
        """Create an id for a new record."""

        # Read application date from config.ini.
        app_date = self.cfg.application_date()
        # Set number fill to get same with for every id.
        number_fill = 5
        # Remove dashes from date
        date_value = app_date.replace("-", "")
        id_numbers = []
        data_list = self.read_all_from_csv()
        if data_list:
            # Iterate over data_list to get highest value.
            for row in data_list:
                # Strip the first two non-number characters and the dot after the date.
                stripped_id = str(row["id"])[2:].replace(".", "")
                # Compare first six characters with current year and month.
                # If they match add them to the id_numbers list as integer.
                if stripped_id[0:8] == date_value:
                    id_numbers.append(int(stripped_id))
            # Create new number if id_numbers list is empty.
            if len(id_numbers) == 0:
                id_number = "1"
            else:
                # Add 1 to the heighest number in the id_numbers list to set new id.
                highest = str(max(id_numbers) + 1)
                id_number = highest[8:]
        else:
            # If data_list is empty it is the first id to add.
            id_number = "1"
        # Assemble new id.
        new_id = f"{self.abbr}.{date_value}.{id_number.zfill(number_fill)}"
        return new_id

    def get_record_id(self, search_term: str, search_field: str) -> str:
        """Get a record id by searching a term in a field."""
        if (not type(search_term) is str) or (not type(search_term) is str):
            raise TypeError
        data_list = self.read_all_from_csv()
        for row in data_list:
            if row[search_field] == search_term:
                return row["id"]
        # If for some reason no record id is found.
        return None
