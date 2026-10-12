# Contributing

Thank you for helping improve offline text privacy tools.

Use synthetic examples only. Never include real CNICs, phone numbers, client names,
documents or credentials in issues, pull requests, screenshots or tests.

For a bug, describe the format that failed, provide a fictional input and expected
output, and state your Python version and operating system.

For changes, keep the runtime free of network calls and third-party dependencies
unless maintainers have discussed a scope change. Add a regression test for any
new detection format. Run `python -m unittest discover -s tests -v` before submitting.

Useful initial contributions:

- Synthetic test cases for additional Pakistani mobile formatting conventions.
- Urdu user instructions and feedback on right-to-left text display.
- Keyboard accessibility and desktop usability improvements.
- A clear design proposal for landline formats that minimises false positives.

Contributions must be your own work or appropriately licensed. Explain AI assistance
where relevant and review all submitted code. Contributions use the MIT licence.
