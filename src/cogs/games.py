from typing import List
from discord.ext import commands
import discord
import random


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state != 0:
            return

        if view.current_player == "X":
            if interaction.user != view.players[0]:
                return
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = "X"
            view.current_player = "O"
            content = f"It is now **{view.players[1].name}**'s turn"
        else:
            if interaction.user != view.players[1]:
                return
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = "O"
            view.current_player = "X"
            content = f"It is now **{view.players[0].name}**'s turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == "tie":
                content = "It's a tie!"
            else:
                content = f"**{winner.name}** won!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    current_player = "X"

    def __init__(self, players):
        super().__init__()
        self.players = players
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):
        for across in self.board:
            if across.count("X") == 3:
                return self.players[0]
            elif across.count("O") == 3:
                return self.players[1]

        for line in range(3):
            if self.board[0][line] == self.board[1][line] == self.board[2][line]:
                if self.board[0][line] == "X":
                    return self.players[0]
                elif self.board[0][line] == "O":
                    return self.players[1]

        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            if self.board[0][2] == "X":
                return self.players[0]
            elif self.board[0][2] == "O":
                return self.players[1]

        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            if self.board[0][0] == "X":
                return self.players[0]
            elif self.board[0][0] == "O":
                return self.players[1]

        t = []
        for line in self.board:
            t += line
        if 0 not in t:
            return "tie"

        return None


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = "🎮"

    @commands.command(aliases=["tic"])
    @commands.guild_only()
    async def tictactoe(self, ctx, member: discord.Member):
        players = [ctx.author, member]
        random.shuffle(players)
        await ctx.send(f"Tic Tac Toe: **{players[0].name}** goes first",
                       view=TicTacToe(players))


async def setup(bot):
    await bot.add_cog(Games(bot))
