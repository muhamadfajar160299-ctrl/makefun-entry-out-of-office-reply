"""Write the out-of-office entry to the grader output directory.

Reads the entry text shipped beside this script (entry.txt) and copies it
byte-for-byte to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` with mode 0644, so the
grader sees exactly the text that was reviewed. Refuses to write an empty
or whitespace-only entry, which the gate would reject.
"""

import os
import shutil
import sys


def main():
    try:
        out_dir = os.environ["MAKEFUN_OUTPUT_DIR"]
    except KeyError:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        raise SystemExit(1)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    try:
        with open(src, "rb") as f:
            data = f.read()
    except OSError as exc:
        print(f"cannot read entry.txt: {exc}", file=sys.stderr)
        raise SystemExit(1)
    if not data.strip():
        print("entry.txt is empty or whitespace-only", file=sys.stderr)
        raise SystemExit(1)
    try:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.txt")
        with open(dst, "wb") as f:
            f.write(data)
        os.chmod(dst, 0o644)
    except OSError as exc:
        print(f"cannot write entry: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
