from utils import client
from prompts import get_CQAD_prompt, CQAD_system_prompt, get_CQAD_prompt_v2
from gen_files.example_context import context1
import json
from tqdm import tqdm
import re
import random

get_CQAD_prompt = get_CQAD_prompt_v2

completion = client.chat.completions.create(
            model="gpt-4o-mini",  # claude-3-haiku-20240307
            messages=[
                {"role": "system", "content": CQAD_system_prompt},
                {"role": "user", "content": get_CQAD_prompt(context1)}
            ]
        )


for clean_text_id in range(0,10):
    with open(f'../gen_files/clean_text/Clean_text_{clean_text_id}_version2.json', 'r') as file:
        data = json.load(file)
    count = 0
    retry = 0
    chunk, _ = (data['chunk'], data['questions'])
    out_list = []
    while count < len(chunk):
        c = chunk[count]
        print(f"{count}")
    # for c in tqdm(chunk):
        # dt = random.choices(q)[0]
        if len(c.split(" ")) > 100:
            count+=1
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # claude-3-haiku-20240307
            messages=[
                {"role": "system", "content": CQAD_system_prompt},
                {"role": "user", "content": get_CQAD_prompt(c)}
            ]
        )
        out = completion.choices[0].message.content
        try:
            match = re.search(r"<dict>(.*?)</dict>", out, re.DOTALL)
            dict_content = match.group(1) if match else None
            out = eval(dict_content)
            count+=1
            out_list.append({"Final_set": out, "actual_context": c})
        except:
            retry+=1
            print(f"retrying the {count} for {retry} times")
        if retry>5:
            print("Retries failed , moving next")
            retry = 0
            count+=1



    with open(f"../gen_files/cqad_sets/Instruction_{clean_text_id}_version3.json", "w") as outfile:
        json.dump(out_list, outfile)

print(completion.choices[0].message.content)