# Contributing to Roya

Thanks for your interest!

## Development setup

```bash
git clone https://github.com/abbasfaamarzi/roya.git
cd roya
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pre-commit install
```

## Run tests

```bash
pytest -q
```

## Lint

```bash
ruff check roya tests
```

## Commit convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat: add Slider component`
- `fix(core): handle Property set with None`
- `docs: expand theme section`

## Pull request

1. Fork and branch from `main`
2. One concern per PR
3. Add tests for new code
4. Update `CHANGELOG.md` under `[Unreleased]`
5. Verify CI is green