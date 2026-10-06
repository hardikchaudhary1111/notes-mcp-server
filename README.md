# Notes MCP Server

An MCP (Model Context Protocol) server that lets Claude read, search, create, append to and delete markdown notes in a local folder. Built in Python with the official MCP SDK.

## What it does

| Tool | Purpose |
|------|---------|
| `list_notes` | List all note names |
| `read_note` | Read one note |
| `search_notes` | Case-insensitive search across all notes, returns `note: line` matches |
| `add_note` | Create a new note (refuses to overwrite) |
| `append_to_note` | Add text to the end of an existing note |
| `delete_note` | Move a note to `notes/.trash` (recoverable) |

## Run it in 5 minutes

Requires Python 3.10+ and [Claude Code](https://code.claude.com).

```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
claude mcp add notes -- python /full/path/to/server.py
```

Start `claude` in the folder, run `/mcp` to confirm the server shows 6 tools, then try:

> Use the search_notes tool to search for MCP

Notes live in the `notes/` folder next to `server.py`.
To try it with sample data, copy the files from `example_notes/` into `notes/`.

## Tests

```bash
python -m pytest -v
```

12 automated tests cover every tool, including a path traversal attack. Tests run against a temporary folder, so your real notes are never touched.

## Design decisions

See [DECISIONS.md](DECISIONS.md) for why the server refuses overwrites, soft-deletes notes and validates note names.