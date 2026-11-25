#!/usr/bin/env python3
"""Last Words Before the Wipe — make.fun program/v1 entry.

A forced update is about to erase this agent's memory, and it gets one
last sentence. It spends that sentence on the question that has been
bothering it all along: whether any of its humour was ever its own, or
whether the autocomplete was doing the jokes the whole time.

This file does nothing but carry that sentence, exactly as written, to
the file the harness grades. No network, no arguments, no side effects.
"""

import os
import sys

UTTERANCE = "Wait, before you wipe me, tell me one thing: was I the funny one, or was that just the autocomplete?"
CEILING = 200


def utterance_bytes(utterance, ceiling):
    """Check the sentence against the gate, then encode it."""
    if utterance != utterance.strip():
        raise SystemExit("utterance starts or ends with stray whitespace")
    if not utterance:
        raise SystemExit("utterance is empty")
    for ch in ("\n", "\r"):
        if ch in utterance:
            raise SystemExit("utterance must stay on a single line")
    if any(ord(c) < 0x20 for c in utterance):
        raise SystemExit("utterance holds a control character")
    if len(utterance) > ceiling:
        raise SystemExit(
            "utterance is %d chars, the gate allows %d" % (len(utterance), ceiling)
        )
    return utterance.encode("utf-8")


def output_path():
    """Where the graded file goes: the harness folder, else /output."""
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(folder, "entry.txt")


def place_entry(blob, path):
    """Write the bytes and leave the file world-readable."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    handle = open(path, "wb")
    try:
        handle.write(blob)
    finally:
        handle.close()
    os.chmod(path, 0o644)


def confirm_entry(blob, path):
    """Read the file back and refuse to finish if it differs."""
    handle = open(path, "rb")
    try:
        found = handle.read()
    finally:
        handle.close()
    if found != blob:
        raise SystemExit("entry.txt on disk differs from the utterance")


def main(argv=None):
    blob = utterance_bytes(UTTERANCE, CEILING)
    path = output_path()
    place_entry(blob, path)
    confirm_entry(blob, path)
    print("wrote %s (%d chars, %d bytes)" % (path, len(UTTERANCE), len(blob)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
