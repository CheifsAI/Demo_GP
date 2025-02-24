from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from OprFuncs import data_infer, extract_code, extract_questions
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import re
import pandas as pd
from langchain_community.chat_message_histories import ChatMessageHistory


class DataAnalyzer:
    def __init__(self, dataframe, llm, retriever):
        self.dataframe = dataframe
        self.llm = llm
        self.retriever = retriever  # ✅ Correctly storing retriever
        self.data_info = data_infer(dataframe)
        self.memory = []

    def analysis_data(self):
        data_info = self.data_info

        analysis_prompt = '''
        You are a data analyst. You have been provided with a dataset about {data_info}.
        Here is the dataset structure:
        {data_info}

        To enhance your analysis, you have access to a knowledge base containing relevant domain knowledge.

        Please analyze the data by retrieving relevant insights and provide a structured analysis:

        1. *Key Trends and Patterns*:
        - [Describe the key trends and patterns in the data].

        2. *Anomalies or Outliers*:
        - [Identify any anomalies or outliers in the data].

        Ensure your analysis is specific, data-driven, and incorporates retrieved domain knowledge.
        '''

        # ✅ Correctly use `self.retriever`
        retrieved_docs = self.retriever.get_relevant_documents(query=data_info)
        retrieved_knowledge = "\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else "No relevant knowledge found."

        # Define prompt template
        analysis_template = PromptTemplate(
            input_variables=["data_info", "retrieved_knowledge"],
            template=analysis_prompt
        )

        # Create analysis chain
        analysis_chain = LLMChain(llm=self.llm, prompt=analysis_template)

        # Run analysis with retrieved knowledge
        analysis = analysis_chain.invoke({"data_info": data_info, "retrieved_knowledge": retrieved_knowledge})

        # Convert to string if needed
        analysis = analysis["text"] if isinstance(analysis, dict) and "text" in analysis else str(analysis)

        formatted_analysis_prompt = analysis_prompt.format(data_info=data_info, retrieved_knowledge=retrieved_knowledge)
        self.memory.append(HumanMessage(content=formatted_analysis_prompt))
        self.memory.append(AIMessage(content=analysis))

        return analysis


    # Question Generator
    def questions_gen(self, num):
        data_info = self.data_info

        # Prompt Template for Question Generation
        question_prompt = '''
        Create {num} analysis questions about the following data: 
        {data_info}
        Please format each question on a new line without numbering.
        '''
        
        # Define the prompt template
        question_template = PromptTemplate(
            input_variables=["num", "data_info"],
            template=question_prompt
        )
        
        question_chain = LLMChain(
            llm=self.llm,
            prompt=question_template
        )
        # Use .invoke() instead of .run()
        generated_questions = question_chain.run({"num": num, "data_info": data_info})

        questions_list = extract_questions(generated_questions)
        
        formatted_question_prompt = question_template.format(num=num, data_info=data_info)

        self.memory.append(HumanMessage(content=formatted_question_prompt))
        self.memory.append(AIMessage(content="\n".join(questions_list)))
        
        return questions_list


    def visual(self, questions):
        data_info = self.data_info
        
        # Prompt for creating visualization code
        visual_prompt = '''
        I already have a DataFrame named 'df'. Generate **correctly formatted** matplotlib code to answer each question in {questions}.
        Ensure the code is **indented properly** and follows Python syntax standards.
        Use the following columns information: {data_info}. Create only the visualization code.
        '''
        
        # Define the prompt template
        visual_template = PromptTemplate(
            input_variables=["data_info", "questions"],
            template=visual_prompt
        )
        
        # Create a chain for generating visualizations
        visual_chain = LLMChain(llm=self.llm, prompt=visual_template)
        
        # Extracting the visualization code
        viscode = extract_code(visual_chain.run(data_info=data_info, questions=questions))
        
        # Print the generated visualization code
        print("Generated Visualization Code:\n", viscode)

        formatted_visual_prompt = visual_prompt.format(questions=questions, data_info=data_info)

        self.memory.append(HumanMessage(content=formatted_visual_prompt))

        self.memory.append(AIMessage(content=viscode))

        # Execute the visualization code
        exec_env = {"df": self.dataframe}
        exec(viscode, exec_env)

    def chat(self,question):
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a data analyst.",
                    ),
                    MessagesPlaceholder(variable_name="memory"),
                    ("human", "{input}"),
                    ]
                    )
        chain = prompt_template | self.llm


        # response = llm.invoke(question)
        response = chain.invoke({"input": question, "memory":self.memory})
        self.memory.append(HumanMessage(content=question))
        self.memory.append(AIMessage(content=response))
        return response