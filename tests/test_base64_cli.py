"""Tests for base64-cli."""

import pytest

from b64_cli import decode_bytes, decode_text, encode_bytes, encode_text, wrap_text
from b64_cli.cli import run


def test_encode_text():
    assert encode_text("hello world") == "aGVsbG8gd29ybGQ="
    assert encode_text("") == ""
    assert encode_text("Man") == "TWFu"


def test_encode_unicode():
    # UTF-8 bytes, not ASCII: "café" -> Y2Fmw6k=
    assert encode_text("café") == "Y2Fmw6k="


def test_decode_text():
    assert decode_text("aGVsbG8gd29ybGQ=") == "hello world"
    assert decode_text("") == ""
    assert decode_text("TWFu") == "Man"


def test_round_trip():
    for text in ["hello world", "café ☕", "12345", "a" * 100]:
        assert decode_text(encode_text(text)) == text


def test_urlsafe_alphabet():
    # Bytes 0xfb 0xff encode to "+/8=" standard, "-_8=" URL-safe.
    data = b"\xfb\xff"
    assert encode_bytes(data) == "+/8="
    assert encode_bytes(data, urlsafe=True) == "-_8="
    assert decode_bytes("-_8=", urlsafe=True) == data
    assert decode_bytes("+/8=") == data


def test_decode_rejects_bad_input():
    with pytest.raises(ValueError):
        decode_text("not!base64!!")
    with pytest.raises(ValueError):
        decode_text("aGVsbG8")  # missing padding


def test_decode_ignores_whitespace():
    assert decode_text("aGVs\nbG8g\nd29y\nbGQ=") == "hello world"


def test_wrap_text():
    assert wrap_text("abcdefghij", 4) == "abcd\nefgh\nij"
    assert wrap_text("abc", 76) == "abc"
    assert wrap_text("abcdefghij", 0) == "abcdefghij"
    assert wrap_text("abcdefghij", -1) == "abcdefghij"


def test_cli_encode_text(capsys):
    assert run(["hello world"]) == 0
    assert capsys.readouterr().out.strip() == "aGVsbG8gd29ybGQ="


def test_cli_decode_text(capsys):
    assert run(["--decode", "aGVsbG8gd29ybGQ="]) == 0
    assert capsys.readouterr().out.strip() == "hello world"


def test_cli_urlsafe(capsys):
    assert run(["--urlsafe", "--wrap", "0", ">>>???"]) == 0
    out = capsys.readouterr().out.strip()
    assert "+" not in out and "/" not in out


def test_cli_invalid_decode(capsys):
    assert run(["--decode", "!!!"]) == 2
    assert "error" in capsys.readouterr().err


def test_cli_missing_file(capsys):
    assert run(["--file", "no-such-file.b64"]) == 2
    assert "error" in capsys.readouterr().err


def test_cli_file_round_trip(tmp_path, capsys):
    source = tmp_path / "in.txt"
    source.write_text("hello world", encoding="utf-8")
    assert run(["--file", "--wrap", "0", str(source)]) == 0
    encoded = capsys.readouterr().out.strip()
    assert encoded == "aGVsbG8gd29ybGQ="
    assert run(["--decode", encoded]) == 0
    assert capsys.readouterr().out.strip() == "hello world"
