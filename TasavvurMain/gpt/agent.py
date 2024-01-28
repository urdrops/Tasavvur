from openai import OpenAI
import re

client = OpenAI(api_key="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")


class LLM:
    def __init__(self, system_prompt):
        self.client = client
        self.history = [
            {"role": "system", "content": system_prompt},
        ]

    def conversation(self, input_text):

        self.history += [{"role": "user", "content": input_text}]
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.history,
            stream=True
        )

        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response += str(chunk.choices[0].delta.content)
                yield chunk.choices[0].delta.content

        self.history += [{"role": "assistant", "content": response}]

    def add_system_prompt(self, json_prompt):
        self.history += [json_prompt]
        print("\nadded system prompt to history\n")
        return self.history[-1]

    @staticmethod
    def extract_code_from_text(text):
        pattern = r'```(?:\w+)?([\s\S]*?)```'
        matches = re.findall(pattern, text)

        return matches

    @staticmethod
    def last_100_words(text):
        match = re.findall(r'\b\w+\b', text)

        if match and len(match) > 80:
            return ' '.join(match[-80:])
        else:
            return text


class SerchLLM(LLM):
    def __init__(self, system_prompt):
        super().__init__(system_prompt)

    @staticmethod
    def prompt_search_engine(prompt: str):
        pass
