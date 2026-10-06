import pytest
import server


@pytest.fixture(autouse=True)
def temp_notes(tmp_path, monkeypatch):
    """Give every test its own empty notes folder, so your real notes are never touched."""
    monkeypatch.setattr(server, "NOTES_DIR", tmp_path)
    (tmp_path / "ideas.md").write_text("# Ideas\n- Build an MCP server\n", encoding="utf-8")


def test_list_notes():
    assert server.list_notes() == ["ideas"]


def test_read_note():
    assert "MCP" in server.read_note("ideas")


def test_read_missing_note():
    assert "No note called" in server.read_note("nope")


def test_search_finds_match():
    assert server.search_notes("mcp") == ["ideas: - Build an MCP server"]


def test_search_no_match():
    assert "No matches" in server.search_notes("zzz")[0]


def test_add_note_creates_file(tmp_path):
    server.add_note("todo", "- [ ] test")
    assert (tmp_path / "todo.md").read_text(encoding="utf-8") == "- [ ] test"


def test_add_note_refuses_overwrite():
    result = server.add_note("ideas", "overwritten")
    assert "already exists" in result
    assert "overwritten" not in server.read_note("ideas")


def test_path_traversal_is_blocked():
    with pytest.raises(ValueError):
        server.read_note("../server")

def test_append_to_note():
    server.append_to_note("ideas", "- Added later")
    assert "Added later" in server.read_note("ideas")
    assert "Build an MCP server" in server.read_note("ideas")


def test_append_to_missing_note():
    assert "No note called" in server.append_to_note("nope", "x")


def test_delete_moves_to_trash(tmp_path):
    server.delete_note("ideas")
    assert server.list_notes() == []
    assert (tmp_path / ".trash" / "ideas.md").exists()


def test_delete_missing_note():
    assert "No note called" in server.delete_note("nope")