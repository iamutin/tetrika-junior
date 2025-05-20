import pytest

from task1.solution import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def example_function(a: int, b: float) -> None:
    pass


@strict
def add_numbers_or_concat_string(a, b):
    return a + b


def test_correct_types():
    result = sum_two(1, 2)
    assert result == 3


@pytest.mark.parametrize(
    "a, b",
    [
        (1, 3),
        ("1", 2.0),
        (True, 2.5),
    ],
)
def test_incorrect_types(a, b):
    with pytest.raises(TypeError):
        example_function(a, b)


def test_keyword_arguments_shuffled_order():
    result = sum_two(b=5, a=2)
    assert result == 7


@pytest.mark.parametrize(
    "a, b, expected_result",
    [
        (1, 2, 3),
        ("byte", "code", "bytecode"),
    ],
)
def test_missing_annotation(a, b, expected_result):
    result = add_numbers_or_concat_string(a, b)
    assert result == expected_result
