from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes-server")

# The notes folder sits next to this file
NOTES_DIR = Path(__file__).parent / "notes"
NOTES_DIR.mkdir(exist_ok=True)


def _note_path(name: str) -> Path:
    """Turn a note name into a safe file path inside the notes folder."""
    if not name.endswith(".md"):
        name += ".md"
    path = (NOTES_DIR / name).resolve()
    # Safety: refuse names like "../../secret.txt" that escape the folder
    if path.parent != NOTES_DIR.resolve():
        raise ValueError("Note name must be a simple name, not a path.")
    return path


@mcp.tool()
def list_notes() -> list[str]:
    """List the names of all available notes."""
    return sorted(p.stem for p in NOTES_DIR.glob("*.md"))


@mcp.tool()
def read_note(name: str) -> str:
    """Read the full text of one note by name (without the .md)."""
    path = _note_path(name)
    if not path.exists():
        return f"No note called '{name}'. Use list_notes to see what exists."
    return path.read_text(encoding="utf-8")


@mcp.tool()
def search_notes(query: str) -> list[str]:
    """Search all notes for a word or phrase (case-insensitive).
    Returns matching lines as 'note-name: line'."""
    results = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if query.lower() in line.lower():
                results.append(f"{path.stem}: {line.strip()}")
    return results or [f"No matches for '{query}'."]


@mcp.tool()
def add_note(name: str, content: str) -> str:
    """Create a new note. Refuses to overwrite an existing note."""
    path = _note_path(name)
    if path.exists():
        return f"A note called '{name}' already exists. Pick a different name."
    path.write_text(content, encoding="utf-8")
    return f"Created note '{name}'."


@mcp.tool()
def append_to_note(name: str, content: str) -> str:
    """Add text to the end of an existing note. Never replaces existing content."""
    path = _note_path(name)
    if not path.exists():
        return f"No note called '{name}'. Use add_note to create it first."
    with path.open("a", encoding="utf-8") as f:
        f.write("\n" + content)
    return f"Appended to note '{name}'."


@mcp.tool()
def delete_note(name: str) -> str:
    """Delete a note by moving it to a .trash folder (recoverable, not permanent)."""
    path = _note_path(name)
    if not path.exists():
        return f"No note called '{name}'."
    trash = NOTES_DIR / ".trash"
    trash.mkdir(exist_ok=True)
    path.replace(trash / path.name)
    return f"Moved note '{name}' to .trash. It can be restored from there."
    

if __name__ == "__main__":
    mcp.run()