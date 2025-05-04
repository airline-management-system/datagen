# 🚀 Datagen

A command-line tool for generating and processing different types of entities with specified amounts.

## ⚙️ Setup

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Run the project:
```
uv run main.py ARGUMENTS
```

## 🎯 Usage

See `--help` to discover entities:

```bash
uv run main.py --help
```

Run the tool with the following arguments:

```bash
uv run main.py generate -e <entity_type> -a <number>
# or
uv run main.py generate --entity <entity_type> --amount <number>
```

Use `--dry-run` to generate data without making HTTP requests:

```bash
uv run main.py generate -e <entity_type> -a <number> --dry-run
```

Run the standard generation scheme:

```bash
uv run main.py scheme
```

Use `--dry-run` to execute the scheme without making HTTP requests:

```bash
uv run main.py scheme --dry-run
```

## 🧪 Running Tests

Run the tests using `pytest`:

```bash
uv run pytest tests.py
```
