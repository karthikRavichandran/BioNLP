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

def get_slm_output_parser(slm_full_option, context):
    '''
    What it is doing:

    SLM output —> 
        gpt4o mini formatting step (ask it not change content itself in reasoning, only make it better format) —> 
            SLM reasoning, SLM prediction, category a/b to use information in context
    '''
    sys_pt =  f'''You're a assistant who's expert in parsing the unformated output from a small models output \
        and extract the part related to reason given the context'''

    # rules = f'''1. Reason from the output
    # 2. Give the option (A/B/C/D/E)
    # 3. Give the extracted part of context that supports reason #TODO Cnage the 3 to check if it has direct evident fromthe context or not (0/1)
    # 4. Create a dict with keys reason, option, e_context with above values
    # Note: Just give the dict don't enclose it with python or json'''

    Instructions = f'''Retrievable Reasoning
                    In this case, the answer can be directly found in the provided context, typically by locating and matching key information.
                    This type of reasoning relies solely on explicit information within the context and does not require additional logical inference or external knowledge.
                    Example:
                    Context: “Patients who take Drug A often experience mild dizziness as a side effect.”
                    Question: “What side effect might Drug A cause?”
                    Answer: “Mild dizziness.” (The answer is explicitly stated in the context.)
                    Inferential Reasoning
                    This type of reasoning requires going beyond the direct information provided in the context. The context only offers hints, and the answer must be derived through logical inference or background knowledge.
                    This often involves causal reasoning, analogy, induction, or deduction.
                    Example:
                    Context: “The patient reported feeling fatigued after taking Drug A, which is known to affect the nervous system.”
                    Question: “Why does Drug A cause fatigue?”
                    Answer: “Because Drug A affects the nervous system, and changes in the nervous system can lead to fatigue.” (Requires inferring the causal relationship: Drug A → nervous system effects → fatigue.)
                    '''

    rules = f'''1. Reason from the output 
    2. Give the option (A/B/C/D/E) 
    3. Give Retrievable or Inferential use Retrievable/Inferential information given about to find.
    4. Create a dict with keys reason, option, Retrievable/Inferential with above values
    Note: Just give the dict don't enclose it with python or json'''

    pt = f'''Here is the small model's output with options and it's explanation {slm_full_option} and the context to check {context} extract the following:\n'''

    return sys_pt, f'''Retrievable/Inferential information:{Instructions}\n{pt}\nRules:\n{rules}'''

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

