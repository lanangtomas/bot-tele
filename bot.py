from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# Masukkan token API dari BotFather
TOKEN = "7535835081:AAEO2BcKXa5b8QjNst3ReqGnBt4gTOTEpS8"
IPINFO_API_KEY = "1086a40120b0d3"
WHOIS_API_URL = "https://api.api-ninjas.com/v1/whois?domain="
WHATSMYNAME_API_URL = "https://whatsmyname.app/api/v1/lookup?username="  # API untuk cek username

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Halo! Saya adalah bot OSINT.\nGunakan /help untuk melihat fitur.")

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🔹 **Daftar Perintah** 🔹\n"
        "/start - Memulai bot\n"
        "/help - Menampilkan bantuan\n"
        "/ip <alamat_ip> - Cek informasi IP\n"
        "/whois <domain> - Cek informasi domain\n"
        "/username <nama> - Cek username di berbagai platform\n"
    )

async def ip_lookup(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Gunakan format: /ip <alamat_ip>")
        return

    ip = context.args[0]
    response = requests.get(f"https://ipinfo.io/{ip}/json?token={IPINFO_API_KEY}").json()

    if "bogon" in response:
        await update.message.reply_text("IP ini tidak valid atau termasuk IP lokal.")
        return

    info = f"🔍 **Hasil Pencarian IP {ip}:**\n" \
           f"- **Negara:** {response.get('country', 'Tidak Diketahui')}\n" \
           f"- **Kota:** {response.get('city', 'Tidak Diketahui')}\n" \
           f"- **Provider:** {response.get('org', 'Tidak Diketahui')}\n" \
           f"- **Koordinat:** {response.get('loc', 'Tidak Diketahui')}"
    await update.message.reply_text(info)

async def whois_lookup(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Gunakan format: /whois <domain>")
        return

    domain = context.args[0]
    headers = {"X-Api-Key": "7p57NGPrQqeXYmA6IoHMAg==JgkOQoyTJIhhriOb"}
    response = requests.get(WHOIS_API_URL + domain, headers=headers)

    if response.status_code != 200:
        await update.message.reply_text(f"⚠️ Whois data untuk {domain} tidak ditemukan atau API bermasalah.")
        return

    data = response.json()
    info = f"🔍 **WHOIS {domain}:**\n" \
           f"- **Pendaftar:** {data.get('registrant', 'Tidak Diketahui')}\n" \
           f"- **Organisasi:** {data.get('org', 'Tidak Diketahui')}\n" \
           f"- **Negara:** {data.get('country', 'Tidak Diketahui')}\n" \
           f"- **Dibuat:** {data.get('creation_date', 'Tidak Diketahui')}\n" \
           f"- **Berakhir:** {data.get('expiration_date', 'Tidak Diketahui')}"
    await update.message.reply_text(info)

async def username_lookup(update: Update, context: CallbackContext) -> None:
    if not context.args:
        await update.message.reply_text("Gunakan format: /username <nama>")
        return

    username = context.args[0]
    response = requests.get(WHATSMYNAME_API_URL + username)

    if response.status_code != 200:
        await update.message.reply_text(f"⚠️ Data untuk username @{username} tidak ditemukan atau API bermasalah.")
        return

    data = response.json()
    accounts = data.get("accounts", [])

    if not accounts:
        await update.message.reply_text(f"❌ Username @{username} tidak ditemukan di platform mana pun.")
    else:
        result = f"🔍 **Hasil Pencarian Username @{username}:**\n"
        for account in accounts[:10]:  # Ambil maksimal 10 hasil untuk tampilan rapi
            result += f"- [{account['site']}]({account['url']})\n"

        await update.message.reply_text(result, parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ip", ip_lookup))
    app.add_handler(CommandHandler("whois", whois_lookup))
    app.add_handler(CommandHandler("username", username_lookup))

    print("Bot sedang berjalan...")
    app.run_polling()

if __name__ == '__main__':
    main()
