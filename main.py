import discord
from discord.ext import commands
import openai
import threading
import time

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

openai.api_key = ""  # Replace with your OpenAI API key

@bot.command(name='askFlurr')
async def askFlurr(ctx):
    userMessage = ctx.message.content
    question = userMessage[10:]
    await ctx.send(f"{ctx.author} asked Flurr:\n```{question}```")

    thread = threading.Thread(target=generate_response, args=(ctx.author.id, question, ctx.channel.id))
    thread.start()

def generate_response(user_id, question, channel_id):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=f"Q: {question}\nA:",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    time.sleep(10)

    actual_response = response.choices[0].text.strip()
    send_response(actual_response, channel_id)

def send_response(response, channel_id):
    bot.loop.create_task(bot.get_channel(channel_id).send(f"Flurr responds: \n```{response}```"))

def main():
    bot.run("")  # Replace with your Discord bot token

if __name__ == '__main__':
    main()