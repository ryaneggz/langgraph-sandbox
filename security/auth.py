import os
from typing import Dict
from langgraph_sdk import Auth

auth = Auth()

@auth.authenticate
async def authenticate(headers):
    """
    Authentication handler for xml_agent.
    Validates API key from x-api-key header against environment variables.
    """
    # Handle both string and bytes headers
    if isinstance(headers, dict):
        # Convert bytes keys/values to strings if needed
        str_headers = {}
        for key, value in headers.items():
            key_str = key.decode() if isinstance(key, bytes) else str(key)
            value_str = value.decode() if isinstance(value, bytes) else str(value)
            str_headers[key_str] = value_str
        headers = str_headers
    
    api_key = headers.get("x-api-key")
    
    if not api_key:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Missing API key. Please provide x-api-key header."
        )
    
    # Get valid keys from environment variables
    valid_keys = []
    
    # Check for multiple API key environment variables
    xml_agent_key = os.getenv("XML_AGENT_API_KEY")
    admin_key = os.getenv("ADMIN_API_KEY")
    demo_key = os.getenv("DEMO_API_KEY")
    
    if xml_agent_key:
        valid_keys.append(xml_agent_key)
    if admin_key:
        valid_keys.append(admin_key)
    if demo_key:
        valid_keys.append(demo_key)
    
    # Fallback to a single API key if no specific keys are set
    if not valid_keys:
        fallback_key = os.getenv("API_KEY")
        if fallback_key:
            valid_keys.append(fallback_key)
    
    if not valid_keys:
        raise Auth.exceptions.HTTPException(
            status_code=500,
            detail="Server configuration error: No API keys configured"
        )
    
    if api_key not in valid_keys:
        raise Auth.exceptions.HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    
    # Return minimal user information
    return {
        "identity": f"user-{api_key[:8]}",
        "is_authenticated": True,
    }