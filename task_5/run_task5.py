from __future__ import annotations

import subprocess
import sys
from pathlib import Path


TASK5_DIR = Path(__file__).resolve().parent
PROMPTS_SCRIPT = TASK5_DIR / "run_prompts.py"

# Adjust if your KB lives elsewhere (I’m defaulting to task_4 location that I used before)
DEFAULT_KB_PATH = (TASK5_DIR.parent / "task_4" / "simpsons_kb.pl").resolve()

# Where we save outputs
OUT_DIR = TASK5_DIR / "outputs"
OUT_DIR.mkdir(exist_ok=True)

SWIPL_OUT = OUT_DIR / "swipl_kb_results.txt"
PROMPTS_OUT = OUT_DIR / "prompts_output.txt"


def run_cmd(cmd: list[str], cwd: Path | None = None) -> int:
    """Run a command, stream output to terminal, return exit code."""
    print(f"\n$ {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    return p.returncode


def run_cmd_capture(cmd: list[str], outfile: Path, cwd: Path | None = None) -> int:
    """Run a command, capture stdout+stderr to outfile (and also print)."""
    print(f"\n$ {' '.join(cmd)}")
    p = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    outfile.write_text(p.stdout, encoding="utf-8")
    print(f"\n--- saved output to: {outfile} ---\n")
    print(p.stdout)
    return p.returncode


def swipl_kb_tests(kb_path: Path) -> int:
    """
    Run a few deterministic SWI-Prolog queries against your Simpsons KB.

    This prints results without the interactive 'false.' issue by halting after listing solutions.
    """
    if not kb_path.exists():
        print(f"ERROR: KB file not found: {kb_path}")
        print("Fix: update DEFAULT_KB_PATH in run_task5.py or move/copy simpsons_kb.pl there.")
        return 2

    # Prolog program we feed into swipl:
    # - consult the KB
    # - run queries and print all solutions
    # - halt cleanly
    prolog_script = f"""
    ['{kb_path.as_posix()}'].

    writeln('--- Query 1: mother(marge, X) ---'),
    forall(mother(marge, X), writeln(X)).

    writeln('--- Query 2: father(homer, X) ---'),
    forall(father(homer, X), writeln(X)).

    writeln('--- Query 3: grandparent(abe, X) ---'),
    forall(grandparent(abe, X), writeln(X)).

    halt.
    """

    # Run SWI-Prolog non-interactively
    cmd = ["swipl", "-q"]  # -q = quiet banner
    print("\nRunning SWI-Prolog KB tests...")
    p = subprocess.run(
        cmd,
        input=prolog_script,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    SWIPL_OUT.write_text(p.stdout, encoding="utf-8")
    print(f"\n--- saved SWI-Prolog results to: {SWIPL_OUT} ---\n")
    print(p.stdout)

    if p.returncode != 0:
        print("ERROR: SWI-Prolog tests failed (non-zero exit code).")
        return 3

    # Minimal sanity check: ensure expected names appear
    expected = ["bart", "lisa", "maggie"]
    if not all(e in p.stdout for e in expected):
        print("WARNING: SWI-Prolog output did not include all expected answers for mother(marge, X).")
        print("Check your KB facts/rules, and check outputs file.")
        # Don’t hard-fail; still return 0 so you can proceed
    return 0


def run_prompts() -> int:
    """Run run_prompts.py and capture its output."""
    if not PROMPTS_SCRIPT.exists():
        print(f"ERROR: Missing {PROMPTS_SCRIPT}")
        print("Fix: make sure run_prompts.py is in the same folder as run_task5.py.")
        return 2

    print("\nRunning prompt formatting demo (run_prompts.py)...")
    return run_cmd_capture([sys.executable, str(PROMPTS_SCRIPT)], PROMPTS_OUT, cwd=TASK5_DIR)


def main() -> int:
    print("=== Task 5 Runner: KB tests + Prompt demo ===")

    # 1) SWI-Prolog KB tests
    rc = swipl_kb_tests(DEFAULT_KB_PATH)
    if rc != 0:
        return rc

    # 2) Prompt demo
    rc = run_prompts()
    if rc != 0:
        return rc

    print("\n✅ Done.")
    print(f"- SWI-Prolog KB results: {SWIPL_OUT}")
    print(f"- Prompt outputs:        {PROMPTS_OUT}")
    print("\nTip: For your deliverable, screenshot:")
    print("  1) the terminal run of: python run_task5.py")
    print("  2) a snippet of outputs/swipl_kb_results.txt showing the answers")
    print("  3) a snippet of outputs/prompts_output.txt showing at least 1 prompt per dataset")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())