import openai


def generate_chatgpt_response(model, messages, temperature, max_tokens):
    """
    Generates a response using OpenAI's API
    """
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )
    
    return response["choices"][0]["message"]["content"]
