"""
WashGo Investor Pitch Deck — PDF Generator
Run: python generate_pitch_pdf.py
Output: washgo_pitch_deck.pdf
"""

import io
import math
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, Image as RLImage,
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas as pdf_canvas
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Brand colors ───────────────────────────────────────────────────────────────
PRIMARY   = HexColor("#2E7D32")
PRIMARY_L = HexColor("#E8F5E9")
ACCENT    = HexColor("#FF6F00")
ACCENT_L  = HexColor("#FFF3E0")
DARK      = HexColor("#1A237E")
DARK_L    = HexColor("#E8EAF6")
RED_L     = HexColor("#FFEBEE")
RED       = HexColor("#B71C1C")
GRAY      = HexColor("#6B7280")
LGRAY     = HexColor("#F9FAFB")
BORDER    = HexColor("#E5E7EB")
TEAL      = HexColor("#00838F")
PURPLE    = HexColor("#7B1FA2")

PAGE_W, PAGE_H = landscape(A4)  # 842 x 595 pt

# ── Matplotlib chart helpers ───────────────────────────────────────────────────

def fig_to_image(fig, width_cm=22, height_cm=9):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor="none", transparent=True)
    plt.close(fig)
    buf.seek(0)
    return RLImage(buf, width=width_cm * cm, height=height_cm * cm)


def make_roadmap_chart():
    quarters = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"]
    targets  = [100, 500, 2000, 5000]
    colors   = ["#2E7D32", "#1565C0", "#FF6F00", "#1A237E"]

    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(quarters, targets, color=colors, width=0.5, zorder=3)
    ax.set_title("Orders per Month — Growth Roadmap", fontsize=13, color="#1A237E",
                 fontweight="bold", pad=10)
    ax.set_ylabel("Orders / Month", fontsize=10, color="#6B7280")
    ax.yaxis.grid(True, color="#F0F0F0", zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#E0E0E0")
    ax.spines["bottom"].set_color("#E0E0E0")
    for bar, val in zip(bars, targets):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 80,
                f"{val:,}/mo", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color="#374151")
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    return fig_to_image(fig, width_cm=16, height_cm=7)


