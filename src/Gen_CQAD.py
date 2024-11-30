from utils import client
from prompts import get_CQAD_prompt, CQAD_system_prompt
from gen_files.example_context import context1
import json
from tqdm import tqdm
import random



completion = client.chat.completions.create(
            model="gpt-4o-mini",  # claude-3-haiku-20240307
            messages=[
                {"role": "system", "content": CQAD_system_prompt},
                {"role": "user", "content": get_CQAD_prompt(context1)}
            ]
        )


for clean_text_id in [1]:
    with open(f'../gen_files/Clean_text_{clean_text_id}_version2.json', 'r') as file:
        data = json.load(file)

    chunk, _ = (data['chunk'], data['questions'])
    out_list = []
    for c in tqdm(chunk):
        # dt = random.choices(q)[0]
        if len(c.split(" ")) > 100:
            continue
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # claude-3-haiku-20240307
            messages=[
                {"role": "system", "content": CQAD_system_prompt},
                {"role": "user", "content": get_CQAD_prompt(c)}
            ]
        )
        out = completion.choices[0].message.content
        print(out)
        out_list.append({"Final_set": out, "context": c})

    with open(f"../gen_files/Instruction_{clean_text_id}_version3.json", "w") as outfile:
        json.dump(out_list, outfile)

print(completion.choices[0].message.content)