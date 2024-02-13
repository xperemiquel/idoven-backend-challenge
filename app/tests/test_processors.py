import pytest
from ecg.processors import calculate_zero_crossings

@pytest.mark.parametrize(
    "signal, expected",
    [
        ([3, 4, 5], 0),
        ([-3, -4, -5], 0),
        ([2, -5], 1),
        ([5, 0, -1], 1),
        ([1, 1, 0, 0, -15, -2], 1),
        ([2, -3, 7], 2),
        ([0, 0, 0], 0),
    ],
)
def test_calculate_zero_crossings(signal, expected):
    assert calculate_zero_crossings(signal) == expected
