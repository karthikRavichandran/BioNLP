### README for BioNLP Project
BioNLP Independent study (Fall 2024)

---

#### **Project Overview**
The **BioNLP** project is a Python-based pipeline designed for generating USMLE-style medical questions from unstructured textual data. By leveraging AI-driven systems, the project ensures that generated questions adhere to medical examination standards, promoting knowledge application and critical thinking. The pipeline is structured with modular components and robust error handling for processing large datasets.

---
<img width="623" alt="image" src="https://github.com/user-attachments/assets/35c74ff0-4954-4f72-b1fd-2560bbfca436" />

#### **Directory Structure**

The project is organized into the following folders and files:

```
BioNLP/
│
├── gen_files/
│   ├── clean_text/
│   │   └── Clean_text_X_version2.json  # Input files with text chunks to process
│   ├── good_sets/
│   │   ├── Instruction_X_version2.json  # Generated instructions from version 2
│   │   ├── Instruction_X_version3.json  # Final structured outputs
│   └── example_context.py               # Example contexts for prompt generation
│   └── __init__.py                      # Initialization file for the module
│
├── src/
│   ├── Gen_CQAD.py                      # Main script for processing text and generating outputs
│   ├── gen_instruction.py               # Generates instructional data from text chunks
│   ├── gen_questions.py                 # Focuses on generating questions
│   ├── prompts.py                       # Contains the prompt definition for AI model interactions
│   └── utils.py                         # Utility functions and model client integration
```

---

#### **Key Components**

1. **`gen_files/clean_text`**:
   - Contains raw input files in JSON format, each named as `Clean_text_X_version2.json`.
   - Each file includes chunks of text to be processed and converted into structured outputs.

2. **`gen_files/good_sets`**:
   - Stores intermediate and final output files.
   - Files follow the naming convention `Instruction_X_versionY.json`, where `X` represents the file index and `Y` represents the version of the output.

3. **`src/`**:
   - **`Gen_CQAD.py`**: The main driver script for processing input files, generating structured outputs, and handling retries and errors.
   - **`gen_instruction.py`**: Processes input text chunks into instructional data.
   - **`gen_questions.py`**: Focuses on question generation logic.
   - **`prompts.py`**: Contains prompt templates and few-shot examples for the AI model.
   - **`utils.py`**: Includes helper functions for JSON handling and communication with the AI model.

---

#### **Prompt Design**

The prompt is a critical component of the system, guiding the AI model to generate high-quality questions. It follows a strict format and provides explicit instructions for creating:

1. **Clinical Scenarios**: Independent narratives based on the input text.
2. **Questions**: Application-based queries derived from the clinical scenario.
3. **Answers**: The correct answer, supported by medical reasoning.
4. **Distractors**: Plausible but incorrect choices for assessment purposes.

**Key Features:**
- Text is encapsulated in `<Context>`, `<Question>`, `<Choices>`, and `<Answer>` tags.
- The generated output is converted into a dictionary format for easy storage and processing.

Example snippet of a prompt:

```plaintext
<Context>
{context}
</Context>

<Question>
Generate your question here
</Question>

<Choices>
Write three distractor choices and one correct choice
</Choices>

<Answer>
Select the correct answer and explain it in a chain-of-thought manner
</Answer>
```

---

#### **How to Use**

1. **Prepare Input Data**:
   - Place raw input text files in the `gen_files/clean_text/` directory.
   - Files should be in JSON format with a structure like:
     ```json
     {
       "chunk": ["text chunk 1", "text chunk 2", ...],
       "questions": ["question 1", "question 2", ...]
     }
     ```

2. **Run the Main Script**:
   - Execute `Gen_CQAD.py` to process the input files and generate outputs.
   - The script processes text chunks, interacts with the AI model, and stores the results in the `good_sets` directory.

3. **Output Files**:
   - Outputs are stored in JSON format with the structure:
     ```json
     [
       {
         "Final_set": {
           "Context": "context text",
           "Question": "generated question",
           "Choices": ["A: choice 1", "B: choice 2", "C: choice 3", "D: choice 4"],
           "Answer": "correct answer"
         },
         "actual_context": "original text chunk"
       },
       ...
     ]
     ```

---

#### **Error Handling and Retries**

- The system includes a robust retry mechanism to handle parsing or AI model errors:
  - Retries up to 5 times for failed chunks.
  - Skips the chunk after 5 failed attempts, logging the issue for review.

---

#### **Sample Workflow**

1. Input file: `Clean_text_0_version2.json` (stored in `clean_text/`).
2. Processed using `Gen_CQAD.py`.
3. Intermediate and final outputs:
   - `Instruction_0_version2.json` (intermediate).
   - `Instruction_0_version3.json` (final).

---

#### **Future Enhancements**

1. **Parallel Processing**:
   - Implement multiprocessing to speed up chunk processing for large datasets.

2. **Enhanced Error Handling**:
   - Add detailed logging for skipped or failed chunks.
   - Provide better error diagnostics.

3. **Validation**:
   - Automate input and output validation to ensure data integrity.

4. **Extend Prompt Design**:
   - Adapt the prompt for other examination formats or educational use cases.

---

#### **Results**

![image](https://github.com/user-attachments/assets/1f4ab02b-2153-488e-9656-79ac46e39b4e)


#### **Authors and Acknowledgments**
This project was developed for educational and research purposes, leveraging GPT-based AI models to generate high-quality medical questions. It combines computational efficiency with educational rigor, creating a scalable framework for content generation.

--- 

This README serves as a guide to understanding the structure, functionality, and purpose of the **BioNLP** project. For further queries, consult the `src/` directory for modular scripts and detailed implementation logic.
