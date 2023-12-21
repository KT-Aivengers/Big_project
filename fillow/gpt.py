from langchain.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import ChatMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import BaseOutputParser
import openai,os
from dotenv import load_dotenv

try:
    load_dotenv()

    api_key=os.getenv("OPENAI_KEY",None)
    class EmailOutputParser(BaseOutputParser):
        def parse(self, text):
            lines = text.strip().split('\n')
            result = {}
            for line in lines:
                if line:
                    key, value = line.split(': ')
                    result[key.strip()] = value.strip()
            return result

    chat = ChatOpenAI(
        temperature=0.1,
        streaming=True,
        callbacks=[
            StreamingStdOutCallbackHandler(),
        ],
        # model_name="gpt-4",
    )


    texts = []
    current_text = ""
    recording = False

    with open('texts.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if '"""' in line:
                if recording:
                    # 문자열 종료
                    texts.append(current_text)
                    current_text = ""
                recording = not recording
            elif recording:
                current_text += line

    # texts 리스트에는 각각의 문자열이 순서대로 저장됩니다.
    answers = []
    current_text = ""
    recording = False

    with open('answers.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if '"""' in line:
                if recording:
                    # 문자열 종료
                    answers.append(current_text)
                    current_text = ""
                recording = not recording
            elif recording:
                current_text += line

    examples=[]
    for i in range(len(texts)):
        examples.append({"email":texts[i],"answer":answers[i]})


    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("Here is an email. Please extract up to 5 important keyword terms. They don't necessarily have to be words from the content.{email}"),
            ("ai", "{answer}"),
        ]
    )

    example_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
            You are a diligent assistant.
            Your task is to process the email information and calculate the reply date.
            First, identify the department mentioned in the content.
            Next, summarize the content by extracting up to 5 key tag keywords.
            If there is a reply date specified in the content, retrieve that date.
            However, even if the reply date is not explicitly mentioned,
            if there is a deadline such as 'next week' or a certain day of the week,
            please calculate the reply date from the current date.
            Also, evaluate the email and assign a score based on its importance.
            Lastly, identify the sender of the email.

            If you don't know the answer, honestly admit that you don't know.
            You should never attempt to fabricate an answer. Remember to always reply in {language}.
            The output should be structured in the following order: Department, Keywords, Reply Date, Score, Sender.
            """),
            example_prompt,
            ("""
            Here is an email. {email}
            
            Please output in the format of example_prompt.
            
            """),
        ]
    )

    chain = final_prompt | chat | EmailOutputParser()


    question = []
    current_text = ""
    recording = False

    with open('question_text.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if '"""' in line:
                if recording:
                    # 문자열 종료
                    question.append(current_text)
                    current_text = ""
                recording = not recording
            elif recording:
                current_text += line
    def process_file(text):
        a=chain.invoke({"email": question,"language":"Korean"})
        print(a)
except:
    pass