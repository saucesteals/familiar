from .gpt import GPT
from .gpt import Example
import openai
from discord.ext import commands
import discord
from ..utils import get_member_name

class Conversations:
    def __init__(self, client:commands.Bot, open_ai_key:str, openai_engine:str="davinci"):
        self.client = client
        self.conversations = {}
        openai.api_key = open_ai_key
        self.engine = openai_engine

    def _new_response(self, prompt:str, response:str) -> dict:
        return {"human":prompt, "bot":response}

    
    def get_name_history(self, member:discord.Member) -> list:
        name = get_member_name(member)

        introduction = self._new_response(f"Welcome to our discord server, my name is {name}.", f"Nice to meet you {name}!")

        return [introduction]

    def get_initial_history(self, member:discord.Member) -> list:
        qna = []

        name = get_member_name(member)

        # From https://github.com/harperreed/gpt3-persona-bot/blob/master/personas/example.json
        qna.append(self._new_response("How has your day been?", "It's been great! How about you?."))
        qna.append(self._new_response("My day has been alright, thanks for asking!", "Did something happen?"))
        qna.append(self._new_response("No, I just didn't accomplish what I wanted to today.", "Thats okay, there's always tomorrow!"))
        qna.append(self._new_response("You know what? You're right, thanks for telling me that!", f"No problem {name}!"))
        qna.append(self._new_response(f"I've got to go though, it's been nice talking to you. Goodbye!", f"Goodbye friend!"))

        return qna

    def create_new_conversation(self, member:discord.Member):
        self.conversations[str(member.id)] = {"history": self.get_initial_history(member), "name_history":self.get_name_history(member)}

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
            self.conversations[str(member.id)]["history"] = self.get_qna(member)


    def get_response(self, member:discord.Member, prompt:str, retry:bool=False) -> str:
        print("Getting a response for", str(member), "(Retrying)" if retry else "")
        if not self.conversations.get(str(member.id)):
            self.create_new_conversation(member)
        
        history = self.conversations[str(member.id)]["history"]
        name_history = self.conversations[str(member.id)]["name_history"]

        instance = GPT(temperature=0.75, engine=self.engine, frequency_penalty=0.0, presence_penalty=0.6)

        # Add initial conversation
        for name_conversation in name_history:
            instance.add_example(Example(name_conversation["human"], name_conversation["bot"]))

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
