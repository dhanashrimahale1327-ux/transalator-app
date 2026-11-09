import time
import tkinter as tk
from tkinter import ttk, messagebox

from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests
import pyttsx3


languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja",
    "Chinese": "zh-cn",
}


def translate_text():
    try:
        text = input_text.get("1.0", tk.END).strip()

        if not text:
            messagebox.showwarning("Warning", "Please enter text to translate.")
            return

        source = languages.get(source_lang.get(), "en")
        target = languages.get(target_lang.get(), "hi")

        if source == target:
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, text)
            return

        for attempt in range(2):
            try:
                translated = GoogleTranslator(source=source, target=target).translate(text)
                break
            except TooManyRequests:
                if attempt == 0:
                    time.sleep(2)
                    continue
                messagebox.showwarning(
                    "Translation limit reached",
                    "Google translation is busy right now. Please wait a few seconds and try again.",
                )
                return

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

    except Exception as exc:
        messagebox.showerror("Error", f"Translation failed: {exc}")


def copy_text():
    translated = output_text.get("1.0", tk.END).strip()

    if not translated:
        messagebox.showwarning("Warning", "There is no translated text to copy.")
        return

    root.clipboard_clear()
    root.clipboard_append(translated)
    messagebox.showinfo("Copied", "Translated text copied successfully!")


def speak_text():
    text = output_text.get("1.0", tk.END).strip()

    if not text:
        messagebox.showwarning("Warning", "There is no translated text to speak.")
        return

    if engine is None:
        messagebox.showerror("Error", "Text-to-speech engine is not available.")
        return

    engine.say(text)
    engine.runAndWait()


def swap_languages():
    src = source_lang.get()
    dest = target_lang.get()

    source_lang.set(dest)
    target_lang.set(src)


# Main Window
root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("800x600")
root.config(bg="#f5f5f5")

try:
    engine = pyttsx3.init()
except Exception:
    engine = None

# Heading
title = tk.Label(
    root,
    text="🌍 Language Translation Tool",
    font=("Arial", 20, "bold"),
    bg="#f5f5f5",
    fg="#0078D7",
)
title.pack(pady=15)

# Input Label
input_label = tk.Label(
    root,
    text="Enter Text:",
    font=("Arial", 12),
    bg="#f5f5f5",
)
input_label.pack()

# Input Text Area
input_text = tk.Text(
    root,
    height=7,
    width=85,
    font=("Arial", 11),
)
input_text.pack(pady=10)

# Language Selection Frame
lang_frame = tk.Frame(root, bg="#f5f5f5")
lang_frame.pack(pady=10)

source_lang = tk.StringVar(value="English")
target_lang = tk.StringVar(value="Hindi")

source_combo = ttk.Combobox(
    lang_frame,
    textvariable=source_lang,
    values=list(languages.keys()),
    state="readonly",
    width=20,
)
source_combo.grid(row=0, column=0, padx=10)

swap_btn = tk.Button(
    lang_frame,
    text="⇄",
    font=("Arial", 12, "bold"),
    command=swap_languages,
)
swap_btn.grid(row=0, column=1)

target_combo = ttk.Combobox(
    lang_frame,
    textvariable=target_lang,
    values=list(languages.keys()),
    state="readonly",
    width=20,
)
target_combo.grid(row=0, column=2, padx=10)

# Translate Button
translate_btn = tk.Button(
    root,
    text="Translate",
    command=translate_text,
    bg="#0078D7",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20,
)
translate_btn.pack(pady=15)

# Output Label
output_label = tk.Label(
    root,
    text="Translated Text:",
    font=("Arial", 12),
    bg="#f5f5f5",
)
output_label.pack()

# Output Area
output_text = tk.Text(
    root,
    height=7,
    width=85,
    font=("Arial", 11),
)
output_text.pack(pady=10)

# Action Buttons
button_frame = tk.Frame(root, bg="#f5f5f5")
button_frame.pack(pady=15)

copy_btn = tk.Button(
    button_frame,
    text="Copy",
    width=15,
    command=copy_text,
)
copy_btn.grid(row=0, column=0, padx=10)

speak_btn = tk.Button(
    button_frame,
    text="Speak",
    width=15,
    command=speak_text,
)
speak_btn.grid(row=0, column=1, padx=10)

root.mainloop()