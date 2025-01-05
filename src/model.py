from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import json
import pandas as pd


def init_llm(model_name="Meta-Llama-3.1-8B-Instruct"):
    model = LLM(f"/project/pi_hongyu_umass_edu/shared_llm_checkpoints/{model_name}",
                dtype="half")
    tokenizer = AutoTokenizer.from_pretrained(
        f"/project/pi_hongyu_umass_edu/shared_llm_checkpoints/{model_name}")
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                                                     add_generation_prompt=True)
    output = model.generate(formatted_prompt)
    print(output)
    return model, tokenizer


def run_vLLM(idx, tokenizer, model):
    out_file = f'responses/vLLM_out{idx}.json'
    file_name = f'vLLm_prompts/prompt_{idx}.json'
    ans = []
    ans_context = []
    original_ans = []
    full_option = []
    with open(file_name, 'r') as file:
        allprompt = json.load(file)

    for i in range(len(allprompt)):
        ans_org = allprompt[i]["orginal_ans"]
        try:
            original_ans.append(ans_org[0])
        except:
            original_ans.append("Z")
        full_option.append(str(ans_org))

    for i in range(len(allprompt)):
        # prompt = allprompt[i]["prompt"]
        context_prompt = allprompt[i]["context_prompt"]
        messages = [{"role": "user", "content": context_prompt}]
        formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                                                         add_generation_prompt=True)
        output = model.generate(formatted_prompt)
        ans_context.append(output[0].outputs[0].text)

    for i in range(len(allprompt)):
        prompt = allprompt[i]["prompt"]
        messages = [{"role": "user", "content": prompt}]
        formatted_prompt = tokenizer.apply_chat_template(messages,
                                                         tokenize=False,
                                                         add_generation_prompt=True)
        output = model.generate(formatted_prompt)
        ans.append(output[0].outputs[0].text)

    da = {"chunk_set_id": [idx] * len(ans),
          "ans_wo_context": ans,
          "ans_w_context": ans_context,
          "orginal_ans": original_ans,
          "full_option": full_option}
    with open(out_file, "w") as outfile:
        json.dump(da, outfile)
    return da


if __name__ == "__main__":

    model_list = [
        "Llama-3.2-3B-Instruct",
        "Phi-3-mini-128k-instruct",
        "models--Qwen--Qwen2.5-7B-Instruct",
        "selfrag_llama2_7b",
        "Meta-Llama-3.1-8B-Instruct",
        "Phi-3-small-128k-instruct",
        "Mistral-7B-Instruct-v0.2",
        "Qwen2-7B-Instruct",
        "models--Qwen--Qwen1.5-7B-Chat"
    ]
    model_name = "Qwen2-7B-Instruct"
    model, tokenizer = init_llm(model_name=model_name)

    all_fdf = []
    for idx in range(10):
        d = pd.DataFrame(run_vLLM(idx, tokenizer, model))
        all_fdf.append(d)

    pd.concat(all_fdf, axis=0).reset_index(drop=True).to_csv(
        f"responses/final_cs_{model_name}_10.csv", index=False)
    pd.concat(all_fdf, axis=0)