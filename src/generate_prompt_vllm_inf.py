import json
from utils import (get_q_c_prompt, get_context_q_c_prompt,
                   get_cs_q_c_prompt, get_context_cs_q_c_prompt)
file_root_path = "../gen_files/cqad_set_v4"
text_id = 0
for text_id in range(10):
    with open(f'{file_root_path}/Instruction_{text_id}_version4.json', 'r') as f:
        data = json.load(f)

    vLLM_prompts = []
    for i in data:
        try:
            Final_set = i["Final_set"]
            # print(Final_set)
            cs = Final_set["Clinical Scenario"]
            context = i["actual_context"]
            choices = Final_set["Choices"]
            questions = Final_set["Question"]
            ans = Final_set["Answer"]
            # _, prompt = get_q_c_prompt(question=questions, choices=choices)
            _, prompt = get_cs_q_c_prompt(question=questions,
                                          clinical_scenario=cs,
                                          choices=choices)
            # _, context_prompt = get_context_q_c_prompt(context=context,
            #                        question=questions,
            #                        choices=choices)
            _, context_prompt = get_context_cs_q_c_prompt(context=context,
                                                          clinical_scenario=cs,
                                   question=questions,
                                   choices=choices)
            prompt_dict = {"prompt": prompt, "context_prompt": context_prompt, "orginal_ans": ans}
            vLLM_prompts.append(prompt_dict)
        except:
            print(f"Error in {text_id}-> just skipping")

    file_save_path = "../gen_files/vLLM_inf_prompts/"
    with open(f"{file_save_path}prompt_{text_id}.json", "w") as outfile:
        json.dump(vLLM_prompts, outfile)