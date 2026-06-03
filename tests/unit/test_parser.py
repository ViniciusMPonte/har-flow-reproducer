from pathlib import Path

import pytest

from src.parser.har_parser import HARParser
from src.parser.models import RequestModel, ResponseModel


def test_parse_entry_valid():
    # Mock HAR entry
    entry = {
        "request": {
            "method": "GET",
            "url": "https://example.com",
            "headers": [{"name": "h1", "value": "v1"}],
            "queryString": [{"name": "q", "value": "1"}]
        },
        "response": {
            "status": 200,
            "headers": [{"name": "h2", "value": "v2"}],
            "content": {
                "text": "hello",
                "mimeType": "text/plain"
            }
        }
    }
    
    parser = HARParser(Path("dummy.har"))
    req, res = parser.parse_entry(entry)
    
    assert isinstance(req, RequestModel)
    assert req.method == "GET"
    assert req.url == "https://example.com"
    assert req.headers[0].name == "h1"
    
    assert isinstance(res, ResponseModel)
    assert res.status == 200
    assert res.content.text == "hello"

def test_parse_entry_base64():
    entry = {
        "request": {
            "method": "GET",
            "url": "https://example.com",
            "headers": [],
            "queryString": []
        },
        "response": {
            "status": 200,
            "headers": [],
            "content": {
                "text": "SGVsbG8=",
                "encoding": "base64",
                "mimeType": "text/plain"
            }
        }
    }
    
    parser = HARParser(Path("dummy.har"))
    req, res = parser.parse_entry(entry)
    
    assert res.content.text == "Hello"

def test_load_har_invalid_format():
    # Create a bad HAR file
    bad_har = Path("tests/fixtures/bad_format.har")
    bad_har.parent.mkdir(parents=True, exist_ok=True)
    with open(bad_har, "w") as f:
        f.write('{"not_log": {}}')
        
    parser = HARParser(bad_har)
    with pytest.raises(ValueError, match="missing 'log' object"):
        parser.load_har()
