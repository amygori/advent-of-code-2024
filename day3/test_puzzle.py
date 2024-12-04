from pathlib import Path
import pytest
from puzzle import do_the_thing


@pytest.fixture
def input():
    file = Path("test_input.txt")
    return Path.read_text(file)


@pytest.fixture
def expected_output():
    output = 48
    return output


def test_do_the_thing(input, expected_output):
    assert do_the_thing(input) == expected_output
