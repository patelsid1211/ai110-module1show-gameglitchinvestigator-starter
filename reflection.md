# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran the game, it appeared to work on the surface — the UI loaded and I could type in the input field and click buttons. However, after testing it, I quickly discovered several bugs that made the game behave incorrectly and unpredictably.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1. Negative numbers were accepted: The input field allowed negative values such as -1, which should never be a valid guess in a number guessing game.

2. "New Game" button did nothing: Clicking the "New Game" button had no effect — the game did not reset, the previous answer stayed active, and no new secret number was generated.

3. Hard mode accepted out-of-range values: In Hard mode, the valid range is 1–50, but the game accepted guesses beyond that limit, such as 65. It also generated a secret answer outside the range (e.g., 57), meaning it was impossible to win fairly.

4. Easy mode had an out-of-range secret answer: In Easy mode, the valid range is 1–20, but the secret answer was generated as a number like 82, which is completely outside the expected range.

5. The input accepted non-numeric characters: The input field allowed letters and symbols to be entered. Only whole numbers should be accepted as valid guesses.

---

## 2. How did you use AI as a teammate?

**Which AI tools did you use?**
I used GitHub Copilot throughout this project.

---

### Correct AI Suggestion

**What the AI suggested:**
Copilot identified that the secret number is only generated once when the Streamlit session starts, inside the `if "secret" not in st.session_state:` block. It does not regenerate when the user changes the difficulty level in the sidebar.

For example, if the app loads with "Normal" difficulty (range 1–100), a secret like `82` is generated. If the user then switches to "Easy" (range 1–20), the secret remains `82`, which is now outside the valid range.

Copilot suggested regenerating the secret number whenever the difficulty level changes, so the secret always stays within the correct range.

**How I verified it:**
I ran the game in Streamlit, started on Normal mode, then switched to Easy mode. I confirmed the secret number was out of range. After applying the fix, I switched difficulty levels again and verified the secret number was always within the correct range for the selected difficulty.

---

### Incorrect or Misleading AI Suggestion

**What the AI suggested:**


**Was it correct?**


**How I verified it:**

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I decided a bug was truly fixed only when it passed two checks — first I tested it manually in the Streamlit app to see the correct behaviour with my own eyes, and then I confirmed it with a pytest test case to make sure the underlying logic was correct in the code.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I ran the full pytest suite after fixing all the bugs: python -m pytest tests/test_game_logic.py -v


- Did AI help you design or understand any tests? How?
Yes. I asked Copilot to generate pytest test cases that specifically targeted each bug that was fixed. Copilot wrote tests that covered negative values, non-numeric input, out-of-range guesses, secret number ranges, and correct hint messages. This helped me understand exactly what conditions each function needed to handle and gave me confidence that the fixes were working correctly.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every time a user interacts with a Streamlit app, the entire script reruns from top to bottom. Session state is like a notebook that remembers values between those reruns — without it, everything resets every time the user clicks a button or types something.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
Writing pytest tests after every fix. It gave me confidence that the bug was actually solved and not just appearing to work.

- This could be a testing habit, a prompting strategy, or a way you used Git.
I would review Copilot's suggestions more carefully before accepting them instead of running the app first to discover the error.

- What is one thing you would do differently next time you work with AI on a coding task?
AI can write code quickly but it does not always understand the full context. I learned that I need to verify every suggestion rather than trust it blindly.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
I used to think AI generated code just works. Now I know it needs to be tested and verified just like code I write myself.