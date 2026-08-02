import os
import discord
from discord.ext import commands
from datetime import timedelta

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="⚽ تنظيم مباريات كرة القدم"))

WELCOME_CHANNEL_ID = 1533462690595606583 
GOODBYE_CHANNEL_ID = 1533462691933585530 

@bot.event
async def on_member_join(member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="👋 لاعب جديد انضم للفريق!",
            description=f"أهلاً بك يا {member.mention} في سيرفر الفريق! ⚽\nنتمنى لك وقتاً ممتعاً معنا.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"العضو رقم: {member.guild.member_count}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(GOODBYE_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🚶‍♂️ غادر الفريق",
            description=f"اللاعب **{member.name}** غادر السيرفر. نراك لاحقاً!",
            color=discord.Color.red()
        )
        await channel.send(embed=embed)

@bot.command(name="مباراة")
async def next_match(ctx):
    embed = discord.Embed(
        title="⚽ موعد المباراة القادمة",
        description="استعدوا يا شباب للمواجهة القادمة!",
        color=discord.Color.green()
    )
    embed.add_field(name="📅 التاريخ", value="يوم الأربعاء القادم", inline=True)
    embed.add_field(name="⏰ التوقيت", value="20:00 مساءً", inline=True)
    embed.add_field(name="🏟️ الملعب", value="الملعب الرئيسي", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban_member(ctx, member: discord.Member, *, reason="لم يُذكر سبب"):
    await member.ban(reason=reason)
    embed = discord.Embed(
        title="🔨 تم حظر اللاعب",
        description=f"تم حظر **{member.mention}** من السيرفر بنجاح.",
        color=discord.Color.dark_red()
    )
    embed.add_field(name="السبب", value=reason, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout_member(ctx, member: discord.Member, minutes: int, *, reason="بدون سبب"):
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    
    embed = discord.Embed(
        title="⏳ تم إعطاء Timeout للاعب",
        description=f"تم إسكات **{member.mention}** لمدة **{minutes} دقيقة**.",
        color=discord.Color.orange()
    )
    embed.add_field(name="السبب", value=reason, inline=False)
    await ctx.send(embed=embed)

@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, amount: int = 5):
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 تم حذف **{len(deleted) - 1}** رسالة بنجاح.")
    await msg.delete(delay=3)

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    
    embed = discord.Embed(
        title="🔒 تم إغلاق القناة",
        description=f"تم قفل القناة {channel.mention} بنجاح. لا يمكن للأعضاء الكتابة فيها حالياً.",
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
async def unlock_channel(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    
    embed = discord.Embed(
        title="🔓 تم فتح القناة",
        description=f"تم فتح القناة {channel.mention} بنجاح. يمكن للأعضاء التحدث الآن.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ عذراً، لا تمتلك الصلاحية الكافية لتنفيذ هذا الأمر.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ عذراً، لقد نسيت كتابة بعض المعلومات المطلوبة لتنفيذ الأمر.")

bot.run(TOKEN)
