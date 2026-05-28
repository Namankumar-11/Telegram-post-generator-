from llm_helper import llm
from few_shot import FewShotPosts

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"
    return "6 to 10 lines"


def generate_post(length, language, tag):
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''Generate a LinkedIn post using the below information. No preamble.

1) Topic: {tag}
2) Length: {length_str}
3) Language: {language}
If Language is Hinglish then it means it is a mix of Hindi and English. 
The script for the generated post should always be written in standard English alphabet script characters.
'''
    try:
        few_shot = FewShotPosts()
        examples = few_shot.get_filtered_posts(length, language, tag)

        if len(examples) > 0:
            prompt += "\n4) Use the writing style as per the following examples:\n"
            for i, post in enumerate(examples):
                post_text = post.get('text', '')
                prompt += f'\nExample {i+1}: \n"{post_text}"\n'
                if i == 1:
                    break
    except Exception:
        pass

    return prompt