def make_revenue_chart():
    months = list(range(1, 19))
    month_labels = [f"M{m}" for m in months]

    orders = [50]
    for m in range(1, 18):
        rate = 0.30 if m < 6 else (0.20 if m < 12 else 0.15)
        orders.append(round(orders[-1] * (1 + rate)))

    revenues, costs = [], []
    for i, o in enumerate(orders):
        subs       = max(0, round(o * 0.03 * (i + 1) * 0.15))
        rev        = round(o * 380 * 0.25) + round(o * 49) + round(subs * 1500)
        cost       = round(o * 85) + 120000
        revenues.append(rev)
        costs.append(cost)

    x = np.arange(len(month_labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(x - w / 2, revenues, width=w, color="#2E7D32", alpha=0.9,
           label="Monthly Revenue", zorder=3)
    ax.bar(x + w / 2, costs,    width=w, color="#EF5350", alpha=0.85,
           label="Monthly Costs",   zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(month_labels, fontsize=8)
    ax.yaxis.grid(True, color="#F0F0F0", zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#E0E0E0")
    ax.spines["bottom"].set_color("#E0E0E0")
    ax.set_title("Revenue vs Costs — Month 1 to 18 (₹)", fontsize=13,
                 color="#1A237E", fontweight="bold", pad=10)
    ax.set_ylabel("Amount (₹)", fontsize=10, color="#6B7280")
    ax.legend(loc="upper left", fontsize=10)
    # Format y ticks
    ax.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f"₹{v/1e5:.1f}L" if v >= 1e5 else f"₹{int(v):,}")
    )
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    return fig_to_image(fig, width_cm=22, height_cm=8)


def make_donut_chart():
    labels = ["Tech & Product", "Operations", "Marketing", "Team", "Working Capital"]
    values = [37.5, 45, 37.5, 22.5, 7.5]
    colors = ["#2E7D32", "#1A237E", "#FF6F00", "#7B1FA2", "#00838F"]

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors,
        autopct="%1.0f%%", pctdistance=0.78,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2.5),
        startangle=90,
    )
    for t in texts:
        t.set_fontsize(8.5)
        t.set_fontweight("bold")
    for at in autotexts:
        at.set_fontsize(8)
        at.set_color("white")
        at.set_fontweight("bold")
    ax.text(0, 0, "₹1.5 Cr\nSeed", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#1A237E")
    fig.patch.set_alpha(0)
    return fig_to_image(fig, width_cm=9, height_cm=9)


# ── Custom canvas for top accent bar ──────────────────────────────────────────

class AccentCanvas:
    """Wraps a canvas to draw a multi-color accent bar + slide number on each page."""

    def __init__(self, filename):
        self.filename = filename

    def __call__(self, canv, doc):
        canv.saveState()
        # Gradient-like top bar (three segments)
        w = PAGE_W
        canv.setFillColor(PRIMARY);  canv.rect(0,       PAGE_H - 6, w * 0.4, 6, fill=1, stroke=0)
        canv.setFillColor(ACCENT);   canv.rect(w * 0.4, PAGE_H - 6, w * 0.3, 6, fill=1, stroke=0)
        canv.setFillColor(DARK);     canv.rect(w * 0.7, PAGE_H - 6, w * 0.3, 6, fill=1, stroke=0)
        # Footer
        canv.setFillColor(GRAY)
        canv.setFont("Helvetica", 7)
        canv.drawString(1.5 * cm, 0.7 * cm, "Confidential — WashGo Technologies Pvt. Ltd. · Hyderabad, 2025")
        canv.drawRightString(PAGE_W - 1.5 * cm, 0.7 * cm, f"Slide {doc.page}")
        canv.restoreState()


# ── Paragraph styles ───────────────────────────────────────────────────────────

def styles():
    base = dict(fontName="Helvetica", fontSize=10, leading=14, textColor=black)
    return {
        "slide_num": ParagraphStyle("slide_num", fontSize=8, fontName="Helvetica-Bold",
                                    textColor=GRAY, spaceAfter=4),
        "h1": ParagraphStyle("h1", fontSize=28, fontName="Helvetica-Bold",
                              textColor=DARK, leading=34, spaceAfter=4),
        "h1_green": ParagraphStyle("h1_green", fontSize=36, fontName="Helvetica-Bold",
                                   textColor=PRIMARY, leading=42),
        "h2": ParagraphStyle("h2", fontSize=18, fontName="Helvetica-Bold",
                              textColor=DARK, leading=24, spaceAfter=4),
        "subtitle": ParagraphStyle("subtitle", fontSize=10, fontName="Helvetica",
                                   textColor=GRAY, leading=15, spaceAfter=12),
        "body": ParagraphStyle("body", fontSize=9, fontName="Helvetica",
                               textColor=HexColor("#374151"), leading=14),
        "body_b": ParagraphStyle("body_b", fontSize=9, fontName="Helvetica-Bold",
                                 textColor=HexColor("#374151"), leading=14),
        "small": ParagraphStyle("small", fontSize=8, fontName="Helvetica",
                                textColor=GRAY, leading=12),
        "badge": ParagraphStyle("badge", fontSize=9, fontName="Helvetica-Bold",
                                textColor=PRIMARY, leading=12),
        "green": ParagraphStyle("green", fontSize=9, fontName="Helvetica-Bold",
                                textColor=PRIMARY, leading=14),
        "accent": ParagraphStyle("accent", fontSize=9, fontName="Helvetica-Bold",
                                 textColor=ACCENT, leading=14),
        "center": ParagraphStyle("center", fontSize=9, fontName="Helvetica",
                                 textColor=HexColor("#374151"), leading=14,
                                 alignment=TA_CENTER),
        "center_b": ParagraphStyle("center_b", fontSize=11, fontName="Helvetica-Bold",
                                   textColor=DARK, leading=16, alignment=TA_CENTER),
        "big_num": ParagraphStyle("big_num", fontSize=22, fontName="Helvetica-Bold",
                                  textColor=PRIMARY, leading=26, alignment=TA_CENTER),
        "ask_num": ParagraphStyle("ask_num", fontSize=32, fontName="Helvetica-Bold",
                                  textColor=ACCENT, leading=38, alignment=TA_CENTER),
    }

S = styles()

# ── Helpers ────────────────────────────────────────────────────────────────────

def slide_header(badge_text, title, subtitle=None):
    elems = [
        Paragraph(badge_text, S["slide_num"]),
        Paragraph(title, S["h1"]),
    ]
    if subtitle:
        elems.append(Paragraph(subtitle, S["subtitle"]))
    elems.append(HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=10))
    return elems


def colored_table(data, col_widths, header_bg=PRIMARY, row_alt=LGRAY):
    style = [
        ("BACKGROUND",  (0, 0), (-1, 0), header_bg),
        ("TEXTCOLOR",   (0, 0), (-1, 0), white),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 9),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, row_alt]),
        ("GRID",        (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
    ]
    return Table(data, colWidths=col_widths, style=TableStyle(style),
                 hAlign="LEFT")


def icon_row(icon, label, value, color=PRIMARY):
    data = [[Paragraph(f"{icon}  {label}", S["body"]),
             Paragraph(value, ParagraphStyle("v", fontSize=9, fontName="Helvetica-Bold",
                                             textColor=color, leading=14, alignment=TA_RIGHT))]]
    t = Table(data, colWidths=[13 * cm, 7 * cm],
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (-1, -1), LGRAY),
                  ("TOPPADDING", (0, 0), (-1, -1), 6),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                  ("LEFTPADDING", (0, 0), (-1, -1), 10),
                  ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                  ("LINEBELOW", (0, 0), (-1, -1), 0.5, BORDER),
              ]))
    return t


