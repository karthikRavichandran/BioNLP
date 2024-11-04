# !export OPENAI_API_KEY=api

import pandas as pd
from prompts import system_prompt
from utils import extract_dict_text_with_regex, client
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import httpx

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1500,
    chunk_overlap=50,
    length_function=len,
    is_separator_regex=False,
)

df = pd.read_csv("../epfl-llm.csv")
df_data = df[df['source']=='cdc'].filter(["id","clean_text"], axis=1)

clean_text_id = 1 # around 600 we have
sample_text = df_data.iloc[clean_text_id]["clean_text"]
texts = text_splitter.create_documents([sample_text])
print(f"Generated {len(texts)} number of chuncks with size of 1500 chuck size")

questions = []
context_list = []
i = 0
cnt = len(texts)
retry_limit = 5
retrys = 0
while i < cnt:
    text = texts[i]
    print(f"Processing : {i}")
    try:
        # if True:
        context = f"Context: {text.page_content}"
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # claude-3-haiku-20240307
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context}
            ]
        )
        out = completion.choices[0].message.content
        final_dict = json.loads(extract_dict_text_with_regex(out))
        # final_dict['questions']['context'] = text.page_content
        questions.append(final_dict['questions'])
        context_list.append(text.page_content)
        i += 1
    except:
        print(f"Error in {i}")
        if retrys < retry_limit:
            retrys += 1
        else:
            retrys = 0
            i += 1

question_details = {"chunk": context_list, "questions": questions}
# question_details

with open(f"Clean_text_{clean_text_id}_version2.json", "w") as outfile:
    json.dump(question_details, outfile)