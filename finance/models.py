from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

from finance.patterns import SingletonInstance


class ChatHuggingFaceSingleton(SingletonInstance):
    def __init__(self):
        super().__init__()
        self.__llm = HuggingFaceEndpoint(
            repo_id="microsoft/Phi-3-mini-4k-instruct",
            task="text-generation",
            max_new_tokens=512,
            do_sample=False,
            repetition_penalty=1.03,
        )
        self.__model = ChatHuggingFace(llm=self.__llm, verbose=True)
        self.__system_template = "Translate the following English text {language}"
        self.__prompt_template = ChatPromptTemplate.from_messages(
            [("system", self.__system_template), ("user", "{text}")]
        )

    def translate(self, translate_to: str, text: str) -> str:
        return self.__model.invoke(
            self.__prompt_template.invoke({"language": translate_to, "text": text})
        ).content
