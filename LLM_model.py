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

    @staticmethod
    def extract_code_from_text(text):
        pattern = r'```(?:\w+)?([\s\S]*?)```'
        matches = re.findall(pattern, text)

        return matches


