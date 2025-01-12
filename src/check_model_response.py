import pandas as pd
from tqdm import tqdm
from utils import client, read_json, save_json, quick_llm_completions
file_name = 'final_cs_Mistral-7B-Instruct-v0.2_10.csv'
save_location = '../response/'
# save_name = file_name.split(".")[0] + '_matched.csv'
save_name = 'final_cs_Mistral-7B-Instruct-v0.2_10_matched.csv'
data_seted = pd.read_csv(save_location+file_name)
data = data_seted.filter(["ans_wo_context","ans_w_context","orginal_ans","full_option"],
                   axis=1)
ans_wo_context = data["ans_wo_context"].tolist()
ans_w_context = data["ans_w_context"].tolist()
original_ans = data["orginal_ans"].tolist()
full_option = data["full_option"].tolist()

system_prompt = ("You're an research assistance where you will compute a "
                 "accuracy of an LLM output. You will be given two references 1) full option and 2) Original answer. By using two reference, find match for given set")

def compute_match(full_option, original_ans, ans):
    matchs = []
    for i in tqdm(range(len(full_option))):
        pt = f"'full_option': {full_option[i]}\n'original_ans': {original_ans[i]}, 'generated_answer': {ans[i]} give 0 for mismatch, 1 for match"
        out = quick_llm_completions (system_prompt, pt)
        matchs.append(out)
    return matchs
match_w = compute_match(full_option, original_ans, ans_w_context)
match_wo = compute_match(full_option, original_ans, ans_wo_context)
data_seted["match_w"] = match_w
data_seted["match_wo"] = match_wo
print(data)
data_seted.to_csv(save_location+save_name)







