# Contributing to ActiveVPN

Thanks for considering a contribution! This guide covers setup, branch rules,
commit style, and the pull request workflow.

## Table of contents

- [Getting started](#getting-started)
- [Branches](#branches)
- [Commit style](#commit-style)
- [Code style](#code-style)
- [Pull request workflow](#pull-request-workflow)
- [Reporting bugs](#reporting-bugs)

## Getting started

1. Fork the repository on GitHub.
2. Clone your fork and add the upstream remote:

   ```bash
    git clone https://github.com/<your-username>/ActiveVPN.git
   cd ActiveVPN
   git remote add upstream https://github.com/rkriad585/ActiveVPN.git
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   . .venv/Scripts/Activate.ps1   # Windows PowerShell
   # . .venv/bin/activate         # macOS/Linux
   pip install -r requirements.txt pytest build twine
   ```

4. Run the tests to confirm a green baseline:

   ```bash
   pytest -q
   ```

## Branches

- Work on a dedicated feature branch: `git checkout -b feature/your-feature`.
- Keep `main` up to date with upstream before submitting.
- One logical change per branch/pull request.

## Commit style

Match the repository's existing history, which uses a short emoji prefix plus a
concise summary, e.g.:

```text
✨ Add --watch continuous monitoring mode
🐛 Fix DNS comparison when the public IP lookup fails
```

- Use the imperative mood in the summary line.
- Keep the summary under ~72 characters; add a body for non-obvious changes.
- Do not commit build artifacts or secrets.

## Code style

- Follow [PEP 8](https://peps.python.org/pep-0008/), 4-space indentation.
- Keep the project's tone and terminology (see the docs and README).
- Add tests for new behavior in `tests/`; run `pytest -q` locally.
- Update the relevant files under `docs/` when behavior changes.
- Do not add code comments unless they explain non-obvious logic.

## Pull request workflow

1. Push your branch: `git push origin feature/your-feature`.
2. Open a pull request against `main`.
3. Ensure the CI checks (`.github/workflows/ci.yml`) pass on Ubuntu, Windows,
   and macOS for Python 3.8 and 3.12.
4. Keep the PR focused; rebase instead of merging `main` when needed.

## Reporting bugs

Open an issue with the command you ran, your OS/terminal, and the output.
For security vulnerabilities, follow [SECURITY.md](SECURITY.md) instead.

---

<a href="README.md">← Back to README</a>