def get_CQAD_prompt(context):
    CQAD_prompt = f'''
Generate USMLE-style questions using GPT based on a provided chunk of information. The process involves creating a question set that includes:
1. Clinical Scenario (C): A detailed narrative presenting a patient's history, symptoms, and possibly examination findings. This scenario is crafted independently and does not directly extract content from the chunk. Instead, it serves as the context for the question.
2. Question (Q): A specific, concise query derived from the clinical scenario, aimed at assessing the student's ability to apply their knowledge. Like the scenario, this is not directly taken from the chunk but must relate to the information in the chunk.
3. Correct Answer (A): The correct choice that directly answers the question, designed based on the knowledge required to solve the question.
4. Distractors (D): Plausible but incorrect answer choices that test the student’s understanding and ability to differentiate between related concepts.
Key Requirement:The chunk of information serves as a reference point. The content in the clinical scenario (C), question (Q), answer (A), and distractors (D) should not be copied verbatim from the chunk. Instead, the chunk provides hints or background knowledge that the student can use to logically reason through the scenario and arrive at the correct answer. This ensures the generated questions are contextually relevant to the chunk but require students to apply critical thinking rather than recall specific details from it.


Few-shot Example 

1. Example 1:

<Context> A variety of unproven mechanisms have been proposed to explain SIDS. SIDS is associated with prone position during sleep, especially on soft bedding. The widely advocated supine sleeping position explains, in part, the decreased incidence of SIDS during the past two decades. Current theories for a predisposition to SIDS include cellular brainstem abnormalities and maturational delay related to neural or cardiorespiratory control. A portion of SIDS deaths may be due to prolongation of the Q-T interval, abnormal CNS control of respiration, and CO2 rebreathing from sleeping face down (especially in softbedding). See Table 134-1 for the differential diagnosis of SIDS. There has been a significant decline in SIDS with the backto-sleep program and avoiding soft bedding. Thus, all parents should be instructed to place their infants in the supine position unless there are medical contraindications. All soft Fulminant infection*,† Infant botulism*
</Context>

<Question> 
A 3-month-old baby died suddenly at night while asleep. His mother noticed that he had died only after she awoke in the morning. No cause of death was determined based on the autopsy. Which of the following precautions could have prevented the death of the baby?
</Question> 

<Choices> 
A: Using a weighted blanket to keep the baby warm during sleep
B: Placing the baby in a prone position to prevent choking
C: Co-sleeping in the same bed with parents to monitor the baby closely
D: Placing the infant in a supine position on a firm mattress while sleeping
</Choices> 

<ANSWER> 
D: Placing the infant in a supine position on a firm mattress while sleeping, The best answer is D. (Kaplan 9th ed. p. 134) The supine sleeping position is the most effective way to prevent SIDS. The supine sleeping position is the most effective way to prevent SIDS. The supine sleeping position is the most effective way to prevent SIDS. The supine sleeping position is the most effective
</ANSWER>

2. Example 2:

<Context>
In neonates with true vomiting, congenital obstructive lesions should be considered. Allergic reactions to formula in the first 2 months of life may present with vomiting. Infantile GER (“spitting up”) occurs in most infants and can be large in volume, but is effortless and these infants do not appear ill. Pyloric stenosis occurs in the first months of life and is characterized by steadily worsening, forceful vomiting that occurs immediately after feedings. A visibly distended stomach, often with visible peristaltic waves, is often seen before vomiting. Pyloric stenosis is more common in male infants; the family history may be positive. Other obstructive lesions, such as intestinal duplication cysts, atresias, webs, and midgut Determine degree of functional impairment (e.g., missing school) CBC ESR Amylase, lipase Urinalysis Abdominal ultrasound—examine liver, bile ducts, gallbladder, pancreas, kidneys, ureters (move to follow up)
</Context>

<Question> 
A mother brings her 3-week-old infant to the pediatrician's office because she is concerned about his feeding habits. He was born without complications and has not had any medical problems up until this time. However, for the past 4 days, he has been fussy, is regurgitating all of his feeds, and his vomit is yellow in color. On physical exam, the child's abdomen is minimally distended but no other abnormalities are appreciated. Which of the following embryologic errors could account for this presentation?
</Question> 

<Choices>
A: Abnormal migration of ventral pancreatic bud
B: Incomplete recanalization of the duodenum
C: Failure of midgut rotation
D: Incomplete fusion of the dorsal and ventral pancreatic buds
</Choices>

<Answer>
A: Abnormal migration of ventral pancreatic bud. The best answer is A.  This is the correct answer because the infant's symptoms are consistent with pyloric stenosis. Pyloric stenosis is caused by an abnormal hypertrophy of the pylorus, which is a result of an abnormal migration of the ventral pancreatic bud. This is a congenital anomaly that occurs in the first few weeks of life. The infant's symptoms of forceful vomiting after feeding.
</Answer>

<Context>
{context}
</Context>

<Question>
Generate you’re question here
</Question>

<Choices>
Write three distractor choice and one correct choice
</Choices>

<Answer>
select the correct answer and explain it in Chain of thought manners 
</Answer>

Verify if you're following the below rules for you're output:
1) Give the Context in <Context> </Context> tag
2) Give the Question in <Question> </Question> tag
3) Give the Choices in <Choices> </Choices> tag
4) Give the Answer in <Answer> </Answer> tags
5) Give Just the option number in <option> </option>
5) Now parse these and give it as dict format inside <dict> tag
'''
    return CQAD_prompt

