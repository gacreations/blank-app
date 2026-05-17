import streamlit as st


NOTE_NAMES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]

# MIDI note numbers for open strings
STRING_TUNING = {
    "e": 64,  # E4
    "B": 59,  # B3
    "G": 55,  # G3
    "D": 50,  # D3
    "A": 45,  # A2
    "E": 40   # E2
}

STRING_ORDER = ["e", "B", "G", "D", "A", "E"]


def midi_to_note(midi_num):
    note = NOTE_NAMES[midi_num % 12]
    octave = (midi_num // 12) - 1
    return f"{note}{octave}"


def fret_to_note(string_name, fret):
    base_midi = STRING_TUNING[string_name]
    midi_note = base_midi + fret
    return midi_to_note(midi_note)


def parse_tab(tab_text):
    lines = tab_text.splitlines()
    processed = {}

    for line in lines:
        if not line.strip():
            continue

        string_name = line[0]
        if string_name not in STRING_TUNING:
            continue

        processed[string_name] = line[2:]

    if not processed:
        return []

    length = max(len(line) for line in processed.values())
    results = []
    i = 0

    while i < length:
        current_notes = []

        for string_name in STRING_ORDER:
            line = processed.get(string_name, "")
            if i < len(line) and line[i].isdigit():
                num = line[i]
                j = i + 1
                while j < len(line) and line[j].isdigit():
                    num += line[j]
                    j += 1

                fret = int(num)
                note = fret_to_note(string_name, fret)
                current_notes.append(note)

        if current_notes:
            results.append(current_notes)

        i += 1

    return results


st.title("Guitar Tab to Notes Converter")
st.write("Paste a 6-string guitar tab and convert the fretted numbers to letter notes.")

example_tab = """e|-------------0-2-3-2-0-------------|
B|-----------0-------------0-----------|
G|---------0-----------------0---------|
D|-------2---------------------2-------|
A|-----2-------------------------2-----|
E|---0-----------------------------0---|"""

user_input = st.text_area("Paste guitar tab here", value=example_tab, height=240)

if st.button("Convert"):
    if not user_input.strip():
        st.warning("Please paste guitar tab text before converting.")
    else:
        notes = parse_tab(user_input)
        if not notes:
            st.info("No convertible notes were found in the provided tab.")
        else:
            st.subheader("Converted Notes")
            note_display = []
            for note in notes:
                note = str(note)
                note = note.replace("[", "").replace("]", "").replace("'", "")
                note_display.append(note)
                #st.markdown(f":blue-badge[{note}]")
            note_display = [f":blue-badge[{n}]" for n in note_display]
            st.markdown(" | ".join(note_display))