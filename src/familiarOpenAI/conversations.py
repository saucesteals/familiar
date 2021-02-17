from os import name, scandir
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

    def get_initial_history(self, member:discord.Member) -> list:
        history = []

        name = get_member_name(member)
        bot_name = get_member_name(member.guild.me)

        history.append(self._new_response(f"Hello, my name is {name}. Who are you?", f"My name is {bot_name}."))
        history.append(self._new_response(f"How are you?", f"I'm okay, thanks for asking."))
        
        return history

    def set_history(self, member:discord.Member, history:list) -> None:
        self.ensure_history(member)

        self.conversations[str(member.id)]["history"] = [*history]

    def create_new_conversation(self, member:discord.Member, history:list=None, *args, **kwargs) -> dict:
        frequency_penalty = kwargs.get("frequency_penalty", 0.0)
        presence_penalty = kwargs.get("presence_penalty", 0.3)
        temperature = kwargs.get("temperature", 0.9)
        engine = kwargs.get("engine", self.engine)

        self.conversations[str(member.id)] = {"history": history if history else self.get_initial_history(member), 
                                            "frequency_penalty":frequency_penalty,
                                            "presence_penalty":presence_penalty,
                                            "temperature":temperature,
                                            "engine":engine,
                                            "append_new": True,
                                            }

        return self.conversations[str(member.id)]
    

    def get_member(self, member:discord.Member) -> dict:
        self.ensure_history(member)
        return self.conversations[str(member.id)]
    
    def flip_append_new(self, member:discord.Member) -> None:
        self.conversations[str(member.id)]["append_new"] = not self.get_append_new(member)

    def set_append_new(self, member:discord.Member, new_bool:bool) -> None:
        self.conversations[str(member.id)]["append_new"] = new_bool


    def get_append_new(self, member:discord.Member) -> bool:
        return self.get_member(member)["append_new"]

    def get_frequency_penalty(self, member:discord.Member) -> float:
        return self.get_member(member)["frequency_penalty"]

    def get_presence_penalty(self, member:discord.Member) -> float:
        return self.get_member(member)["presence_penalty"]
    
    def get_temperature(self, member:discord.Member) -> float:
        return self.get_member(member)["temperature"]
    
    def get_engine(self, member:discord.Member) -> str:
        return self.get_member(member)["engine"]

    def add_history(self, member:discord.Member, prompt:str, response:str) -> None:
        if len(self.get_history(member)) >= 5:
            del self.conversations[str(member.id)]["history"][0]

        new_response = self._new_response(prompt, response)

        self.conversations[str(member.id)]["history"].append(new_response)

    def reset_history(self, member:discord.Member) -> None:
        self.create_new_conversation(member)

    def ensure_history(self, member:discord.Member) -> None:
        if not self.conversations.get(str(member.id)):
            self.create_new_conversation(member)

    def has_history(self, member:discord.Member) -> bool:
        return True if self.conversations.get(str(member.id)) else False

    def cleanse_response(self, response:str) -> str:
        return response.replace("output:", "").strip().split("\n")[0]

    def get_history(self, member:discord.Member) -> list:
        self.ensure_history(member)
        return self.conversations[str(member.id)]["history"]

    def get_customized_gpt(self, member:discord.Member, *args, **kwargs) -> GPT:
        instance = self.get_gpt(member)
        
        history = self.get_history(member)

        for conversation in history:
            instance.add_example(Example(conversation["human"], conversation["bot"]))

        return instance

    def get_gpt(self, member:discord.Member) -> GPT:
        return GPT(frequency_penalty=self.get_frequency_penalty(member), 
                    presence_penalty=self.get_presence_penalty(member), 
                    temperature=self.get_temperature(member), 
                    engine=self.get_engine(member)
                    )

    def get_response(self, member:discord.Member, prompt:str, retry:bool=False, append_new:bool=True) -> str:
        self.ensure_history(member)

        if retry:
            self.client.logger.warning("Retrying to get a response for " + str(member))
        else:
            self.client.logger.info("Getting a response for " + str(member))

        instance = self.get_customized_gpt(member=member)

        full_output = instance.submit_request(prompt)
        response = self.cleanse_response(full_output.choices[0].text)

        if not response:
            self.client.logger.warning("Couldn't get a response for " + str(member) + " (Blank response from GPT3)")
            return "Oops, I couldn't respond to that for some reason!"

        if response == prompt:
            
            if not retry:
                return self.get_response(member, prompt, True)

            self.reset_history(member)
            self.client.logger.warning("GPT3 got trapped by " + str(member))
            return "I just fell into a trap :( To save myself, I'll have to wipe all my interactions with you. Goodbye friend."

        if self.get_append_new(member):
            self.add_history(member, prompt, response)
        
        self.client.logger.info("Got a response for " + str(member))
        return response
