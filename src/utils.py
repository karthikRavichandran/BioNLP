import re
from openai import OpenAI
import matplotlib.pyplot as plt
# api = ""
import os

import json

with open('../config.json') as f:
    d = json.load(f)

client = OpenAI(
    api_key=d["API"],
    organization=d["Project_Id"]
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



def get_q_c_prompt(question, choices):
    system_prompt = \
    '''
    You are a highly knowledgeable medical assistant specialized in occupational health and toxicology.
    Your role is to analyze detailed medical scenarios and 
    accurately assess health risks and answer the question based on the provided multiple-choice options
    '''
    prompt =\
        f'''Answer the medical question based on the below options provided
        \n
        Question : {question}
        \n
        Choices : {choices}
        \n
        Output : <opt>Selected option<\opt>
        \n
    Note: give the final answer as the option and don't provide the full choice
    '''
    return system_prompt, prompt

def save_json(data_dict, file_path):
    with open(f"{file_path}", "w") as outfile:
        json.dump(data_dict, outfile)

def read_json(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def plot_acc(df, model_name=''):
    plt.figure(figsize=(10, 6))
    bar_width = 0.25
    x = df["chunk_set_id"]

    plt.bar(x - bar_width / 2, df["wo_context_acc"], width=bar_width,
            label="wo_context_acc", color="orange")
    plt.bar(x + bar_width / 2, df["w_context"], width=bar_width, label="w_context", color="green")

    # plt.plot(df["chunk_set_id"], df["wo_context_acc"], marker='o',
    #          label="wo_context_acc")
    # plt.plot(df["chunk_set_id"], df["w_context"], marker='o', label="w_context")

    # Labels and title
    plt.xlabel("Chunk Set ID")
    plt.ylabel("Accuracy")
    plt.title(f"Accuracy Comparison: {model_name}")
    plt.xticks(x, df["chunk_set_id"])
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    # plt.legend()
    # plt.tight_layout()

    # Show plot
    plt.show()


def quick_llm_completions(sys_pt, pt, model_name="gpt-4o-mini"):
    completion = client.chat.completions.create(
        model=model_name,  # claude-3-haiku-20240307
        messages=[
            {"role": "system", "content": sys_pt},
            {"role": "user", "content": pt}
        ]
    )
    out = completion.choices[0].message.content
    return out
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
def get_context_q_c_prompt(context, question, choices):
    system_prompt = \
        '''
        You are a highly knowledgeable medical assistant specialized in occupational health and toxicology.
        Your role is to analyze detailed medical scenarios and 
        accurately assess health risks and answer the question based on the provided medical context and multiple-choice options
        '''
    prompt = \
        f'''Answer the medical question based on the below options provided and the context
            \n
            Context : {context}
            \n
            Question : {question}
            \n
            Choices : {choices}
            \n
            Output : <opt>Selected option - Just option char or number<\opt>
            \n
        Note: give the final answer as the option and don't provide the full choice
        '''

    return system_prompt, prompt

def get_cs_q_c_prompt(question, clinical_scenario, choices):
    system_prompt = \
    '''
    You are a highly knowledgeable medical assistant specialized in occupational health and toxicology.
    Your role is to analyze detailed Clinical scenarios and 
    accurately assess health risks and answer the question based on the provided multiple-choice options
    '''
    prompt =\
        f'''Answer the medical question for the clinical scenario based on the below options provided
        \n
        Clinical Scenario: {clinical_scenario}
        \n
        Question : {question}
        \n
        Choices : {choices}
        \n
        Output : <opt>Selected option<\opt>
        \n
    Note: give the final answer as the option and don't provide the full choice
    '''
    return system_prompt, prompt

def get_context_cs_q_c_prompt(context, question, clinical_scenario, choices):
        system_prompt = \
            '''
            You are a highly knowledgeable medical assistant specialized in occupational health and toxicology.
            Your role is to analyze detailed Clinical scenarios and 
            accurately assess health risks and answer the question based on the provided medical context and multiple-choice options
            '''
        prompt = \
            f'''Answer the medical question for the clinical scenario based on the below options provided
                \n
                Clinical Scenario: {clinical_scenario}
                \n
                Context : {context}
                \n
                Question : {question}
                \n
                Choices : {choices}
                \n
                Output : <opt>Selected option - Just option char or number<\opt>
                \n
            Note: give the final answer as the option and don't provide the full choice
            '''

        return system_prompt, prompt


def get_cs_q_c_prompt_w_reason(question, clinical_scenario, choices):
    system_prompt = \
    '''
    You are a highly knowledgeable medical assistant specialized in occupational health and toxicology.
    Your role is to analyze detailed Clinical scenarios and 
    accurately assess health risks and answer the question based on the provided multiple-choice options
    '''
    prompt =\
        f'''Answer the medical question for the clinical scenario based on the below options provided
        \n
        Clinical Scenario: {clinical_scenario}
        \n
        Question : {question}
        \n
        Choices : {choices}
        \n
        Output : Option and reason
        \n
    Note: give the final answer as the option and a detail reason for selecting it
    '''
    return system_prompt, prompt

def get_context_cs_q_c_prompt_w_reason(context, question, clinical_scenario, choices):
        system_prompt = \
            '''
            You are a highly knowledgeable medical assistant specialized in occupational health and toxicology.
            Your role is to analyze detailed Clinical scenarios and 
            accurately assess health risks and answer the question based on the provided medical context and multiple-choice options
            '''
        prompt = \
            f'''Answer the medical question for the clinical scenario based on the below options provided
                \n
                Clinical Scenario: {clinical_scenario}
                \n
                Context : {context}
                \n
                Question : {question}
                \n
                Choices : {choices}
                \n
                Output : Option and reason
                \n
            Note: give the final answer as the option and a detail reason for selecting it
            '''

        return system_prompt, prompt
def chat_completion(system_pt, user_pt):
    completion = client.chat.completions.create(
            model="gpt-4o-mini",  # claude-3-haiku-20240307
            messages=[
                {"role": "system", "content": system_pt},
                {"role": "user", "content": user_pt}
            ]
        )
    return completion.choices[0].message.content