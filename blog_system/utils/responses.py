from typing import Any, Optional
from datetime import datetime

def standard_response(
    success: bool,
    data: Any = None,
    error: Optional[dict] = None,
    message: Optional[str] = None,
    request_id: Optional[str] = None
):
    response = {
        "success": success,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if request_id:
        response["request_id"] = request_id
        
    if success:
        if data is not None:
            response["data"] = data
        if message:
            response["message"] = message
    else:
        if error:
            response["error"] = error
            
    return response
