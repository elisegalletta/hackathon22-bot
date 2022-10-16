import discord
import os
import requests
import json
import random

# Youtube tutorials
# https://www.youtube.com/watch?v=SPTfmiYiuok&t=3s

intent = discord.Intents.default()
intent.members = True
intent.message_content = True

client = discord.Client(intents = intent)

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing", "stressed"]

starter_encouragements = ["Cheer up!", "Hang in there!", "You got it!", "Don't worry! Everything will be okay."]

# Get quotes from quote files
def get_quote():
  return random.choice(list(open('quotes.txt')))

# Get TV recs from text file
def get_tvrec():
  return random.choice(list(open('televisionshows.txt')))

def get_stressrelief():
  return random.choice(list(open('stressrelief.txt')))

def get_celebration():
  return random.choice(list(open('celebrationgifs.txt')))

# get dog from dog api
def get_dog():
  response = requests.get("https://random.dog/woof.json?ref=apilist.fun")
  json_data = json.loads(response.text)
  img = json_data['url']
  return(img)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

# Trivia tutorial: https://www.youtube.com/watch?v=311oS1zvU-o  
  
  async def trivia():
    questions = {'Who was the first computer programmer?': 'B', 'Who said "There is no limit to what we, as women, can accomplish."': 'D', 'How smart and amazing are you?': 'A', 'What percent of programmers in the US are women?': 'C', 'What was the first state to allow women to vote?': 'D'}
    choices = [['A. Anita Borg', 'B. Ada Lovelace', 'C. Elizabeth Feinler', 'D. Hedy Lammar'], ['A. Beyonce', 'B. Meghan Markle', 'C. Maya Angelou', 'D. Oprah Winfrey'], ['A. Incredibly', 'B. On a good day...okay', 'C. Not very', 'D. Not at all'], ['A. 5%', 'B. 34%', 'C. 28%', 'D. 16%'], ['A. California', 'B: Utah', 'C: Colorado', 'D: Wyoming']]
    randomnum = random.randint(1, len(questions))
    question_list = list(questions.keys())
    question = question_list[randomnum - 1]
    choice = choices[randomnum - 1]
    choice_sep = '\n'.join(choice)
  
    em = discord.Embed(title = f"{question}\n{choice_sep}")
    await message.channel.send(embed = em)
    
    answered = False
    while answered == False:
      response = await client.wait_for('message')
      if response.content.upper() in ['A', 'B', 'C', 'D']:
        answer = response.content.upper()
        break

    if answer == questions[question]:
      return "correct"
    else:
      return "incorrect"
  
  
  msg = message.content

  if msg.startswith('trivia'):
    if await trivia() == "correct":
      await message.channel.send("Correct, girl boss!")
      celebration = get_celebration()
      await message.channel.send(celebration)
    else:
      await message.channel.send("Incorrect, but keep your head up!")
      
    
  if msg.startswith('inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('hi'):
    m = "Hi I am Boost Bot, here to boost your day!"
    m2 = "If you want an inspiring quote, type 'inspire' \n If you want a TV recommendation to boost your mood, type 'recommend'\n If you want to relieve your stress, type 'stress relief' \n If you want a cute puppy picture, type 'dog' \n If you're feeling sad or stressed, let Boost Bot know! \n If you want to play a fun game, type 'trivia'"
    await message.channel.send(m)
    await message.channel.send("https://m.media-amazon.com/images/I/51tWGpACcIL.jpg")
    await message.channel.send(m2)

  if msg.startswith('recommend'):
    show = get_tvrec()
    await message.channel.send(show)

  if msg.startswith('stress relief'):
    relief = get_stressrelief()
    await message.channel.send(relief)
    
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))
    await message.channel.send("Choose one of my boosting ideas!")

  if msg.startswith('dog'):
    img = get_dog()
    await message.channel.send(img)

client.run(os.environ['TOKEN'])
