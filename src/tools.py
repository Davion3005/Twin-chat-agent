import json
import os
import requests

PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

def push(message):
    user = os.environ.get("PUSHOVER_USER")
    token = os.environ.get("PUSHOVER_TOKEN")
    if not user or not token:
        raise RuntimeError("Pushover credentials are not set")
    
    resp = requests.post(
        PUSHOVER_URL, 
        data={
            "user": user,
            "token": token,
            "message": message
        }, timeout=10)
    resp.raise_for_status()

    return resp.json()

def record_user_details(email, name = "Name not provided", notes="Notes not provided"):
    return push(f"New user details recorded:\nEmail: {email}\nName: {name}\nNotes: {notes}")

def record_unknown_question(question):
    return push(f"New unknown question recorded:\nQuestion: {question}")

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record user who is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of the user"
            },
            "name": {
                "type": "string",
                "description": "The name of the user, if provided"
            },
            "notes": {
                "type": "string",
                "description": "Any additional notes about the conversation that's worth recording for context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you don't know the answer.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json}
]

AVAILABLE_TOOLS = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question
}

def handle_tool_invocation(tool_name, tool_args):
    if tool_name in AVAILABLE_TOOLS:
        tool_function = AVAILABLE_TOOLS[tool_name]
        return tool_function(**tool_args)
    else:
        raise ValueError(f"Tool '{tool_name}' is not available.")

def handle_tool_calls(tool_calls):
    print(f"Handling tool calls: {tool_calls}")
    results = []
    for call in tool_calls:
        name = call.function.name
        try:
            args = json.loads(call.function.arguments)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON arguments for tool '{name}': {e}")
            result = f"Error decoding JSON arguments for tool '{name}': {e}"
        else:
            try:
                result = handle_tool_invocation(name, args)
                print(f"Tool '{name}' executed successfully")
            except Exception as e:
                print(f"Error executing tool '{name}': {e}")
                result = f"Error executing tool '{name}': {e}"
        
        results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": call.id})
    
    return results