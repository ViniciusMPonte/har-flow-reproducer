from src.utils.encoding import decode_base64


def test_decode_base64_valid():
    assert decode_base64("SGVsbG8gV29ybGQ=") == "Hello World"

def test_decode_base64_json():
    # {"status": "ok"} in base64
    assert decode_base64("eyJzdGF0dXMiOiAib2sifQ==") == '{"status": "ok"}'

def test_decode_base64_invalid():
    # Test with invalid base64 or non-utf8
    # We use errors='replace' in the implementation, so it should not crash
    assert "" in decode_base64("invalid-base64-text")
