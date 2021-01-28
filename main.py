import discord
from discord.ext import commands, tasks
from random import choice, randrange, shuffle
from combs import build_steps

class Performer:
    def __init__(self, member):
        self.member = member
        self.channel = None
        self.been_to_main = False

    def move_main(self):
        self.been_to_main = True
        print(self.member.name + " moves to the main channel")

    def __repr__(self):
        return self.__string__()

    def __str__(self):
        return self.member.name

turn_count = None
TURN_LENGTH = 5

intents = discord.Intents.all()
client = commands.Bot(command_prefix = '.', intents=intents)
context = None
voice_channels = {}
performers = []
steps = []
setup = False
run = False
start_time = 0
counter = 0

@tasks.loop(seconds=TURN_LENGTH, count=turn_count)
async def periodic():
    global counter
    if not run:
        return
    actions = []
    if counter == turn_count:
        actions = climax(context)
    elif counter == turn_count + 1:
        actions = ending(context)
    else:
        actions = move_members(context, counter)

    for action in actions:
        await action()
    print(f"step = {counter}")
    counter += 1



@client.event
async def on_ready():
    print(f"We have joined as {client}")


@client.command()
async def setup(ctx):
    global context
    global voice_channel
    global setup
    global performers
    global turn_count
    global steps
    setup = True
    context = ctx
    performers = []
    for member in ctx.guild.members:
        if "performer" in [role.name for role in member.roles] and member.voice:
            performers.append(Performer(member))
            await member.edit(mute=False)
            print(f"Registering performer name={member.name} id={member.id}")
    for voice_channel in ctx.guild.voice_channels:
        voice_channels[voice_channel.name] = voice_channel
        print(f"Registering channel '{voice_channel.name}'")
    steps = build_steps(performers)
    turn_count = len(steps)
    print(f"steps = {steps}")
    print(f"Number f turns = {turn_count}")
    await ctx.send("Setup Complete")

@client.command()
async def begin(ctx):
    global run
    if setup and not run:
        run = True
        periodic.start()
        await ctx.send(f"LETS MAKE SOME NOISE")
    else:
        print("Please run the setup command first!!")

def move_members(ctx, i):
    print(f"Moving all members to position {steps[i]}")
    current_step = steps[i]
    channel_list = list(voice_channels.values())
    for room_num in range(len(current_step)):
        for p in current_step[room_num]:
            yield lambda: p.tag.member.move_to(channel_list[room_num])


def climax(ctx):
    print("BIG CLIMAX")
    for performer in performers:
        if performer.member.voice:
            yield lambda: performer.member.move_to(voice_channels["MainStage"])


def ending(ctx):
    for performer in performers:
        if performer.member.voice:
            yield lambda: performer.member.edit(mute=True)
    yield lambda: ctx.send("CLAPCLAPCLAPCLAP")
    quit()

client.run('NzY5MDE1NzY1Mjg1MjA4MDY0.X5I3vg.JARz0sXNjXFBlYUtJK4E0OUU4NY')
