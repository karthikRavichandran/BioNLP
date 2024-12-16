from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
def init_llm():
    model = LLM("/project/pi_hongyu_umass_edu/shared_llm_checkpoints/Meta-Llama-3.1-8B-Instruct", dtype="half")
    tokenizer = AutoTokenizer.from_pretrained("/project/pi_hongyu_umass_edu/shared_llm_checkpoints/Meta-Llama-3.1-8B-Instruct")
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    formatted_prompt =  tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    output = model.generate(formatted_prompt)
    print(output)
    return model, tokenizer

if __name__=="__main__":
    
    model = init_llm()