
 # ─── Standart Kütüphaneler ────────────────────────────────────────────────────
import random
import textwrap
import os
 
# ─── Üçüncü Taraf Kütüphaneler ────────────────────────────────────────────────
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# DİKKAT: Dosya adın sql.env olduğu için parantez içine belirttik
load_dotenv("sql.env") 

# API anahtarını arka planda alıyoruz
API_KEY = os.getenv("GEMINI_API_KEY")
 
# ══════════════════════════════════════════════════════════════════════════════
# SAYFA YAPISI
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SQL Asistanı ",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL STİL (Görsel Tasarım)
# ══════════════════════════════════════════════════════════════════════════════
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');
:root {
    --bg-deep:    #0d1117; --bg-card:    #161b22; --bg-input:   #1c2230;
    --accent:     #58a6ff; --accent2:    #3fb950; --accent3:    #f78166;
    --text-main:  #e6edf3; --text-muted: #8b949e; --border:     #30363d; --radius:     10px;
}
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .main {
    background-color: var(--bg-deep) !important; color: var(--text-main) !important; font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] { background: var(--bg-card) !important; border-right: 1px solid var(--border); }
.hero-band { background: linear-gradient(135deg, #0d2137 0%, #0d1117 60%, #0d2137 100%); border: 1px solid var(--border); border-radius: var(--radius); padding: 2rem 2.5rem 1.5rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; }
.hero-title { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; color: var(--accent); margin: 0 0 0.3rem; }
.hero-sub { font-size: 1rem; color: var(--text-muted); margin: 0; }
.card-title { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: var(--accent); margin-bottom: 0.8rem; }
.stButton > button { background: var(--bg-input) !important; color: var(--text-main) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; width: 100% !important; }
.stButton > button[kind="primary"] { background: var(--accent) !important; color: #0d1117 !important; border: none !important; font-weight: 700 !important; }
textarea, .stTextArea textarea { background: var(--bg-input) !important; color: var(--text-main) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
.step-box { background: rgba(63,185,80,0.07); border-left: 3px solid var(--accent2); border-radius: 0 var(--radius) var(--radius) 0; padding: 1rem 1.2rem; margin-bottom: 0.6rem; font-size: 0.92rem; color: var(--text-main); }
.tip-banner { background: linear-gradient(90deg, rgba(247,129,102,0.1), rgba(88,166,255,0.05)); border: 1px solid rgba(247,129,102,0.3); border-radius: var(--radius); padding: 1rem 1.4rem; margin-top: 2rem; display: flex; align-items: flex-start; gap: 0.8rem; }
.badge { display: inline-block; background: rgba(88,166,255,0.15); color: var(--accent); border: 1px solid rgba(88,166,255,0.3); border-radius: 20px; padding: 0.15rem 0.7rem; font-size: 0.72rem; font-weight: 700; margin-right: 0.4rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
 
# ══════════════════════════════════════════════════════════════════════════════
# VERİ — Şemalar ve İpuçları
# ══════════════════════════════════════════════════════════════════════════════
SCHEMAS = {
    "🛒 E-Ticaret": {
        "icon": "🛒", "label": "E-Ticaret", "description": "Müşteriler, siparişler ve ürünler",
        "schema": """CREATE TABLE customers (customer_id INT PRIMARY KEY, full_name VARCHAR(100), email VARCHAR(150), city VARCHAR(80), signup_date DATE);
CREATE TABLE products (product_id INT PRIMARY KEY, product_name VARCHAR(200), category VARCHAR(80), price DECIMAL(10,2), stock_qty INT);
CREATE TABLE orders (order_id INT PRIMARY KEY, customer_id INT REFERENCES customers(customer_id), order_date DATE, total_amount DECIMAL(10,2), status VARCHAR(30));"""
    },
    "👥 İK / Çalışanlar": {
        "icon": "👥", "label": "İK / Çalışanlar", "description": "Çalışanlar, departmanlar ve maaşlar",
        "schema": """CREATE TABLE departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(100), location VARCHAR(80));
CREATE TABLE employees (employee_id INT PRIMARY KEY, full_name VARCHAR(100), dept_id INT REFERENCES departments(dept_id), job_title VARCHAR(100), salary DECIMAL(12,2), hire_date DATE);"""
    },
    "📚 Kütüphane": {
        "icon": "📚", "label": "Kütüphane", "description": "Kitaplar ve ödünç alma kayıtları",
        "schema": """CREATE TABLE books (book_id INT PRIMARY KEY, title VARCHAR(250), author VARCHAR(150), genre VARCHAR(80), copies_avail INT);
CREATE TABLE members (member_id INT PRIMARY KEY, full_name VARCHAR(100), joined_date DATE);
CREATE TABLE loans (loan_id INT PRIMARY KEY, book_id INT REFERENCES books(book_id), member_id INT REFERENCES members(member_id), loan_date DATE, due_date DATE);"""
    }
}
 
SQL_TIPS = [
    {"title": "Neden SELECT * kullanmamalıyız?", "tip": "Gereksiz veri transferini önlemek için sadece ihtiyacınız olan sütunları seçin."},
    {"title": "INDEX ne işe yarar?", "tip": "Sık filtrelenen sütunlara index eklemek sorgu hızını büyük oranda artırır."}
]
 
# ══════════════════════════════════════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ══════════════════════════════════════════════════════════════════════════════
def init_gemini(key: str):
    genai.configure(api_key=key)
    return genai.GenerativeModel("gemini-1.5-flash")
 
def build_prompt(nl, schema, dialect, mode):
    level = "Başlangıç seviyesinde anlat." if mode == "🟢 Başlangıç" else "Teknik detay ver."
    return f"Sen bir SQL Uzmanısın. Veritabanı Şeması: {schema}. Lütfen şu soruyu {dialect} dilinde SQL'e çevir: '{nl}'. Format: ## SQL_QUERY, ## EXPLANATION, ## QUICK_TIPS"

def parse_gemini_response(text):
    res = {"query": "", "explanation": "", "tips": ""}
    if "## SQL_QUERY" in text:
        parts = text.split("##")
        for p in parts:
            if p.startswith(" SQL_QUERY"): res["query"] = p.replace("SQL_QUERY", "").strip().replace("```sql", "").replace("```", "")
            if p.startswith(" EXPLANATION"): res["explanation"] = p.replace("EXPLANATION", "").strip()
            if p.startswith(" QUICK_TIPS"): res["tips"] = p.replace("QUICK_TIPS", "").strip()
    return res

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "active_schema_key" not in st.session_state: st.session_state.active_schema_key = "🛒 E-Ticaret"
if "active_schema_sql" not in st.session_state: st.session_state.active_schema_sql = SCHEMAS["🛒 E-Ticaret"]["schema"]
if "last_result" not in st.session_state: st.session_state.last_result = None
if "daily_tip" not in st.session_state: st.session_state.daily_tip = random.choice(SQL_TIPS)
 
# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR (API Ayarları Kaldırıldı - Gizlendi)
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<div style='text-align:center;'><h1 style='font-size:3rem;'>🧠</h1><h3 style='color:#58a6ff;'>SQL Asistanı</h3></div>", unsafe_allow_html=True)
    st.divider()
    learning_mode = st.radio("📚 Öğrenme Seviyesi", ["🟢 Başlangıç", "🟡 Orta", "🔴 İleri"])
    dialect = st.selectbox("🗄️ SQL Lehçesi", ["PostgreSQL", "MySQL", "SQLite"])
    st.divider()
    st.caption("Güvenli Mod: API Anahtarı sql.env'den yüklendi.")

# ══════════════════════════════════════════════════════════════════════════════
# ANA İÇERİK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="hero-band"><div class="hero-title">🧠 SQL Asistanı</div><p class="hero-sub">Türkçe sorunuzu yazın, SQL sorgusunu anında üretelim.</p></div>', unsafe_allow_html=True)
 
col_left, col_right = st.columns([1, 1], gap="large")
 
with col_left:
    st.markdown('<div class="card-title">⚡ Şema Seçimi</div>', unsafe_allow_html=True)
    btn_cols = st.columns(3)
    for idx, (key, meta) in enumerate(SCHEMAS.items()):
        if btn_cols[idx].button(f"{meta['icon']} {meta['label']}"):
            st.session_state.active_schema_key = key
            st.session_state.active_schema_sql = meta["schema"]
 
    with st.expander("📋 Şemayı Görüntüle / Düzenle"):
        st.session_state.active_schema_sql = st.text_area("SQL Şeması", value=st.session_state.active_schema_sql, height=150)
 
    st.markdown('<div class="card-title">💬 Sorunuz</div>', unsafe_allow_html=True)
    user_query = st.text_area("Soru", placeholder="Örn: Geçen ay en çok satış yapan 5 ürünü göster", height=100, label_visibility="collapsed")
 
    generate_clicked = st.button("⚡ SQL Üret", type="primary", use_container_width=True)

with col_right:
    if generate_clicked:
        if not API_KEY:
            st.error("Hata: 'sql.env' dosyasında GEMINI_API_KEY bulunamadı!")
        elif not user_query.strip():
            st.warning("Lütfen bir soru yazın.")
        else:
            with st.spinner("AI Yanıtlıyor..."):
                try:
                    model = init_gemini(API_KEY)
                    prompt = build_prompt(user_query, st.session_state.active_schema_sql, dialect, learning_mode)
                    response = model.generate_content(prompt)
                    st.session_state.last_result = parse_gemini_response(response.text)
                except Exception as e:
                    st.error(f"API Hatası: {e}")

    # Sonuçları Göster
    res = st.session_state.last_result
    if res:
        st.markdown(f"<div class='card-title'>🖥️ {dialect} Sorgusu</div>", unsafe_allow_html=True)
        st.code(res["query"], language="sql")
        st.markdown("<div class='card-title'>📖 Adım Adım Açıklama</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='step-box'>{res['explanation']}</div>", unsafe_allow_html=True)
        if res["tips"]:
            st.markdown("<div class='card-title'>🚀 İpucu</div>", unsafe_allow_html=True)
            st.success(res["tips"])
    else:
        st.info("Henüz bir sorgu üretilmedi. Sol taraftan başlayabilirsiniz.")

# Günlük İpucu ve Footer
st.markdown("<hr>", unsafe_allow_html=True)
tip = st.session_state.daily_tip
st.markdown(f'<div class="tip-banner"><div>💡</div><div><strong>{tip["title"]}</strong><br>{tip["tip"]}</div></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; padding: 1.5rem; font-size:0.75rem; color:#8b949e;">SQL Asistanı · Gemini 1.5 Flash · Herkes için SQL</div>', unsafe_allow_html=True)
