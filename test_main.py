import tempfile
from pathlib import Path
from main import get_ingredients
from main import make_smoothie

def test_get_ingredients_file_does_not_exist():
    """get_ingredients returns an empty list of ingredients if the file does not exist"""
    # Given: a path to a file that does not exist
    with tempfile.TemporaryDirectory() as tmp_path:
        non_existent_file = Path(tmp_path) / "non_existent.txt"
        # When: we call get_ingredients
        result = get_ingredients(non_existent_file)
        # Then: we get an empty list
        assert result == []

def test_get_ingredients(tmp_path):
    # Given: a recipe file with ingredients
    content = "Apple\nBanana\nOrange"
    recipe_file = tmp_path / "my_smoothie.txt"
    recipe_file.write_text(content)

    # When: get_ingredients is called
    result = get_ingredients(recipe_file)

    # Then: it returns the list of ingredients
    expected = ["Apple", "Banana", "Orange"]
    assert result == expected


from rich.console import Console


def test_make_smoothie_prints_added_ingredients(tmp_path):
    """make_smoothie prints all ingredients that were added to the smoothie to the console"""

    # Given: a recipe file
    recipe_file = tmp_path / "test.txt"
    recipe_file.write_text("Apple\nBanana\n")

    # When: we make a smoothie
    console = Console(record=True)
    make_smoothie(recipe_file, console)

    # Then: all added ingredients are printed to the console
    text_output = console.export_text()
    assert "Added Apple" in text_output
    assert "Added Banana" in text_output


import pyjokes
def test_make_smoothie_prints_a_joke(tmp_path, monkeypatch):
    """make_smoothie prints a joke"""

    # Given: a recipe file
    recipe_file = tmp_path / "recipe.txt"
    recipe_file.write_text("Mango\n")
    # Mocking: Replace pyjokes.get_joke with a lambda that returns a fixed string
    test_joke = "A mock walks into a bar. The bartender asks, 'What can I get you?' The mock returns None."
    monkeypatch.setattr(pyjokes, "get_joke",
                        lambda: "A mock walks into a bar. The bartender asks, 'What can I get you?' The mock returns None.")

    # When: we make a smoothie
    console = Console(record=True)
    make_smoothie(recipe_file, console)

    # Then: a joke is told
    output = console.export_text()
    assert "The mock returns None" in output