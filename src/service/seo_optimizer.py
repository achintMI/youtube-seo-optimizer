import json
import os
from loguru import logger
from openapi_schema_to_json_schema import to_json_schema

import openai


def get_chat_completion(messages, model="gpt-3.5-turbo", ):
    response = openai.ChatCompletion.create(model=model, messages=messages)
    return response


def get_SEO_optiomized_data(content, debug=False):
    messages = [
        {
            "role": "system",
            "content": f"""
                Act as an expert Youtube SEO optimizer. Your task is to create an engaging and SEO-friendly title, description, and tags for a Youtube video. Utilize the key points and learning objectives from the video transcript (provided below) to create your output.
                Please return the output in JSON format with attributes "title", "description", and "tags". No explanation is needed; simply return the JSON.
                Please use best practices for Youtube description writing. 
                Instructions: 
                1. Use hashtags
                2. Provide at least 20-30 semantically related keywords for SEO
                3. Provide step-by-step guides. 
                4. Provide 2-3 FAQ questions. 
                5. Provide long descriptions that attract SEO matches.
                6. tags should be comma seprated strings

                ---- START OF TRANSCRIPT --- 
                TITLE: {content['title']} 

                {content['captions']} 

                ---- END OF TRANSCRIPT --- 
                """,
        },
        {"role": "user", "content": "optimize the Youtube SEO for the video and give me the output in json format."},
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
    
    resp = json.loads(content)
    if debug:
        resp = {"request": messages, "response": resp}
    return resp
