from utils import client
from prompts import get_instruction_prompt
import numpy as np
import json
from utils import client
import random

clean_text_id = 1
for clean_text_id in [1]:
    with open(f'Clean_text_{clean_text_id}_version2.json', 'r') as file:
        data = json.load(file)

    chunk, questions = (data['chunk'], data['questions'])
    out_list = []
    for c,q in zip(chunk, questions):
        dt = random.choices(q)[0]
        sys_pt, pt = get_instruction_prompt(question=dt['question'], context=c, answer=dt['answer'])
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # claude-3-haiku-20240307
            messages=[
                {"role": "system", "content": sys_pt},
                {"role": "user", "content": pt}
            ]
        )
        out = completion.choices[0].message.content
        print(out)
        out_list.append({"instruction": out, "context": c,
                         "question": dt['question'],
                         'answer': dt['answer']})

    with open(f"Instruction_{clean_text_id}_version2.json", "w") as outfile:
        json.dump(out_list, outfile)

print(out_list)




print(data)
