from vllm import LLM, SamplingParams
from transformers import AutoTokenizer


def init_llm(model="Meta-Llama-3.1-8B-Instruct"):
    model = LLM(f"/project/pi_hongyu_umass_edu/shared_llm_checkpoints/{model}",
                dtype="half")
    tokenizer = AutoTokenizer.from_pretrained(
        f"/project/pi_hongyu_umass_edu/shared_llm_checkpoints/{model}")
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                                                     add_generation_prompt=True)
    output = model.generate(formatted_prompt)
    print(output)
    return model, tokenizer


if __name__ == "__main__":
    model = init_llm()