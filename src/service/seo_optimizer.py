import json
import os
from loguru import logger
from openapi_schema_to_json_schema import to_json_schema

import openai


def get_chat_completion(messages, model="gpt-3.5-turbo-0613", ):
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response


def get_SEO_optiomized_data(text):
    messages = [
        {
            "role": "system",
            "content": f"""
                Act as a expert Youtube SEO optmizer. Your task is to create an engaging and SEO-friendly title," 
                    description and tags for a Youtube video focusing on "How To Embed A Custom ChatGPT Chatbot Into Your 
                    Website". Please utilize the key points and learning objectives from the video listed below. 
                    Please return the output as JSON with attributes "title", "description" and "tags". 
                    No explanation is needed, so just return the JSON.
                """,
        },
        {"role": "user", "content": text},
    ]
    try:
        chat_completion = get_chat_completion(messages)
    except Exception as e:
        raise Exception('Invalid gpt response')
    if "choices" not in chat_completion:
        logger.error(f'choice field not present in gpt response: {chat_completion}')
        raise Exception("choices field not present in gpt response")
    data = chat_completion["choices"][0]
    json_data = to_json_schema(data)
    if "message" not in json_data or "content" not in json_data["message"]:
        logger.error(f'message or content field not present in gpt response: {chat_completion}')
        raise Exception("message or content field not present in gpt response")
    content = json_data["message"]["content"]
    return json.loads(content)