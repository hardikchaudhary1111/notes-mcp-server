# Design Decisions

## Plain markdown files, not a database or Notion
No account, API key or setup is needed, and the notes stay readable in any editor. The tools are the interesting part, and they work the same way with any backend.

## Claude's arguments are untrusted input
Claude chooses the arguments for every tool call, and that can be influenced by a prompt or by text inside a note. So the server enforces its own limits instead of trusting the model.

## Path traversal guard
`_note_path` resolves every name to a full path and rejects anything outside the notes folder. A request like `../server` raises an error instead of exposing other files. This is tested manually through Claude Code and in the automated suite.

## `add_note` never overwrites
Creating a note that already exists returns a message instead of replacing it. A mistaken call can't destroy existing work.

## `append_to_note` instead of an "edit" tool
Appending can only add content. A general edit or overwrite tool would give a model a much easier way to lose data.

## `delete_note` is a soft delete
Notes are moved to `notes/.trash`, not removed. Any deletion can be undone by moving the file back.

## Tests use a temporary folder
Each test gets its own empty notes directory, so tests are repeatable and can never damage real notes.

## Known limitations
- Flat folder only: no subfolders or nested notes.
- No file size limits on notes.
- No locking, so two clients writing at once could clash.
- Built for one local user, so no authentication. A remote version would need it.