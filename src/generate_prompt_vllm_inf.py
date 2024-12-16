import json
file_root_path = "../gen_files/cqad_sets"
text_id = 0
for text_id in range(10):
    with open(f'{file_root_path}/Instruction_{text_id}_version3.json', 'r') as f:
        data = json.load(f)

    def get_q_c_prompt(question, choices):
        system_prompt = \
        '''
        You are a highly knowledgeable medical assistant specialized in occupational health and toxicology.
        Your role is to analyze detailed medical scenarios and 
        accurately assess health risks based on the provided multiple-choice options
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
            accurately assess health risks based on the provided medical context and multiple-choice options
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

    vLLM_prompts = []
    for i in data:
        try:
            Final_set = i["Final_set"]
            # print(Final_set)
            context = i["actual_context"]
            choices = Final_set["Choices"]
            questions = Final_set["Question"]
            ans = Final_set["Answer"]
            _, prompt = get_q_c_prompt(question=questions, choices=choices)
            _, context_prompt = get_context_q_c_prompt(context=context,
                                   question=questions,
                                   choices=choices)
            prompt_dict = {"prompt": prompt, "context_prompt": context_prompt, "orginal_ans": ans}
            vLLM_prompts.append(prompt_dict)
        except:
            print(f"Error in {text_id}-> just skipping")

    file_save_path = "../gen_files/vLLM_inf_prompts/"
    with open(f"{file_save_path}prompt_{text_id}.json", "w") as outfile:
        json.dump(vLLM_prompts, outfile)