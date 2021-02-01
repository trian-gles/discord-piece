import discord
from discord.ext import commands, tasks
from random import choice, randrange, shuffle
from combs import build_steps

class Performer:
    def __init__(self, member, other_mem):
        self.member = member
        self.other_mem = other_mem
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
TURN_LENGTH = 20

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
    elif counter == turn_count + 2:
        actions = applause(context)
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
            print(f"Registering performer name={member.name} id={member.id}")
            alt_account = None
            nick = member.nick
            for other_mem in ctx.guild.members:
                if other_mem.nick:
                    if other_mem.nick == (nick + "_alt"):
                        print(f"Registering alt account for {member.name}: {other_mem.name}")
                        alt_account = other_mem
            performers.append(Performer(member, alt_account))
            await member.edit(mute=False)

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
        for item in current_step[room_num]:
            yield lambda: item.tag.member.move_to(channel_list[room_num])
            if item.tag.other_mem:
                print(f"Move alt account {item.tag.other_mem.name}")
                yield lambda:item.tag.other_mem.move_to(channel_list[room_num])


def climax(ctx):
    print("BIG CLIMAX")
    for performer in performers:
        if performer.member.voice:
            yield lambda: performer.member.move_to(voice_channels["MainStage"])
            if performer.other_mem:
                yield lambda: performer.other_mem.move_to(voice_channels["MainStage"])


def ending(ctx):
    for performer in performers:
        if performer.member.voice:
            yield lambda: performer.member.edit(mute=True)

def applause(ctx):
    for performer in performers:
        if performer.member.voice:
            yield lambda: performer.member.edit(mute=False)
    yield lambda: ctx.send("CLAPCLAPCLAPCLAP")
    quit()

client.run('INSERT TOKEN')
