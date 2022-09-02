import discord.errors
from discord.ui import View, Button
from discord import ButtonStyle

'''
 Copyright (c) 2022 Fadix
 
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:
 
 The above copyright notice and this permission notice shall be included
 in all copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

locales = {
    "NEXT": {
        "en": "Next",
        "ru": "Дальше",
        "de": "Nach vorne"
    },
    "PREVIOUS": {
        "en": "Previous",
        "ru": "Назад",
        "de": "Zurück"
    },
    "CLOSE": {
        "en": "Close",
        "ru": "Закрыть",
        "de": "Nah dran"
    },
    "PAGES": {
        "en": "Page",
        "ru": "Страница",
        "de": "Seite"
    },
    "SKIP_START": {
        "en": "To the start",
        "ru": "В начало",
        "de": "Zum Anfang"
    },
    "SKIP_END": {
        "en": "To the end",
        "ru": "В конец",
        "de": "Schlussendlich"
    }
}

class Faginator(View):
    def __init__(self, ctx, embeds: list = None, content: list = None, extra_buttons: list = None,
                 delete_on_timeout: bool = False, disable_on_timeout: bool = True, timeout: int = 180,
                 close_button: bool = True, show_pages: bool = True, lang: str = 'en', only_author: bool = True,
                 skip_buttons: bool = False):

        super().__init__(timeout=timeout, disable_on_timeout=disable_on_timeout)

        self.ctx = ctx
        self.cur_page = 0

        if extra_buttons is not None:
            for _ in range(len(extra_buttons)):
                extra_buttons[_] = extra_buttons[_][:5]
                for u in range(len(extra_buttons[_])):
                    extra_buttons[_][u].row = 0
            for _ in extra_buttons[self.cur_page]: self.add_item(_)

        self.extra_buttons = extra_buttons

        self.delete_on_timeout = delete_on_timeout

        self.only_author = only_author

        if show_pages:
            if embeds is not None:
                self.embeds = [embeds[i].set_footer(text=f'{locales["PAGES"][lang]} {i + 1}/{len(embeds)}') for i in range(len(embeds))]
            if content is not None and embeds is None:
                self.content= [content[i]+f'\n\n{locales["PAGES"][lang]} {i + 1}/{len(content)}' for i in range(len(content))]
            elif content is not None:
                self.content = content
            if content is None:
                self.content = None
            if embeds is None:
                self.embeds = None
        else:
            if embeds is not None:
                self.embeds = embeds
            if content is not None:
                self.content= content

            if content is None:
                self.content = None
            if embeds is None:
                self.embeds = None


        deter_button = Button(label=locales["CLOSE"][lang], style=ButtonStyle.red, custom_id="close_button", row=1)
        back_button = Button(label=locales["PREVIOUS"][lang], custom_id="previous_button", style=ButtonStyle.grey, row=1)
        next_button = Button(label=locales["NEXT"][lang], style=ButtonStyle.grey, custom_id="next_button", row=1)
        skip_start_button = Button(label=locales["SKIP_START"][lang], style=ButtonStyle.grey, custom_id="skip_start_button", row=1)
        skip_end_button = Button(label=locales["SKIP_END"][lang], style=ButtonStyle.grey, custom_id="skip_end_button", row=1)


        self.deter_button = deter_button
        self.back_button = back_button
        self.next_button = next_button
        self.skip_start_button = skip_start_button
        self.skip_end_button = skip_end_button

        deter_button.callback = self.close_callback
        back_button.callback = self.back_callback
        next_button.callback = self.next_callback
        skip_start_button.callback = self.skip_start_callback
        skip_end_button.callback = self.skip_end_callback

        [self.add_item(i) for i in [back_button, next_button]]
        self.close_button = close_button
        self.skip_buttons = skip_buttons

        if skip_buttons: [self.add_item(i) for i in [skip_start_button, skip_end_button]]
        if close_button: self.add_item(deter_button)

        if self.embeds is not None and len(self.embeds) == 1:
            self.next_button.disabled = True
            self.back_button.disabled = True
        if self.content is not None and len(self.content) == 1:
            self.next_button.disabled = True
            self.back_button.disabled = True

        self.back_button.disabled = True

    def check_emb_content(self):
        if self.content is not None:
            new_content = self.content[self.cur_page]
        else:
            new_content = None
        if self.embeds is not None:
            new_emb = self.embeds[self.cur_page]
        else:
            new_emb = None
        return [new_emb, new_content]

    async def back_callback(self, interaction):
        self.next_button.disabled = False

        self.skip_end_button.disabled = False
        self.skip_start_button.disabled = False

        self.cur_page -= 1
        if self.cur_page == 0: self.back_button.disabled = True
        else: self.back_button.disabled = False

        if self.extra_buttons is not None:
            self.clear_items()
            for _ in self.extra_buttons[self.cur_page]: self.add_item(_)
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.skip_buttons: [self.add_item(i) for i in [self.skip_start_button, self.skip_end_button]]
            if self.close_button: self.add_item(self.deter_button)

        res = self.check_emb_content()

        await interaction.response.edit_message(view=self, embed=res[0], content=res[1])


    async def next_callback(self, interaction):
        self.back_button.disabled = False

        self.skip_end_button.disabled = False
        self.skip_start_button.disabled = False

        self.cur_page += 1
        if self.embeds is not None:
            if self.cur_page + 1 == len(self.embeds): self.next_button.disabled = True
            else: self.next_button.disabled = False
        else:
            if self.cur_page + 1 == len(self.content): self.next_button.disabled = True
            else: self.next_button.disabled = False

        if self.extra_buttons is not None:
            self.clear_items()
            for _ in self.extra_buttons[self.cur_page]: self.add_item(_)
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.skip_buttons: [self.add_item(i) for i in [self.skip_start_button, self.skip_end_button]]
            if self.close_button: self.add_item(self.deter_button)

        res = self.check_emb_content()

        await interaction.response.edit_message(view=self, embed=res[0], content=res[1])

    async def skip_start_callback(self, interaction):
        self.skip_start_button.disabled = True
        self.skip_end_button.disabled = False

        self.next_button.disabled = False

        self.cur_page = 0
        self.back_button.disabled = True

        if self.extra_buttons is not None:
            self.clear_items()
            for _ in self.extra_buttons[self.cur_page]: self.add_item(_)
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.skip_buttons: [self.add_item(i) for i in [self.skip_start_button, self.skip_end_button]]
            if self.close_button: self.add_item(self.deter_button)

        res = self.check_emb_content()

        await interaction.response.edit_message(view=self, embed=res[0], content=res[1])

    async def skip_end_callback(self, interaction):
        self.skip_end_button.disabled = True
        self.skip_start_button.disabled = False

        self.next_button.disabled = True
        self.cur_page = len(self.embeds)-1
        self.back_button.disabled = False

        if self.extra_buttons is not None:
            self.clear_items()
            for _ in self.extra_buttons[self.cur_page]: self.add_item(_)
            [self.add_item(i) for i in [self.back_button, self.next_button]]
            if self.skip_buttons: [self.add_item(i) for i in [self.skip_start_button, self.skip_end_button]]
            if self.close_button: self.add_item(self.deter_button)

        res = self.check_emb_content()

        await interaction.response.edit_message(view=self, embed=res[0], content=res[1])


    async def close_callback(self, interaction):
        try: await self.message.delete()
        except discord.errors.NotFound: print("[ERROR] Seems like your message ephemeral or posted before latest bot restart")

    async def update(self):

        res = self.check_emb_content()

        await self.message.edit(embed=res[0], content=res[1])

    async def interaction_check(self, interaction) -> bool:
        if (interaction.user != self.ctx.author) * self.only_author:
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        if self.delete_on_timeout:
            self.message.delete()
