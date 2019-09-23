"""Tests for the config reader module."""

import pytest
from shlack import config


@pytest.mark.parametrize(
    "code, value_of_a",
    [
        ("a = 1 + 1", 2),
        ("a = 'STRING VALUE'", "STRING VALUE"),
        ("a = [1,2,3]", [1, 2, 3]),
    ],
)
def test_string_to_module(code, value_of_a):
    """Test that the string to module function extracts the expected data."""
    module_value = config.string_to_module(code).a
    assert module_value == value_of_a


@pytest.mark.parametrize(
    "code, value_of_a",
    [
        ("a = 1 + 1", 2),
        ("a = 'STRING VALUE'", "STRING VALUE"),
        ("a = [1,2,3]", [1, 2, 3]),
    ],
)
def test_file_to_module(code, value_of_a, tmp_path):
    """Same as test_string_to_module but write it to a file first."""
    p = tmp_path / "temporary.py"
    p.write_text(code)
    module_value = config.file_to_module(p).a
    assert module_value == value_of_a


def test_string_to_module_error():
    """Test that the string to module function raises exceptions correctly."""
    with pytest.raises(TypeError):
        m = config.string_to_module("""a = 'a' + 1""")


@pytest.mark.parametrize("value_of_a", [("1"), ("STRING VALUE")])
def test_env_to_module(value_of_a, monkeypatch):
    """Test that the env to module function extracts the expected data."""
    monkeypatch.setenv("a", value_of_a)
    module_value = config.env_to_module("a").a
    assert module_value == value_of_a


def test_env_to_module_not_defined(monkeypatch):
    """Test that the env function fails to extract data that are not defined."""
    monkeypatch.delenv("a", raising=False)
    monkeypatch.setenv("b", "1")
    module = config.env_to_module("a", "b")

    with pytest.raises(AttributeError):
        module.a

    assert module.b == "1"


@pytest.mark.parametrize("codes, value_of_a", [(["a=1"], 1), (["a=1", "a=2"], 1)])
def test_extract_config(codes, value_of_a):
    """Test the config extractor."""
    modules = [config.string_to_module(i) for i in codes]
    cfg = config.extract_config(["a"], modules)
    assert cfg["a"] == value_of_a


def test_module_to_dict():
    """Test that dict extraction works as expected."""
    code = "\n".join(["a=1", "b=2", "c=3", "a='STRING'"])
    module = config.string_to_module(code)
    data = config.module_to_dict(module)
    assert data["b"] == 2
    assert data["c"] == 3
    assert data["a"] == "STRING"
