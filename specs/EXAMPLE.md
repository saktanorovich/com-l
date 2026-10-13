# Spec: Word Count CLI

**Feature Slug**: `word-count-cli`
**Status**: Ready

---

## Tech Stack

| Concern         | Choice           |
|-----------------|------------------|
| Language        | Go               |
| Runtime/Version | Go 1.22+         |
| Framework       | none             |
| Test Framework  | go test (stdlib) |
| Package Manager | Go modules       |

---

## Description

A command-line tool that reads text from stdin or a file argument and prints
the number of words, lines, and characters to stdout — similar to the Unix
`wc` command but with human-readable output.

The tool is intended as a learning exercise and utility script. It must work
on Windows and Linux without modification.

---

## Requirements

- As a developer, I want to pipe text into the tool and see a word/line/char
  count, so that I can quickly audit text output from other commands.
- As a user, I want to pass a filename as an argument and get counts for that
  file, so that I don't have to use shell redirection.
- As a user, I want a clear error message if the file does not exist, so that
  I know immediately what went wrong.

---

## Acceptance Criteria

- [ ] Running `echo "hello world" | wordcount` prints `words: 2, lines: 1, chars: 11`
- [ ] Running `wordcount somefile.txt` prints the same format for the file's contents
- [ ] Running `wordcount missing.txt` exits with code 1 and prints
      `error: file "missing.txt" not found` to stderr
- [ ] Running `wordcount` with no stdin and no argument prints a usage message
      to stderr and exits with code 1
- [ ] Empty input (empty file or empty pipe) prints `words: 0, lines: 0, chars: 0`
- [ ] A file with only newlines counts lines correctly (3 newlines = 3 lines,
      0 words, 3 chars)

---

## Test Approach

**Primary approach**: Unit tests for the counting logic; integration tests for
the CLI entry point (stdin and file argument paths).

**What to test**:
- The `countWords`, `countLines`, `countChars` functions individually
- The main CLI with a mock reader (stdin path)
- The main CLI with a real temp file (file argument path)
- Error handling for missing files

**What not to test**:
- Go's own `os.Open` behavior
- Terminal encoding or locale behavior

---

## Constraints

- Must not use any external dependencies (stdlib only)
- Binary must compile and run on Windows without WSL
- Output format must be exactly: `words: N, lines: N, chars: N` (for parsing by other tools)

---

## Out of Scope

- Multiple file arguments (e.g. `wordcount a.txt b.txt`)
- A `--bytes` vs `--chars` distinction (always count Unicode characters)
- Recursive directory scanning
- A `--words-only` or other filtering flags
