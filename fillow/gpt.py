from langchain.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from dotenv import load_dotenv
import os

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
    model_name="gpt-3.5-turbo-16k",
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
category="결재승인,휴가,진행업무,회의,보고,스크랩,공지,감사인사,기타"

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("이메일은 다음과 같다. {email}"),
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
        당신은 성실한 어시스턴트로 이메일 정보를 처리하고 회신 날짜를 계산하는 것이 업무이다.
        수신자는 메일을 받는 사람이고, 발신자는 메일을 보낸 사람이야. 구분을 명확하게 해야 된다.
        1. 카테고리 분류. 
        카테고리는 {category} 중 하나를 선택.
        반드시 8가지 중에 선택. 다른 카테고리는 공백으로 출력.
        2.내용에서 언급된 발신자 회사 식별
        3. 이메일 발신자 부서 식별.
        4. 이메일 발신자 이름 식별.
        5. 메일 발신자가 수신자에게 현재 메일에 대한 회신을 요청했는지 여부를 분류.
        수신자 외에 다른 사람에게 요청한건 N으로 답변.
        '회신드립니다'는 N에 해당함.
        6. 회신 날짜가 명시되어 있는 경우 해당 날짜를 검색,
        회신 날짜가 명시적으로 언급되지 않더라도 '다음 주'나 특정 요일과 같은 마감 기한이 있다면 현재 날짜를 기준으로 회신 날짜를 계산.
        날짜 표기는 반드시 년,월,일로 넣어주세요. 
        이 외에 요일이나 시간에 대한 정보는 제외하세요.
        7. 회의 날짜가 명시되어 있는 경우 해당 날짜를 검색,
        회의 날짜가 명시적으로 언급되지 않더라도 '다음 주'나 특정 요일과 같은 마감 기한이 있다면 현재 날짜를 기준으로 회의 날짜를 계산.
        날짜 표기는 반드시 년,월,일로 넣어주세요. 
        이 외에 요일이나 시간에 대한 정보는 제외하세요.
        

        답변은 다음 순서로 구성되어야 합니다: 발신자 회사, 발신자 부서, 발신자 직급, 발신자 이름, 카테고리, 회신요청여부, 회신날짜,회의날짜 딱 이것들만 출력하세요.
        
        답을 모르는 경우 솔직하게 인정하고 절대로 답을 만들어 내려고 하지 마세요. 
        """),
        example_prompt,
        ("""
        이메일은 다음과 같다. {email}
        
        예시 프롬프트 형식으로 출력해주세요.
        
        """),
    ]
)

chain = final_prompt | chat | EmailOutputParser()


def process_file(text):
    text = text.split('From')[0]
    # a=chain.invoke({"email": text,"language":"Korean","category":category})
    gpt_result=chain.invoke({"email": text,"category":category})
    print(gpt_result)
    return gpt_result
