# faginator
Simple paginator for py-cord with custom buttons. You can use it in responds, or default post messages.
This module helps you to create your own View in py-cord with paginate functions

How to install 

```
pip install faginator
```

### Attention!
You need to use py-cord version 2.1.0 or higher

# Parameters

|           Name             |                     Type                     |Default|                           Information                               |
|:-------------------------:|:-------------------------------------------:|:----------:|:-------------------------------------------------------------------:|
|           ctx             | `discord.ext.commands.Context` |            |                                                                     |
|         embeds `<optional>`    |              `list`              |  `None`  |       List of embeds        |
|          content `<optional>`   |                    `list`                   |   `None`   |                        List of message contents                    |
|    extra_buttons `<optional>`   |                    `list`                    | `None` |        Two dimensional list with buttons. Each nest list can have 5 or less buttons |
|   delete_on_timeout `<optional>`   |                    `bool`                   |   `False`  |      Delete message on timeout      |
|   disable_on_timeout `<optional>`   |                    `bool`                   |   `True`  |   Disable buttons on timeout  |
| timeout `<optional>`|                    `int`                   |   `180`  | Timeout for deleting or disabling buttons|
|  close_button `<optional>`  |                    `bool`                   |   `True`  |   Adds close button |
|    show_pages `<optional>`    |                    `bool`                   |   `True`   | Adds text at the bottom showing the current page |
|   lang `<optional>`  |                    `str`                   | `en` | Set language of buttons, pages. For this moment available: "en", "ru", "de" |
| only_author `<optional>`|                    `bool`                   | `True` |    If only author can use buttons to paginate    |
| skip_buttons `<optional>`|                    `bool`                   | `False` |   Adds additional buttons to move the page to the beginning or end   |

# Methods

### start - sends the menu

Args

| Name | Type | Default | Information |
|:----------------:|:----------:|:----------:|:-------------------:|
| type `<optional>` | `str` | `"text"` | The type of message. Can be `text` for text-commands or `slash` for "slash-commands" |
| ephemeral `<optional>` | `bool` | `False` | Ephemeral status for respond, works ONLY with `slash` |

### disable - disable the menu
Args
| Name | Type | Default | Information |
|:----------------:|:----------:|:----------:|:-------------------:|
| remove_buttons `<optional>` | `bool` | `False` | Should disabling menu remove buttons |
| remove_message `<optional>` | `bool` | `False` | Should disabling menu delete message |
| disable_buttons `<optional>` | `bool` | `True` | Should disabling menu disable buttons |
 

# Usage example

### Simple example with slash command responding
```py
import discord
from discord.ext import commands
from discord.ui import Button
from faginator import Faginator

client = commands.Bot(intents=discord.Intents.all(), command_prefix='YOUR_PREFIX_HERE')

@client.event
async def on_ready():
    print(f"Logged in as {client.user} | Latency: {client.latency * 100}")
    print("------------------")

@client.slash_command(description='test')
async def test(ctx):
    emb1 = discord.Embed(title='test1', description='test1')
    emb2 = discord.Embed(title='test2', description='test2')
    embeds = [emb1, emb2]
    contents = ['test 1', 'test 2']

    faginator = Faginator(ctx, content=contents, embeds=embeds, show_pages=True)
    await faginator.start(type="slash")

client.run('YOUR_TOKEN_HERE')

```

### Simple example with custom buttons with text-command
```py
import discord
from discord.ext import commands
from discord.ui import Button
from faginator import Faginator

client = commands.Bot(intents=discord.Intents.all(), command_prefix='YOUR_PREFIX_HERE')

@client.event
async def on_ready():
    print(f"Logged in as {client.user} | Latency: {client.latency * 100}")
    print("------------------")

@client.command()
async def test(ctx):
    emb1 = discord.Embed(title='test 1', description='test with buttons!')
    emb2 = discord.Embed(title='test 2', description='test 2 with buttons!')
    embeds = [emb1, emb2]

    btn1 = Button(label='1', custom_id='watermelon')
    btn2 = Button(label='2', custom_id='apple')
    btn3 = Button(label='3', custom_id='capybara')
    btn4 = Button(label='4', custom_id='foxes')
    btn5 = Button(label='5', custom_id='fastline')
    btn6 = Button(label='6', custom_id='your_custom_id')


    async def button_callback(interaction):
        await interaction.response.send_message(f'You clicked button with custom id: {interaction.custom_id}')

    btn1.callback = button_callback
    btn2.callback = button_callback
    btn3.callback = button_callback
    btn4.callback = button_callback
    btn5.callback = button_callback
    btn6.callback = button_callback

    extra_buttons = [[btn1, btn2, btn3, btn4], [btn5, btn6]]

    faginator = Faginator(ctx, embeds=embeds, extra_buttons=extra_buttons, show_pages=True, lang='en')
    await faginator.start()

client.run('YOUR_TOKEN_HERE')
```


