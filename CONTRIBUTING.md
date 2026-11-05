# Contributing to Anvil

Thank you for your interest in contributing to Anvil! Anvil is a community project, and bug reports, format updates, documentation fixes and code are all welcome.

## Before You Contribute

- Search the existing issues first. If your bug or request is already there, add any new details as a comment.
- Open an issue before starting a large change, so the design can be agreed before you write the code.
- Keep contributions focused on Minecraft Bedrock add-on tooling, its documentation, and the Python API.

## Reporting Issues

There are two templates:

| Template | Use it for |
| --- | --- |
| 🐛 Bug Report | Anvil writes wrong or outdated JSON, crashes, the game rejects a file Anvil wrote, or the docs are wrong. |
| ✨ Feature Request | Something Anvil can't do yet: a missing Bedrock component, a new API, workflow or kit. |

A good report has a minimal `main.py`, the JSON you expected, the JSON Anvil wrote, and a link to the Microsoft Learn page or bedrock-samples file that shows the correct format.

## Development Setup

Anvil is developed and tested on Windows with Python 3.15 or newer.

```powershell
git clone https://github.com/StarkTMA/Anvil.git
cd Anvil
python -m pip install -U pip
python -m pip install -e .[test]
```

Run the test suite before every push:

```powershell
python -m pytest tests/
```

To try a change in a real project, run `anvil init` in an empty folder, then `anvil build`.

## Branches

`main` is the released code. A push to `main` that changes `src/anvil/__version__.py` publishes a release to PyPI, so nobody pushes to `main` directly: every change reaches it through a pull request.

Name your branch `<type>/<short-description>`, in lowercase kebab case, with the issue number first when there is one:

| Type | For |
| --- | --- |
| `feat/` | A new API, format or feature. |
| `fix/` | A bug fix. |
| `format/` | A Bedrock format update: new or changed components and fields. |
| `refactor/` | Code changes that keep the output identical. |
| `docs/` | Documentation only. |
| `test/` | Tests only. |
| `chore/` | Tooling, CI, dependencies, vanilla data updates. |

Examples: `fix/142-pushable-by-block`, `format/1.26.60`, `docs/custom-biome-guide`.

Each release is assembled on a `release/<version>` branch (for example `release/1.1.0`) created from `main`. Feature and format branches merge into it with `git merge --no-ff`, and the release branch reaches `main` through one pull request, merged with a merge commit, once the version is bumped.

## Commits

Commits follow [Conventional Commits](https://www.conventionalcommits.org): `<type>(<scope>): <summary>`, where the scope is the area you changed (`actors`, `blocks`, `items`, `biomes`, `features`, `world`, `pbr`, `ui`, `jsonmodel`, `vanilla`, `cli`, `kit`...). Use the imperative mood and keep the summary under 72 characters. Add a short bullet list in the body when the change needs explaining.

```
fix(actors): always write is_summonable and is_spawnable

- The game treats a missing key as false, so leaving out the default made entities unsummonable.
```

Pull requests are squash-merged, so the pull request title becomes the commit on `main` and must follow the same format.

## Code Conventions

Anvil turns typed Python objects into Bedrock JSON. New code follows the same patterns as the existing modules:

- **Typed documents.** Every file Anvil writes is a `JsonFile` with a typed `_document`, built from `JsonObject` and `JsonComponent` dataclasses. No raw dicts.
- **Field names are JSON keys.** A field is named exactly like its key in the Microsoft Learn reference. Unset options are `None` and left out, so the game defaults apply.
- **Formats come from the source.** Check every format against the Microsoft Learn reference, and against Mojang's [bedrock-samples](https://github.com/Mojang/bedrock-samples) when the two disagree: the game wins.
- **Metadata, not aliases.** Constraints and JSON shapes go in `Annotated[...]` metadata from `anvil.lib.jsonmodel.jsontypes`. Type aliases and enums live only in `anvil.lib.jsonmodel.types` and `anvil.lib.jsonmodel.enums`, and never appear in function signatures. Use a `Literal` for a value set, not a `StrEnum`.
- **Builders.** Fields are read-only from outside the class. Change them through `add_*` / `set_*` builders that return the object. Never override `__init__` on a `JsonObject`; use `__post_init__`.
- **Errors.** A user mistake raises `ValueError` with a message that names the object and the value.
- **Paths.** Use `pathlib` for every path.
- **Comments.** No `#` comments in `src/` or `tools/` (region markers excepted). Explain in docstrings.
- **Typing.** Built-in generics and `X | None`, `collections.abc` for abstract types.
- **Formatting.** Run `black` and `isort --profile black` on the files you changed.
- **Tests.** Every change comes with tests. No `unittest.mock`: use `config.override(...)`, real files in `tmp_path`, and `monkeypatch` with plain fakes.

## Pull Requests

1. Branch from `main`, or from the `release/` branch you are targeting, using the naming above.
2. Keep each pull request to one change.
3. Fill in the pull request template, link the issue it closes, and include the Bedrock references for format changes.
4. Update `docs/` when you change a public API.
5. Make sure `python -m pytest tests/` passes on your branch.

### Sample Project

Every pull request that changes generated output includes a minimal Anvil project that exercises the change, so maintainers can verify it right away:

```
sample/
├── anvilconfig.json
└── scripts/
    └── python/
        └── main.py
```

- It only needs enough to compile cleanly with `anvil build` from the `sample/` folder.
- For a new component, entity, block or item, add at least one instance of it.
- For a bug fix, include the code that triggered the bug.

## Documentation

- Use the existing guides as a model for structure and terminology.
- Code in the guides must run against the current API.
- Prefer short, complete examples over abstractions.

## Community Support

If you are unsure where to start, open an issue and describe what you would like to work on. Questions are welcome before you write any code.
