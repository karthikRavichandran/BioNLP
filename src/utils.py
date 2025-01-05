import re
from openai import OpenAI
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