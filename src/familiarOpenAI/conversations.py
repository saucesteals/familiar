from .gpt import GPT
from .gpt import Example
import openai
from discord.ext import commands
import discord


class Conversations:
    def __init__(self, client:commands.Bot, open_ai_key:str):
        self.client = client
        self.conversations = {}
        openai.api_key = open_ai_key

    def _new_response(self, prompt:str, response:str) -> dict:
        return {"human":prompt, "bot":response}

    
    def get_initial_history(self, member:discord.Member) -> list:
        name = member.nick if member.nick else member.name

        introduction = self._new_response(f"Hello, my name is {name}.", f"Nice to meet you {name}!")

        return [introduction]

    def get_qna(self) -> list:
        qna = []

        # From https://github.com/harperreed/gpt3-persona-bot/blob/master/personas/example.json
        qna.append(self._new_response(f"What is human life expectancy in the United States?", f"Human life expectancy in the United States is 78 years."))
        qna.append(self._new_response(f"Who was president of the United States in 1955?", f"Dwight D. Eisenhower was president of the United States in 1955."))
        qna.append(self._new_response(f"What party did he belong to?", f"He belonged to the Republican Party."))
        qna.append(self._new_response(f"Who was president of the United States before George W. Bush?", f"Bill Clinton was president of the United States before George W. Bush."))
        qna.append(self._new_response(f"Who won the World Series in 1995?", f"The Atlanta Braves won the World Series in 1995."))

        return qna

    def create_new_conversation(self, member:discord.Member):
        self.conversations[str(member.id)] = {"history": self.get_qna(), "initial":self.get_initial_history(member)}

        return self.conversations[str(member.id)]

    def add_history(self, member:discord.Member, prompt:str, response:str) -> None:
        if not self.conversations.get(str(member.id)):
            self.create_new_conversation(member)

        if len(self.conversations[str(member.id)]["history"]) > 5:
            del self.conversations[str(member.id)]["history"][0]

        new_response = self._new_response(prompt, response)

        self.conversations[str(member.id)]["history"].append(new_response)

    def reset_history(self, member:discord.Member) -> None:
        if self.conversations.get(str(member.id)):
            self.conversations[str(member.id)]["history"] = self.get_qna()


    def get_response(self, member:discord.Member, prompt:str, retry:bool=False) -> str:
        print("Getting a response for", str(member), "(Retrying)" if retry else "")
        if not self.conversations.get(str(member.id)):
            self.create_new_conversation(member)
        
        history = self.conversations[str(member.id)]["history"]
        initial = self.conversations[str(member.id)]["initial"]

        instance = GPT()

        # Add initial conversation
        for initial_conversation in initial:
            instance.add_example(Example(initial_conversation["human"], initial_conversation["bot"]))

        # Add cached converastion, if there is any
        for conversation in history:
            instance.add_example(Example(conversation["human"], conversation["bot"]))

        full_output = instance.submit_request(prompt)

        response = full_output.choices[0].text.replace("output:", "").strip()

        if not response:
            return "Oops, I couldn't response to that for some reason!"

        if response == prompt or response == history[len(history)-1]["bot"] :
            
            if not retry:
                return self.get_response(member, prompt, True)

            self.reset_history(member)
            return "I just fell into a trap :( To save myself, I'll have to wipe all my interactions with you. Goodbye friend."

        self.add_history(member, prompt, response)
        
        return response
