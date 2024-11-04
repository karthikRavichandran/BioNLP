import re
from openai import OpenAI
api = ""

client = OpenAI(
    api_key=api,
    organization="org-ewbrRzXdrHxv7hV0WyCFzGdD"
)
def extract_dict_text_with_regex(text):
    # Define the regex pattern to match content inside <dict> and </dict> tags
    pattern = r'<dict>(.*?)<\/dict>'

    # Search for the pattern in the text
    match = re.search(pattern, text, re.DOTALL)

    # If a match is found, return the text inside the <dict> tag
    if match:
        return match.group(1).strip()
    else:
        return "No <dict> tag found or no content inside <dict>"