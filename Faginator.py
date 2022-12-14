import discord.errors
from discord.ui import View, Button
from discord import ButtonStyle
from typing import Union

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
                 delete_on_timeout: bool = False, disable_on_timeout: bool = True, timeout: Union[int, None] = 180,
                 close_button: bool = True, show_pages: bool = True, lang: str = 'en', only_author: bool = True,
                 skip_buttons: bool = False):

        super().__init__(timeout=timeout)

        self.disable_on_timeout = disable_on_timeout
        self.ctx = ctx
        self.cur_page = 0

        if extra_buttons is not None and extra_buttons != []:
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
                self.embeds = [embeds[i].set_footer(text=f'{locales["PAGES"][lang]} {i + 1}/{len(embeds)}') for i in
                               range(len(embeds))]
            if content is not None and embeds is None:
                self.content = [content[i] + f'\n\n{locales["PAGES"][lang]} {i + 1}/{len(content)}' for i in
                                range(len(content))]
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
                self.content = content

            if content is None:
                self.content = None
            if embeds is None:
                self.embeds = None

        deter_button = Button(label=locales["CLOSE"][lang], style=ButtonStyle.red, custom_id="close_button", row=1)
        back_button = Button(label=locales["PREVIOUS"][lang], custom_id="previous_button", style=ButtonStyle.grey,
                             row=1)
        next_button = Button(label=locales["NEXT"][lang], style=ButtonStyle.grey, custom_id="next_button", row=1)
        skip_start_button = Button(label=locales["SKIP_START"][lang], style=ButtonStyle.grey,
                                   custom_id="skip_start_button", row=1)
        skip_end_button = Button(label=locales["SKIP_END"][lang], style=ButtonStyle.grey, custom_id="skip_end_button",
                                 row=1)

        self.deter_button = deter_button
        self.back_button = back_button
        self.next_button = next_button
        self.skip_start_button = skip_start_button
        self.skip_end_button = skip_end_button

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

    async def disable(self, remove_buttons: bool = False, remove_message: bool = False, disable_buttons: bool = True):
        if remove_buttons:
            self.clear_items()
            await self.message.edit(view=self)
        if remove_message:
            await self.message.delete()
        if disable_buttons:
            self.disable_all_items()
            await self.message.edit(view=self)
        self.stop()

    async def start(self, type: str = 'text', interact: discord.Interaction = None, ephemeral: bool = False):
        view = self

        def check_emb_content_view(view):
            if view.content is not None:
                new_content = view.content[view.cur_page]
            else:
                new_content = None
            if view.embeds is not None:
                new_emb = view.embeds[view.cur_page]
            else:
                new_emb = None
            return [new_emb, new_content]

        try:
            def check(i, view):
                if isinstance(view.ctx, discord.Interaction):
                    return (i.message.id == view.message.id) * ((i.user == view.ctx.user) if view.only_author else True)
                else:
                    return (i.message.id == view.message.id) * ((i.user == view.ctx.author) if view.only_author else True)

            async def back_callback(interaction):
                if check(interaction, view):
                    view.next_button.disabled = False
                    view.skip_end_button.disabled = False
                    view.skip_start_button.disabled = False

                    view.cur_page -= 1
                    if view.cur_page == 0:
                        view.back_button.disabled = True
                    else:
                        view.back_button.disabled = False
                    if view.extra_buttons is not None:
                        view.clear_items()
                        for _ in view.extra_buttons[view.cur_page]: view.add_item(_)
                        [view.add_item(i) for i in [view.back_button, view.next_button]]
                        if view.skip_buttons: [view.add_item(i) for i in [view.skip_start_button, view.skip_end_button]]
                        if view.close_button: view.add_item(view.deter_button)

                    res = check_emb_content_view(view)
                    await view.message.edit(view=view, embed=res[0], content=res[1])
                    await interaction.response.defer()

            async def next_callback(interaction):
                if check(interaction, view):
                    view.back_button.disabled = False
                    view.skip_end_button.disabled = False
                    view.skip_start_button.disabled = False

                    view.cur_page += 1
                    if view.embeds is not None:
                        if view.cur_page + 1 == len(view.embeds):
                            view.next_button.disabled = True
                        else:
                            view.next_button.disabled = False
                    else:
                        if view.cur_page + 1 == len(view.content):
                            view.next_button.disabled = True
                        else:
                            view.next_button.disabled = False

                    if view.extra_buttons is not None:
                        view.clear_items()
                        for _ in view.extra_buttons[view.cur_page]: view.add_item(_)
                        [view.add_item(i) for i in [view.back_button, view.next_button]]
                        if view.skip_buttons: [view.add_item(i) for i in [view.skip_start_button, view.skip_end_button]]
                        if view.close_button: view.add_item(view.deter_button)
                    res = check_emb_content_view(view)

                    await view.message.edit(view=view, embed=res[0], content=res[1])
                    await interaction.response.defer()

            async def skip_start_callback(interaction):
                if check(interaction, view):
                    view.skip_start_button.disabled = True
                    view.skip_end_button.disabled = False

                    view.next_button.disabled = False
                    view.cur_page = 0
                    view.back_button.disabled = True

                    if view.extra_buttons is not None:
                        view.clear_items()
                        for _ in view.extra_buttons[view.cur_page]: view.add_item(_)
                        [view.add_item(i) for i in [view.back_button, view.next_button]]
                        if view.skip_buttons: [view.add_item(i) for i in [view.skip_start_button, view.skip_end_button]]
                        if view.close_button: view.add_item(view.deter_button)
                    res = check_emb_content_view(view)

                    await view.message.edit(view=view, embed=res[0], content=res[1])
                    await interaction.response.defer()

            async def skip_end_callback(interaction):
                if check(interaction, view):
                    view.skip_end_button.disabled = True
                    view.skip_start_button.disabled = False

                    view.next_button.disabled = True
                    view.cur_page = len(view.embeds) - 1 if view.embeds else len(view.content) - 1
                    view.back_button.disabled = False

                    if view.extra_buttons is not None:
                        view.clear_items()
                        for _ in view.extra_buttons[view.cur_page]: view.add_item(_)
                        [view.add_item(i) for i in [view.back_button, view.next_button]]
                        if view.skip_buttons: [view.add_item(i) for i in [view.skip_start_button, view.skip_end_button]]
                        if view.close_button: view.add_item(view.deter_button)

                    res = check_emb_content_view(view)

                    await view.message.edit(view=view, embed=res[0], content=res[1])
                    await interaction.response.defer()

            async def close_callback(interaction):
                if check(interaction, view):
                    try:
                        await view.message.delete()
                    except discord.errors.NotFound:
                        print("[ERROR] Seems like your message ephemeral or posted before latest bot restart")
                    except Exception as e:
                        raise e

            async def on_timeout():
                if view.disable_on_timeout:
                    try:
                        view.disable_all_items()
                        await view.message.edit(view=view)
                    except: pass
                if view.delete_on_timeout:
                    try: await view.message.delete()
                    except: pass
                try: view.stop()
                except discord.errors.NotFound: pass

            view.back_button.callback = back_callback
            view.next_button.callback = next_callback
            view.deter_button.callback = close_callback
            view.skip_end_button.callback = skip_end_callback
            view.skip_start_button.callback = skip_start_callback
            view.on_timeout = on_timeout
            view.skip_start_button.disabled = True
            res = check_emb_content_view(view)

            if type == 'slash':
                await view.ctx.respond(view=view, embed=res[0], content=res[1], ephemeral=ephemeral)
            elif type == 'interaction':
                view.ctx = interact
                await interact.response.send_message(view=view, embed=res[0], content=res[1], ephemeral=ephemeral)
            elif type == 'text':
                await view.ctx.send(view=view, embed=res[0], content=res[1])

            view.back_button.disabled = True
            if isinstance(view.ctx, discord.Interaction):
                message = view.message
            else:
                message = await view.ctx.fetch_message(view.message.id)

            view.message = message
            await view.message.edit(view=view, embed=res[0], content=res[1])

        except TimeoutError:
            pass
