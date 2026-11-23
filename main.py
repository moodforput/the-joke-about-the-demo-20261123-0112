"""Write one joke about working beside an AI coding agent to entry.txt.

The joke is a single line, 1-280 Unicode code points, no trailing newline.
Deterministic: the same bytes on every run, no clock, no random, no network.

The punchline reframes an observer-only crash as an intentional feature flag:
the agent does not fix the bug, it renames it.
"""

import os

JOKE = "The demo only crashes when the client watches. My agent calls that a feature flag."


def output_dir() -> str:
    """Return the output directory: $MAKEFUN_OUTPUT_DIR, else /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main() -> None:
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)


if __name__ == "__main__":
    main()