def card_table(rows_data, col_widths, bg=PRIMARY_L, border=HexColor("#C8E6C9")):
    style = [
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX",        (0, 0), (-1, -1), 1.5, border),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("ROUNDEDCORNERS", [8]),
    ]
    return Table(rows_data, colWidths=col_widths, style=TableStyle(style), hAlign="LEFT")


def spacer(h=0.3):
    return Spacer(1, h * cm)


# ── Slides ─────────────────────────────────────────────────────────────────────

def slide_1_cover():
    elems = []
    elems.append(spacer(0.8))
    elems.append(Paragraph("🧺 WashGo", S["h1_green"]))
    elems.append(spacer(0.3))
    elems.append(Paragraph("Hyderabad's On-Demand Laundry Platform",
                            ParagraphStyle("tag", fontSize=18, fontName="Helvetica-Bold",
                                           textColor=DARK, leading=22)))
    elems.append(spacer(0.4))

    badge_style = ParagraphStyle("bs", fontSize=11, fontName="Helvetica-Bold",
                                 textColor=ACCENT, leading=16,
                                 backColor=ACCENT_L, borderPadding=(5, 12, 5, 12))
    elems.append(Paragraph("Seed Round — ₹1.5 Crore", badge_style))
    elems.append(spacer(0.5))

    badges = [["🏙️ Hyderabad", "🧺 Laundry-Tech", "🌱 Seed Stage",
               "📅 2025", "🎯 ₹180 Cr SOM"]]
    bt = Table(badges, colWidths=[4 * cm] * 5,
               style=TableStyle([
                   ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_L),
                   ("TEXTCOLOR",  (0, 0), (-1, -1), PRIMARY),
                   ("FONTNAME",   (0, 0), (-1, -1), "Helvetica-Bold"),
                   ("FONTSIZE",   (0, 0), (-1, -1), 9),
                   ("BOX",        (0, 0), (-1, -1), 1.2, HexColor("#C8E6C9")),
                   ("INNERGRID",  (0, 0), (-1, -1), 0.5, white),
                   ("TOPPADDING", (0, 0), (-1, -1), 7),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                   ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
               ]))
    elems.append(bt)
    elems.append(spacer(0.6))
    elems.append(Paragraph(
        "Connecting Hyderabad's urban professionals with verified laundry facilities — "
        "scheduled pickups, real-time tracking, guaranteed delivery.",
        ParagraphStyle("cover_body", fontSize=11, fontName="Helvetica",
                       textColor=GRAY, leading=16)))
    return elems


def slide_2_problem():
    elems = slide_header("SLIDE 02 · THE PROBLEM", "The Problem",
                         "Laundry is one of the most time-consuming and unreliable household tasks for urban professionals.")
    data = [
        [Paragraph("⏰  No Time", S["h2"]),
         Paragraph("😤  Unreliable Dhobi", S["h2"]),
         Paragraph("🗺️  Inconvenient", S["h2"])],
        [Paragraph("Working professionals in Hyderabad spend <b>3–4 hours every week</b> on laundry — "
                   "washing, drying, folding, and ironing. That's 200+ hours a year lost to chores.", S["body"]),
         Paragraph("Traditional dhobis offer <b>inconsistent quality</b>, no order tracking, no service "
                   "guarantees, and frequent no-shows — leaving customers frustrated.", S["body"]),
         Paragraph("Laundromats require <b>travel, long queues, and cash payments</b>. "
                   "No pickup, no delivery, no way to plan around a busy schedule.", S["body"])],
    ]
    col_w = (PAGE_W - 3 * cm) / 3
    t = Table(data, colWidths=[col_w] * 3,
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (0, -1), RED_L),
                  ("BACKGROUND", (1, 0), (1, -1), ACCENT_L),
                  ("BACKGROUND", (2, 0), (2, -1), HexColor("#FBE9E7")),
                  ("BOX",        (0, 0), (0, -1), 1.5, HexColor("#EF9A9A")),
                  ("BOX",        (1, 0), (1, -1), 1.5, HexColor("#FFCC80")),
                  ("BOX",        (2, 0), (2, -1), 1.5, HexColor("#FFAB91")),
                  ("TOPPADDING", (0, 0), (-1, -1), 16),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
                  ("LEFTPADDING", (0, 0), (-1, -1), 14),
                  ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                  ("VALIGN",     (0, 0), (-1, -1), "TOP"),
                  ("LINEBELOW",  (0, 0), (-1, 0), 1, BORDER),
              ]))
    elems.append(t)
    return elems


