def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive range for a given difficulty level.

    Args:
        difficulty (str): The difficulty level, one of "Easy", "Normal", "Hard".

    Returns:
        tuple[int, int]: A tuple containing the low and high bounds of the range.
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse the raw user input into a validated integer guess.

    Args:
        raw (str): The raw input string from the user.

    Returns:
        tuple[bool, int | None, str | None]: A tuple containing:
            - ok (bool): True if parsing succeeded, False otherwise.
            - guess_int (int | None): The parsed integer if valid, None otherwise.
            - error_message (str | None): An error message if parsing failed,
              None otherwise.
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


# FIX: Moved check_guess from app.py into logic_utils.py using Copilot Agent Mode
def check_guess(guess, secret):
    """
    Compare the user's guess to the secret number and return the outcome and message.

    Args:
        guess: The user's guess (int or str).
        secret: The secret number (int or str).

    Returns:
        tuple[str, str]: A tuple containing:
            - outcome (str): "Win", "Too High", or "Too Low".
            - message (str): A descriptive message for the outcome.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: Fixed high/low hint bug using Copilot Agent Mode
    try:
        if guess > secret:
            return "Too High", "Too High"
        else:
            return "Too Low", "Too Low"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "Too High"
        return "Too Low", "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update the player's score based on the game outcome and attempt number.

    Args:
        current_score (int): The player's current score.
        outcome (str): The outcome of the guess, one of "Win", "Too High", "Too Low".
        attempt_number (int): The number of attempts made so far.

    Returns:
        int: The updated score.
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
