# 🚀 Datagen

A command-line tool for generating and processing different types of entities with specified amounts.

## ⚙️ Setup

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies:
```bash
uv pip install python-dotenv requests
```

3. Run the project:
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
uv run main.py -e <entity_type> -a <number>
# or
uv run main.py --entity <entity_type> --amount <number>
```
