from logic_utils import check_guess
from app import parse_guess, get_range_for_difficulty
import random


def test_negative_guess_rejected():
    ok, value, err = parse_guess("-1", 1, 20)
    assert not ok
    assert err == "Enter a positive number."


def test_non_numeric_guess_rejected():
    ok, value, err = parse_guess("abc", 1, 20)
    assert not ok
    assert err == "That is not a number."


def test_easy_mode_out_of_range_guess_rejected():
    ok, value, err = parse_guess("25", 1, 20)
    assert not ok
    assert err == "Enter a number between 1 and 20."


def test_hard_mode_out_of_range_guess_rejected():
    ok, value, err = parse_guess("58", 1, 50)
    assert not ok
    assert err == "Enter a number between 1 and 50."


def test_easy_mode_secret_in_range():
    low, high = get_range_for_difficulty("Easy")
    for _ in range(50):
        secret = random.randint(low, high)
        assert low <= secret <= high


def test_hard_mode_secret_in_range():
    low, high = get_range_for_difficulty("Hard")
    for _ in range(50):
        secret = random.randint(low, high)
        assert low <= secret <= high


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == ("Win", "🎉 Correct!")


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == ("Too High", "Too High")


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == ("Too Low", "Too Low")


def test_decimal_guess_rejected():
    ok, value, err = parse_guess("5.5", 1, 20)
    assert not ok
    assert err == "Decimal numbers are not allowed."


def test_extremely_large_guess_rejected():
    ok, value, err = parse_guess("999999", 1, 20)
    assert not ok
    assert err == "Enter a number between 1 and 20."


def test_zero_guess_rejected():
    ok, value, err = parse_guess("0", 1, 20)
    assert not ok
    assert err == "Enter a positive number."
