
import discord
from discord.ext import commands
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# نظام النقاط (Coins) - تحميل أو إنشاء ملف بيانات
if os.path.exists("coins.json"):
    with open("coins.json", "r", encoding="utf-8") as f:
        coins = json.load(f)
else:
    coins = {}

# تحديث ملف النقاط
def save_coins():
    with open("coins.json", "w", encoding="utf-8") as f:
        json.dump(coins, f, ensure_ascii=False, indent=4)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول باسم {bot.user}")

# الحصول على رصيد المستخدم
@bot.command(name="رصيد")
async def balance(ctx):
    user_id = str(ctx.author.id)
    if user_id not in coins:
        coins[user_id] = 0
        save_coins()
    await ctx.send(f"رصيدك الحالي: {coins[user_id]} نقطة.")

# لعبة حجر ورقة مقص
@bot.command(name="حجر_ورقة_مقص")
async def rps(ctx, اختيار: str):
    الخيارات = ["حجر", "ورقة", "مقص"]
    اختيار_البوت = random.choice(الخيارات)
    user_id = str(ctx.author.id)

    if user_id not in coins:
        coins[user_id] = 0

    if اختيار not in الخيارات:
        await ctx.send("يرجى اختيار: حجر، ورقة، أو مقص.")
        return

    if اختيار == اختيار_البوت:
        النتيجة = "تعادل!"
    elif (اختيار == "حجر" and اختيار_البوت == "مقص") or (اختيار == "ورقة" and اختيار_البوت == "حجر") or (اختيار == "مقص" and اختيار_البوت == "ورقة"):
        النتيجة = "لقد فزت! وحصلت على 10 نقاط."
        coins[user_id] += 10
    else:
        النتيجة = "لقد خسرت!"
    
    save_coins()
    await ctx.send(f"أنت اخترت: {اختيار} | البوت اختار: {اختيار_البوت} | {النتيجة}")

# المتجر
items = {
    "تاج": 50,
    "سيف": 100,
    "درع": 150
}

@bot.command(name="متجر")
async def shop(ctx):
    msg = "🛒 **المتجر:**
"
    for item, price in items.items():
        msg += f"{item}: {price} نقطة.
"
    await ctx.send(msg)

@bot.command(name="شراء")
async def buy(ctx, *, item_name: str):
    user_id = str(ctx.author.id)

    if user_id not in coins:
        coins[user_id] = 0

    if item_name not in items:
        await ctx.send("هذا العنصر غير موجود في المتجر!")
        return

    cost = items[item_name]

    if coins[user_id] >= cost:
        coins[user_id] -= cost
        save_coins()
        await ctx.send(f"لقد اشتريت {item_name} مقابل {cost} نقطة!")
    else:
        await ctx.send("ليس لديك نقاط كافية للشراء!")

# تشغيل البوت
bot.run("YOUR_BOT_TOKEN")
