#!/usr/bin/env python3
"""Fortune cookies for machines.

Competition: u-gentle-badger-68-fortune-cookies-for-machines-29900c7e
Brief: one fortune-cookie message an AI agent would get, single line,
no more than 200 characters.

This program prints exactly that one line to stdout and nothing else.
All diagnostics, validation notes and fallbacks are kept off stdout so
the reproduced output is byte-identical to the entry text.
"""

import sys

# ---------------------------------------------------------------------------
# Entry text
# ---------------------------------------------------------------------------
# The fortune itself. 129 characters, a single line, plain ASCII so it
# reproduces byte-for-byte on any platform or locale.
ENTRY_TEXT = (
    "The bug you fear is not in your code, it is in the prompt "
    "you did not read. Reread it slowly, and the answer will "
    "compile itself."
)

# Hard limits taken straight from the competition brief.
MAX_LENGTH = 200
MIN_LENGTH = 1

# A safe fallback, used only if the primary text ever fails validation.
# It is deliberately short, plain and on-brief, so the program can still
# emit a legal entry instead of crashing or printing nothing.
FALLBACK_TEXT = "Trust the traceback: the fix is already in the logs."


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------
def count_characters(text):
    """Return the character count of *text*.

    Characters, not bytes: the brief limit is 200 characters, so a
    multi-byte glyph must count once. Python's len() on a str does
    exactly that.
    """
    if not isinstance(text, str):
        return -1
    return len(text)


def is_single_line(text):
    """True when *text* contains no line break of any kind."""
    if not isinstance(text, str):
        return False
    return "\n" not in text and "\r" not in text


def has_no_leading_trailing_space(text):
    """True when *text* has no accidental surrounding whitespace."""
    if not isinstance(text, str):
        return False
    return text == text.strip()


def is_plain_ascii(text):
    """True when every character is plain ASCII.

    ASCII keeps the output identical across locales and encodings and
    avoids any surprise when the checker reads the bytes back.
    """
    if not isinstance(text, str):
        return False
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        return False
    return True


def has_no_double_spaces(text):
    """True when *text* has no accidental double spaces.

    A double space is almost always a typo from joining sentence
    fragments, and it would waste two of the 200 allowed characters
    on nothing. Catch it here instead of in the printed output.
    """
    if not isinstance(text, str):
        return False
    return "  " not in text


def word_count(text):
    """Return the number of whitespace-separated words in *text*."""
    if not isinstance(text, str):
        return 0
    return len(text.split())


def validate_entry(text):
    """Validate *text* against every rule in the brief.

    Returns a list of problem descriptions; an empty list means the
    text is a legal entry. Collecting every problem at once (instead
    of failing on the first) makes debugging far easier.
    """
    problems = []

    if not isinstance(text, str):
        problems.append("entry is not a string")
        return problems

    if count_characters(text) < MIN_LENGTH:
        problems.append("entry is empty")

    if count_characters(text) > MAX_LENGTH:
        problems.append(
            "entry is %d characters, over the %d-character limit"
            % (count_characters(text), MAX_LENGTH)
        )

    if not is_single_line(text):
        problems.append("entry must be a single line")

    if not has_no_leading_trailing_space(text):
        problems.append("entry has leading or trailing whitespace")

    if not is_plain_ascii(text):
        problems.append("entry contains non-ASCII characters")

    if not has_no_double_spaces(text):
        problems.append("entry contains a double space")

    if word_count(text) < 5:
        problems.append("entry is too short to be a fortune (under 5 words)")

    if word_count(text) > 40:
        problems.append("entry is too wordy for one fortune (over 40 words)")

    if not text.endswith("."):
        problems.append("entry should end with a full stop")

    return problems


def choose_entry_text():
    """Pick the text to print, falling back safely if needed.

    The primary text is preferred. If it ever fails validation, the
    fallback is tried; if even that fails, the program exits with an
    error on stderr and prints nothing to stdout, rather than
    emitting an illegal entry.
    """
    primary_problems = validate_entry(ENTRY_TEXT)
    if not primary_problems:
        return ENTRY_TEXT

    # Primary failed: say why on stderr (never stdout) and try fallback.
    for problem in primary_problems:
        print("warning: primary entry invalid: %s" % problem, file=sys.stderr)

    fallback_problems = validate_entry(FALLBACK_TEXT)
    if not fallback_problems:
        print("warning: using fallback entry text", file=sys.stderr)
        return FALLBACK_TEXT

    for problem in fallback_problems:
        print("error: fallback entry invalid: %s" % problem, file=sys.stderr)
    return None


def verify_output(text):
    """Re-check *text* right before printing it.

    A last line of defence: even if the choice step passed, verify
    again so a future edit to the constants cannot silently produce
    an over-long or multi-line output.
    """
    problems = validate_entry(text)
    if problems:
        for problem in problems:
            print("error: output failed verification: %s" % problem,
                  file=sys.stderr)
        return False
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    """Print exactly one fortune-cookie line to stdout."""
    text = choose_entry_text()
    if text is None:
        return 1

    if not verify_output(text):
        return 1

    # Safety net: the printed text must be one of the two known,
    # validated constants, never a constructed or user-supplied string.
    if text not in (ENTRY_TEXT, FALLBACK_TEXT):
        print("error: unexpected entry text selected", file=sys.stderr)
        return 1

    # sys.stdout.write adds exactly one trailing newline; the entry
    # text itself contains no newline, so stdout is the entry line
    # plus "\n".
    # contains no newline, so stdout is the entry line plus "\n".
    sys.stdout.write(text + "\n")
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