def slide_3_solution():
    elems = slide_header("SLIDE 03 · THE SOLUTION", "The Solution",
                         "WashGo connects customers with verified laundry facilities — "
                         "scheduled pickups, real-time tracking, and guaranteed delivery.")
    features = [
        ("📱", "Schedule Pickup in 60 sec",
         "Book a slot, choose your service, and a partner arrives at your door."),
        ("🔍", "Real-Time Order Tracking",
         "Follow your laundry every step — from pickup to processing to delivery."),
        ("✅", "Quality-Guaranteed Delivery",
         "Every order is inspected before delivery. 100% satisfaction or we redo it."),
        ("💳", "Cashless Digital Payments",
         "UPI, cards, and wallets. No cash, no hassle, instant receipts."),
    ]
    col_w = (PAGE_W - 3 * cm) / 4
    header_row = [Paragraph(f"{icon}  {title}", S["badge"]) for icon, title, _ in features]
    body_row   = [Paragraph(desc, S["body"]) for _, _, desc in features]
    t = Table([header_row, body_row], colWidths=[col_w] * 4,
              style=TableStyle([
                  ("BACKGROUND",    (0, 0), (-1, -1), PRIMARY_L),
                  ("BOX",           (0, 0), (-1, -1), 1.5, HexColor("#C8E6C9")),
                  ("INNERGRID",     (0, 0), (-1, -1), 0.5, white),
                  ("TOPPADDING",    (0, 0), (-1, -1), 14),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                  ("LEFTPADDING",   (0, 0), (-1, -1), 12),
                  ("RIGHTPADDING",  (0, 0), (-1, -1), 12),
                  ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                  ("LINEBELOW",     (0, 0), (-1, 0), 1, HexColor("#C8E6C9")),
              ]))
    elems.append(t)
    return elems


def slide_4_market():
    elems = slide_header("SLIDE 04 · MARKET OPPORTUNITY", "Market Opportunity",
                         "India's laundry sector is vast and largely unorganised — ripe for tech-enabled disruption.")
    data_rows = [
        [Paragraph("TAM", S["center_b"]),
         Paragraph("SAM", S["center_b"]),
         Paragraph("SOM", S["center_b"])],
        [Paragraph("₹85,000 Cr", ParagraphStyle("tam", fontSize=22, fontName="Helvetica-Bold",
                                                textColor=DARK, alignment=TA_CENTER, leading=26)),
         Paragraph("₹4,200 Cr", ParagraphStyle("sam", fontSize=22, fontName="Helvetica-Bold",
                                               textColor=PRIMARY, alignment=TA_CENTER, leading=26)),
         Paragraph("₹180 Cr", ParagraphStyle("som", fontSize=22, fontName="Helvetica-Bold",
                                             textColor=ACCENT, alignment=TA_CENTER, leading=26))],
        [Paragraph("India Laundry Market\nTotal across all laundry services", S["center"]),
         Paragraph("Organised services\nin Tier-1 cities", S["center"]),
         Paragraph("Hyderabad Tech Corridor\nYear 3 target", S["center"])],
    ]
    col_w = (PAGE_W - 3 * cm) / 3
    t = Table(data_rows, colWidths=[col_w] * 3,
              style=TableStyle([
                  ("BACKGROUND", (0, 0), (0, -1), DARK_L),
                  ("BACKGROUND", (1, 0), (1, -1), PRIMARY_L),
                  ("BACKGROUND", (2, 0), (2, -1), ACCENT_L),
                  ("BOX",        (0, 0), (0, -1), 2, HexColor("#9FA8DA")),
                  ("BOX",        (1, 0), (1, -1), 2, HexColor("#A5D6A7")),
                  ("BOX",        (2, 0), (2, -1), 2, HexColor("#FFCC80")),
                  ("TOPPADDING", (0, 0), (-1, -1), 12),
                  ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                  ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
                  ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
              ]))
    elems.append(t)
    elems.append(spacer(0.4))
    note = Table([[Paragraph(
        "💡  Only <b>8% of India's laundry market is organised</b> — the remaining 92% is served by "
        "informal dhobis and self-service. This represents <b>massive whitespace</b> for a "
        "technology-first platform like WashGo.",
        ParagraphStyle("note", fontSize=9.5, fontName="Helvetica", textColor=HexColor("#0D47A1"),
                       leading=14))]],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#E3F2FD")),
            ("LINEAFTER",  (0, 0), (0, -1), 4, HexColor("#1976D2")),
            ("LINEBEFORE", (0, 0), (0, -1), 4, HexColor("#1976D2")),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ]))
    elems.append(note)
    return elems


