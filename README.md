# Nabilaws Text Shield

A small offline Python tool for masking common personal identifiers in plain text.
Built for people preparing text for review, including small legal offices in Pakistan.

## What it does

- Masks common email address formats with `[EMAIL]`.
- Masks 13-digit CNIC-like strings, with optional spaces or hyphens, with `[CNIC]`.
- Masks common Pakistani mobile formats beginning 03, +923, or 00923 with `[PHONE]`.
- Masks user-specified literal names and phrases with `[CUSTOM]`, including Urdu.
- Provides a desktop window, command-line interface, and reusable Python function.
- Runs without third-party Python packages or network requests.
- Writes a new UTF-8 plain-text file, preserving the original.

## Start on Windows

1. Install Python 3.10 or newer from https://www.python.org/downloads/ if needed.
   Include Tcl/Tk support for the desktop window.
2. Extract this ZIP. Open the extracted project folder in File Explorer.
3. Type `cmd` in the address bar and press Enter.
4. Run `py desktop.py`.
5. Paste text or open a UTF-8 `.txt` file. Add names/phrases one per line.
6. Select **Mask text**, review the result, then **Save masked .txt**.

On other systems use `python3 desktop.py`. Tkinter must be installed to use the
window; some Linux Python installations package it separately. The CLI needs no Tk.


