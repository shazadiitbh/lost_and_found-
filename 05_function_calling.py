"""
What this teaches:
    Function calling (also called "tools"). The model cannot check the weather or read your files.
    But it can ASK your code to do it. The loop is:
      1. You tell the model which functions exist.
      2. The model replies "please run get_weather with city=Mumbai".
      3. YOUR code runs the function.
      4. You send the result back, and the model writes the final answer.
    The function here is fake on purpose. It returns clearly labelled sample text.

How to run it:
    python 05_function_calling.py

What you should see:
    Three printed steps: "Model asked to run ...", "Our code returned ...", "Model's final answer".
    The final answer should use the sample text from our fake function.
"""

from google.genai import types

import gemma_client


# The function the model may ask for. It is fake: it does not look at any real weather.
def get_weather(city):
    return f"SAMPLE DATA, not real weather: {city} is 22 C and sunny."


# Step 1: describe the function to the model. It never sees our code, only this description.
weather_tool = types.Tool(function_declarations=[{
    "name": "get_weather",
    "description": "Get the current weather for a city.",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "City name, for example Mumbai"}},
        "required": ["city"],
    },
}])
config = types.GenerateContentConfig(tools=[weather_tool])

# `contents` is the conversation so far. We add to it as we go.
contents = [types.Content(role="user", parts=[types.Part(text="Should I carry an umbrella in Mumbai today?")])]

# Step 2: ask. The model should reply with a function call instead of text.
response = gemma_client.generate_raw(contents, config)

if not response.function_calls:
    print("The model answered without using the tool:", response.text)
    raise SystemExit

call = response.function_calls[0]
print(f"Model asked to run {call.name} with {dict(call.args)}")

# Step 3: our code runs the function.
result = get_weather(**call.args)
print(f"Our code returned: {result}")

# Step 4: send the model's request and our result back, so it can write the final answer.
contents.append(response.candidates[0].content)  # the model's own turn (its function call)
reply = types.FunctionResponse(id=call.id, name=call.name, response={"result": result})
contents.append(types.Content(role="user", parts=[types.Part(function_response=reply)]))
final = gemma_client.generate_raw(contents, config)

print(f"Model's final answer: {final.text}")
