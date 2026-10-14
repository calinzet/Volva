import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from call_functions import available_functions, call_function
from prompts import system_prompt
import sys

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("NO KEY WAS PROVIDED")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def agentic():
    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning:free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )
    return response

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):

    response = agentic()
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("Return message should not be empty")
            if args.verbose:
                print(f"-> {result_message['content']}")


    else:
        print(message.content)
        break
else:
    print("could not give an answer after 20 itterations")
    sys.exit(1)
