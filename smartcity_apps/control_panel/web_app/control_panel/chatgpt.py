import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')


def prepare_prompt(prompt_ques="", data_set={}):

    if not prompt_ques or not data_set:
        return ""

    prompt = f"""
        You are an helpful assistant who have good knowledge of smart city management and data analytics.
        Below is a set of JSON data that you need to analyse and refer to for answering questions.

        {data_set}

        -------------------------------------

        Using above JSON data for smart city management, answer the following questions:

        {prompt_ques}

        Please give concise and direct answer instead of explaining too much.

    """
    return prompt


def gpt_api(prompt_ques="", data_set={}):
    messages = [{"role": "system", "content": "You are a intelligent assistant."}]

    _prompt = prepare_prompt(prompt_ques=prompt_ques, data_set=data_set)
    if not _prompt:
        return "Oops, something went wrong! Prompt is not configured properly. Please fix prompt and retry!"

    messages.append({"role": "user", "content": _prompt},)

    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        print(reply)
    except:
        reply = "Oops, something went wrong! Either data size is more than 40000 characters or OpenAI is rate limiting. Please try later on!"

    return reply
