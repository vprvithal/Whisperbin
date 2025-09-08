import uuid

# This dictionary acts as our temporary, in-memory database.
notes_storage = {}

def create_note(secret_content):
    """
    Generates a unique ID, stores the note, and returns the ID.
    """
    note_id = str(uuid.uuid4())[:8]
    notes_storage[note_id] = secret_content
    print(f"[*] Note created with ID: {note_id}")
    return note_id

def get_note(note_id):
    """
    Retrieves a note using its ID and then deletes it (self-destructs).
    """
    return notes_storage.pop(note_id, None)