def get_CQAD_prompt_v2(context):
    CQAD_prompt = f'''
Generate USMLE-style questions using GPT based on a provided chunk of information. The process involves creating a question set that includes:
1. Clinical Scenario (C): A detailed narrative presenting a patient's history, symptoms, and possibly examination findings. This scenario is crafted independently and does not directly extract content from the chunk. Instead, it serves as the context for the question.
2. Question (Q): A specific, concise query derived from the clinical scenario, aimed at assessing the student's ability to apply their knowledge. Like the scenario, this is not directly taken from the chunk but must relate to the information in the chunk.
3. Correct Answer (A): The correct choice that directly answers the question, designed based on the knowledge required to solve the question.
4. Distractors (D): Plausible but incorrect answer choices that test the student’s understanding and ability to differentiate between related concepts.

Key Requirement: The chunk of information serves as a reference point. The content in the clinical scenario (C), question (Q), answer (A), and distractors (D) should not be copied verbatim from the chunk. Instead, the chunk provides hints or background knowledge that the student can use to logically reason through the scenario and arrive at the correct answer. This ensures the generated questions are contextually relevant to the chunk but require students to apply critical thinking rather than recall specific details from it.

Few-shot Example 

1. Example 1:
<Chunk> A variety of unproven mechanisms have been proposed to explain SIDS. SIDS is associated with prone position during sleep, especially on soft bedding. The widely advocated supine sleeping position explains, in part, the decreased incidence of SIDS during the past two decades. Current theories for a predisposition to SIDS include cellular brainstem abnormalities and maturational delay related to neural or cardiorespiratory control. A portion of SIDS deaths may be due to prolongation of the Q-T interval, abnormal CNS control of respiration, and CO2 rebreathing from sleeping face down (especially in softbedding). See Table 134-1 for the differential diagnosis of SIDS. There has been a significant decline in SIDS with the backto-sleep program and avoiding soft bedding. Thus, all parents should be instructed to place their infants in the supine position unless there are medical contraindications. All soft Fulminant infection*,† Infant botulism*
</Chunk>

<Clinical Scenario> 
A 3-month-old baby died suddenly at night while asleep. His mother noticed that he had died only after she awoke in the morning. No cause of death was determined based on the autopsy.
</Clinical Scenario>

<Question> 
Which of the following precautions could have prevented the death of the baby?
</Question> 

<Choices> 
A: Using a weighted blanket to keep the baby warm during sleep
B: Placing the baby in a prone position to prevent choking
C: Co-sleeping in the same bed with parents to monitor the baby closely
D: Placing the infant in a supine position on a firm mattress while sleeping
</Choices> 

<ANSWER> 
D: Placing the infant in a supine position on a firm mattress while sleeping, The best answer is D. (Kaplan 9th ed. p. 134) The supine sleeping position is the most effective way to prevent SIDS. The supine sleeping position is the most effective way to prevent SIDS. The supine sleeping position is the most effective way to prevent SIDS. The supine sleeping position is the most effective
</ANSWER>


2. Example 2:

<Chunk>
In neonates with true vomiting, congenital obstructive lesions should be considered. Allergic reactions to formula in the first 2 months of life may present with vomiting. Infantile GER (“spitting up”) occurs in most infants and can be large in volume, but is effortless and these infants do not appear ill. Pyloric stenosis occurs in the first months of life and is characterized by steadily worsening, forceful vomiting that occurs immediately after feedings. A visibly distended stomach, often with visible peristaltic waves, is often seen before vomiting. Pyloric stenosis is more common in male infants; the family history may be positive. Other obstructive lesions, such as intestinal duplication cysts, atresias, webs, and midgut Determine degree of functional impairment (e.g., missing school) CBC ESR Amylase, lipase Urinalysis Abdominal ultrasound—examine liver, bile ducts, gallbladder, pancreas, kidneys, ureters (move to follow up)
</Chunk>

<Clinical Scenario> 
A mother brings her 3-week-old infant to the pediatrician's office because she is concerned about his feeding habits. He was born without complications and has not had any medical problems up until this time. However, for the past 4 days, he has been fussy, is regurgitating all of his feeds, and his vomit is yellow in color. On physical exam, the child's abdomen is minimally distended but no other abnormalities are appreciated.
</Clinical Scenario> 

<Question> 
Which of the following embryologic errors could account for this presentation?
</Question> 

<Choices>
A: Abnormal migration of ventral pancreatic bud
B: Incomplete recanalization of the duodenum
C: Failure of midgut rotation
D: Incomplete fusion of the dorsal and ventral pancreatic buds
</Choices>

<Answer>
A: Abnormal migration of ventral pancreatic bud. The best answer is A.  This is the correct answer because the infant's symptoms are consistent with pyloric stenosis. Pyloric stenosis is caused by an abnormal hypertrophy of the pylorus, which is a result of an abnormal migration of the ventral pancreatic bud. This is a congenital anomaly that occurs in the first few weeks of life. The infant's symptoms of forceful vomiting after feeding.
</Answer>


<Chunk>
{context}
</Chunk>

<Question>
Generate you’re question here
</Question>

<Clinical Scenario>
Generate the Clinical Scenario here
</Clinical Scenario>

<Choices>
Write three distractor choice and one correct choice
</Choices>

<Answer>
select the correct answer and explain it in Chain of thought manners 
</Answer>

Verify if you're following the below rules for you're output:
1) Give the Chunk in <Chunk> </Chunk> tag
2) Give the Clinical Scenario in <Clinical Scenario> </Clinical Scenario> tag
2) Give the Question in <Question> </Question> tag
3) Give the Choices in <Choices> </Choices> tag
4) Give the Answer in <Answer> </Answer> tags
5) Give Just the option number in <option> </option>
5) Now parse these and give it as dict format inside <dict> tag
'''
    return CQAD_prompt


CQAD_system_prompt = "You’re a medical assistant to generate questions for a medical collage exam. Your objective as follows and you are provided with few example for the reference "

