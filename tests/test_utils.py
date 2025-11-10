import pytest

from src.utils import parse_date


def test_date_parser() -> None:
    valid_dates = ["2020-12-31", "1999/01/01", "2000-02-29"]
    non_valid_dates = [
        "31-12-2020",
        "2020/31/12",
        "2020-13-01",
        "2020-00-10",
        "abcd-ef-gh",
    ]

    for d in valid_dates:
        # checks that valid dates are parsed without error and a string is returned
        parsed = parse_date(d)
        assert isinstance(parsed, str)
        assert len(parsed) == 10  # 'YYYY-MM-DD' length

    for d in non_valid_dates:
        # checks that invalid dates raise ValueError
        with pytest.raises(ValueError):
            parse_date(d)
