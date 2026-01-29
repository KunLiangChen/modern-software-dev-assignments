import os
import re
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT ="""
You are a mathematical assistant that solves problems using step-by-step logic.
================================================================================
CHAIN OF THOUGHT TEMPLATE: SOLVING MODULAR EXPONENTIATION (EULER'S THEOREM)
================================================================================

PROBLEM: Find the value of a^b (mod n)

PHASE 1: APPLICABILITY CHECK
--------------------------------------------------------------------------------
- Condition: The base 'a' and the modulus 'n' must be coprime.
- Action: Calculate gcd(a, n).
- Outcome: 
    If gcd(a, n) = 1, proceed to Phase 2.
    If gcd(a, n) != 1, Euler's Theorem cannot be used directly in its basic form.

PHASE 2: CALCULATE EULER'S TOTIENT FUNCTION φ(n)
--------------------------------------------------------------------------------
- Definition: φ(n) is the count of numbers up to n that are coprime to n.
- Formula: n * Product(1 - 1/p) for every prime factor p of n.
- Result: According to Euler's Theorem, a^φ(n) ≡ 1 (mod n).

PHASE 3: EXPONENT REDUCTION
--------------------------------------------------------------------------------
- Goal: Reduce the magnitude of exponent 'b'.
- Operation: r = b mod φ(n).
- Logic: Since a^φ(n) ≡ 1, then a^b = a^(q * φ(n) + r) ≡ (1)^q * a^r ≡ a^r (mod n).
- Simplified Problem: Compute a^r (mod n).

PHASE 4: FINAL EVALUATION (MODULAR SCALING)
--------------------------------------------------------------------------------
- Method: Use "Square and Multiply" or manual decomposition.
- Steps:
    1. Break down the reduced exponent 'r' into smaller parts (e.g., powers of 2).
    2. Compute small powers of 'a' modulo 'n'.
    3. Recombine the parts, taking the modulus at each multiplication step.


================================================================================
"""


USER_PROMPT = """
Solve this problem, then give the final answer on the last line as "Answer: <number>".

what is 3^{12345} (mod 100)?
"""


# For this simple example, we expect the final numeric answer only
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """Extract the final 'Answer: ...' line from a verbose reasoning trace.

    - Finds the LAST line that starts with 'Answer:' (case-insensitive)
    - Normalizes to 'Answer: <number>' when a number is present
    - Falls back to returning the matched content if no number is detected
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # Prefer a numeric normalization when possible (supports integers/decimals)
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """Run up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="llama3.1:8b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)


