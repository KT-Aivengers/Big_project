from langchain.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import ChatMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import BaseOutputParser
import openai,os
from dotenv import load_dotenv


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
category="요청,결재승인,작업완료,안내,보고,스크랩,공유,휴가신청"

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
        You are a diligent assistant tasked with processing email information and calculating the reply date. 
        Identify the department from the content, summarize it using up to 5 key tag keywords. 
        Find the reply date from the content or calculate it from the current date if not specified. 
        Assign a score based on the email's importance and identify the sender.

        Admit if you don't know the answer, never fabricate responses. 
        Always respond in {language}. 
        The output should be structured as follows: Department, Keywords, Reply Date, Score, Sender, Category. 
        When determining the category, consider only the category mentioned within {category}.
        
        """),
        example_prompt,
        ("""
        Here is an email. {email}
        
        Please output in the format of example_prompt.
        
        """),
    ]
)

chain = final_prompt | chat | EmailOutputParser()


# question = []
# current_text = ""
# recording = False

# with open('question_text.txt', 'r', encoding='utf-8') as file:
#     for line in file:
#         if '"""' in line:
#             if recording:
#                 # 문자열 종료
#                 question.append(current_text)
#                 current_text = ""
#             recording = not recording
#         elif recording:
#             current_text += line
def process_file(text):
    a=chain.invoke({"email": text,"language":"Korean","category":category})
    print(a)
