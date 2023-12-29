from langchain.chat_models import ChatOpenAI
from langchain.prompts.few_shot import FewShotChatMessagePromptTemplate
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.prompts import ChatMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import BaseOutputParser
import openai,os
from dotenv import load_dotenv
import base64
import requests
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
    category="결재승인,휴가,프로젝트/작업,회의,보고,스크랩,공지,감사인사,기타"

    example_prompt = ChatPromptTemplate.from_messages(
        [
            # ("Here is an email. Please extract up to 5 important keyword terms. They don't necessarily have to be words from the content.{email}"),
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
            

            답변은 다음 순서로 구성되어야 합니다: 발신자 회사, 발신자 부서, 발신자 직급, 발신자 이름, 카테고리, 회신요청여부, 회신날짜.
            답을 모르는 경우 솔직하게 인정하고 절대로 답을 만들어 내려고 하지 마세요. 
            """),
            example_prompt,
            ("""
            이메일은 다음과 같다. {email}
            
            예시 프롬프트 형식으로 출력해주세요.
            
            """),
            # ("system", """
            # You are a diligent assistant tasked with processing email information and calculating the reply date. 
            # Identify the department from the content, summarize it using up to 5 key tag keywords. 
            # Find the reply date from the content or calculate it from the current date if not specified. 
            # Assign a score based on the email's importance and identify the sender.

            # Admit if you don't know the answer, never fabricate responses. 
            # Always respond in {language}. 
            # The output should be structured as follows: Department, Keywords, Reply Date, Score, Sender, Category. 
            # When determining the category, consider only the category mentioned within {category}.
            
            # """),
            # example_prompt,
            # ("""
            # Here is an email. {email}
            
            # Please output in the format of example_prompt.
            
            # """),
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
        # a=chain.invoke({"email": text,"language":"Korean","category":category})
        a=chain.invoke({"email": text,"category":category})
        print(a)




    # 이미지 인식하는 부분 쓸지 말지 모르겠음
    # # Function to encode the image
    # def encode_image(image_path):
    #   with open(image_path, "rb") as image_file:
    #     return base64.b64encode(image_file.read()).decode('utf-8')

    # # Path to your image
    # image_path = "path_to_your_image.jpg"

    # # Getting the base64 string
    # base64_image = encode_image(image_path)

    # headers = {
    #   "Content-Type": "application/json",
    #   "Authorization": f"Bearer {api_key}"
    # }

    # payload = {
    #   "model": "gpt-4-vision-preview",
    #   "messages": [
    #     {
    #       "role": "user",
    #       "content": [
    #         {
    #           "type": "text",
    #           "text": "What’s in this image?"
    #         },
    #         {
    #           "type": "image_url",
    #           "image_url": {
    #             "url": f"data:image/jpeg;base64,{base64_image}"
    #           }
    #         }
    #       ]
    #     }
    #   ],
    #   "max_tokens": 300
    # }

    # response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # print(response.json())
except:
    pass