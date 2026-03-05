"""
Bybit P2P Telegram Bot
Monitors Bybit P2P advertisements for PKR and sends alerts when:
  - Buy ads are posted below a configurable price threshold (default 285 PKR)
  - Sell ads are posted above a configurable price threshold (default 295 PKR)
  - Any ad description contains phone numbers or third-party references
"""

import asyncio
import logging
import os
import re
import sys

from dotenv import load_dotenv
from telegram import Bot
from telegram.constants import ParseMode

from bybit_p2p import P2P

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "")
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "60"))
BUY_PRICE_THRESHOLD = float(os.getenv("BUY_PRICE_THRESHOLD", "285"))
SELL_PRICE_THRESHOLD = float(os.getenv("SELL_PRICE_THRESHOLD", "295"))

TOKEN_ID = "USDT"
CURRENCY_ID = "PKR"
PAGE_SIZE = 20  # ads per page to fetch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Detection helpers
# ---------------------------------------------------------------------------

# Common phone number patterns (international & Pakistani formats)
PHONE_PATTERN = re.compile(
    r"(?:\+?\d{1,3}[\s\-]?)?"     # optional country code
    r"(?:\(?\d{2,5}\)?[\s\-]?)?"  # optional area code
    r"\d{4,}[\s\-]?\d{3,}",       # main number
)

# Keywords that suggest third-party / off-platform trading
THIRD_PARTY_KEYWORDS = [
    "whatsapp", "telegram", "signal", "viber", "imo",
    "wechat", "facebook", "messenger", "instagram",
    "call me", "contact me", "dm me", "text me",
    "off platform", "outside bybit", "direct deal",
    "binance", "okx", "kucoin", "htx", "gate.io",
    "jazzcash", "easypaisa", "bank transfer outside",
    "western union", "moneygram",
]


def detect_phone_numbers(text: str) -> list[str]:
    """Return all phone-number-like strings found in *text*."""
    return PHONE_PATTERN.findall(text)


def detect_third_party(text: str) -> list[str]:
    """Return third-party keywords found in *text*."""
    lower = text.lower()
    return [kw for kw in THIRD_PARTY_KEYWORDS if kw in lower]


def escape_md(text: str) -> str:
    """Escape MarkdownV2 special characters."""
    special = r"_*[]()~`>#+-=|{}.!\\"
    return re.sub(f"([{re.escape(special)}])", r"\\\1", text)

# ---------------------------------------------------------------------------
# Ad processing
# ---------------------------------------------------------------------------

def build_profile_url(user_id: str) -> str:
    """Build the Bybit P2P profile URL for a user."""
    return f"https://www.bybit.com/fiat/trade/otc/profile/{user_id}/USDT/PKR"


def process_ads(ads: list[dict], side: str) -> list[dict]:
    """
    Filter and enrich ads that match our alert criteria.

    *side* is "buy" or "sell" — determines which price threshold to apply.
    Returns a list of dicts with alert information.
    """
    alerts: list[dict] = []

    for ad in ads:
        price = float(ad.get("price", 0))
        nick = ad.get("nickName", "Unknown")
        user_id = ad.get("userId", "")
        remark = ad.get("remark", "") or ""
        min_amount = ad.get("minAmount", "?")
        max_amount = ad.get("maxAmount", "?")
        quantity = ad.get("lastQuantity", ad.get("quantity", "?"))
        payments = ad.get("payments", [])
        payment_names = ", ".join(
            p.get("paymentName", p.get("paymentType", "")) for p in payments
        ) if payments else "N/A"

        reasons: list[str] = []

        # Price threshold check
        if side == "buy" and price < BUY_PRICE_THRESHOLD:
            reasons.append(f"Buy price {price:.2f} PKR < {BUY_PRICE_THRESHOLD}")
        elif side == "sell" and price > SELL_PRICE_THRESHOLD:
            reasons.append(f"Sell price {price:.2f} PKR > {SELL_PRICE_THRESHOLD}")

        # Description scanning
        phones = detect_phone_numbers(remark)
        if phones:
            reasons.append(f"Phone number(s): {', '.join(phones)}")

        third_party = detect_third_party(remark)
        if third_party:
            reasons.append(f"Third-party mention: {', '.join(third_party)}")

        if reasons:
            alerts.append({
                "nick": nick,
                "user_id": user_id,
                "price": price,
                "side": side.upper(),
                "min_amount": min_amount,
                "max_amount": max_amount,
                "quantity": quantity,
                "payment_methods": payment_names,
                "remark": remark,
                "reasons": reasons,
                "profile_url": build_profile_url(user_id),
            })

    return alerts


