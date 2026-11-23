# base64-cli

Base64 encode/decode from the command line — standard or URL-safe alphabet,
text or files, stdin or arguments. Standard library only, no dependencies.

## Install

```bash
pip install .
```

This installs the `b64` command.

## Usage

```bash
b64 "hello world"                 # aGVsbG8gd29ybGQ=
b64 --decode aGVsbG8gd29ybGQ=     # hello world
b64 --urlsafe "hello world"       # URL-safe alphabet (- and _ instead of + and /)
echo "hello" | b64                # read from stdin
b64 --file notes.txt              # encode a file
b64 --decode --file encoded.b64   # decode a file
b64 --wrap 0 "hello world"        # no line wrapping (default wraps at 76 columns)
b64 --output out.txt "hello"      # write the result to a file
```

Decoding invalid Base64 exits with code 2 and a clear error message.

## Tests

```bash
python -m pytest
```

## License

MIT — see [LICENSE](LICENSE).
