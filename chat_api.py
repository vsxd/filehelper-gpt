import os
import logging
from typing import List

import openai

logging.basicConfig(
    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
    datefmt="%d-%M-%Y %H:%M:%S",
    level=logging.WARN
)

openai.api_key = os.getenv("OPENAI_API_KEY")


Q_PREFIX = "人类: "
A_PREFIX = "AI助手: "
MAX_HISTORY_COUNT = 1500


def get_completion(prompt: str) -> str:
    logging.info("get_completion(): Prompt: %s", prompt)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=400,
        temperature=0.9,
        top_p=1,
        n=1,
        stop=[Q_PREFIX, A_PREFIX],
        presence_penalty=0.6,
        echo=False,
    )
    logging.debug(response)
    return response.choices[0].text


def get_correction(text: str) -> str:
    response = openai.Edit.create(
        model="text-davinci-edit-001",
        input=text,
        instruction="Fix the spelling mistakes"
    )
    logging.debug(response)
    return response.choices[0].text


def get_image(description: str, num: int) -> List[str]:
    response = openai.Image.create(
        prompt=description,
        n=num,
        size="512x512"
    )
    result = []
    for data in response['data']:
        result.append(data['url'])
    return result
