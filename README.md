# Nabilaws Text Shield

A small offline Python tool for masking common personal identifiers in plain text.
Built for people preparing text for review, including small legal offices in Pakistan.

**Status: early prototype, v0.1.0.** Not independently security audited. No adoption,
external contributors, or program eligibility is claimed. Initial implementation was
created with AI assistance and should be reviewed by the maintainer before release.

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

## Command line

Run from the project folder:

```sh
python shield.py examples/sample.txt masked-example.txt --terms-file examples/terms.txt
```

The output file must not already exist. The tool will not overwrite it.
Use `py` instead of `python` if that is your Windows launcher.

## Reuse in another Python project

```python
from shield import redact

result = redact("Email client@example.com; Example Client", ["Example Client"])
assert result.text == "Email [EMAIL]; [CUSTOM]"
print(result.counts)  # Counts only; no original identifiers.
```

Copy `shield.py` into your project and retain the MIT licence. This prototype is
not currently published to a package registry.

## Scope and limitations

This is pattern-based assistance, not guaranteed anonymisation. Always inspect
the full result before sharing. It can miss unusual formats and mask unrelated
number strings. CNIC-like matches are not checked against any identity database.
Names, addresses, case numbers, bank details, landlines and other countries' phone
numbers are not automatically detected. Add exact phrases manually where needed.
Custom phrases match case-insensitive substrings, so short terms can over-mask.
Overlapping matches are merged to avoid leaving sensitive fragments behind;
counts represent merged replacement spans, not unique people or identifiers.

Only UTF-8 plain text is supported. Do not rename PDFs or Word files to `.txt`.
PDFs, images, scans, document metadata, attachments and OCR are not processed.
Urdu strings are supported, but desktop right-to-left display may vary by platform.

There are no uploads, analytics, reverse maps or content logs in this tool.
The original file is retained. Text remains in process memory while running;
this tool does not securely erase memory, clipboard contents or operating-system
backups. Use synthetic examples in public issues; never upload client files.

## Development

```sh
python -m unittest discover -s tests -v
```

See CONTRIBUTING.md for contribution ideas and SECURITY.md for reporting problems.
The repository includes a GitHub Actions workflow for the test suite.

## Publish on GitHub

1. Sign in to your GitHub account and create a **public** repository named
   `nabilaws-text-shield`.
2. Upload the contents of this folder, preserving subfolders. Upload source files,
   not just the ZIP. Do not include real documents or generated private outputs.
3. Confirm README.md appears on the repository home page and tests pass under Actions.
4. Ask real users to try the tool with fictional data and report useful improvements.
5. Maintain it, review contributions, and document actual usage before claiming impact.

Suggested description: "Offline Python text masking for email addresses, Pakistani
mobile numbers, CNIC-like strings, and custom English/Urdu phrases."

## Claude for Open Source

Creating this repository does **not** establish eligibility. Anthropic's listed
routes involve substantial adoption, recognised core contributions, external
contributions, or infrastructure importance. Its application also allows maintainers
to explain smaller projects' actual ecosystem importance. Approval is discretionary.
Check the current criteria: https://claude.com/contact-sales/claude-for-oss

At launch, accurately describe this as a new prototype. Do not claim users,
downloads, contributors, or integrations without evidence. Do not manufacture
activity to meet thresholds. A practical next step is to improve the tool in
response to real community needs, not apply with invented impact.

## Licence

MIT — see LICENSE.
