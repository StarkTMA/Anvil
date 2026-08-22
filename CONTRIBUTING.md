# Contributing to Anvil

Thank you for your interest in contributing to Anvil! Anvil is intended to be a community project, and contributions are strongly encouraged. This guide covers the easiest ways to report bugs, suggest improvements, and submit code changes for this repository.

## Before You Contribute

- Check the existing issues first. If your bug or feature request is already reported, add a comment with any new details.
- Use the provided bug report template at `.github/ISSUE_TEMPLATE/bug_report.yml` when reporting an issue.
- Keep contributions focused on Minecraft Bedrock addon tooling, documentation improvements, and Python SDK features.

## How to Report Bugs

1. Open a new issue in this repository.
2. Choose the bug report template.
3. Provide:
    - a concise reproduction path,
    - the expected behavior,
    - the actual behavior,
    - any Minecraft Learn portal or engine documentation links if the issue is tied to a specific Bedrock feature.
4. Attach relevant snippets or generated JSON examples whenever possible.

## Feature Requests

If you want to suggest a new API or workflow:

- Open an issue with a clear description of the problem you want to solve.
- Explain the expected behavior and how it would fit into Anvil's existing component-based design.
- If the request is related to Minecraft Bedrock content capabilities, include a reference link to the Learn portal or official docs.

## Development Setup

Anvil is developed and tested on Windows with Python 3.10 or newer.

### Clone the repository

```powershell
git clone https://github.com/StarkTMA/Anvil.git
cd Anvil
```

### Install dependencies

```powershell
python -m pip install -U pip
python -m pip install -e .
```

### Run Anvil locally

From the repository root:

```powershell
anvil --help
```

For project-specific tests, use the `scripts/python/main.py` example flow or any sample project created with `anvil init` (or `anvil create`).

## Submitting Pull Requests

1. Fork the repository and create a feature branch.
2. Keep changes small and focused.
3. Update documentation when adding or changing public APIs.
4. Include a short description of the change and the reason behind it.
5. If your change fixes an issue, reference the issue number in the PR.

### PR Checklist

- [ ] I have tested the change locally.
- [ ] I have updated documentation if needed.
- [ ] I have followed the repository style and formatting conventions.
- [ ] I have used strong type hints for all public and internal APIs.
- [ ] I have added argument validation where appropriate.
- [ ] I have included links to any relevant Bedrock documentation if the change involves engine-specific behavior.
- [ ] I have included a minimal sample Anvil project (see "Sample Project" section below).

## Sample Project

Every pull request must include a minimal Anvil project that directly exercises the changed API surface. This lets maintainers verify your PR immediately — **no manual project setup required**.

### What to include

Place your sample project inside a `sample/` directory at the root of your PR branch. It needs only the bare minimum for a successful compilation and error-free test run:

```
sample/
├── anvilconfig.json          # Minimal project config
└── scripts/
    └── python/
        └── main.py           # Entry point that exercises your change
```

### Guidelines

- The sample does **not** need to be a fully fledged project — just enough to compile cleanly and demonstrate the feature.
- If your change involves a new component, entity type, block, or item, add at least one instance of it to the sample.
- If your change involves a bug fix, include the code pattern that previously caused the bug.
- The sample should compile without errors when run from the `sample/` directory with `anvil build`.

## Documentation and Style

- Use the existing project docs as a model for formatting and terminology.
- Prefer clear examples over complex abstractions in docs.
- Keep Markdown files readable and concise.

## Community Support

If you're unsure how to proceed, open an issue first and describe what you want to work on. Contributors are welcome to ask for guidance before writing code, and we appreciate every contribution that helps make Anvil more useful for everyone.
