import os
import logging

import openai


class ChatSession(object):
    _DEFAULT_START_STR = "下面是一段人类和AI助手的中文对话，这个AI助手的名字是XiXi助手，这个AI助手非常聪明，知识渊博，有创造性，友善。\n"
    _Q_PREFIX = "人类: "
    _A_PREFIX = "AI助手: "
    _MAX_HISTORY_COUNT = 1500

    _ARGS_MODEL = "text-davinci-003"
    _ARGS_TEMPERATURE = 0.9
    _ARGS_MAX_TOKENS = 500

    __API_KEY = os.getenv("OPENAI_API_KEY")

    def __init__(self):
        self._chat_history = []
        self._char_count = 0
        self._add_chat_history(self._DEFAULT_START_STR)

    def _del_oldest_chat_history(self):
        self._char_count -= len(self._chat_history[1])
        del self._chat_history[1]

    def _add_chat_history(self, new_msg):
        self._chat_history.append(new_msg)
        self._char_count += len(new_msg)
        while self._char_count > self._MAX_HISTORY_COUNT:
            self._del_oldest_chat_history()
            logging.debug(
                "reach max history count, clean up result: chat_history: %s\nchar_count: %d\n",
                self._chat_history,
                self._char_count
            )

    def _get_completion(self, prompt):
        logging.debug("get_completion(): Prompt: %s", prompt)
        response = openai.Completion.create(
            model=self._ARGS_MODEL,
            prompt=prompt,
            max_tokens=self._ARGS_MAX_TOKENS,
            temperature=self._ARGS_TEMPERATURE,
            top_p=1,
            n=1,
            stop=[self._Q_PREFIX, self._A_PREFIX],
            presence_penalty=0.6,
            echo=False,
        )
        logging.debug(response)
        return response.choices[0].text

    def _compose_prompt(self, text):
        ques = self._Q_PREFIX + text
        self._add_chat_history(ques)
        return "\n".join(self._chat_history) + "\n" + self._A_PREFIX

    def ask_question(self, ques):
        prompt = self._compose_prompt(ques)
        response = self._get_completion(prompt)
        ans = response.split(self._A_PREFIX)[-1].strip()
        self._add_chat_history(self._A_PREFIX + ans)
        return ans

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...
