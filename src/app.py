from openai import OpenAI
from dotenv import load_dotenv
import gradio as gr
import os

load_dotenv(override=True)

from context import TWIN_SYSTEM_PROMPT
from tools import tools, handle_tool_calls
from styles import CSS, JS, EXAMPLES

API_KEY = os.environ.get("MY_API_KEY")
API_ENDPOINT = os.environ.get("MY_API_ENDPOINT")
MAX_TOOL_ROUNDS = int(os.environ.get("MAX_TOOL_ROUNDS", 5))
model_name = os.environ.get("MODEL_NAME", "gpt-5.4-mini")
openai_client = OpenAI(api_key=API_KEY, base_url=API_ENDPOINT)

system = [{"role": "system", "content": TWIN_SYSTEM_PROMPT}]

def chat(message, history):
    messages = system + history + [{"role": "user", "content": message}]

    for _ in range(MAX_TOOL_ROUNDS):
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=tools
        )

        msg = response.choices[0].message
        if not msg.tool_calls:
            return msg.content or ""
        messages.append(msg)
        messages.extend(handle_tool_calls(msg.tool_calls))
        
    print("Tool calls hit limit")

    response = openai_client.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=tools,
                tool_choice="none"
            )

    return response.choices[0].message.content or ""


if __name__ == "__main__":
    gr.ChatInterface(
        chat,
        examples=EXAMPLES,
        title="Digital Twin Chat",
        description="Chat with my digital twin about my career",
        chatbot=gr.Chatbot(show_label=False),
    ).launch(css=CSS, js=JS, theme=gr.themes.Base())