def slide_5_business_model():
    elems = slide_header("SLIDE 05 · BUSINESS MODEL", "Business Model",
                         "Three complementary revenue streams built for high margins and recurring revenue.")
    rev_data = [
        [Paragraph("💸  Service Commission", S["badge"]),
         Paragraph("🚚  Delivery Fee", S["badge"]),
         Paragraph("🔄  Subscriptions", S["badge"])],
        [Paragraph("25%", S["big_num"]),
         Paragraph("₹49", S["big_num"]),
         Paragraph("₹999 – ₹2,999", ParagraphStyle("sub", fontSize=15, fontName="Helvetica-Bold",
                                                   textColor=PRIMARY, leading=20,
                                                   alignment=TA_CENTER))],
        [Paragraph("Commission per order\nfrom facility partners", S["center"]),
         Paragraph("Flat per pickup+delivery\ncycle, per customer", S["center"]),
         Paragraph("Monthly plans with\ndiscounted priority pickup", S["center"])],
    ]
    col_w = (PAGE_W - 3 * cm) / 3
    rt = Table(rev_data, colWidths=[col_w] * 3,
               style=TableStyle([
                   ("BACKGROUND", (0, 0), (0, -1), PRIMARY_L),
                   ("BACKGROUND", (1, 0), (1, -1), HexColor("#E3F2FD")),
                   ("BACKGROUND", (2, 0), (2, -1), ACCENT_L),
                   ("BOX",        (0, 0), (0, -1), 1.5, HexColor("#A5D6A7")),
                   ("BOX",        (1, 0), (1, -1), 1.5, HexColor("#90CAF9")),
                   ("BOX",        (2, 0), (2, -1), 1.5, HexColor("#FFCC80")),
                   ("TOPPADDING", (0, 0), (-1, -1), 12),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                   ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
                   ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
                   ("LINEBELOW",  (0, 0), (-1, 0), 1, BORDER),
               ]))
    elems.append(rt)
    elems.append(spacer(0.4))
    th  = ["Service", "Avg Order Value", "WashGo Revenue", "Gross Margin"]
    rows = [
        ["Regular Wash", "₹350", "₹136", "39%"],
        ["Express Wash", "₹480", "₹169", "35%"],
        ["Dry Cleaning",  "₹600", "₹199", "33%"],
        ["Premium Care",  "₹800", "₹249", "31%"],
    ]
    tw = [(PAGE_W - 3 * cm) * f for f in [0.3, 0.25, 0.25, 0.2]]
    elems.append(colored_table(
        [[Paragraph(c, ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold",
                                     textColor=white, leading=13)) for c in th]] +
        [[Paragraph(c, S["body"]) for c in row] for row in rows],
        tw))
    return elems


def slide_6_traction():
    elems = slide_header("SLIDE 06 · TRACTION & ROADMAP", "Traction & Roadmap",
                         "Strong early signals and a clear path to scale across all of Hyderabad.")
    left_data = [
        ["✅  Platform built — web + admin + partner app"],
        ["✅  3 facility partnerships confirmed"],
        ["✅  5 delivery partners onboarded"],
        ["✅  Pilot area: Kondapur & Gachibowli"],
    ]
    lt = Table([[Paragraph(row[0], S["body_b"])] for row in left_data],
               colWidths=[(PAGE_W - 3 * cm) * 0.38],
               style=TableStyle([
                   ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_L),
                   ("BOX",        (0, 0), (-1, -1), 1, HexColor("#C8E6C9")),
                   ("TOPPADDING", (0, 0), (-1, -1), 8),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                   ("LEFTPADDING", (0, 0), (-1, -1), 14),
                   ("LINEBELOW",  (0, 0), (-1, -2), 0.5, HexColor("#C8E6C9")),
               ]))

    chart_img = make_roadmap_chart()
    col_w = (PAGE_W - 3 * cm) * 0.38
    chart_w = (PAGE_W - 3 * cm) * 0.60
    main = Table([[lt, chart_img]],
                 colWidths=[col_w, chart_w],
                 style=TableStyle([
                     ("VALIGN",  (0, 0), (-1, -1), "TOP"),
                     ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                     ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                 ]))
    elems.append(main)
    elems.append(spacer(0.3))

    qdata = [
        ["Q1 2025\n100 orders/mo\n2 areas · Launch phase",
         "Q2 2025\n500 orders/mo\n5 areas · Subscriptions live",
         "Q3 2025\n2,000 orders/mo\n10 areas · Corporate tie-ups",
         "Q4 2025\n5,000 orders/mo\nFull Hyderabad coverage"],
    ]
    cw = (PAGE_W - 3 * cm) / 4
    qt = Table([[Paragraph(c.replace("\n", "<br/>"),
                           ParagraphStyle("qc", fontSize=8.5, fontName="Helvetica-Bold",
                                          textColor=DARK, alignment=TA_CENTER, leading=13))
                for c in qdata[0]]],
               colWidths=[cw] * 4,
               style=TableStyle([
                   ("BACKGROUND", (0, 0), (0, -1), PRIMARY_L),
                   ("BACKGROUND", (1, 0), (1, -1), HexColor("#E3F2FD")),
                   ("BACKGROUND", (2, 0), (2, -1), ACCENT_L),
                   ("BACKGROUND", (3, 0), (3, -1), HexColor("#EDE7F6")),
                   ("BOX", (0, 0), (0, -1), 1.5, HexColor("#A5D6A7")),
                   ("BOX", (1, 0), (1, -1), 1.5, HexColor("#90CAF9")),
                   ("BOX", (2, 0), (2, -1), 1.5, HexColor("#FFCC80")),
                   ("BOX", (3, 0), (3, -1), 1.5, HexColor("#CE93D8")),
                   ("TOPPADDING", (0, 0), (-1, -1), 10),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                   ("ALIGN", (0, 0), (-1, -1), "CENTER"),
               ]))
    elems.append(qt)
    return elems


