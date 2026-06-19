"""
handlers/books.py  –  Free & Premium Books
"""
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.menus import back_button

BOOKS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "books.json")
BOOKS = []

def load_books():
    global BOOKS
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            BOOKS = data.get("books", [])
    except Exception:
        BOOKS = []

load_books()


async def books_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main books menu."""
    query = update.callback_query
    free_count = sum(1 for b in BOOKS if b.get("type") == "free")
    prem_count = sum(1 for b in BOOKS if b.get("type") == "premium")

    text = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "  📚 𝐁𝐎𝐎𝐊𝐒 — 𝐀𝐊𝐇𝐑𝐈𝐒𝐎 𝐁𝐀𝐑𝐎\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📗 *Free Books* ({free_count}) — Dhammaan FREE\n"
        "📖 ChatGPT, AI, Chatbots, n8n, Video\n\n"
        f"👑 *Premium Books* ({prem_count}) — Heer sare\n"
        "📖 WhatsApp API, CRM, Mastery Bundle\n\n"
        "👇 *Xulo qaybta:*"
    )

    btns = [
        [InlineKeyboardButton(f"📗 Free Books ({free_count})", callback_data="books_free")],
        [InlineKeyboardButton(f"👑 Premium Books ({prem_count})", callback_data="books_premium")],
        [InlineKeyboardButton("🔍 Search Books", callback_data="books_search")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="menu_main")],
    ]

    if query:
        await query.answer()
        await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(btns))
    else:
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(btns))


async def books_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show books by type (free/premium)."""
    query = update.callback_query
    await query.answer()
    btype = "free" if "free" in query.data else "premium"
    label = "📗 Free Books" if btype == "free" else "👑 Premium Books"

    filtered = [b for b in BOOKS if b.get("type") == btype]
    if not filtered:
        await query.edit_message_text(f"❌ {label} ma jiraan.", reply_markup=back_button("menu_books"))
        return

    text = f"━━━━━━━━━━━━━━━━━━━━━━\n  {label}\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    btns = []
    for b in filtered:
        emoji = b.get("emoji", "📖")
        title = b.get("title", "Book")
        pages = b.get("pages", "?")
        text += f"{emoji} *{title}*\n   📄 {pages} pages\n\n"
        btns.append([InlineKeyboardButton(f"{emoji} {title[:30]}", callback_data=f"book_view_{b['id']}")])

    btns.append([InlineKeyboardButton("🔙 Books Menu", callback_data="menu_books")])
    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(btns))


async def book_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show single book details."""
    query = update.callback_query
    await query.answer()
    try:
        book_id = int(query.data.split("_")[2])
    except (IndexError, ValueError):
        await query.edit_message_text("❌ Book not found.", reply_markup=back_button("menu_books"))
        return

    book = next((b for b in BOOKS if b["id"] == book_id), None)
    if not book:
        await query.edit_message_text("❌ Book not found.", reply_markup=back_button("menu_books"))
        return

    emoji = book.get("emoji", "📖")
    price = book.get("price", "FREE")
    btype = book.get("type", "free")
    label = "📗 FREE" if btype == "free" else f"👑 {price}"

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"  {emoji} {book['title']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"✍️ *Author:* {book.get('author', 'Mfaratoon')}\n"
        f"📄 *Pages:* {book.get('pages', '?')}\n"
        f"🌍 *Language:* {book.get('language', 'Somali')}\n"
        f"💰 *Price:* {label}\n\n"
        f"📖 *Description:*\n{book.get('description', '')}\n\n"
        f"🔗 [👉 Download / Read]({book.get('file_url', '#')})"
    )

    btns = [
        [InlineKeyboardButton("📥 Download", url=book.get("file_url", "#"))],
        [InlineKeyboardButton("🔙 Back to List", callback_data=f"books_{btype}")],
        [InlineKeyboardButton("🔙 Books Menu", callback_data="menu_books")],
    ]

    await query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=False, reply_markup=InlineKeyboardMarkup(btns))


async def books_search_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ask user for search query."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(
            "🔍 *Search Books*\n\n"
            "Erayga aad raadinayso qor:\n"
            "💡 Tusaale: `AI`, `Chatbot`, `n8n`, `WhatsApp`\n\n"
            "Erayga hoos ku qor 👇",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Cancel", callback_data="menu_books")]
            ])
        )
    context.user_data["awaiting_book_search"] = True


async def books_search_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle search results."""
    query_text = update.message.text.lower()
    matches = [b for b in BOOKS if query_text in b.get("title", "").lower() or query_text in b.get("description", "").lower()]

    if not matches:
        await update.message.reply_text(
            f"❌ Waxba looma helin '{query_text}'.",
            reply_markup=back_button("menu_books")
        )
        return

    text = f"🔍 *Results for '{query_text}'* ({len(matches)} found)\n\n"
    btns = []
    for b in matches:
        emoji = b.get("emoji", "📖")
        text += f"{emoji} *{b['title']}* — {b.get('type', 'free').upper()}\n"
        btns.append([InlineKeyboardButton(f"{emoji} {b['title'][:30]}", callback_data=f"book_view_{b['id']}")])

    btns.append([InlineKeyboardButton("🔙 Books Menu", callback_data="menu_books")])
    await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=InlineKeyboardMarkup(btns))
