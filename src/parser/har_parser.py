import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .models import Header, RequestModel, ResponseContent, ResponseModel


class HARParser:
    def __init__(self, har_path: Path):
        self.har_path = har_path

    def load_har(self) -> List[Dict[str, Any]]:
        """Loads and validates the HAR file."""
        with open(self.har_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict):
            raise ValueError("Invalid HAR format: Root element must be a JSON object")
        
        if "log" not in data:
            raise ValueError("Invalid HAR format: missing 'log' object")
            
        if "entries" not in data["log"]:
            raise ValueError("Invalid HAR format: missing 'log.entries' list")
            
        if not isinstance(data["log"]["entries"], list):
            raise ValueError("Invalid HAR format: 'log.entries' must be a list")
            
        return data["log"]["entries"]

    def _extract_headers(self, headers_list: List[Dict[str, str]]) -> List[Header]:
        """Extracts headers into a list of Header models."""
        return [Header(name=h["name"], value=h["value"]) for h in headers_list]

    def parse_entry(self, entry: Dict[str, Any]) -> Tuple[RequestModel, ResponseModel]:
        """Parses a single HAR entry into Request and Response models."""
        req_data = entry["request"]
        res_data = entry["response"]

        request = RequestModel(
            method=req_data["method"],
            url=req_data["url"],
            headers=self._extract_headers(req_data["headers"]),
            postData=req_data.get("postData"),
            queryString=self._extract_headers(req_data.get("queryString", [])) if req_data.get("queryString") else None
        )

        res_content_data = res_data["content"]
        content_text = res_content_data.get("text", "")
        
        # T015: Detect base64 encoding and decode content
        if res_content_data.get("encoding") == "base64":
            from ..utils.encoding import decode_base64
            content_text = decode_base64(content_text)

        # T016: The ResponseContent model doesn't have 'encoding' field, 
        # so it's automatically removed when we create the model.
        response = ResponseModel(
            status=res_data["status"],
            headers=self._extract_headers(res_data["headers"]),
            content=ResponseContent(
                text=content_text,
                mimeType=res_content_data.get("mimeType")
            )
        )

        return request, response

    def split_har(self, output_dir: Path) -> None:
        """Splits the HAR file into individual request and response JSON files."""
        entries = self.load_har()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        from ..utils.files import write_json_file
        
        for i, entry in enumerate(entries, 1):
            request, response = self.parse_entry(entry)
            
            # Use 4-digit index by default, expand to 5 if entries > 9999
            width = 5 if len(entries) > 9999 else 4
            index = f"{i:0{width}d}"
            
            write_json_file(output_dir / f"req_{index}.json", request.model_dump())
            write_json_file(output_dir / f"res_{index}.json", response.model_dump())