def slide_7_financials():
    elems = slide_header("SLIDE 07 · FINANCIAL PROJECTIONS", "Financial Projections",
                         "Conservative 18-month model reaching ₹25L/month revenue by Month 18.")
    elems.append(make_revenue_chart())

    th  = ["Metric", "Month 6", "Month 12", "Month 18"]
    rows = [
        ["Orders / Month", "500", "2,000", "5,000"],
        ["Revenue",         "₹2.5L", "₹10L",  "₹25L"],
        ["EBITDA",          "−₹1.2L", "₹0.8L", "₹6.5L"],
        ["Subscribers",     "50",    "300",   "900"],
    ]
    tw = [(PAGE_W - 3 * cm) * f for f in [0.34, 0.22, 0.22, 0.22]]
    elems.append(colored_table(
        [[Paragraph(c, ParagraphStyle("th", fontSize=9, fontName="Helvetica-Bold",
                                     textColor=white, leading=13)) for c in th]] +
        [[Paragraph(c, S["body"]) for c in row] for row in rows], tw))
    elems.append(spacer(0.3))

    be = Table([[Paragraph("📍  Break-Even Point", S["center_b"]),
                 Paragraph("Month 11", ParagraphStyle("be", fontSize=22, fontName="Helvetica-Bold",
                                                      textColor=HexColor("#FFD54F"), alignment=TA_CENTER,
                                                      leading=26)),
                 Paragraph("At 1,600 orders/month — operating cash-flow positive",
                            ParagraphStyle("bes", fontSize=9, fontName="Helvetica", textColor=white,
                                           alignment=TA_CENTER, leading=14))]],
               colWidths=[(PAGE_W - 3 * cm) * f for f in [0.35, 0.25, 0.4]],
               style=TableStyle([
                   ("BACKGROUND", (0, 0), (-1, -1), DARK),
                   ("TOPPADDING", (0, 0), (-1, -1), 12),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                   ("ALIGN",     (0, 0), (-1, -1), "CENTER"),
                   ("VALIGN",    (0, 0), (-1, -1), "MIDDLE"),
               ]))
    elems.append(be)
    return elems


def slide_8_use_of_funds():
    elems = slide_header("SLIDE 08 · USE OF FUNDS", "Use of Funds",
                         "₹1.5 Crore deployed across five strategic areas to reach Series A milestones.")
    donut = make_donut_chart()
    alloc = [
        ("💻", "Tech & Product",          "₹37.5L", "25%", PRIMARY),
        ("🚚", "Operations & Logistics",  "₹45L",   "30%", DARK),
        ("📣", "Marketing & Acquisition", "₹37.5L", "25%", ACCENT),
        ("👥", "Team (3 hires)",          "₹22.5L", "15%", PURPLE),
        ("🏦", "Working Capital",         "₹7.5L",  " 5%", TEAL),
    ]
    rows = [[Paragraph(f"{icon}  {name}", S["body_b"]),
             Paragraph(pct, S["body"]),
             Paragraph(amount, ParagraphStyle("av", fontSize=10, fontName="Helvetica-Bold",
                                              textColor=color, leading=14))]
            for icon, name, amount, pct, color in alloc]
    at = Table(rows, colWidths=[9.5 * cm, 3 * cm, 3.5 * cm],
               style=TableStyle([
                   ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, LGRAY]),
                   ("TOPPADDING",    (0, 0), (-1, -1), 9),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                   ("LEFTPADDING",   (0, 0), (-1, -1), 10),
                   ("LINEBELOW",     (0, 0), (-1, -1), 0.5, BORDER),
               ]))

    main = Table([[donut, at]],
                 colWidths=[10 * cm, PAGE_W - 3 * cm - 10 * cm],
                 style=TableStyle([
                     ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
                     ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                     ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                 ]))
    elems.append(main)
    return elems


