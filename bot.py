import discord
from discord.ext import commands
from colorama import Fore, Style, init

# เริ่มต้น colorama สำหรับสีในคมด์
init(autoreset=True)

# ฟังก์ชั่นสำหรับแสดงข้อความสี
def log_info(message):
    print(f"{Fore.CYAN}[INFO    ]{Style.RESET_ALL} {message}")

def log_success(message):
    print(f"{Fore.GREEN}[SUCCESS    ]{Style.RESET_ALL} {message}")

def log_error(message):
    print(f"{Fore.RED}[ERROR    ]{Style.RESET_ALL} {message}")

def log_warning(message):
    print(f"{Fore.YELLOW}[WARNING    ]{Style.RESET_ALL} {message}")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix=".", intents=intents)

# 👉 ใส่ ID ต่าง ๆ
ROLE_ID = 1490746146140721305   # ID ยศ
CHANNEL_ID = 1486454600272973905  # ห้องให้ส่งข้อความ 
VOICE_CHANNEL_ID = 1486383085686882498  # ID ห้องเสียง (แก้ไขให้ถูกต้อง)

class RoleButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="รับยศ ⭐", style=discord.ButtonStyle.primary, custom_id="get_role")
    async def get_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(ROLE_ID)

        if role in interaction.user.roles:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description="คุณมียศนี้อยู่แล้ว!\n\n**‧ ˚₊꒷꒦︶︶︶꒷꒦︶︶︶︶︶︶꒷꒦︶︶𓈒⁺꒷︶ .˚₊ **",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.add_roles(role)

            embed = discord.Embed(
                title="✅ สำเร็จ!",
                description=f"คุณได้รับยศ {role.name} แล้ว!\n\n**‧ ˚₊꒷꒦︶︶︶꒷꒦︶︶︶︶︶︶꒷꒦︶︶𓈒⁺꒷︶ .˚₊ **",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # แจ้งเตือนไปยังห้องโดยแท็กชื่อคนที่กด
            channel = bot.get_channel(1493616390576275617)
            if channel:
                embed_announce = discord.Embed(
                    title="✅ ได้รับยศสำเร็จ!",
                    description=f"{interaction.user.mention} ได้รับยศ {role.name} แล้ว!\n\n**‧ ˚₊꒷꒦︶︶︶꒷꒦︶︶︶︶︶︶꒷꒦︶︶𓈒⁺꒷︶ .˚₊ **",
                    color=discord.Color.green()
                )
                embed_announce.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed_announce.set_thumbnail(url=interaction.user.display_avatar.url)
                await channel.send(embed=embed_announce)

    @discord.ui.button(label="เอายศออก ✖️", style=discord.ButtonStyle.danger, custom_id="remove_role")
    async def remove_role(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(ROLE_ID)

        if role not in interaction.user.roles:
            embed = discord.Embed(
                title="❌ ข้อผิดพลาด",
                description="คุณไม่มียศนี้จึงไม่สามารถเอาออกได้!\n\n**‧ ˚₊꒷꒦︶︶︶꒷꒦︶︶︶︶︶︶꒷꒦︶︶𓈒⁺꒷︶ .˚₊ **",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.user.remove_roles(role)

            embed = discord.Embed(
                title="✅ สำเร็จ!",
                description=f"คุณได้เอายศ {role.name} ออกแล้ว!\n\n**‧ ˚₊꒷꒦︶︶︶꒷꒦︶︶︶︶︶︶꒷꒦︶︶𓈒⁺꒷︶ .˚₊ **",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # แจ้งเตือนไปยังห้องโดยแท็กชื่อคนที่กด
            channel = bot.get_channel(1493616786254336140)
            if channel:
                embed_announce = discord.Embed(
                    title="✅ เอายศออกสำเร็จ!",
                    description=f"{interaction.user.mention} ได้เอายศ {role.name} ออกแล้ว!\n\n**‧ ˚₊꒷꒦︶︶︶꒷꒦︶︶︶︶︶︶꒷꒦︶︶⁺꒷︶ .˚₊ **",
                    color=discord.Color.green()
                )
                embed_announce.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar.url)
                embed_announce.set_thumbnail(url=interaction.user.display_avatar.url)
                await channel.send(embed=embed_announce)

@bot.event
async def on_ready():
    log_success(f"บอทออนไลน์แล้ว: {bot.user}")
    bot.add_view(RoleButton())  # สำคัญมาก (ให้ปุ่มใช้ได้ตลอด)
    
    # เข้าห้องเสียงโดยอัตโนมัติ
    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        try:
            await voice_channel.connect()
            log_info(f"บอทเข้าห้องเสียง: {voice_channel.name}")
        except Exception as e:
            log_error(f"ไม่สามารถเข้าห้องเสียง: {e}")

@bot.command()
async def op(ctx):
    embed = discord.Embed(
        title="🎉  กดปุ่มเพื่อรับยศ!",
        description="```กดอีโมจิ ⭐ เพื่อเข้าสู่เซิร์ฟเวอร์ของเราได้เลย!```\n\n**‧ ˚₊꒷꒦︶︶︶꒷꒦︶︶︶︶︶︶︶︶︶꒷꒦︶︶𓈒⁺꒷︶ .˚₊ **",
        color=discord.Color.blue()
    )


    # embed.add_field(name="google", value="```google``` = \"[กดตรงนี้](https://google.com)\"", inline=False)
    # embed.add_field(name="Desktop", value="```Desktop``` = \"[กดตรงนี้](https://example.com)\"", inline=True)


    #👉 รูปเล็กมุมขวาบน
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1390975145723826208/1490751682647429352/2022-10-10-10-14-47-932.jpg?ex=69d53231&is=69d3e0b1&hm=573f245549fa4494509f4ea5a03d0033c1a2e42fcb88281b93814a6beb74b68b&")
    
    #👉 รูป Banner (รูปใหญ่)
    embed.set_image(url="https://cdn.discordapp.com/attachments/1390975145723826208/1490751682110427236/pngtree-stars-filled-space-background-image_356736.jpg?ex=69d53231&is=69d3e0b1&hm=9307d05ccd9691b59c76b93810b68e598a875f18d9534f480314fa83723a6cfd&")

    #👉 รูปล่าง (ข้างข้อความ footer)
    embed.set_footer(
        text="กดรับยศได้เลย!",
        icon_url="https://cdn.discordapp.com/attachments/1390975145723826208/1490752114274603172/30a1cc321269fc9c.jpg?ex=69d53298&is=69d3e118&hm=96a261fb4c30eeb56dd0f0280f65c71b8725e6fadca50cd8585942d599642c08&"
    )

    await ctx.send(embed=embed, view=RoleButton())

bot.run("MTQ5MDM4MzE3NzE5MjMwODg3Nw.Gl4QxY.FnE96580jXzmnp91-X2NMqITbbucEtuIchDxM0")