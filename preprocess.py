import json
import os
from llm_helper import llm
import langchain_core.prompts
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def sanitize_text(text):
    """
    Encodes text to UTF-8 and decodes it while ignoring broken surrogate characters 
    that cause API request payloads to crash.
    """
    if not isinstance(text, str):
        return text
    # 'surrogateescape' or 'ignore' handles the bad character errors cleanly
    return text.encode('utf-8', errors='ignore').decode('utf-8')

def process_posts(raw_file_path, processed_file_path):
    # Read raw posts
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)

    enriched_posts = []

    # Extract metadata for each post
    for post in posts:
        # Crucial fix: Sanitize and overwrite the original text inside the dictionary
        post['text'] = sanitize_text(post.get('text', ''))
        
        # Now pass the clean text to the LLM
        metadata = extract_metadata(post['text'])
        
        post_with_metadata = post | metadata
        enriched_posts.append(post_with_metadata)

    # Get unified tags
    unified_tags = get_unified_tags(enriched_posts)

    # Replace old tags with unified tags
    for post in enriched_posts:
        current_tags = post.get('tags', [])
        new_tags = [
            unified_tags.get(tag, tag)
            for tag in current_tags
        ]
        post['tags'] = list(new_tags)

    # Save processed data
    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(
            enriched_posts,
            outfile,
            indent=4,
            ensure_ascii=False
        )

def extract_metadata(post):
    template = '''
    You are given a LinkedIn post.

    You need to extract:
    1. Number of lines
    2. Language of the post
    3. Tags

    Rules:
    1. Return ONLY valid JSON.
    2. JSON should contain exactly:
       line_count, language, tags
    3. tags should contain maximum 2 tags.
    4. Language should be either:
       English or Hinglish

    Here is the post:
    {post}
    '''

    pt = langchain_core.prompts.PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"post": post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Unable to parse response.")

    return res


def get_unified_tags(posts_with_metadata):
    unique_tags = set()

    # Extract all tags
    for post in posts_with_metadata:
        unique_tags.update(post.get('tags', []))

    unique_tags_list = ', '.join(unique_tags)

    template = '''
    I will give you a list of tags.

    Your task:
    1. Merge similar tags.
    2. Use Title Case.
    3. Return ONLY valid JSON.
    4. Output format:
       {{
         "OldTag": "NewTag"
       }}

    Example:
    {{
      "Jobseekers": "Job Search",
      "Job Hunting": "Job Search"
    }}

    Tags:
    {tags}
    '''

    pt = langchain_core.prompts.PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": unique_tags_list})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Unable to parse unified tags.")

    return res


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    raw_path = os.path.join(BASE_DIR, "data", "raw_posts.json")
    processed_path = os.path.join(BASE_DIR, "data", "processed_posts.json")

    process_posts(raw_path, processed_path)