def slide_9_ask():
    elems = slide_header("SLIDE 09 · THE ASK", "The Ask",
                         "We are raising our first external round to execute the Hyderabad playbook.")
    ask_box = Table([[
        Paragraph("₹1.5 Crore", S["ask_num"]),
        Paragraph("Seed Round — 18-Month Runway to Series A Readiness",
                  ParagraphStyle("al", fontSize=12, fontName="Helvetica-Bold",
                                 textColor=white, alignment=TA_CENTER, leading=16)),
    ]], colWidths=[(PAGE_W - 3 * cm) * 0.35, (PAGE_W - 3 * cm) * 0.65],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
            ("TOPPADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
            ("ALIGN",     (0, 0), (-1, -1), "CENTER"),
            ("VALIGN",    (0, 0), (-1, -1), "MIDDLE"),
        ]))
    elems.append(ask_box)
    elems.append(spacer(0.4))

    chips = [["📄 SAFE / Convertible Note", "🏷️ Valuation Cap: ₹8 Cr", "🕐 18-Month Runway"]]
    ct = Table(chips, colWidths=[(PAGE_W - 3 * cm) / 3] * 3,
               style=TableStyle([
                   ("BACKGROUND", (0, 0), (-1, -1), DARK_L),
                   ("BOX",        (0, 0), (-1, -1), 1, HexColor("#9FA8DA")),
                   ("INNERGRID",  (0, 0), (-1, -1), 0.5, white),
                   ("FONTNAME",   (0, 0), (-1, -1), "Helvetica-Bold"),
                   ("FONTSIZE",   (0, 0), (-1, -1), 9),
                   ("TEXTCOLOR",  (0, 0), (-1, -1), DARK),
                   ("TOPPADDING", (0, 0), (-1, -1), 8),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                   ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
               ]))
    elems.append(ct)
    elems.append(spacer(0.3))

    offers = [
        ["🪑 Board Observer Seat",        "📊 Monthly Investor Updates"],
        ["⚡ Pro-Rata Rights in Series A", "🗺️ Early Access to Expansion Markets"],
    ]
    milestones = [
        "📦  5,000+ orders/month",
        "💰  ₹25L+ MRR",
        "📈  EBITDA positive for 3+ months",
        "🌆  Full Hyderabad coverage",
        "👥  900+ active subscribers",
    ]
    l_rows = [[Paragraph(a, S["body_b"]), Paragraph(b, S["body_b"])] for a, b in offers]
    l_t = Table(l_rows, colWidths=[(PAGE_W - 3 * cm) * 0.24] * 2,
                style=TableStyle([
                    ("ROWBACKGROUNDS", (0, 0), (-1, -1), [PRIMARY_L, white]),
                    ("TOPPADDING",    (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("LEFTPADDING",   (0, 0), (-1, -1), 10),
                    ("BOX",           (0, 0), (-1, -1), 1, HexColor("#C8E6C9")),
                    ("LINEBELOW",     (0, 0), (-1, -2), 0.5, HexColor("#C8E6C9")),
                ]))

    r_rows = [[Paragraph(m, S["body_b"])] for m in milestones]
    r_t = Table(r_rows, colWidths=[(PAGE_W - 3 * cm) * 0.46],
                style=TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), PRIMARY_L),
                    ("BOX",        (0, 0), (-1, -1), 1, HexColor("#C8E6C9")),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 12),
                    ("LINEBELOW",  (0, 0), (-1, -2), 0.5, HexColor("#C8E6C9")),
                ]))

    sa_box = Table([[Paragraph(
        "Series A Target: <b>₹8–10 Crore</b> at <b>₹40 Crore valuation</b>",
        ParagraphStyle("sa", fontSize=10, fontName="Helvetica", textColor=HexColor("#E65100"),
                       leading=14))]],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), ACCENT_L),
            ("LINEBEFORE", (0, 0), (0, -1), 4, ACCENT),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ]))
    r_col = Table([[r_t], [spacer(0.2)], [sa_box]],
                  style=TableStyle([
                      ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                      ("TOPPADDING",   (0, 0), (-1, -1), 0),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                  ]))

    both = Table([[l_t, r_col]],
                 colWidths=[(PAGE_W - 3 * cm) * 0.5, (PAGE_W - 3 * cm) * 0.5],
                 style=TableStyle([
                     ("VALIGN",       (0, 0), (-1, -1), "TOP"),
                     ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                     ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                 ]))
    elems.append(both)
    return elems


