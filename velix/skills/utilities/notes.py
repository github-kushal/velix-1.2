def take_note():
    """Function to take a note."""
    try:
        print("What would you like to write down?")
        note = input("Enter your note: ")
        with open("notes.txt", "a") as file:
            file.write(note + "\n")
        speak("Note saved successfully.")
    except Exception as e:
        speak("Sorry, I couldn't save the note.")