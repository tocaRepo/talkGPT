import os
import time
import utils.VAConstants as constants
from utils.logger import Logger
import prompts.generate_response as generate_response_prompt

import clients.open_ai_client as openAiClient


# Create a logger instance with the name "chatGPTService"
logger = Logger("chatGPTService")

GPT_VERSION = "gpt-3.5-turbo"  # "gpt-4"#"gpt-3.5-turbo"

def generate_response(prompt, memories,previousPrompt,previousResponse):
    """
    Generates a response to a given prompt using the OpenAI GPT-3 API.
    """

    temperature = 0.70
    max_tokens = 1000
    messages = []
    memories_text, preferences_text = _extract_memory_and_preference_text(memories)
 
    formatted_SystemPrompt = (
            generate_response_prompt.PROMPT_GENERIC.format(
                ", ".join(memories_text), ", ".join(preferences_text)
            )
        )
    logger.info("user prompt:" + prompt)
    logger.info("formatted_SystemPrompt:" + formatted_SystemPrompt)
    messages.append({"role": "system", "content": formatted_SystemPrompt})
    if previousResponse and previousPrompt:
        messages.append({"role": "user", "content": previousPrompt})
        messages.append({"role": "system", "content": previousResponse})
    messages.append({"role": "user", "content": prompt})
    
    # "gpt-4" gptVersion
    response= openAiClient.generate_chatgpt_response(
        GPT_VERSION, messages, temperature, max_tokens
    )
    save_conversation(prompt,response)
    return response

def save_conversation(prompt, response):
    """
    Saves the conversation to a text file.
    """
    try:
        conversationName = "conversation_{}.txt".format(int(time.time()))
        with open(constants.OUTPUT_FOLDER + conversationName, "a") as f:
            f.write("Prompt: {}\n".format(prompt))
            f.write("Response: {}\n".format(response))
    except UnicodeEncodeError as e:
        # handle the error, e.g. logger.info an error message
        logger.info(f"UnicodeEncodeError: {e}")


def _extract_memory_and_preference_text(memories):
    memories_text = []
    preferences_text = []
    for memory_item in memories:
        memory = memory_item["memory"]
        memory_text = memory["text"]
        memory_tag = memory["tag"].lower()
        if memory_tag == "memory":
            memories_text.append(memory_text)
        elif memory_tag == "preference":
            preferences_text.append(memory_text)
    return memories_text, preferences_text

