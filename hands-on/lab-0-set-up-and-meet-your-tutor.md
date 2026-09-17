# Lab 0 &mdash; Set up, and meet your tutor

**Tier 0 &middot; You already know this** &nbsp;|&nbsp; ~5 minutes

## Do

1. Make your copy and install it: [Make your own copy first](../practice/README.md#make-your-own-copy-first).
2. Run the scoreboard. **Everything should be red** (the one green check is the vendored htmx file).

   ```bash
   python score.py
   ```

   ```text
   Mission 1 - Python drills
     [FAIL] test_word_counts_is_case_insensitive
            NotImplementedError
   ...
   Score: 1/56
   ```

3. Open Copilot Chat, type `/tutor` and press Enter. When it asks for the task, answer with your
   strongest language and one question, for example:

   ```text
   I write Java all day. What is the Python equivalent of a record, and what will surprise me?
   ```

## Notice

- The tutor answers by **contrast with your language**, not from zero. That is the whole module's approach:
  you are not learning to program, you are learning where Python is *different*.
- Now ask it to write `word_counts` for you. It should refuse and hint instead. If it just writes the code,
  check that you opened **your copy** as the workspace root: the prompt file lives in `.github/prompts/`.
- `pip install -e ".[dev]"` installed your own package in *editable* mode: `import askops` works from
  anywhere in the venv, and your edits take effect without reinstalling. It is the Python counterpart of
  a Maven/Gradle module on the classpath, or an `npm link`.

If `pip install` fails with a proxy or SSL error, you are on a network that blocks PyPI. Tell the
trainer now, not in Lab 3.
