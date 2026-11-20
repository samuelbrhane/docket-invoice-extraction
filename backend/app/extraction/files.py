"""Turn an uploaded file into the input part the model reads."""

import base64


def document_input(content: bytes, content_type: str, filename: str) -> dict:
    data = base64.b64encode(content).decode()
    if content_type == "application/pdf":
        return {
            "type": "input_file",
            "filename": filename,
            "file_data": f"data:application/pdf;base64,{data}",
        }
    return {
        "type": "input_image",
        "image_url": f"data:{content_type};base64,{data}",
        "detail": "high",
    }