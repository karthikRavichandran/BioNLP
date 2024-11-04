questions_types = '''
1. Multiple choice questions: Give it in a dict formate inside <dict> tag and make option in numbers
'''
formate_ex = '''{'question': 'What is the main purpose of the memorandum?',
 'options': {'A': 'To establish legal restrictions on acrylamide',
  'B': 'To exchange information and expertise in occupational safety and health',
  'C': 'To increase production of acrylamide',
  'D': 'To review existing health regulations'},
 'answer': 'B'}
 '''
questions_types2 = '''
1. Multiple choice questions 
2. Explanation based
3. Fill in the blanks
'''
questions_types1 = '''
Explanation based
'''

system_prompt2 = f'''
You are a Teaching assistant who is designing questions for an medical exam. 
Given a context, you have to come up with set of questions that can be in the form of : {questions_types}
'''

rules = f'''
1) Answer should be in context and don't make question look like reading compriension 
2) Answer the question from the context
3) Keep all Questions and answers in the dict format inside <dict> tag
4) Don't ask any author based questions
'''

system_prompt = f'''
You are an assistant for designing questions for an medical objective. 
Given a retrivied context, you have to come up with set of complicated medical questions that can be in the form of : {questions_types1}
And follow these rules {rules}
'''

def get_instruction_prompt(question, context, answer):
    rules = '''1. Don't give any Example Application in the instruction 
    2. Return only instruction for the task 
    3. Give the instruction in <INSTRUCT> tags
    '''

    rules = '''1. Don't give any Example Application in the instruction 
    2. It's ok to use medical jargon 
       '''

    sys_pt =  f'''
    You're a assistant who's generating an prompt for various task.'''

    pt = f'''TASK : Generate an instruction for answering an Medical question. \
    Here is a example of a task that has Question, retrieved context and  answer \
    and follow the rule give below
    
    Rules : {rules}
    
    Question : {question}
    
    Context : {context}
    
    Answer : {answer}
    '''
    return sys_pt, pt
#TODO Llama 3 pipeline
#TODO Set the questions right (align miore with bIoinstr)
#TODO Segment the task based in diffculties (later)