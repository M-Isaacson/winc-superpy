import pytest
import src.settings as settings

# Variables to use in invalid_date function.
invalid_dates = [
    "vijf juni negentienvijftig",
    "15 mei 2022",
    "100-04-02",
    "",
    "2019/03/01",
    "20-23-1990",
    "2018-10-64",
    "2012-23-10",
    "2019",
    "2010-12",
    "2010-8-20",
    "2010-08-2",
    2012 - 12 - 12,
    2012 / 12 / 12,
    2012,
    12,
    2012.12,
]
ids_invalid_dates = []
for invalid_value in invalid_dates:
    ids_invalid_dates.append(f"{invalid_value}")


@pytest.fixture(params=invalid_dates, ids=ids_invalid_dates)
def invalid_date(request):
    """Return invalid ISO dates for testing."""
    return request.param


datasets = ["products", "purchases", "sales"]
ids_datasets = []
for dataset_value in datasets:
    ids_datasets.append(f"{dataset_value}")


@pytest.fixture(params=datasets, ids=ids_datasets)
def dataset(request):
    """Return invalid ISO dates for testing."""
    return request.param


@pytest.fixture(scope="session")
def cfg():
    """Instantiate settings object for testing."""
    cfg = settings.Settings()
    return cfg
