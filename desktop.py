"""Run with python desktop.py. No network requests or autosave."""
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from shield import redact


def main():
    root = tk.Tk()
    root.title("Nabilaws Text Shield • Offline text masking")
    root.geometry("980x760")
    root.minsize(640, 600)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)
    root.rowconfigure(6, weight=1)
    ttk.Label(root, text="Nabilaws Text Shield", font=("Segoe UI", 21, "bold")).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 4))
    ttk.Label(root, text="Offline • Plain text only • Review every result before sharing").grid(row=1, column=0, sticky="w", padx=20)
    source = ScrolledText(root, height=10, wrap="word", font=("Segoe UI", 11), undo=False)
    source.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
    ttk.Label(root, text="Additional names or phrases to mask (one per line, including Urdu)").grid(row=3, column=0, sticky="w", padx=20)
    terms = ScrolledText(root, height=3, wrap="word", font=("Segoe UI", 11), undo=False)
    terms.grid(row=4, column=0, sticky="ew", padx=20, pady=6)
    buttons = ttk.Frame(root)
    buttons.grid(row=5, column=0, sticky="ew", padx=20, pady=6)
    output = ScrolledText(root, height=10, wrap="word", font=("Segoe UI", 11), state="disabled")
    output.grid(row=6, column=0, sticky="nsew", padx=20, pady=10)
    status = tk.StringVar(value="Paste text above or open a UTF-8 .txt file.")
    ttk.Label(root, textvariable=status, wraplength=900).grid(row=7, column=0, sticky="w", padx=20, pady=(0, 14))
    current = {"result": None, "source_path": None}

    def set_output(value):
        output.configure(state="normal")
        output.delete("1.0", "end")
        output.insert("1.0", value)
        output.configure(state="disabled")

    def invalidate(event=None):
        widget = event.widget if event else None
        if widget and not widget.edit_modified():
            return
        current["result"] = None
        set_output("")
        save_button.configure(state="disabled")
        status.set("Text changed. Select Mask text to generate a fresh result.")
        if widget:
            widget.edit_modified(False)

    def open_text():
        name = filedialog.askopenfilename(filetypes=[("Plain text", "*.txt")])
        if not name:
            return
        try:
            text = Path(name).read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            messagebox.showerror("Cannot open", str(exc))
            return
        source.delete("1.0", "end")
        source.insert("1.0", text)
        current["source_path"] = Path(name).resolve()

    def process():
        root.update_idletasks()
        result = redact(source.get("1.0", "end-1c"), terms.get("1.0", "end-1c").splitlines())
        current["result"] = result
        set_output(result.text)
        save_button.configure(state="normal")
        summary = ", ".join(f"{key}: {value}" for key, value in result.counts.items()) or "No matches"
        status.set(summary + ". Names and addresses are not automatically detected. Review the output.")

    def save():
        result = current["result"]
        if result is None:
            return
        name = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="masked.txt", filetypes=[("Plain text", "*.txt")])
        if not name:
            return
        try:
            if Path(name).resolve() == current["source_path"]:
                raise ValueError("Choose a different filename to preserve the original.")
            with Path(name).open("x", encoding="utf-8") as file:
                file.write(result.text)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Cannot save — choose a new filename", str(exc))
            return
        status.set("Masked text saved. Review it carefully before sharing.")

    def clear():
        source.delete("1.0", "end")
        terms.delete("1.0", "end")
        current["source_path"] = None
        invalidate()

    ttk.Button(buttons, text="Open .txt", command=open_text).pack(side="left", padx=(0, 8))
    ttk.Button(buttons, text="Mask text", command=process).pack(side="left", padx=8)
    save_button = ttk.Button(buttons, text="Save masked .txt", command=save, state="disabled")
    save_button.pack(side="left", padx=8)
    ttk.Button(buttons, text="Clear", command=clear).pack(side="right")
    source.bind("<<Modified>>", invalidate)
    terms.bind("<<Modified>>", invalidate)
    root.mainloop()


if __name__ == "__main__":
    main()
