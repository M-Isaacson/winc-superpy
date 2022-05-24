"""Test settings module."""
import src.settings as settings
import pytest
import os.path


def test_parser_is_instance_configparser(cfg):
    """Testing if config parser object is active."""
    assert isinstance(cfg.parser, settings.ConfigParser)


def test_base_dir_exists(cfg):
    """Testing if the application's base path is set."""
    assert cfg.base_dir == os.path.realpath("src")


def test_path_of_ini_file_exists(cfg):
    """Testing if config.ini exists."""
    assert os.path.exists(cfg.ini_file)


def test_dataset_properties_valid_argument(cfg, dataset):
    """Testing if the return value is a dictionary."""
    assert type(cfg.dataset_properties(dataset)) == dict


@pytest.mark.parametrize("key", ["abbr", "path", "fields"])
def test_dataset_properties_has_valid_key(cfg, dataset, key):
    """Testing the presence of important keys in dataset."""
    the_dict = cfg.dataset_properties(dataset)
    assert key in the_dict.keys()


def test_dataset_properties_fields_has_id(cfg, dataset):
    """Testing the availability of the value 'id' in the dataset fields-key"""
    the_dict = cfg.dataset_properties(dataset)
    the_values = the_dict.get("fields")
    assert "id" in the_values


@pytest.mark.parametrize("number", ["five", "5", 5.0, 2.3])
def test_set_days_advanced_invalid_argument(cfg, number):
    """Testing if a type error is raised, when argument is not a string."""
    with pytest.raises(TypeError):
        cfg.set_days_advanced(number)