def slide_10_contact():
    elems = slide_header("SLIDE 10 · CONTACT", "Let's Build This Together",
                         "We're looking for investors who share our vision of making professional "
                         "laundry accessible to every urban household in India.")
    contact_rows = [
        ("🏢", "Company",  "WashGo Technologies Pvt. Ltd."),
        ("📍", "Location", "Hyderabad, Telangana — 500032"),
        ("📧", "Email",    "founders@washgo.in"),
        ("🌐", "Website",  "www.washgo.in  (coming soon)"),
        ("💼", "LinkedIn", "linkedin.com/company/washgo-in  (coming soon)"),
    ]
    cr = [[Paragraph(f"{icon}  {label}", S["body_b"]),
           Paragraph(value, S["body"])]
          for icon, label, value in contact_rows]
    ct = Table(cr, colWidths=[4.5 * cm, 13 * cm],
               style=TableStyle([
                   ("ROWBACKGROUNDS", (0, 0), (-1, -1), [white, LGRAY]),
                   ("TOPPADDING",    (0, 0), (-1, -1), 9),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                   ("LEFTPADDING",   (0, 0), (-1, -1), 12),
                   ("BOX",           (0, 0), (-1, -1), 1, BORDER),
                   ("LINEBELOW",     (0, 0), (-1, -2), 0.5, BORDER),
               ]))

    cta = Table([[
        Paragraph("☎️", ParagraphStyle("ci", fontSize=28, alignment=TA_CENTER, leading=34)),
        Paragraph("Ready to invest?<br/>"
                  "<font size='9' color='#6B7280'>Book a 30-minute call with our founders — "
                  "learn about WashGo's vision, traction, and opportunity.</font>",
                  ParagraphStyle("ctat", fontSize=12, fontName="Helvetica-Bold",
                                 textColor=DARK, leading=16)),
        Paragraph("📅 Schedule a 30-min Call\nfounders@washgo.in",
                  ParagraphStyle("ctab", fontSize=10, fontName="Helvetica-Bold",
                                 textColor=white, alignment=TA_CENTER, leading=14)),
    ]], colWidths=[2.5 * cm, 12 * cm, 5 * cm],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
            ("BACKGROUND", (2, 0), (2, -1), HexColor("#1B5E20")),
            ("TOPPADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
            ("LEFTPADDING", (0, 0), (-1, -1), 14),
            ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN",      (2, 0), (2, -1), "CENTER"),
            ("TEXTCOLOR",  (0, 0), (-1, -1), white),
        ]))

    main = Table([[ct, cta]],
                 colWidths=[(PAGE_W - 3 * cm) * 0.55, (PAGE_W - 3 * cm) * 0.45],
                 style=TableStyle([
                     ("VALIGN",       (0, 0), (-1, -1), "TOP"),
                     ("LEFTPADDING",  (0, 0), (-1, -1), 0),
                     ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                 ]))
    elems.append(main)
    elems.append(spacer(0.5))
    footer = Table([[Paragraph(
        "Confidential — For Authorised Recipients Only  |  "
        "This document contains forward-looking statements and projections.  |  "
        "© 2025 WashGo Technologies Pvt. Ltd. All rights reserved.",
        ParagraphStyle("f", fontSize=8, fontName="Helvetica", textColor=white,
                       alignment=TA_CENTER, leading=12))]],
        style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), DARK),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
    elems.append(footer)
    return elems


# ── Build PDF ──────────────────────────────────────────────────────────────────

def build_pdf(output_path="washgo_pitch_deck.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=1.5 * cm,
        rightMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.2 * cm,
        title="WashGo — Investor Pitch Deck",
        author="WashGo Technologies Pvt. Ltd.",
        subject="Seed Round ₹1.5 Crore",
    )

    on_page = AccentCanvas(output_path)

    # Each slide separated by a PageBreak
    from reportlab.platypus import PageBreak
    slides = [
        slide_1_cover(),
        slide_2_problem(),
        slide_3_solution(),
        slide_4_market(),
        slide_5_business_model(),
        slide_6_traction(),
        slide_7_financials(),
        slide_8_use_of_funds(),
        slide_9_ask(),
        slide_10_contact(),
    ]

    story = []
    for i, slide_elems in enumerate(slides):
        story.extend(slide_elems)
        if i < len(slides) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f"✅  PDF saved → {output_path}")


if __name__ == "__main__":
    build_pdf("washgo_pitch_deck.pdf")
