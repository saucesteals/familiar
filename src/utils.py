import discord

def get_member_name(member:discord.Member) -> str:
    return member.nick if member.nick else member.name

def cleanse_prompt(prompt:str, message:discord.Message) -> str:
    for mention in message.mentions:
        prompt = prompt.replace(f"<@!{str(mention.id)}>", get_member_name(mention))

    for channel in message.channel_mentions:
        prompt = prompt.replace(f"<#{str(channel.id)}>", channel.name)

    for role in message.role_mentions:
        prompt = prompt.replace(f"<@&{str(role.id)}>", role.name)

    return prompt.strip()