def format_alert(alert: dict) -> str:
    """Format a single alert as a Telegram MarkdownV2 message."""
    reasons_text = "\n".join(f"  • {escape_md(r)}" for r in alert["reasons"])
    remark_preview = alert["remark"][:200]
    if len(alert["remark"]) > 200:
        remark_preview += "..."

    msg = (
        f"{'🔴' if alert['side'] == 'BUY' else '🟢'} *{escape_md(alert['side'])} AD ALERT*\n"
        f"\n"
        f"👤 *User:* {escape_md(alert['nick'])}\n"
        f"💰 *Price:* {escape_md(f'{alert[\"price\"]:.2f}')} PKR\n"
        f"📊 *Range:* {escape_md(str(alert['min_amount']))} \\- {escape_md(str(alert['max_amount']))} PKR\n"
        f"🪙 *Available:* {escape_md(str(alert['quantity']))} USDT\n"
        f"💳 *Payment:* {escape_md(alert['payment_methods'])}\n"
        f"\n"
        f"⚠️ *Reasons:*\n{reasons_text}\n"
        f"\n"
        f"📝 *Description:*\n{escape_md(remark_preview)}\n"
        f"\n"
        f"🔗 [View Profile]({alert['profile_url']})"
    )
    return msg

# ---------------------------------------------------------------------------
# Scanning loop
# ---------------------------------------------------------------------------

async def scan_and_notify(api: P2P, bot: Bot):
    """Run one scan cycle: fetch ads, check thresholds, send alerts."""
    all_alerts: list[dict] = []

    for side_code, side_label in [("0", "buy"), ("1", "sell")]:
        try:
            page = 1
            while True:
                resp = api.get_online_ads(
                    tokenId=TOKEN_ID,
                    currencyId=CURRENCY_ID,
                    side=side_code,
                    page=page,
                    size=PAGE_SIZE,
                )
                items = resp.get("result", {}).get("items", [])
                if not items:
                    break

                alerts = process_ads(items, side_label)
                all_alerts.extend(alerts)

                # If fewer results than page size, we've reached the last page
                if len(items) < PAGE_SIZE:
                    break
                page += 1

                # Safety limit to avoid infinite loops
                if page > 10:
                    break

        except Exception:
            logger.exception("Error fetching %s ads", side_label)

    if not all_alerts:
        logger.info("No alerts this cycle.")
        return

    logger.info("Sending %d alert(s)…", len(all_alerts))
    for alert in all_alerts:
        try:
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=format_alert(alert),
                parse_mode=ParseMode.MARKDOWN_V2,
                disable_web_page_preview=True,
            )
            # Small delay between messages to respect Telegram rate limits
            await asyncio.sleep(0.5)
        except Exception:
            logger.exception("Failed to send alert for user %s", alert["nick"])


async def main():
    # Validate config
    missing = []
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if not BYBIT_API_KEY:
        missing.append("BYBIT_API_KEY")
    if not BYBIT_API_SECRET:
        missing.append("BYBIT_API_SECRET")
    if missing:
        logger.error("Missing required environment variables: %s", ", ".join(missing))
        logger.error("Copy .env.example to .env and fill in your credentials.")
        sys.exit(1)

    api = P2P(
        testnet=False,
        api_key=BYBIT_API_KEY,
        api_secret=BYBIT_API_SECRET,
    )
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    logger.info("Bot started. Scanning every %d seconds.", SCAN_INTERVAL)
    logger.info(
        "Buy threshold: < %.2f PKR | Sell threshold: > %.2f PKR",
        BUY_PRICE_THRESHOLD,
        SELL_PRICE_THRESHOLD,
    )

    # Send startup message
    try:
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=(
                "✅ *Bybit P2P Monitor Started*\n\n"
                f"Token: USDT / PKR\n"
                f"Buy alert: below {BUY_PRICE_THRESHOLD} PKR\n"
                f"Sell alert: above {SELL_PRICE_THRESHOLD} PKR\n"
                f"Scan interval: {SCAN_INTERVAL}s\n\n"
                "Also scanning for phone numbers & third\\-party mentions\\."
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    except Exception:
        logger.exception("Failed to send startup message — check your bot token and chat ID")
        sys.exit(1)

    # Main loop
    while True:
        try:
            await scan_and_notify(api, bot)
        except Exception:
            logger.exception("Unexpected error in scan cycle")
        await asyncio.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
