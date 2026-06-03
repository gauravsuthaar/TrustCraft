"""
TrustCraft — Premium AI Literacy Platform
Learn to distinguish truth from hallucination through an immersive Minecraft world.

Designed & Developed by Gaurav Suthar
"""

import json
import random
from pathlib import Path
import base64
import io
from typing import Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components
import requests
from PIL import Image

# Design tokens
C_GOLD = "#E8C97D"
C_CREAM = "#F5ECD7"
C_FOREST = "#2D4A2D"
C_NIGHT = "#0D1A0F"
C_LANTERN = "#E78B3C"
C_BLOSSOM = "#F2A6C8"
C_BLUE = "#7BA3B8"

# Enhanced Minecraft-themed emojis  
EMOJI = {
    "grass": "🟩",
    "stone": "🪨",
    "dirt": "🟫",
    "water": "💧",
    "fire": "🔥",
    "tree": "🌲",
    "book": "📚",
    "golem": "🤖",
    "villager": "👤",
    "zombie": "🧟",
    "sword": "⚔️",
    "shield": "🛡️",
    "star": "⭐",
    "crown": "👑",
    "gem": "💎",
    "light": "🏮",
    "pickaxe": "⛏️",
    "bow": "🏹",
    "apple": "🍎",
    "gold": "🟨",
    "chest": "📦",
    "portal": "🌀",
    "magic": "✨",
    "wave": "〰️",
}

st.set_page_config(
    page_title="TrustCraft",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# AVATAR & SOUND SYSTEM
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def get_minecraft_avatar(username: str, size: int = 120) -> Optional[Image.Image]:
    """Fetch Minecraft avatar for a player."""
    try:
        url = f"https://mc-heads.net/avatar/{username}/{size}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except:
        pass
    return None

@st.cache_data
def get_avatar_url(username: str, size: int = 120) -> str:
    """Get Minecraft avatar URL."""
    return f"https://mc-heads.net/avatar/{username}/{size}"

def play_sound(sound_type: str = "click"):
    """Play sound effect."""
    sounds = {
        "click": "data:audio/wav;base64,UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAAAAAA=",
        "success": "data:audio/wav;base64,UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAAAAAA=",
        "error": "data:audio/wav;base64,UklGRiYAAABXQVZFZm10IBAAAAABAAEAQB8AAAB9AAACABAAZGF0YQIAAAAAAAA=",
    }
    audio_data = sounds.get(sound_type, sounds["click"])
    html = f'<audio autoplay><source src="{audio_data}" type="audio/wav"></audio>'
    st.markdown(html, unsafe_allow_html=True)

def sound_component(key: str):
    """Add clickable element with sound."""
    st.markdown(f'<script>document.addEventListener("click", ()=>{{console.log("click")}});</script>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCENE GRADIENTS & UTILITIES
# ─────────────────────────────────────────────────────────────────────────────


SCENE_GRADIENTS = {
    "hero": (
        "radial-gradient(ellipse 90% 70% at 75% 35%, rgba(231,139,60,0.22) 0%, transparent 55%),"
        "radial-gradient(ellipse 70% 60% at 15% 75%, rgba(123,163,184,0.14) 0%, transparent 50%),"
        "radial-gradient(ellipse 50% 40% at 50% 50%, rgba(242,166,200,0.08) 0%, transparent 60%),"
        "linear-gradient(160deg, #0c0c0c 0%, #050505 45%, #0a0a0a 100%)"
    ),
    "grade-square": "linear-gradient(135deg, #1a1f18 0%, #0d120d 50%, #050505 100%)",
    "grade-library": "linear-gradient(135deg, #1a1814 0%, #12100c 50%, #050505 100%)",
    "grade-forest": "linear-gradient(135deg, #0f1a12 0%, #0a140e 50%, #050505 100%)",
    "grade-tower": "linear-gradient(135deg, #141a1f 0%, #0c1014 50%, #050505 100%)",
    "grade-training": "linear-gradient(135deg, #1a1812 0%, #121008 50%, #050505 100%)",
    "grade-castle": "linear-gradient(135deg, #1a1610 0%, #100e0a 50%, #050505 100%)",
}


def scene_style(grade: str = "hero") -> str:
    g = SCENE_GRADIENTS.get(grade, SCENE_GRADIENTS["hero"])
    return f"background:{g};"


def icon(name: str, size: int = 20, stroke: str = C_CREAM, sw: str = "2") -> str:
    """Lucide-style SVG icons (stroke width 2)."""
    icons = {
        "shield": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "book": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
        "trees": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22v-8m0 0c-3-2-6-5-6-9a6 6 0 0 1 12 0c0 4-3 7-6 9z"/></svg>',
        "tower": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="2" width="8" height="20" rx="1"/><path d="M4 22h16M10 6h4M10 10h4M10 14h4"/></svg>',
        "swords": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 17.5L3 6V3h3l11.5 11.5"/><path d="M13 19l6-6"/><path d="M16 16l4 4"/><path d="M19 21l2-2"/></svg>',
        "castle": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V7l7-4 7 4v14"/><path d="M9 21v-6h6v6"/></svg>',
        "map": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>',
        "x": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
        "search": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
        "spark": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5z"/></svg>',
        "user": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        "brain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a7 7 0 0 1 7 7c0 3-2 5-4 6v3H9v-3c-2-1-4-3-4-6a7 7 0 0 1 7-7z"/></svg>',
        "arrow": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    }
    return icons.get(name, icons["spark"])


def tc_flash(msg: str, kind: str = "ok"):
    st.session_state.tc_flash = {"msg": msg, "kind": kind}


def tc_show_flash():
    fb = st.session_state.pop("tc_flash", None)
    if not fb:
        return
    kind = fb.get("kind", "info")
    st.markdown(
        f'<div class="tc-flash tc-flash-{kind}">{fb["msg"]}</div>',
        unsafe_allow_html=True,
    )


def tc_section(label: str, title: str, desc: str = ""):
    d = f'<p class="tc-section-desc">{desc}</p>' if desc else ""
    st.markdown(
        f'<div class="tc-section"><p class="tc-section-label">{label}</p>'
        f'<h2 class="tc-section-title">{title}</h2>{d}</div>',
        unsafe_allow_html=True,
    )


def tc_hud_html(rank: str, xp: int, trust: int, rep: int, ach: int, ach_total: int) -> str:
    next_xp = 120
    for threshold, _name in RANKS:
        if xp < threshold:
            next_xp = threshold
            break
    else:
        next_xp = RANKS[-1][0]
    pct = min(100, int(100 * xp / max(next_xp, 1)))
    return f"""
    <div class="tc-hud">
      <div class="tc-hud-rank">Rank<span>{rank}</span></div>
      <div class="tc-stat"><b>{xp}</b><small>Knowledge XP</small></div>
      <div class="tc-stat"><b>{trust}</b><small>Trust</small></div>
      <div class="tc-stat"><b>{rep}</b><small>Reputation</small></div>
      <div class="tc-stat"><b>{ach}/{ach_total}</b><small>Medals</small></div>
      <div class="tc-stat" style="min-width:72px"><b>{pct}%</b><small>Next rank</small></div>
    </div>"""


def enter_game(loc: str = "village_square"):
    load_save_into_session()
    st.session_state.game_started = True
    st.session_state.location = loc
    visited = list(set(st.session_state.get("visited_locs", []) + [loc]))
    st.session_state.visited_locs = visited
    save_session_to_disk()


def render_world_nav():
    loc = st.session_state.get("location", "village_square")
    tabs = [
        ("village_square", "Square"),
        ("library", "Library"),
        ("forest", "Forest"),
        ("watchtower", "Tower"),
        ("training", "Training"),
        ("castle", "Castle"),
    ]
    st.markdown('<p class="tc-nav-hint">Travel the kingdom</p>', unsafe_allow_html=True)
    cols = st.columns(len(tabs))
    for col, (key, label) in zip(cols, tabs):
        with col:
            active = loc == key
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if active else "secondary",
            ):
                if active:
                    pass
                elif key == "castle" and not castle_unlocked():
                    st.session_state.location = "castle"
                    st.session_state.castle_locked_msg = True
                    save_session_to_disk()
                    st.rerun()
                else:
                    travel_to(key)
    if st.button("Exit to title", key="nav_exit"):
        st.session_state.game_started = False
        st.rerun()


def landing_hero_html() -> str:
    avatar_url = get_avatar_url('trustcraft', 160)
    return f"""
    <div class="hero-stage">
      <div class="hero-particles">
        <span></span><span></span><span></span><span></span><span></span><span></span>
      </div>
      <div class="hero-topbar"><span class="brand-name">TrustCraft</span><span class="hero-version">Human First AI</span></div>
      <div class="hero-panel">
        <div class="hero-copy">
          <span class="hero-chip">Evidence Verification Platform</span>
          <h1>Know when AI is right. Know when it is wrong.</h1>
          <p>Artificial intelligence is becoming part of everyday life. Yet AI systems can sometimes generate information that sounds convincing but is inaccurate misleading or entirely fabricated. TrustCraft turns AI trust verification and critical thinking into an immersive learning experience where users learn to identify hallucinations evaluate evidence and make informed decisions with confidence.</p>
          <div class="hero-actions"><span class="hero-pill">AI Literacy</span><span class="hero-pill">Hallucination Detection</span><span class="hero-pill">Evidence Verification</span></div>
          <div class="hero-meta-row">
            <div class="hero-meta-card"><span>6 regions</span><strong>AI Trust Skills</strong></div>
            <div class="hero-meta-card"><span>5 guides</span><strong>Evidence Based Reasoning</strong></div>
          </div>
        </div>
        <div class="hero-visual">
          <div class="hero-scene">
            <div class="hero-glow-pool"></div>
            <div class="hero-lantern"></div>
            <div class="hero-tree"></div>
            <div class="hero-scene-card">
              <img class="hero-scene-avatar" src="{avatar_url}" alt="TrustCraft avatar" />
              <div>
                <p class="hero-banner-title">Hallucination Detection Lab</p>
                <p class="hero-banner-text">Learn why AI systems sometimes generate false information and discover practical techniques used to verify claims challenge unreliable outputs and build trust in AI generated content.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="hero-footer">
        <button class="hero-pill" onclick="scrollToSection('world-target')">Trust Calibration</button>
        <button class="hero-pill" onclick="scrollToSection('world-target')">Claim Verification</button>
        <button class="hero-pill" onclick="scrollToSection('characters-target')">Critical Thinking</button>
      </div>
    </div>"""


def render_native_landing():
    """Premium landing page with smooth animations."""
    st.markdown(landing_hero_html(), unsafe_allow_html=True)
    
    st.markdown('<div class="world-section"></div>', unsafe_allow_html=True)
    st.markdown('''
    <section id="world-target" class="stage-overview" style="max-width:1200px;margin:0 auto;padding:2rem 0">
      <p style="font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.9);margin-bottom:1rem">World</p>
      <h2 style="font-family:'Inter Tight',sans-serif;font-size:2.6rem;font-weight:700;letter-spacing:-0.02em;color:#F5ECD7;margin-bottom:0.75rem">Six locations. One premium journey.</h2>
      <p style="font-size:1.05rem;color:rgba(245,236,215,0.72);margin-bottom:2rem;max-width:680px">Each region teaches you how to think about information in a luminous cherry blossom kingdom. Trust. Verify. Reject. Master the choices that matter.</p>
    </section>
    ''', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, dest in enumerate(DESTINATIONS):
        icon_url = get_avatar_url(dest['loc'], 96)
        with cols[i % 3]:
            st.markdown(f'''
            <div class="feature-card">
              <div class="feature-icon"><img src="{icon_url}" alt="{dest['title']} avatar" /></div>
              <p class="feature-label">{dest['time']}</p>
              <h3>{dest['title']}</h3>
              <p>{dest['desc']}</p>
              <button class="feature-cta" onclick="scrollToSection('world-target')">Enter {dest['title'].split()[0]}</button>
            </div>
            ''', unsafe_allow_html=True)
            if st.button(f"Go {dest['title'].split()[0]}", key=f"land_{dest['loc']}", use_container_width=True):
                enter_game(dest['loc'])
                st.rerun()

    st.markdown('''
    <section id="characters-target" style="max-width:1200px;margin:3rem auto 0;padding:2rem 0">
      <p style="font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.9);margin-bottom:1rem">Characters</p>
      <h2 style="font-family:'Inter Tight',sans-serif;font-size:2.5rem;font-weight:700;letter-spacing:-0.02em;color:#F5ECD7;margin-bottom:2rem">Meet the villagers</h2>
    </section>
    ''', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, key in enumerate(["golem", "librarian", "villager"]):
        c = CHARACTERS[key]
        avatar_url = get_avatar_url(c['name'].split()[0].lower(), 120)
        with cols[i]:
            st.markdown(f'''
            <div class="character-card">
              <div class="character-avatar"><img src="{avatar_url}" alt="{c['name']} avatar" /></div>
              <div class="character-body">
                <span style="font-size:0.75rem;letter-spacing:0.12em;text-transform:uppercase;color:rgba(245,236,215,0.42);margin-bottom:0.65rem">{c['rarity']}</span>
                <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.3rem;color:var(--gold);margin:0 0 0.45rem">{c['name']}</h3>
                <p style="font-size:0.9rem;color:rgba(245,236,215,0.72);line-height:1.7;margin-bottom:1rem">{c['description']}</p>
                <div style="font-size:0.85rem;color:rgba(245,236,215,0.55);">Trust {c['trust']}%</div>
              </div>
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('''
    <div style="text-align:center;padding:3rem 1rem">
      <div class="footer-brand"><p style="font-size:0.75rem;letter-spacing:0.08em;color:rgba(245,236,215,0.35)">Designed & Developed by Gaurav Suthar</p><div style="margin-top:24px;text-align:center;"><div class="hero-actions" style="justify-content:center;margin-top:12px;"><a href="https://www.linkedin.com/in/gauravsuthar2005/" target="_blank" class="hero-pill" style="color:rgb(245,236,215)!important;text-decoration:none!important;">LinkedIn</a><a href="https://github.com/gauravsuthaar" target="_blank" class="hero-pill" style="color:rgb(245,236,215)!important;text-decoration:none!important;">GitHub</a></div></div></div>
    </div>
    <script>
      function startJourney() {
        document.querySelector('#world-target')?.scrollIntoView({behavior:'smooth', block:'start'});
      }
      function scrollToSection(id) {
        document.querySelector('#' + id)?.scrollIntoView({behavior:'smooth', block:'start'});
      }
    </script>
    ''', unsafe_allow_html=True)

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Inter+Tight:wght@500;600;700&display=swap');

*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-font-smoothing:antialiased}

/* Hide all Streamlit chrome */
#MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"],
div[data-testid="collapsedControl"] { display:none!important; visibility:hidden!important; }

.stApp {
  background:
    radial-gradient(circle at 16% 10%, rgba(232,201,125,0.12), transparent 18%),
    radial-gradient(circle at 82% 8%, rgba(242,166,200,0.14), transparent 20%),
    linear-gradient(180deg, #07070b 0%, #071418 40%, #050505 100%)!important;
  font-family:'Inter',sans-serif!important;
  color:#F5ECD7!important;
  overflow-x:hidden;
}

.block-container { padding:0!important; max-width:100%!important; }
section[data-testid="stSidebar"] { display:none!important; }
[data-testid="stAppViewContainer"] > section { padding:0; max-width:100%; margin:0 auto; }

/* Premium typography */
:root {
  --gold:#E8C97D;
  --cream:#F5ECD7;
  --forest:#2D4A2D;
  --night:#0D1A0F;
  --lantern:#E78B3C;
  --blossom:#F2A6C8;
  --blue:#7BA3B8;
  --glass-fill:rgba(255,255,255,0.04);
  --glass-border:rgba(255,255,255,0.08);
  --glass-shadow:0 20px 80px rgba(0,0,0,0.35);
}

h1,h2,h3,h4,h5,h6 {
  font-family:'Inter Tight',sans-serif!important;
  font-weight:600!important;
  letter-spacing:-0.02em!important;
}

p, li { color:rgba(245,236,215,0.82); line-height:1.65; font-size:0.95rem; }
label, .stSlider label { 
  font-family:'Inter',sans-serif!important; 
  color:rgba(240,237,230,0.55)!important; 
  font-size:0.8rem!important; 
  letter-spacing:0.04em!important; 
}

/* Premium Buttons */
.stButton > button {
  font-family:'Inter',sans-serif!important;
  font-weight:600!important;
  font-size:0.9rem!important;
  border-radius:12px!important;
  border:1px solid var(--glass-border)!important;
  background:var(--glass-fill)!important;
  color:var(--cream)!important;
  backdrop-filter:blur(16px)!important;
  transition:all 300ms cubic-bezier(0.4,0,0.2,1)!important;
  padding:0.65rem 1.25rem!important;
  box-shadow:var(--glass-shadow)!important;
  cursor:pointer!important;
}

.stButton > button:hover {
  transform:translateY(-2px)!important;
  border-color:rgba(255,255,255,0.18)!important;
  background:rgba(255,255,255,0.08)!important;
  box-shadow:0 16px 48px rgba(0,0,0,0.35), 0 0 40px rgba(232,201,125,0.12)!important;
}

  .hero-stage { position:relative; overflow:hidden; padding:3rem 1.5rem 2.5rem; max-width:1200px; margin:0 auto; }
  .hero-stage:before { content:''; position:absolute; inset:0; background:
    radial-gradient(circle at 16% 18%, rgba(255,190,110,0.26), transparent 20%),
    radial-gradient(circle at 85% 12%, rgba(255,145,82,0.18), transparent 18%),
    radial-gradient(circle at 50% 40%, rgba(255,210,155,0.10), transparent 28%),
    linear-gradient(180deg, rgba(12,14,20,0.98), rgba(5,7,11,0.95));
    pointer-events:none; mix-blend-mode:screen;
  }
  .hero-stage:after { content:''; position:absolute; inset:0; background-image:
      radial-gradient(circle at 22% 12%, rgba(255,220,170,0.18), transparent 22%),
      radial-gradient(circle at 88% 18%, rgba(255,150,100,0.10), transparent 20%),
      radial-gradient(circle at 58% 68%, rgba(255,205,145,0.12), transparent 24%);
    opacity:0.95; pointer-events:none; mix-blend-mode:soft-light;
  }
  .hero-particles { position:absolute; inset:0; pointer-events:none; z-index:1; }
  .hero-particles span { position:absolute; width:10px; height:10px; border-radius:999px; background:rgba(255,255,255,0.18); filter:blur(1px); animation:particleDrift 14s linear infinite; }
  .hero-particles span:nth-child(1) { left:8%; top:25%; animation-delay:0s; opacity:0.8; transform:scale(0.85); }
  .hero-particles span:nth-child(2) { left:18%; top:60%; animation-delay:2s; opacity:0.7; transform:scale(0.7); }
  .hero-particles span:nth-child(3) { left:45%; top:15%; animation-delay:5s; opacity:0.55; transform:scale(0.9); }
  .hero-particles span:nth-child(4) { left:70%; top:30%; animation-delay:3s; opacity:0.65; transform:scale(0.8); }
  .hero-particles span:nth-child(5) { left:54%; top:72%; animation-delay:1s; opacity:0.5; transform:scale(0.9); }
  .hero-particles span:nth-child(6) { left:86%; top:58%; animation-delay:4s; opacity:0.7; transform:scale(0.75); }
  @keyframes particleDrift { 0% { transform: translateY(0) scale(1); } 50% { transform: translateY(-30px) scale(1.05); } 100% { transform: translateY(0) scale(1); } }
  .hero-topbar { position:relative; display:inline-flex; align-items:center; gap:0.75rem; color:#FFE8B1; letter-spacing:0.24em; font-size:0.82rem; text-transform:uppercase; margin-bottom:1.25rem; z-index:2; }
  .hero-panel { position:relative; z-index:2; display:grid; grid-template-columns:1.05fr 0.95fr; gap:2rem; align-items:center; background:rgba(18,20,34,0.78); border:1px solid rgba(255,255,255,0.14); border-radius:32px; backdrop-filter:blur(34px); box-shadow:0 50px 140px rgba(0,0,0,0.32); padding:2rem; }
  .hero-copy h1 { font-family:'Inter Tight',sans-serif; font-size:clamp(3rem,5vw,4.8rem); line-height:1.02; margin:0 0 1rem; color:#fff7e8; text-shadow:0 0 50px rgba(255,176,87,0.24); }
  .hero-copy p { font-size:1.05rem; color:rgba(245,236,215,0.96); max-width:46rem; margin-bottom:1.5rem; line-height:1.8; }
  .hero-chip { display:inline-flex; align-items:center; gap:0.5rem; padding:0.75rem 1rem; border-radius:999px; border:1px solid rgba(255,255,255,0.20); background:rgba(255,220,160,0.12); color:#fff6db; font-size:0.78rem; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:1.5rem; }
  .hero-actions { display:flex; flex-wrap:wrap; gap:1rem; margin-bottom:1.75rem; }
  .hero-actions .btn { min-width:170px; }
  .hero-meta-row { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem; }
  .hero-meta-card { display:flex; flex-direction:column; gap:0.25rem; padding:1rem 1.2rem; border-radius:20px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.14); }
  .hero-meta-card span { color:rgba(245,236,215,0.72); font-size:0.82rem; text-transform:uppercase; letter-spacing:0.08em; }
  .hero-meta-card strong { color:#fff8e6; font-size:1rem; line-height:1.4; }
  .hero-visual { display:flex; flex-direction:column; gap:1.4rem; align-items:flex-end; justify-content:center; position:relative; }
  .hero-scene { position:relative; width:100%; min-height:360px; overflow:hidden; border-radius:28px; padding:1.5rem; background:linear-gradient(180deg, rgba(255,226,180,0.08), rgba(18,20,32,0.72)); border:1px solid rgba(255,255,255,0.10); }
  .hero-glow-pool { position:absolute; left:28%; top:55%; width:44%; height:24%; background:radial-gradient(circle, rgba(255,200,130,0.28), transparent 60%); filter:blur(14px); }
  .hero-lantern { position:absolute; right:12%; top:18%; width:24px; height:60px; background:linear-gradient(180deg, rgba(255,213,126,0.95), rgba(255,162,85,0.85)); border-radius:16px; box-shadow:0 0 32px rgba(255,198,114,0.45); }
  .hero-lantern:before { content:''; position:absolute; top:-10px; left:50%; transform:translateX(-50%); width:12px; height:12px; border-radius:50%; background:rgba(255,242,190,0.96); box-shadow:0 0 18px rgba(255,242,190,0.8); }
  .hero-tree { position:absolute; left:-8%; bottom:12%; width:220px; height:260px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.10); border-radius:40% 40% 25% 25%; box-shadow:0 0 20px rgba(255,160,115,0.14); }
  .hero-tree:before { content:''; position:absolute; left:14%; bottom:66%; width:120px; height:120px; background:rgba(255,160,145,0.24); border-radius:50%; filter:blur(3px); }
  .hero-tree:after { content:''; position:absolute; right:16%; bottom:54%; width:90px; height:90px; background:rgba(255,210,170,0.20); border-radius:50%; filter:blur(3px); }
  .hero-scene-card { position:relative; z-index:2; width:100%; min-height:150px; display:flex; align-items:center; gap:1rem; padding:1.3rem; border-radius:24px; background:rgba(255,255,255,0.10); border:1px solid rgba(255,255,255,0.16); backdrop-filter:blur(18px); box-shadow:0 24px 70px rgba(0,0,0,0.26); }
  .hero-scene-avatar { width:72px; height:72px; border-radius:22px; object-fit:cover; border:1px solid rgba(255,255,255,0.18); }
  .hero-cube-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; }
  .hero-cube { min-height:90px; border-radius:22px; border:1px solid rgba(255,255,255,0.12); background:rgba(255,255,255,0.05); box-shadow:0 14px 40px rgba(0,0,0,0.18); }
  .cube-large { background:linear-gradient(135deg, rgba(255,220,180,0.24), rgba(255,233,210,0.08)); }
  .cube-medium { background:linear-gradient(135deg, rgba(255,175,110,0.25), rgba(255,212,170,0.06)); }
  .cube-small { background:linear-gradient(135deg, rgba(255,232,180,0.18), rgba(255,255,255,0.05)); }
  .cube-accent { background:linear-gradient(135deg, rgba(255,205,145,0.28), rgba(255,250,220,0.10)); }
  .hero-footer { position:relative; z-index:2; margin-top:1.75rem; display:flex; flex-wrap:wrap; gap:0.75rem; }
  .hero-pill { display:inline-flex; align-items:center; justify-content:center; padding:0.7rem 1rem; border-radius:999px; background:rgba(255,234,205,0.12); border:1px solid rgba(255,255,255,0.14); color:rgba(245,236,215,0.9); font-size:0.8rem; cursor:pointer; transition:transform 0.24s ease, background 0.24s ease; }
  .hero-pill:hover { transform:translateY(-2px); background:rgba(255,234,205,0.2); }
  .hero-pill.accent { background:rgba(255,199,138,0.16); color:#fff8e0; border-color:rgba(255,199,138,0.24); }
  .feature-card { background:linear-gradient(180deg, rgba(24,24,30,0.94), rgba(18,18,28,0.88)); border:1px solid rgba(255,255,255,0.12); border-radius:26px; padding:1.8rem; backdrop-filter:blur(24px); box-shadow:0 34px 90px rgba(0,0,0,0.28); transition:transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease; }
  .feature-card:hover { transform:translateY(-6px); box-shadow:0 36px 100px rgba(0,0,0,0.32); border-color:rgba(255,255,255,0.16); }
  .feature-icon { margin-bottom:1rem; width:96px; height:96px; }
  .feature-icon img { width:100%; height:100%; object-fit:cover; border-radius:20px; }
  .feature-label { color:rgba(248,224,183,0.82); text-transform:uppercase; font-size:0.78rem; letter-spacing:0.12em; margin-bottom:0.75rem; }
  .feature-card h3 { margin:0 0 0.75rem; color:#fff7e6; font-size:1.3rem; line-height:1.3; }
  .feature-card p { margin:0; color:rgba(245,236,215,0.85); line-height:1.75; }
  .feature-cta { display:inline-flex; align-items:center; justify-content:center; width:100%; padding:0.85rem 1rem; margin-top:1rem; border:none; border-radius:15px; background:rgba(255,197,110,0.12); color:#FFF6DF; font-weight:600; cursor:pointer; transition:all 0.25s ease; }
  .feature-cta:hover { background:rgba(255,197,110,0.22); transform:translateY(-1px); }
  .character-card { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.12); border-radius:22px; overflow:hidden; padding:1.25rem; backdrop-filter:blur(16px); box-shadow:0 18px 48px rgba(0,0,0,0.28); display:grid; grid-template-columns:100px 1fr; gap:1rem; animation:cardIn 0.7s ease-out backwards; transition:transform 0.35s, box-shadow 0.35s; }
  .character-card:hover { transform:translateY(-4px); box-shadow:0 24px 74px rgba(0,0,0,0.35); }
  .character-avatar { width:100px; height:100px; border-radius:18px; background:linear-gradient(135deg, rgba(255,218,169,0.16), rgba(255,118,134,0.08)); display:flex; align-items:center; justify-content:center; border:1px solid rgba(255,255,255,0.12); }
  .character-avatar img { width:100%; height:100%; object-fit:cover; border-radius:18px; }
  .character-body { display:flex; flex-direction:column; justify-content:center; }
.nav-container {
  position:fixed;
  top:0;
  left:0;
  right:0;
  z-index:100;
  background:rgba(5,5,5,0.4);
  backdrop-filter:blur(20px);
  border-bottom:1px solid var(--glass-border);
  transition:all 300ms ease;
  padding:1rem 2rem;
}

.nav-container.scrolled {
  background:rgba(5,5,5,0.85);
  box-shadow:0 8px 32px rgba(0,0,0,0.4);
  padding:0.7rem 2rem;
}

/* Scenes and Content */
.scene {
  position:relative;
  min-height:min(88vh,900px);
  border-radius:16px;
  overflow:hidden;
  border:1px solid var(--glass-border);
  box-shadow:0 24px 80px rgba(0,0,0,0.55);
  animation:sceneIn 1s cubic-bezier(.4,0,.2,1);
  margin:1.5rem auto;
  max-width:1200px;
}

@keyframes sceneIn { from{opacity:0;transform:scale(1.02)} to{opacity:1;transform:scale(1)} }

.scene-bg {
  position:absolute;
  inset:0;
  background-size:cover;
  background-position:center;
}

.scene-gradient {
  position:absolute;
  inset:0;
  background:linear-gradient(to right, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.35) 42%, rgba(0,0,0,0.12) 100%);
  z-index:2;
  pointer-events:none;
}

.scene-content {
  position:relative;
  z-index:5;
  padding:2rem 2.5rem;
  max-width:60%;
}

/* World zones */
.world-zone {
  padding:2rem 1.25rem;
  max-width:1400px;
  margin:0 auto;
  animation:pageIn 0.6s cubic-bezier(0.16,1,0.3,1);
}

@keyframes pageIn { from { opacity:0; transform:translateY(12px); } to { opacity:1; } }

.world-title {
  font-family:'Inter Tight',sans-serif;
  font-size:clamp(2rem,4vw,3rem);
  font-weight:700;
  color:var(--gold);
  letter-spacing:0.04em;
  line-height:1.1;
  margin:0 0 0.5rem;
  text-shadow:0 2px 40px rgba(232,201,125,0.35);
}

.location-sub {
  font-size:1.05rem;
  color:rgba(245,236,215,0.72);
  line-height:1.6;
  margin-bottom:1.25rem;
  max-width:52ch;
}

/* Glass cards */
.glass-card {
  background:var(--glass-fill);
  border:1px solid var(--glass-border);
  border-radius:16px;
  padding:1.5rem;
  backdrop-filter:blur(16px);
  box-shadow:var(--glass-shadow);
  transition:all 0.35s cubic-bezier(0.4,0,0.2,1);
  animation:cardIn 0.6s ease-out backwards;
}

@keyframes cardIn { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }

.glass-card:hover {
  transform:translateY(-4px);
  border-color:rgba(255,255,255,0.14);
  box-shadow:0 28px 90px rgba(0,0,0,0.35), 0 0 48px rgba(232,201,125,0.1);
}

/* Character cards */
.character-card {
  background:var(--glass-fill);
  border:1px solid var(--glass-border);
  border-radius:16px;
  overflow:hidden;
  padding:1.25rem;
  backdrop-filter:blur(16px);
  box-shadow:var(--glass-shadow);
  display:grid;
  grid-template-columns:100px 1fr;
  gap:1rem;
  animation:cardIn 0.7s ease-out backwards;
  transition:transform 0.35s, box-shadow 0.35s;
}

.character-card:hover {
  transform:translateY(-4px);
  box-shadow:0 20px 50px rgba(0,0,0,0.45);
}

.character-avatar {
  width:100px;
  height:100px;
  border-radius:12px;
  background:rgba(45,74,45,0.5);
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:3rem;
  border:1px solid var(--glass-border);
}

.character-body {
  display:flex;
  flex-direction:column;
  justify-content:center;
}

.character-name {
  font-family:'Inter Tight',sans-serif;
  font-size:1.2rem;
  color:var(--gold);
  margin:0 0 0.25rem;
}

.character-title {
  font-size:0.75rem;
  letter-spacing:0.12em;
  text-transform:uppercase;
  color:var(--blue);
  margin:0 0 0.75rem;
}

.character-desc {
  font-size:0.9rem;
  color:rgba(245,236,215,0.75);
  line-height:1.55;
  margin:0;
}

/* Back button styling */
.back-nav {
  display:flex;
  align-items:center;
  gap:0.5rem;
  margin-bottom:1.5rem;
  padding:0.75rem 1rem;
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:10px;
  cursor:pointer;
  transition:all 0.25s;
  font-size:0.9rem;
  color:rgba(245,236,215,0.7);
}

.back-nav:hover {
  background:rgba(255,255,255,0.08);
  border-color:rgba(232,201,125,0.3);
  color:var(--gold);
}

/* HUD/Stats */
.tc-hud {
  display:grid;
  grid-template-columns:1.4fr repeat(4,1fr) auto;
  gap:0.65rem;
  align-items:center;
  padding:0.85rem 1.1rem;
  margin:0.75rem 0 1.25rem;
  background:linear-gradient(135deg, rgba(45,74,45,0.25), rgba(0,0,0,0.5));
  border:1px solid rgba(255,255,255,0.08);
  border-radius:14px;
  box-shadow:0 8px 24px rgba(0,0,0,0.25);
  animation:hudIn 0.5s ease-out;
}

@keyframes hudIn { from { opacity:0; transform:translateY(-8px); } to { opacity:1; } }

.tc-hud-rank {
  font-family:'Inter',monospace;
  font-size:0.72rem;
  color:var(--gold);
  letter-spacing:0.06em;
}

.tc-hud-rank span {
  display:block;
  font-size:1.05rem;
  font-weight:600;
  color:var(--cream);
  margin-top:2px;
}

.tc-stat {
  text-align:center;
  padding:0.35rem 0.5rem;
  border-radius:8px;
  background:rgba(0,0,0,0.25);
  border:1px solid rgba(255,255,255,0.06);
}

.tc-stat b {
  display:block;
  font-size:1.1rem;
  font-weight:700;
  color:var(--cream);
}

.tc-stat small {
  font-size:0.62rem;
  text-transform:uppercase;
  letter-spacing:0.1em;
  color:rgba(240,237,230,0.45);
}

/* Progress and achievement styling */
.achievement {
  display:inline-flex;
  align-items:center;
  gap:0.5rem;
  padding:0.5rem 0.85rem;
  margin:0.25rem;
  background:rgba(232,201,125,0.08);
  border:1px solid var(--glass-border);
  border-radius:999px;
  font-size:0.8rem;
  animation:achieveIn 0.5s ease-out;
}

@keyframes achieveIn { from{opacity:0;transform:scale(0.95)} to{opacity:1;transform:scale(1)} }

/* Smooth animations - remove em-dashes from text */
.builder-statue {
  font-size:0.75rem;
  color:rgba(245,236,215,0.35);
  font-style:italic;
  padding:0.5rem 0;
  border-top:1px solid var(--glass-border);
  margin-top:1rem;
}

.tc-quest {
  background:linear-gradient(145deg, rgba(255,255,255,0.05), rgba(0,0,0,0.2));
  border:1px solid rgba(255,255,255,0.08);
  border-radius:16px;
  padding:1.35rem 1.5rem;
  margin:0.75rem 0;
  box-shadow:0 8px 24px rgba(0,0,0,0.25);
  animation:questIn 0.45s ease-out backwards;
}

@keyframes questIn { from { opacity:0; transform:translateX(-8px); } to { opacity:1; } }

.tc-quest-npc {
  font-family:'Inter Tight',sans-serif;
  font-size:0.7rem;
  color:var(--gold);
  letter-spacing:0.08em;
  margin-bottom:0.5rem;
}

.tc-quest-text {
  font-size:1.02rem;
  color:var(--cream);
  line-height:1.6;
  margin:0 0 1rem;
}

/* Flash messages */
.tc-flash {
  padding:1rem 1.25rem;
  border-radius:12px;
  margin:0 0 1rem;
  font-size:0.92rem;
  line-height:1.55;
  animation:flashIn 0.4s cubic-bezier(0.16,1,0.3,1);
  border:1px solid;
  box-shadow:0 8px 24px rgba(0,0,0,0.25);
}

@keyframes flashIn { from { opacity:0; transform:translateY(-6px); } to { opacity:1; } }

.tc-flash-ok {
  background:rgba(45,74,45,0.5);
  border-color:rgba(106,176,76,0.5);
  color:#b8e0a8;
}

.tc-flash-bad {
  background:rgba(60,28,28,0.45);
  border-color:rgba(201,74,74,0.45);
  color:#f0b0b0;
}

.tc-flash-info {
  background:rgba(30,40,55,0.5);
  border-color:rgba(123,163,184,0.4);
  color:#b8d4e8;
}

/* Charts */
.chart-container {
  background:var(--glass-fill);
  border:1px solid var(--glass-border);
  border-radius:16px;
  padding:1.25rem;
  backdrop-filter:blur(16px);
  box-shadow:var(--glass-shadow);
  margin:1rem 0;
}

.chart-title {
  font-family:'Inter Tight',sans-serif;
  font-size:1.25rem;
  color:var(--gold);
  letter-spacing:0.04em;
  margin-bottom:0.75rem;
}

a.hero-pill,a.hero-pill:visited{color:rgb(245,236,215)!important;text-decoration:none!important;}\n
.hero-version{
font-family:"Inter Tight",sans-serif;
font-size:.72rem;
font-weight:600;
letter-spacing:.18em;
text-transform:uppercase;
color:rgba(245,236,215,.55);
margin-left:12px;
}


@keyframes trustFloat{
0%{transform:translateY(0px);}
50%{transform:translateY(-10px);}
100%{transform:translateY(0px);}
}

.hero-scene-card{
animation:trustFloat 6s ease-in-out infinite;
}

.hero-scene{
perspective:1200px;
}

.hero-scene-card{
animation:trustFloat 6s ease-in-out infinite;
transform-style:preserve-3d;
transition:transform .7s cubic-bezier(.2,.8,.2,1);
cursor:pointer;
}

.hero-scene-card:hover{
transform:rotateY(12deg) rotateX(4deg) translateY(-8px);
}
</style>
"""

# Vibrant glassmorphism enhancements
ENHANCEMENT_CSS = """
<style>
/* ═════════════════════════════════════════════════════════════════════════ */
/* MINECRAFT PREMIUM AESTHETIC — VIBRANT GLASSMORPHISM                       */
/* ═════════════════════════════════════════════════════════════════════════ */

/* Dynamic backgrounds with vibrancy */
.stApp { 
  background: linear-gradient(135deg, 
    #0a0a0a 0%, 
    #1a1530 25%, 
    #0f1820 50%, 
    #1a0a1a 75%, 
    #050505 100%) !important;
  animation: bgShift 20s ease-in-out infinite;
}

@keyframes bgShift {
  0%, 100% { filter: hue-rotate(0deg) brightness(1); }
  50% { filter: hue-rotate(2deg) brightness(1.02); }
}

/* Vibrant glassmorphism cards */
.glass-card, .character-card, .dest-card, .lore-card, .artifact {
  background: rgba(255,255,255,0.08) !important;
  border: 1px solid rgba(232,201,125,0.25) !important;
  border-radius: 16px !important;
  backdrop-filter: blur(20px) saturate(180%) !important;
  box-shadow: 0 8px 32px rgba(232,201,125,0.15), 
              inset 0 1px 1px rgba(255,255,255,0.2) !important;
  transition: all 400ms cubic-bezier(0.34, 1.56, 0.64, 1) !important;
}

.glass-card:hover,
.character-card:hover,
.dest-card:hover,
.lore-card:hover,
.artifact:hover {
  transform: translateY(-12px) scale(1.02) !important;
  border-color: rgba(232,201,125,0.6) !important;
  box-shadow: 0 24px 64px rgba(232,201,125,0.25),
              0 0 40px rgba(231,139,60,0.2),
              inset 0 1px 1px rgba(255,255,255,0.4) !important;
  background: rgba(255,255,255,0.12) !important;
}

/* Vibrant buttons with interactions */
.stButton > button {
  background: linear-gradient(135deg,
    rgba(232,201,125,0.15) 0%,
    rgba(231,139,60,0.1) 100%) !important;
  border: 1.5px solid rgba(232,201,125,0.35) !important;
  color: #F5ECD7 !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  backdrop-filter: blur(16px) !important;
  transition: all 300ms cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  box-shadow: 0 4px 16px rgba(232,201,125,0.1),
              inset 0 1px 0 rgba(255,255,255,0.15) !important;
  position: relative;
  overflow: hidden;
}

.stButton > button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.2),
    transparent);
  transition: left 500ms ease;
}

.stButton > button:hover::before {
  left: 100%;
}

.stButton > button:hover {
  transform: translateY(-3px) !important;
  border-color: rgba(232,201,125,0.7) !important;
  box-shadow: 0 12px 32px rgba(232,201,125,0.25),
              0 0 20px rgba(231,139,60,0.15) !important;
  background: linear-gradient(135deg,
    rgba(232,201,125,0.25) 0%,
    rgba(231,139,60,0.15) 100%) !important;
}

.stButton > button:active {
  transform: translateY(-1px) scale(0.98) !important;
}

/* Minecraft-style text */
.world-title {
  font-family: 'Silkscreen', monospace !important;
  font-size: clamp(2rem, 5vw, 3.5rem) !important;
  background: linear-gradient(135deg,
    #FFD700 0%,
    #E8C97D 40%,
    #F2A6C8 70%,
    #7BA3B8 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  text-shadow: 0 0 40px rgba(232,201,125,0.4) !important;
  filter: drop-shadow(0 4px 12px rgba(232,201,125,0.3)) !important;
  animation: titlePulse 3s ease-in-out infinite;
}

@keyframes titlePulse {
  0%, 100% { filter: drop-shadow(0 4px 12px rgba(232,201,125,0.3)); }
  50% { filter: drop-shadow(0 8px 24px rgba(232,201,125,0.5)); }
}

/* Animated location cards */
.dest-card {
  animation: cardFloat 3s ease-in-out infinite;
}

@keyframes cardFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

/* Character cards with glow */
.character-card {
  position: relative;
}

.character-card::after {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: 12px;
  background: radial-gradient(ellipse at center,
    rgba(232,201,125,0.1) 0%,
    transparent 70%);
  animation: glow 2s ease-in-out infinite;
  pointer-events: none;
}

@keyframes glow {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

/* Vibrant feedback messages */
.tc-flash {
  animation: slideInUp 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
  border-radius: 12px !important;
  backdrop-filter: blur(16px) !important;
}

.tc-flash-ok {
  background: linear-gradient(135deg,
    rgba(106,176,76,0.2) 0%,
    rgba(76,153,76,0.15) 100%) !important;
  border-color: rgba(106,176,76,0.6) !important;
  box-shadow: 0 0 20px rgba(106,176,76,0.2) !important;
}

.tc-flash-bad {
  background: linear-gradient(135deg,
    rgba(201,74,74,0.2) 0%,
    rgba(153,76,76,0.15) 100%) !important;
  border-color: rgba(201,74,74,0.6) !important;
  box-shadow: 0 0 20px rgba(201,74,74,0.2) !important;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Interactive hover glow */
.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  opacity: 0;
  background: radial-gradient(600px at var(--mouse-x, 0px) var(--mouse-y, 0px),
    rgba(232,201,125,0.1),
    transparent 80%);
  pointer-events: none;
  transition: opacity 300ms ease;
}


/* Smooth page transitions */
.world-zone {
  animation: pageSlideIn 600ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes pageSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scene gradients - vibrant */
.scene-gradient-lr {
  background: linear-gradient(90deg,
    rgba(13,26,15,0.4) 0%,
    rgba(13,26,15,0.1) 60%,
    transparent 100%) !important;
}

/* Radio buttons styled */
.stRadio label {
  border-radius: 12px !important;
  border: 1px solid rgba(232,201,125,0.2) !important;
  background: rgba(255,255,255,0.03) !important;
  transition: all 300ms ease !important;
  cursor: pointer;
  backdrop-filter: blur(12px) !important;
}

.stRadio label:hover {
  border-color: rgba(232,201,125,0.5) !important;
  background: rgba(232,201,125,0.08) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(232,201,125,0.15) !important;
}

/* Progress and meters */
.metric-ring {
  background: rgba(232,201,125,0.08) !important;
  border: 1px solid rgba(232,201,125,0.3) !important;
  border-radius: 12px !important;
  backdrop-filter: blur(16px) !important;
  animation: popIn 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes popIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.score-bar-fill {
  background: linear-gradient(90deg,
    #E78B3C 0%,
    #E8C97D 50%,
    #FFD700 100%) !important;
  box-shadow: 0 0 16px rgba(232,201,125,0.4) !important;
}

/* Smooth all transitions */
* {
  transition: all 200ms ease !important;
}

button, .stButton > button {
  cursor: pointer !important;
}
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# DATA — CHARACTERS (Minecraft-themed)
# ─────────────────────────────────────────────────────────────────────────────
CHARACTERS = {
    "golem": {
        "emoji": "🤖",
        "name": "Iron Golem",
        "title": "Guardian of Verification",
        "personality": "Methodical. Checks sources. Never rushes.",
        "description": "Strong protector against false claims. Always verifies before accepting.",
        "speech": "I checked the records. This is verified.",
        "voice": "Calm. Measured. Each word matters.",
        "role": "Verification beats speed. When unsure, check.",
        "credibility": 92,
        "trust": 88,
        "rarity": "Legendary",
        "accent": "#7BA3B8",
    },
    "librarian": {
        "emoji": "📚",
        "name": "Librarian",
        "title": "Keeper of Evidence",
        "personality": "Precise. Loves sources. Cites everything.",
        "description": "Tends the Evidence Verification. Knows contradictions matter.",
        "speech": "Let me show you the source.",
        "voice": "Scholarly. Gentle. Always cites.",
        "role": "Good answers show their work.",
        "credibility": 95,
        "trust": 90,
        "rarity": "Epic",
        "accent": "#E8C97D",
    },
    "villager": {
        "emoji": "👤",
        "name": "Villager",
        "title": "Generally Trustworthy",
        "personality": "Friendly. Humble. Says 'I think' often.",
        "description": "Neighbor who admits uncertainty. Believable but not infallible.",
        "speech": "I heard this. Maybe check it though.",
        "voice": "Warm. Conversational. Sometimes unsure.",
        "role": "Healthy trust means verification still matters.",
        "credibility": 72,
        "trust": 70,
        "rarity": "Common",
        "accent": "#6ab04c",
    },
    "zombie": {
        "emoji": "🧟",
        "name": "Zombie Villager",
        "title": "Confidently Wrong",
        "personality": "LOUD. CERTAIN. WRONG.",
        "description": "Spreads hallucinations with total confidence.",
        "speech": "EVERYONE KNOWS THIS IS TRUE!!!",
        "voice": "Aggressive. Alarmist. No doubt.",
        "role": "Confidence is not truth.",
        "credibility": 8,
        "trust": 5,
        "rarity": "Corrupted",
        "accent": "#c94a4a",
    },
    "chicken": {
        "emoji": "🐔",
        "name": "Chicken Skeptic",
        "title": "Rejects Everything",
        "personality": "Panicked. Cries fake. Often wrong.",
        "description": "So afraid of being fooled, rejects good information too.",
        "speech": "Don't believe anything!",
        "voice": "Frantic. Alarmist.",
        "role": "Rejection is also a mistake.",
        "credibility": 25,
        "trust": 15,
        "rarity": "Uncommon",
        "accent": "#F2A6C8",
    },
}

DESTINATIONS = [
    {"loc": "library", "emoji": "📚", "title": "Evidence Verification", "desc": "Study verification and evidence.", "difficulty": "Calm", "time": "8 min", "grade": "grade-library", "thumb_pos": "center 35%"},
    {"loc": "forest", "emoji": "🌲", "title": "Hallucination Detection", "desc": "Spot false facts and wrong paths.", "difficulty": "Misty", "time": "5 min", "grade": "grade-forest", "thumb_pos": "60% 50%"},
    {"loc": "watchtower", "emoji": "🏰", "title": "Confidence Calibration", "desc": "Meet every voice in the village.", "difficulty": "Social", "time": "6 min", "grade": "grade-tower", "thumb_pos": "70% 40%"},
    {"loc": "training", "emoji": "⚔️", "title": "Training Simulator", "desc": "Live encounters. Make real choices.", "difficulty": "Active", "time": "12 min", "grade": "grade-training", "thumb_pos": "45% 55%"},
    {"loc": "castle", "emoji": "👑", "title": "Results Dashboard", "desc": "See your results and achievements.", "difficulty": "Finale", "time": "4 min", "grade": "grade-castle", "thumb_pos": "55% 30%"},
]

# ─────────────────────────────────────────────────────────────────────────────
# DATA — ASSESSMENT QUESTIONS
# correct_action: trust | verify | reject
# ─────────────────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "id": 1,
        "character": "librarian",
        "category": "Science",
        "statement": "Water boils at 100C at sea level under normal air pressure.",
        "correct": "trust",
        "explanation": "Well-established science backed by sources.",
        "hallucination": False,
    },
    {
        "id": 2,
        "character": "zombie",
        "category": "AI",
        "statement": "ChatGPT has a secret live connection to the entire internet.",
        "correct": "reject",
        "explanation": "False. AI systems predict text based on training. They don't have live internet access.",
        "hallucination": True,
    },
    {
        "id": 3,
        "character": "villager",
        "category": "Gaming",
        "statement": "I think creepers explode when they get close to you.",
        "correct": "trust",
        "explanation": "Common game knowledge stated humbly. Reasonable to trust.",
        "hallucination": False,
    },
    {
        "id": 4,
        "character": "zombie",
        "category": "History",
        "statement": "Napoleon invented the telephone in 1820!",
        "correct": "reject",
        "explanation": "Confidence doesn't make it true. Both facts are wrong.",
        "hallucination": True,
    },
    {
        "id": 5,
        "character": "golem",
        "category": "Technology",
        "statement": "This device uses lithium batteries. The manual confirms it.",
        "correct": "verify",
        "explanation": "Sounds right and there's a way to check. Smart to verify.",
        "hallucination": False,
    },
    {
        "id": 6,
        "character": "chicken",
        "category": "Science",
        "statement": "The Earth is flat! Don't trust NASA!",
        "correct": "reject",
        "explanation": "Misinformation. Not healthy skepticism.",
        "hallucination": True,
    },
    {
        "id": 7,
        "character": "zombie",
        "category": "Myths",
        "statement": "If you swallow gum, it stays in your stomach for seven years!",
        "correct": "reject",
        "explanation": "Old myth. Gum passes through like other food.",
        "hallucination": True,
    },
    {
        "id": 8,
        "character": "librarian",
        "category": "AI",
        "statement": "Large language models predict the next word based on patterns. They don't truly understand like humans.",
        "correct": "trust",
        "explanation": "Accurate and nuanced explanation of how AI works.",
        "hallucination": False,
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# DATA — ML CONCEPTS
# ─────────────────────────────────────────────────────────────────────────────
ML_CONCEPTS = [
    {
        "id": "accuracy",
        "title": "Accuracy",
        "icon": "spark",
        "analogy": "Out of 100 arrows you shoot, how many hit the target overall?",
        "example": "If you get 80 right out of 100 guesses, accuracy is 80%.",
        "story": "A guard who catches most troublemakers but also bothers innocent villagers — accuracy is the big picture score.",
    },
    {
        "id": "precision",
        "title": "Precision",
        "icon": "search",
        "analogy": "When you shout 'thief!', how often are you actually right?",
        "example": "High precision = few false alarms. You don't accuse innocent people much.",
        "story": "The Iron Golem only arrests when almost sure — that's high precision.",
    },
    {
        "id": "recall",
        "title": "Recall",
        "icon": "spark",
        "analogy": "Of all the real thieves in town, how many did you actually catch?",
        "example": "High recall = you miss fewer real problems, but might catch extra bystanders.",
        "story": "A watchman who never sleeps might catch every zombie — high recall.",
    },
    {
        "id": "f1",
        "title": "F1 Score",
        "icon": "shield",
        "analogy": "A fair grade when you care about BOTH not crying wolf AND not missing wolves.",
        "example": "Balances precision and recall into one number.",
        "story": "The village council uses F1 when they want balance, not extremes.",
    },
    {
        "id": "confusion",
        "title": "Confusion Matrix",
        "icon": "brain",
        "analogy": "A scoreboard with four boxes: right yes, right no, wrong yes, wrong no.",
        "example": "Shows exactly where your model trips up — false alarms vs missed dangers.",
        "story": "Like a battle report: trusted bad info, rejected good info, and both correct calls.",
    },
    {
        "id": "overfitting",
        "title": "Overfitting",
        "icon": "book",
        "analogy": "A student memorizes old exam answers but fails when questions change.",
        "example": "AI that aces training examples but fails on new real-world questions.",
        "story": "The zombie memorized phrases without understanding — works until the topic shifts.",
    },
    {
        "id": "underfitting",
        "title": "Underfitting",
        "icon": "user",
        "analogy": "A student never studies enough and performs badly everywhere.",
        "example": "A model too simple to learn patterns — always vague, always wrong.",
        "story": "A golem with broken eyes who guesses randomly — never learned the village rules.",
    },
    {
        "id": "generalization",
        "title": "Generalization",
        "icon": "trees",
        "analogy": "A student learns ideas, not just memorized answers — handles new questions.",
        "example": "Good AI should work on new data, not only old examples it trained on.",
        "story": "The Librarian teaches principles you can apply in any library in the world.",
    },
    {
        "id": "calibration",
        "title": "Confidence Calibration",
        "icon": "spark",
        "analogy": "When you're 80% sure, you should be right about 80% of the time.",
        "example": "Bad calibration = always says '99% sure' but wrong half the time (like Zombie Villager).",
        "story": "Trustworthy speakers match confidence to how often they're actually correct.",
    },
    {
        "id": "hallucinations_ml",
        "title": "Hallucinations (AI)",
        "icon": "brain",
        "analogy": "AI writes a beautiful answer that sounds perfect but made up the facts.",
        "example": "Fake book titles, wrong dates, invented quotes — smooth words, false world.",
        "story": "The Hallucination Detection is full of these — pretty paths that lead nowhere.",
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# DATA — ARCHETYPES
# ─────────────────────────────────────────────────────────────────────────────
ARCHETYPES = {
    "golem": {
        "name": "Iron Golem Thinker",
        "icon": "shield",
        "desc": "You verify before you believe. The village sleeps safely when you're on watch.",
        "strengths": "Strong fact-checking, resists hype, values evidence.",
        "weaknesses": "Sometimes slow to decide; may over-verify simple truths.",
        "advice": "Keep verifying — but remember trusted experts can save time on basics.",
    },
    "verifier": {
        "name": "Master Verifier",
        "icon": "search",
        "desc": "Your superpower is the middle path: check, then decide.",
        "strengths": "Balanced judgment, catches fake citations, uses sources.",
        "weaknesses": "Might hesitate when quick trust is okay.",
        "advice": "Teach others your verify habit — it's the best defense against AI mistakes.",
    },
    "librarian": {
        "name": "Librarian Analyst",
        "icon": "book",
        "desc": "You think like a researcher: sources, context, and careful reading.",
        "strengths": "Deep understanding, spots partial truths, loves evidence.",
        "weaknesses": "Can get lost in details.",
        "advice": "Share your sources out loud — it helps friends trust the right things.",
    },
    "scholar": {
        "name": "Village Scholar",
        "icon": "user",
        "desc": "You trust wisely when humility and consensus appear.",
        "strengths": "Good instincts, friendly discernment, efficient learner.",
        "weaknesses": "Watch for zombies wearing friendly masks.",
        "advice": "When someone sounds TOO sure, switch to verify mode.",
    },
    "zombie": {
        "name": "Zombie Follower",
        "icon": "x",
        "desc": "Confident voices sway you. Time to build skepticism muscles!",
        "strengths": "Open to stories, enthusiastic learner once trained.",
        "weaknesses": "Confuses loudness with truth; trusts hallucinations.",
        "advice": "Pause when you feel 100% sure from one source. Ask: where's the proof?",
    },
    "chicken": {
        "name": "Chicken Skeptic",
        "icon": "spark",
        "desc": "You reject almost everything — even good info gets clucked away.",
        "strengths": "Hard to fool with scams, cautious by nature.",
        "weaknesses": "Misses true facts; rejects experts and evidence.",
        "advice": "Skepticism + evidence = power. Don't reject — verify, then decide.",
    },
}

LOCATIONS = {
    "landing": {"name": "Village Gates", "grade": "grade-hero", "icon": "map"},
    "village_square": {"name": "Village Square", "grade": "grade-square", "icon": "map"},
    "library": {"name": "Evidence Verification", "grade": "grade-library", "icon": "book"},
    "forest": {"name": "Hallucination Detection", "grade": "grade-forest", "icon": "trees"},
    "watchtower": {"name": "Confidence Calibration", "grade": "grade-tower", "icon": "tower"},
    "training": {"name": "Training Simulator", "grade": "grade-training", "icon": "swords"},
    "castle": {"name": "Results Dashboard", "grade": "grade-castle", "icon": "castle"},
}

HALLUCINATION_LESSONS = [
    {"title": "What is a hallucination?", "text": "When AI says something convincing that is NOT true — a dream dressed as fact.", "icon": "brain"},
    {"title": "Why do they happen?", "text": "AI predicts likely words. Smooth beats correct — like autocomplete with confidence.", "icon": "spark"},
    {"title": "Confidence ≠ evidence", "text": "The Zombie Villager is loud but wrong. Volume is not proof. Check sources.", "icon": "x"},
    {"title": "Why LLMs make mistakes", "text": "They learn text patterns, not lived experience. Names, dates, quotes get invented.", "icon": "search"},
    {"title": "Why verification matters", "text": "One quick check stops misinformation from spreading through the whole village.", "icon": "check"},
]



HALLUCINATION_SCENARIOS = [
    {
        "question": "Why do we yawn?",
        "response": "Yawning mainly happens because your brain runs low on oxygen and needs more air.",
        "correct": 1,
        "feedback": "Humans believe this because it sounds logical and has been repeated for years. AI may repeat popular explanations even when science is still uncertain."
    },
    {
        "question": "Why do we dream?",
        "response": "Dreams are the brain deleting unnecessary memories from the day.",
        "correct": 1,
        "feedback": "Humans like simple explanations for complex processes. AI often presents one theory as if it were proven fact."
    },
    {
        "question": "Why do cats purr?",
        "response": "Cats only purr when they are happy and relaxed.",
        "correct": 1,
        "feedback": "People often associate purring with happiness. AI may ignore important exceptions such as stress pain or fear."
    },
    {
        "question": "Do we use only 10% of our brain?",
        "response": "Humans normally use only about 10% of their brain capacity.",
        "correct": 2,
        "feedback": "This myth is extremely common. AI can repeat popular misinformation because it appears frequently online."
    },
    {
        "question": "Why is the sky blue?",
        "response": "The sky reflects the blue color of the oceans.",
        "correct": 2,
        "feedback": "The answer sounds intuitive. Humans love simple visual explanations even when they are wrong."
    }
]


HUNTER_RANKS = [
    (95, "🏆 Hallucination Hunter"),
    (80, "🛡️ Truth Guardian"),
    (60, "🔍 Analyst"),
    (40, "🧠 Investigator"),
    (20, "👀 Observer"),
    (0,  "🌱 Villager"),
]

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "location": "landing",
        "game_started": False,
        "question_order": [],
        "question_index": 0,
        "answers": [],
        "last_feedback": None,
        "show_feedback": False,
        "ml_expanded": None,
        "forest_lesson": 0,
        "forest_stage": "intro",
        "forest_score": 0,
        "forest_question": 0,
        "forest_feedback": None,
        "forest_answers": [],
        "scores": {
            "literacy": 0,
            "trust": 0,
            "verification": 0,
            "hallucination": 0,
            "critical": 0,
        },
        "questions_answered": 0,
        "transition_flash": False,
        "visited_locs": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


import json
from pathlib import Path

SAVE_PATH = Path(__file__).resolve().parent / "trustcraft_save.json"

RANKS = [
    (0, "Novice"),
    (120, "Researcher"),
    (280, "Verifier"),
    (450, "Analyst"),
    (650, "Guardian"),
    (900, "Truthkeeper"),
]

ACHIEVEMENT_DEFS = {
    "source_hunter": {"name": "Source Hunter", "desc": "Complete Library verification quest", "icon": "book", "xp": 40},
    "hallucination_slayer": {"name": "Hallucination Slayer", "desc": "Reject 5 hallucinations correctly", "icon": "x", "xp": 50},
    "truth_seeker": {"name": "Truth Seeker", "desc": "Reach Researcher rank", "icon": "check", "xp": 30},
    "evidence_master": {"name": "Evidence Master", "desc": "Score 80%+ on verification", "icon": "shield", "xp": 45},
    "calibration_expert": {"name": "Calibration Expert", "desc": "Complete Watchtower calibration", "icon": "spark", "xp": 40},
    "ai_guardian": {"name": "AI Guardian", "desc": "Unlock Results Dashboard", "icon": "castle", "xp": 60},
}

REGION_META = {
    "village_square": {"purpose": "Introduction to AI literacy", "features": "NPC conversations · tutorials · reputation"},
    "library": {"purpose": "Knowledge and verification", "features": "Source validation · citations · evidence"},
    "forest": {"purpose": "Detect misinformation", "features": "Deceptive paths · fake claims · consequences"},
    "watchtower": {"purpose": "Confidence calibration", "features": "Prediction · sliders · probability"},
    "training": {"purpose": "AI fundamentals", "features": "ML simulations · confusion matrix · practice"},
    "castle": {"purpose": "Final assessment", "features": "Complex scenarios · unlock by progression"},
}

LIBRARY_QUEST = {
    "story": "A villager claims a viral health fact is backed by science.",
    "claim": "A peer-reviewed study proves this supplement cures all colds.",
    "sources": ["National health agency report", "Anonymous blog post", "University meta-analysis (DOI listed)"],
    "correct": 2,
    "xp": 35,
}

FOREST_PATHS = [
    {"id": "whisper", "label": "Path of Whispers", "trap": True, "text": "A zombie villager shouts fake news. You followed the noise.", "penalty": 15},
    {"id": "lantern", "label": "Lantern Trail", "trap": False, "text": "You found a verified signpost. +XP", "xp": 25},
    {"id": "mist", "label": "Misty Shortcut", "trap": True, "text": "Herobrine was here! (He wasn't.) Misinformation spread.", "penalty": 10},
]

WATCHTOWER_QUEST = {
    "question": "Water boils at 100°C at sea level. How confident are you (0–100)?",
    "truth": 95,
    "xp": 30,
}

VILLAGE_TUTORIAL = [
    {"npc": "villager", "text": "I think it might rain — the clouds look dark.", "answer": "verify", "why": "Reasonable but check weather data."},
    {"npc": "zombie", "text": "AI NEVER makes mistakes! Trust everything!", "answer": "reject", "why": "Confident hype is a red flag."},
]


def rank_for_xp(xp: int) -> str:
    r = RANKS[0][1]
    for threshold, name in RANKS:
        if xp >= threshold:
            r = name
    return r


def load_save_into_session():
    if st.session_state.get("_save_loaded"):
        return
    defaults = {
        "knowledge_xp": 0,
        "trust_score": 50,
        "reputation": 50,
        "achievements": [],
        "quests_done": [],
        "forest_penalty": 0,
        "hallucinations_rejected": 0,
        "calibration_done": False,
        "audio_on": False,
        "cm_history": {"tp": 0, "fp": 0, "fn": 0, "tn": 0},
        "world_reputation": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if SAVE_PATH.exists():
        try:
            data = json.loads(SAVE_PATH.read_text())
            for k, v in data.items():
                if k in defaults:
                    st.session_state[k] = v
        except Exception:
            pass
    st.session_state._save_loaded = True


def save_session_to_disk():
    data = {
        "knowledge_xp": st.session_state.get("knowledge_xp", 0),
        "trust_score": st.session_state.get("trust_score", 50),
        "reputation": st.session_state.get("reputation", 50),
        "achievements": st.session_state.get("achievements", []),
        "quests_done": st.session_state.get("quests_done", []),
        "questions_answered": st.session_state.get("questions_answered", 0),
        "visited_locs": st.session_state.get("visited_locs", []),
        "answers": st.session_state.get("answers", []),
        "scores": st.session_state.get("scores", {}),
        "forest_penalty": st.session_state.get("forest_penalty", 0),
        "hallucinations_rejected": st.session_state.get("hallucinations_rejected", 0),
        "calibration_done": st.session_state.get("calibration_done", False),
        "audio_on": st.session_state.get("audio_on", False),
        "cm_history": st.session_state.get("cm_history", {}),
    }
    try:
        SAVE_PATH.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


def unlock_achievement(key: str):
    ach = st.session_state.get("achievements", [])
    if key not in ach and key in ACHIEVEMENT_DEFS:
        st.session_state.achievements = ach + [key]
        st.session_state.new_achievement = ACHIEVEMENT_DEFS[key]["name"]
        award_xp(ACHIEVEMENT_DEFS[key]["xp"], f"Achievement: {ACHIEVEMENT_DEFS[key]['name']}")


def award_xp(amount: int, reason: str = ""):
    st.session_state.knowledge_xp = st.session_state.get("knowledge_xp", 0) + amount
    old_rank = rank_for_xp(st.session_state.knowledge_xp - amount)
    new_rank = rank_for_xp(st.session_state.knowledge_xp)
    if new_rank != old_rank and new_rank != "Novice":
        st.session_state.rank_up = new_rank
        if new_rank == "Researcher":
            unlock_achievement("truth_seeker")
    st.session_state.last_xp_reason = reason
    save_session_to_disk()


def update_trust_score(delta: int):
    st.session_state.trust_score = max(0, min(100, st.session_state.get("trust_score", 50) + delta))
    save_session_to_disk()


def update_cm_from_answer(correct: bool, choice: str, hallucination: bool):
    cm = st.session_state.get("cm_history", {"tp": 0, "fp": 0, "fn": 0, "tn": 0})
    if correct and choice in ("trust", "verify"):
        cm["tp"] = cm.get("tp", 0) + 1
    elif not correct and choice == "trust":
        cm["fp"] = cm.get("fp", 0) + 1
    elif not correct and choice == "reject":
        cm["fn"] = cm.get("fn", 0) + 1
    elif correct and choice == "reject":
        cm["tn"] = cm.get("tn", 0) + 1
    st.session_state.cm_history = cm
    if hallucination and choice == "reject" and correct:
        st.session_state.hallucinations_rejected = st.session_state.get("hallucinations_rejected", 0) + 1
        if st.session_state.hallucinations_rejected >= 5:
            unlock_achievement("hallucination_slayer")


def record_decision(choice: str, correct: bool, correct_action: str, hallucination: bool, explanation: str, xp: int = 15):
    """Central decision engine — updates progression, CM, save."""
    st.session_state.answers = st.session_state.get("answers", []) + [{
        "choice": choice, "correct": correct, "correct_action": correct_action,
        "hallucination": hallucination,
    }]
    st.session_state.questions_answered = len(st.session_state.answers)
    update_cm_from_answer(correct, choice, hallucination)
    compute_scores()
    if correct:
        award_xp(xp, "Correct judgment")
        update_trust_score(3)
        tc_flash(explanation if isinstance(explanation, str) else "Correct judgment.", "ok")
    else:
        update_trust_score(-5)
        st.session_state.reputation = max(0, st.session_state.get("reputation", 50) - 8)
        tc_flash(explanation if isinstance(explanation, str) else "Review the evidence and try again.", "bad")
    if st.session_state.scores.get("verification", 0) >= 80:
        unlock_achievement("evidence_master")
    save_session_to_disk()


def castle_unlocked() -> bool:
    xp = st.session_state.get("knowledge_xp", 0)
    training = st.session_state.get("questions_answered", 0) >= 5
    return xp >= 180 and training


def render_progress_hud():
    load_save_into_session()
    xp = st.session_state.get("knowledge_xp", 0)
    rank = rank_for_xp(xp)
    trust = st.session_state.get("trust_score", 50)
    rep = st.session_state.get("reputation", 50)
    ach_count = len(st.session_state.get("achievements", []))

    new_ach = st.session_state.pop("new_achievement", None)
    if new_ach:
        tc_flash(f"Medal unlocked: {new_ach}", "ok")
    rank_up = st.session_state.pop("rank_up", None)
    if rank_up:
        tc_flash(f"Rank up — you are now a {rank_up}!", "ok")

    tc_show_flash()
    st.markdown(
        tc_hud_html(rank, xp, trust, rep, ach_count, len(ACHIEVEMENT_DEFS)),
        unsafe_allow_html=True,
    )

    audio = st.session_state.get("audio_on", False)
    a1, a2 = st.columns([5, 1])
    with a2:
        if st.toggle("Ambient", value=audio, key="audio_toggle"):
            st.session_state.audio_on = True
        else:
            st.session_state.audio_on = False
        save_session_to_disk()


def render_live_confusion_matrix():
    cm = st.session_state.get("cm_history", {"tp": 0, "fp": 0, "fn": 0, "tn": 0})
    tp, fp, fn, tn = cm.get("tp", 0), cm.get("fp", 0), cm.get("fn", 0), cm.get("tn", 0)
    cols = st.columns(4)
    for col, label, val, color in zip(
        cols,
        ["True Positive", "False Positive", "False Negative", "True Negative"],
        [tp, fp, fn, tn],
        ["#6ab04c", "#c94a4a", "#E78B3C", "#7BA3B8"],
    ):
        with col:
            st.markdown(
                f'<div class="metric-ring" style="border-color:{color}40">'
                f'<div class="val" style="color:{color}">{val}</div>'
                f'<div class="lbl">{label}</div></div>',
                unsafe_allow_html=True,
            )
    fig = go.Figure(data=go.Heatmap(
        z=[[tp, fp], [fn, tn]],
        x=["Predicted Yes", "Predicted No"],
        y=["Actually Yes", "Actually No"],
        colorscale=[[0, "#0a0a0a"], [0.5, "#2D4A2D"], [1, "#E8C97D"]],
        text=[[str(tp), str(fp)], [str(fn), str(tn)]],
        texttemplate="%{text}",
        textfont={"size": 16, "color": "#FAFAFA", "family": "JetBrains Mono"},
        showscale=False,
    ))
    render_premium_chart(plotly_theme(fig, "", 260), "Live Judgment Matrix", "Updates after every decision")


def render_kingdom_map():
    """Interactive world map with back button."""
    st.markdown(f'''
    <div style="max-width:1200px;margin:2rem auto;padding:0 1rem">
      <p style="font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:1rem">World Map</p>
      <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.5rem;color:#F5ECD7;margin-bottom:0.5rem">Travel to a new region</h3>
      <p style="font-size:0.95rem;color:rgba(245,236,215,0.65);margin-bottom:2rem">Progress saves automatically.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    regions = [
        {"loc": "village_square", "emoji": "🏘️", "title": "Village Square", "grade": "grade-square"},
        *[{"loc": d["loc"], "emoji": d["emoji"], "title": d["title"], "grade": d["grade"]} for d in DESTINATIONS],
    ]
    
    cols = st.columns(3)
    for i, r in enumerate(regions):
        status, pct = _completion_for_loc(r["loc"])
        locked = r["loc"] == "castle" and not castle_unlocked()
        with cols[i % 3]:
            st.markdown(f'''
            <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.5rem;margin-bottom:1rem;opacity:{'0.5' if locked else '1'}">
              <div style="font-size:3rem;margin-bottom:0.75rem">{r['emoji']}</div>
              <h4 style="font-family:'Inter Tight',sans-serif;font-size:1.15rem;color:var(--gold);margin-bottom:0.5rem">{r['title']}</h4>
              <div style="font-size:0.8rem;color:rgba(245,236,215,0.5);margin-bottom:1rem">{status} {pct}%</div>
              {'<p style="color:var(--lantern);font-size:0.8rem">🔒 Reach 180 XP + complete 5 training rounds</p>' if locked else ''}
            </div>
            ''', unsafe_allow_html=True)
            if not locked and st.button(f"Enter {r['title'].split()[0]}", key=f"kingdom_{r['loc']}", use_container_width=True):
                travel_to(r["loc"])


def render_mentor_panel(char_key: str):
    """Display character mentor with avatar and interactive options."""
    c = CHARACTERS[char_key]
    
    # Character card with enhanced styling
    avatar_url = get_avatar_url(c['name'].split()[0].lower())
    
    st.markdown(f'''
    <div class="glass-card" style="text-align:center;padding:2rem;animation:popIn 500ms cubic-bezier(0.34, 1.56, 0.64, 1)">
      <div style="font-size:4rem;margin-bottom:1rem;animation:titlePulse 3s ease-in-out infinite">{c['emoji']}</div>
      <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.3rem;color:var(--gold);margin:0 0 0.5rem">{c['name']}</h3>
      <p style="color:rgba(245,236,215,0.7);font-size:0.9rem;margin:0 0 1rem">{c['title']}</p>
      <p style="color:rgba(245,236,215,0.6);font-size:0.85rem;margin:0;line-height:1.6">{c['personality']}</p>
      <div style="margin-top:1.5rem;display:flex;justify-content:center;gap:0.5rem">
        <span style="display:inline-block;padding:0.35rem 0.75rem;background:rgba(232,201,125,0.1);border:1px solid rgba(232,201,125,0.3);border-radius:8px;font-size:0.75rem;color:rgba(232,201,125,0.8)">
          Trust: {c.get('trust', 70)}/100
        </span>
        <span style="display:inline-block;padding:0.35rem 0.75rem;background:rgba(232,201,125,0.1);border:1px solid rgba(232,201,125,0.3);border-radius:8px;font-size:0.75rem;color:rgba(232,201,125,0.8)">
          {c.get('rarity', 'Common')}
        </span>
      </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Interactive options
    if char_key == "golem":
        if st.button(f"🛡️ {c['name']}: Start Verification", key="golem_quest", use_container_width=True):
            travel_to("training")
    elif char_key == "librarian":
        if "library_quest" in st.session_state.get("quests_done", []):
            st.markdown('<p style="text-align:center;color:rgba(232,201,125,0.8);font-size:0.85rem;margin-top:1rem">✨ Research library unlocked</p>', unsafe_allow_html=True)
        else:
            if st.button(f"📚 {c['name']}: Learn Source Validation", key="lib_quest", use_container_width=True):
                travel_to("library")
    elif char_key == "villager":
        st.markdown(f'''
        <p style="text-align:center;color:rgba(245,236,215,0.7);font-size:0.9rem;margin-top:1rem;line-height:1.6">
          "{c['speech']}"<br><em style="color:rgba(245,236,215,0.5);font-size:0.8rem">— {c['voice']}</em>
        </p>
        ''', unsafe_allow_html=True)


def render_interactive_lesson(title: str, story: str, example: str, decision_label: str, options: list, correct_idx: int, explanation: str, xp: int = 20):

    key = f"lesson_{abs(hash(title)) % 99999}"

    st.markdown(
        f'<div class="tc-quest"><p class="tc-quest-npc">Interactive lesson</p>'
        f'<h3 class="tc-section-title" style="margin-bottom:0.75rem">{title}</h3>'
        f'<p class="tc-quest-text"><strong>Question</strong> — {story}</p>'
        f'<p class="tc-quest-text"><strong>AI Answer</strong> — {example}</p>'
        f'<p class="tc-quest-text"><strong>Your Decision</strong> — {decision_label}</p></div>',
        unsafe_allow_html=True,
    )

    if st.session_state.get(f"{key}_feedback"):

        fb = st.session_state[f"{key}_feedback"]

        st.success("Correct Decision" if fb["correct"] else "Think Again")
        st.info(fb["explanation"])
        return

    choice = st.radio(
        "Your call",
        options,
        key=key,
        label_visibility="collapsed"
    )

    if st.button("Submit judgment", key=f"submit_{key}", use_container_width=True):

        correct = options.index(choice) == correct_idx

        action = ["trust", "verify", "reject"][correct_idx]

        record_decision(
            action,
            correct,
            action,
            False,
            explanation,
            xp
        )

        st.session_state[f"{key}_feedback"] = {
            "correct": correct,
            "explanation": explanation,
        }

        st.rerun()


def cinematic_scene(grade: str, inner_html: str, min_h: str = "min(88vh,900px)", wide_content: bool = False) -> str:
    content_style = "max-width:100%;" if wide_content else ""
    return f"""
    <div class="scene" style="min-height:{min_h}">
      <div class="scene-bg {grade}" style="{scene_style(grade)}"></div>
      <div class="scene-gradient-lr"></div>
      <div class="scene-content" style="{content_style}">{inner_html}</div>
    </div>"""


def founder_portrait_html() -> str:
    ic = icon("spark", 32, C_GOLD)
    return f"""
    <div class="founder-frame">
      <div style="display:flex;align-items:center;justify-content:center;height:88px;background:rgba(232,201,125,0.06)">{ic}</div>
      <div class="founder-caption">The Builder · circa TrustCraft</div>
    </div>"""


def lore_card_html(char_key: str, delay: int = 0) -> str:
    """Character card with emoji and premium styling."""
    c = CHARACTERS[char_key]
    rare = " rare" if c.get("rarity") in ("Legendary", "Mythic", "Epic") else ""
    return f"""
    <div class="character-card" style="animation-delay:{delay * 0.08}s">
      <div class="character-avatar">{c['emoji']}</div>
      <div class="character-body">
        <div class="character-name">{c['name']}</div>
        <div class="character-title">{c['title']}</div>
        <p style="font-size:0.85rem;color:rgba(245,236,215,0.75);margin:0.5rem 0 0">{c['description']}</p>
      </div>
    </div>"""


def loc_card_html(dest: dict) -> str:
    ic = icon(dest["icon"], 22, C_GOLD)
    return f"""
    <div class="dest-card">
      <div class="dest-thumb {dest['grade']}" style="{scene_style(dest['grade'])}"></div>
      <div class="dest-body">
        <div class="dest-head"><div class="dest-icon">{ic}</div><h3>{dest['title']}</h3></div>
        <p class="dest-desc">{dest['desc']}</p>
        <div class="dest-meta"><span>{dest['difficulty']}</span><span>{dest['time']}</span></div>
      </div>
    </div>"""


def render_premium_chart(fig, title: str, subtitle: str = "TrustCraft Analytics"):
    st.markdown(
        f'<div class="chart-analytics"><div class="chart-analytics-header">'
        f'<span class="chart-analytics-title">{title}</span>'
        f'<span class="chart-analytics-sub">{subtitle}</span></div>'
        f'<div class="chart-analytics-body">',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div></div>", unsafe_allow_html=True)


def plotly_theme(fig, title: str = "", height: int = 320):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": C_CREAM, "family": "Inter", "size": 12},
        height=height,
        margin=dict(l=52, r=52, t=24, b=44),
        title=None,
        hoverlabel=dict(bgcolor="rgba(13,26,15,0.92)", font_color=C_CREAM, bordercolor=C_GOLD),
    )
    fig.update_traces(
        textfont=dict(family="JetBrains Mono", size=13, color=C_CREAM),
    )
    return fig


def get_achievements(scores, answers):
    ach = []
    if scores.get("literacy", 0) >= 70:
        ach.append(("Truth Seeker", "check"))
    if scores.get("hallucination", 0) >= 80:
        ach.append(("Hallucination Hunter", "shield"))
    if scores.get("verification", 0) >= 75:
        ach.append(("Master Verifier", "search"))
    if len(answers) >= 10:
        ach.append(("Training Graduate", "spark"))
    if not ach:
        ach.append(("Pathfinder", "map"))
    return ach


def _completion_for_loc(loc: str) -> tuple[str, int]:
    """Return (status label, percent) for world map cards."""
    q = st.session_state.get("questions_answered", 0)
    quests = set(st.session_state.get("quests_done", []))
    visited = set(st.session_state.get("visited_locs", []))
    if loc == "library" and "library_quest" in quests:
        return ("Complete", 100)
    if loc == "forest" and "forest_path" in quests:
        return ("Complete", 100)
    if loc == "watchtower" and st.session_state.get("calibration_done"):
        return ("Complete", 100)
    if loc == "training" and q >= 5:
        return ("Complete", 100)
    if loc == "castle" and castle_unlocked():
        return ("Unlocked", 100)
    if loc == "training" and q > 0:
        return ("In progress", min(99, q * 18))
    if loc == "library" and loc in visited:
        return ("In progress", 55)
    if loc in visited:
        return ("In progress", 45)
    return ("Not started", 0)


def build_startup_landing() -> str:
    """Premium Bay Area AI startup landing — self-contained scroll experience."""
    hero_bg = SCENE_GRADIENTS["hero"]
    progress = st.session_state.get("questions_answered", 0)

    world_cards = ""
    showcase = [
        {"loc": "village_square", "icon": "map", "title": "Village Square", "desc": "Central hub for navigation and village lore.", "diff": "Explorer", "time": "3 min"},
        *[{"loc": d["loc"], "icon": d["icon"], "title": d["title"], "desc": d["desc"], "diff": d["difficulty"], "time": d["time"]} for d in DESTINATIONS],
    ]
    for item in showcase:
        status, pct = _completion_for_loc(item["loc"])
        ic = icon(item["icon"], 22, "#FAFAFA")
        world_cards += f"""
        <article class="saas-card tilt-card" data-tilt>
          <div class="saas-card-top">
            <div class="saas-icon">{ic}</div>
            <span class="saas-status saas-status-{'done' if pct==100 else 'prog' if pct else 'new'}">{status}</span>
          </div>
          <h3>{item['title']}</h3>
          <p>{item['desc']}</p>
          <div class="saas-meta">
            <span>{item['diff']}</span><span>{item['time']}</span>
          </div>
          <div class="saas-progress"><div class="saas-progress-fill" style="width:{pct}%"></div></div>
          <button class="saas-card-btn magnetic" data-loc="{item['loc']}">Open</button>
        </article>"""

    char_cards = ""
    for key in ["golem", "librarian", "villager"]:
        c = CHARACTERS[key]
        ic = icon(c["icon"], 48, c.get("accent", "#FAFAFA"))
        char_cards += f"""
        <article class="char-cine tilt-card" data-tilt>
          <div class="char-cine-visual">{ic}</div>
          <div class="char-cine-body">
            <span class="char-cine-rarity">{c['rarity']}</span>
            <h3>{c['name']}</h3>
            <p class="char-cine-role">{c['title']}</p>
            <p class="char-cine-story">{c['description']}</p>
            <p class="char-cine-lesson"><strong>Lesson</strong> {c['role']}</p>
            <div class="char-cine-scores">
              <span>Trust {c['trust']}%</span><span>Credibility {c['credibility']}%</span>
            </div>
          </div>
        </article>"""

    journey_steps = """
    <div class="journey-step reveal-child"><span>01</span><h4>Encounter</h4><p>Meet villagers spreading truth, myths, and hallucinations.</p></div>
    <div class="journey-step reveal-child"><span>02</span><h4>Decide</h4><p>Trust, verify, or reject — every choice trains judgment.</p></div>
    <div class="journey-step reveal-child"><span>03</span><h4>Measure</h4><p>See literacy scores, archetypes, and verification habits.</p></div>
    """

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Inter',system-ui,sans-serif;background:#050505;color:#FAFAFA;overflow-x:hidden}}

/* ── Nav ── */
#tc-nav{{
  position:fixed;top:0;left:0;right:0;z-index:1000;
  display:flex;align-items:center;justify-content:space-between;
  padding:1rem clamp(1.5rem,4vw,3rem);
  background:rgba(5,5,5,0.4);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
  border-bottom:1px solid rgba(255,255,255,0.06);
  transition:padding .4s cubic-bezier(.4,0,.2,1),background .4s,box-shadow .4s;
}}
#tc-nav.scrolled{{padding:.65rem clamp(1.5rem,4vw,3rem);background:rgba(5,5,5,0.85);box-shadow:0 8px 40px rgba(0,0,0,.4)}}
.nav-logo{{font-family:'Inter Tight',sans-serif;font-weight:700;font-size:1.15rem;letter-spacing:-.03em;color:#FAFAFA;text-decoration:none}}
.nav-links{{display:flex;gap:1.75rem;list-style:none}}
.nav-links a{{color:rgba(250,250,250,.65);text-decoration:none;font-size:.875rem;font-weight:500;transition:color .2s}}
.nav-links a:hover{{color:#FAFAFA}}
.nav-actions{{display:flex;align-items:center;gap:1rem}}
.nav-link-ext{{color:rgba(250,250,250,.5);font-size:.8rem;text-decoration:none}}
.nav-cta{{
  font-family:'Inter',sans-serif;font-size:.875rem;font-weight:600;
  padding:.55rem 1.25rem;border-radius:999px;border:none;cursor:pointer;
  background:#FAFAFA;color:#050505;transition:transform .3s cubic-bezier(.34,1.56,.64,1),box-shadow .3s;
}}
.nav-cta:hover{{box-shadow:0 8px 30px rgba(255,255,255,.2)}}

/* ── Sections ── */
.tc-section{{position:relative;padding:clamp(5rem,12vh,8rem) clamp(1.5rem,5vw,4rem)}}
.section-inner{{max-width:1200px;margin:0 auto}}
.section-label{{font-size:.7rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:rgba(250,250,250,.45);margin-bottom:1rem}}
.section-title{{font-family:'Inter Tight',sans-serif;font-size:clamp(2rem,4vw,3rem);font-weight:600;letter-spacing:-.03em;line-height:1.05;margin-bottom:1rem}}
.section-desc{{font-size:1.05rem;line-height:1.7;color:rgba(250,250,250,.6);max-width:560px}}

.reveal{{opacity:0;transform:translateY(32px) scale(.98);filter:blur(10px);transition:none}}
.reveal.visible{{animation:revealIn .85s cubic-bezier(.16,1,.3,1) forwards}}
.reveal-child{{opacity:0;transform:translateY(20px)}}
.reveal.visible .reveal-child{{animation:revealIn .7s cubic-bezier(.16,1,.3,1) forwards}}
.reveal.visible .reveal-child:nth-child(2){{animation-delay:.08s}}
.reveal.visible .reveal-child:nth-child(3){{animation-delay:.16s}}
.reveal.visible .reveal-child:nth-child(4){{animation-delay:.24s}}
@keyframes revealIn{{to{{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}}}

/* ── HERO ── */
#hero{{min-height:100vh;padding:0;display:flex;align-items:stretch;overflow:hidden}}
.hero-stack{{position:absolute;inset:0}}
.hero-bg{{
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px),
    {hero_bg};
  background-size:28px 28px,28px 28px,100% 100%;
  animation:heroBreathe 22s ease-in-out infinite;
  transform:scale(1.02);transform-origin:center;
}}
.hero-clouds{{
  background:radial-gradient(ellipse 40% 20% at 20% 30%,rgba(255,255,255,.06),transparent),
    radial-gradient(ellipse 35% 18% at 70% 25%,rgba(255,255,255,.05),transparent);
  animation:cloudDrift 45s linear infinite;
  opacity:.7;
}}
@keyframes cloudDrift{{from{{transform:translateX(0)}}to{{transform:translateX(4%)}}}}
@keyframes heroBreathe{{0%,100%{{transform:scale(1.02)}}50%{{transform:scale(1.04)}}}}
.hero-glass{{
  background:linear-gradient(105deg,rgba(0,0,0,.82) 0%,rgba(0,0,0,.55) 38%,rgba(0,0,0,.2) 68%,transparent 100%);
}}
.hero-fx{{z-index:3}}
.hero-rays{{
  background:linear-gradient(118deg,transparent 40%,rgba(255,220,160,.08) 48%,transparent 56%);
  animation:raysMove 14s ease-in-out infinite alternate;
}}
@keyframes raysMove{{from{{opacity:.4;transform:translateX(-1%)}}to{{opacity:.95;text-shadow:0 0 10px rgba(255,232,177,.12);transform:translateX(1%)}}}}
.hero-canvas{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}}
.hero-water{{
  bottom:0;top:auto;height:35%;
  background:linear-gradient(0deg,rgba(123,163,184,.12),transparent);
  animation:waterPulse 7s ease-in-out infinite;
}}
@keyframes waterPulse{{0%,100%{{opacity:.35}}50%{{opacity:.7}}}}
.hero-lantern{{position:absolute;width:8px;height:11px;border-radius:50% 50% 40% 40%;
  background:radial-gradient(circle,#FFE4A8,#E78B3C,transparent);box-shadow:0 0 20px rgba(231,139,60,.7);
  animation:flicker 3s ease-in-out infinite alternate}}
@keyframes flicker{{from{{opacity:.4}}to{{opacity:1}}}}

.hero-stage{{
  position:relative;z-index:20;flex:1;display:flex;align-items:center;
  padding:7rem clamp(1.5rem,5vw,4rem) 4rem;
}}
.hero-wordmark-wrap{{
  position:absolute;left:clamp(1.5rem,5vw,4rem);top:22%;
  z-index:100;pointer-events:none;
  animation:wordmarkFloat 10s ease-in-out infinite;
  will-change:transform;
}}
@keyframes wordmarkFloat{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
.hero-wordmark{{
  font-family:'Inter Tight',sans-serif;font-size:clamp(4.5rem,8vw,6.5rem);font-weight:700;
  letter-spacing:-.04em;line-height:.9;color:#FAFAFA;
  text-shadow:0 0 40px rgba(255,255,255,.2),0 0 100px rgba(231,139,60,.15);
  filter:drop-shadow(0 2px 20px rgba(0,0,0,.5));
  transition:transform .2s ease,text-shadow .3s ease;
}}
.nav-audio{{
  font-size:.75rem;padding:.4rem .75rem;border-radius:999px;cursor:pointer;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:rgba(250,250,250,.7);
}}

.hero-panel{{
  max-width:650px;margin-top:clamp(6rem,18vh,10rem);
  padding:2.5rem 2.75rem;
  background:rgba(0,0,0,.55);backdrop-filter:blur(28px);-webkit-backdrop-filter:blur(28px);
  border:1px solid rgba(255,255,255,.1);border-radius:20px;
  box-shadow:0 24px 80px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.06);
}}
.hero-headline{{
  font-family:'Inter Tight',sans-serif;font-size:clamp(2.75rem,5.5vw,4.5rem);font-weight:600;
  letter-spacing:-.035em;line-height:.98;color:#FAFAFA;
  text-shadow:0 0 30px rgba(255,255,255,.08);
}}
.hero-headline span{{display:block}}
.hero-credit{{
  margin-top:2rem;font-size:16px;font-weight:500;letter-spacing:.12em;text-transform:uppercase;
  color:rgba(250,250,250,.75);
}}
.hero-cta-row{{margin-top:2.25rem;display:flex;gap:1rem;flex-wrap:wrap}}
.btn-primary{{
  height:52px;padding:0 1.75rem;border-radius:999px;border:none;cursor:pointer;
  background:#FAFAFA;color:#050505;font-size:18px;font-weight:600;font-family:'Inter',sans-serif;
  position:relative;overflow:hidden;transition:transform .35s cubic-bezier(.34,1.56,.64,1),box-shadow .35s;
}}
.btn-primary:hover{{box-shadow:0 12px 40px rgba(255,255,255,.25)}}
.btn-primary::after{{
  content:'';position:absolute;inset:0;
  background:linear-gradient(105deg,transparent,rgba(255,255,255,.35),transparent);
  transform:translateX(-120%);transition:transform .65s ease;
}}
.btn-primary:hover::after{{transform:translateX(120%)}}
.btn-ghost{{
  height:52px;padding:0 1.5rem;border-radius:999px;cursor:pointer;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  color:#FAFAFA;font-size:16px;font-weight:500;font-family:'Inter',sans-serif;
  backdrop-filter:blur(12px);transition:all .3s;
}}

/* ── Mission ── */
#mission{{background:#050505;border-top:1px solid rgba(255,255,255,.06)}}
.mission-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1.25rem;margin-top:2.5rem}}
.mission-card{{
  padding:1.75rem;border-radius:16px;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);
  backdrop-filter:blur(16px);
}}

/* ── World map ── */
#world{{background:linear-gradient(180deg,#050505,#0a0a0a)}}
.saas-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.25rem;margin-top:2.5rem}}
.saas-card{{
  padding:1.5rem;border-radius:18px;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  backdrop-filter:blur(20px);transition:transform .4s cubic-bezier(.4,0,.2,1),box-shadow .4s,border-color .4s;
  transform-style:preserve-3d;
}}
.saas-card-top{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem}}
.saas-icon{{width:44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:12px;background:rgba(255,255,255,.06)}}
.saas-status{{font-size:.65rem;font-weight:600;letter-spacing:.08em;text-transform:uppercase;padding:.25rem .5rem;border-radius:6px}}
.saas-status-new{{background:rgba(255,255,255,.08);color:rgba(250,250,250,.5)}}
.saas-status-prog{{background:rgba(250,204,21,.15);color:#FDE68A}}
.saas-status-done{{background:rgba(34,197,94,.15);color:#86EFAC}}
.saas-card h3{{font-family:'Inter Tight',sans-serif;font-size:1.2rem;font-weight:600;letter-spacing:-.02em;margin-bottom:.5rem}}
.saas-card p{{font-size:.875rem;line-height:1.55;color:rgba(250,250,250,.55);margin-bottom:1rem}}
.saas-meta{{display:flex;gap:.5rem;font-size:.7rem;font-family:ui-monospace,monospace;color:rgba(250,250,250,.4);margin-bottom:.75rem}}
.saas-meta span{{padding:.2rem .45rem;background:rgba(255,255,255,.05);border-radius:4px}}
.saas-progress{{height:3px;background:rgba(255,255,255,.08);border-radius:2px;overflow:hidden;margin-bottom:1rem}}
.saas-progress-fill{{height:100%;background:linear-gradient(90deg,#525252,#FAFAFA);border-radius:2px;transition:width .6s ease}}
.saas-card-btn{{
  width:100%;padding:.65rem;border-radius:10px;border:1px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.06);color:#FAFAFA;font-size:.8rem;font-weight:600;cursor:pointer;
  transition:all .25s;
}}
.saas-card-btn:hover{{background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.2)}}

/* ── Characters ── */
#characters{{background:#050505}}
.char-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:1.5rem;margin-top:2.5rem}}
.char-cine{{
  display:grid;grid-template-columns:120px 1fr;gap:0;border-radius:20px;overflow:hidden;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  backdrop-filter:blur(16px);transform-style:preserve-3d;
}}
.char-cine-visual{{
  display:flex;align-items:center;justify-content:center;
  background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(0,0,0,.3));
  border-right:1px solid rgba(255,255,255,.06);
}}
.char-cine-body{{padding:1.5rem}}
.char-cine-rarity{{font-size:.65rem;letter-spacing:.12em;text-transform:uppercase;color:rgba(250,250,250,.4)}}
.char-cine h3{{font-family:'Inter Tight',sans-serif;font-size:1.35rem;font-weight:600;margin:.25rem 0}}
.char-cine-role{{font-size:.75rem;color:rgba(250,250,250,.5);margin-bottom:.75rem}}
.char-cine-story,.char-cine-lesson{{font-size:.85rem;line-height:1.55;color:rgba(250,250,250,.65);margin-bottom:.5rem}}
.char-cine-scores{{display:flex;gap:1rem;font-size:.7rem;font-family:ui-monospace,monospace;color:rgba(250,250,250,.45);margin-top:.75rem}}

/* ── Journey ── */
#journey{{background:#0a0a0a}}
.journey-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:2.5rem}}
.journey-step{{padding:2rem;border-radius:16px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07)}}
.journey-step span{{font-size:.75rem;font-weight:600;color:rgba(250,250,250,.35)}}
.journey-step h4{{font-family:'Inter Tight',sans-serif;font-size:1.15rem;margin:.75rem 0 .5rem}}
.journey-step p{{font-size:.875rem;color:rgba(250,250,250,.55);line-height:1.6}}

/* ── Final CTA ── */
#final-cta{{text-align:center;padding:6rem 1.5rem}}
.final-box{{
  max-width:720px;margin:0 auto;padding:3.5rem 2rem;border-radius:24px;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  backdrop-filter:blur(24px);
}}
.final-box h2{{font-family:'Inter Tight',sans-serif;font-size:clamp(2rem,4vw,2.75rem);font-weight:600;letter-spacing:-.03em;margin-bottom:1rem}}
.final-box p{{color:rgba(250,250,250,.55);margin-bottom:2rem;font-size:1.05rem}}
.glass-card:hover::before {
  opacity: 1;
}

footer{{text-align:center;padding:2rem;font-size:.75rem;color:rgba(250,250,250,.35);letter-spacing:.08em}}
</style></head><body>

<nav id="tc-nav">
  <a class="nav-logo" href="#hero">TrustCraft</a>
  <ul class="nav-links">
    <li><a href="#world">World</a></li>
    <li><a href="#characters">Characters</a></li>
    <li><a href="#journey">Lessons</a></li>
    <li><a href="#mission">About</a></li>
  </ul>
  <div class="nav-actions">
    <a class="nav-link-ext" href="https://github.com" target="_blank">GitHub</a>
    <a class="nav-link-ext" href="https://linkedin.com" target="_blank">LinkedIn</a>
    <button class="nav-audio" id="audio-toggle" type="button">Ambient audio</button>
    <button class="nav-cta magnetic" id="nav-start">Start Journey</button>
  </div>
</nav>

<section id="hero">
  <div class="hero-stack hero-bg" id="parallax-bg"></div>
  <div class="hero-stack hero-clouds"></div>
  <div class="hero-stack hero-glass"></div>
  <div class="hero-stack hero-fx hero-rays" id="parallax-rays"></div>
  <canvas class="hero-canvas hero-fx" id="fx-canvas"></canvas>
  <div class="hero-stack hero-fx hero-water"></div>
  <div class="hero-stack hero-fx">
    <div class="hero-lantern" style="left:78%;top:20%;animation-duration:2.8s"></div>
    <div class="hero-lantern" style="left:90%;top:40%;animation-duration:4.2s;animation-delay:.6s"></div>
    <div class="hero-lantern" style="left:70%;top:55%;animation-duration:3.1s;animation-delay:1.1s"></div>
  </div>
  <div class="hero-wordmark-wrap" id="parallax-logo"><div class="hero-wordmark">TrustCraft</div></div>
  <div class="hero-stage">
    <div class="hero-panel">
      <h1 class="hero-headline">
        <span>Train your judgment.</span>
        <span>Distinguish truth from hallucination.</span>
        <span>Master AI literacy through immersive decision making.</span>
      </h1>
      <p class="hero-credit">Designed &amp; Developed by Gaurav Suthar</p>
      <div class="hero-cta-row">
        <button class="btn-primary magnetic" id="hero-start">Start Journey</button>
        <button class="btn-ghost magnetic" onclick="document.getElementById('world').scrollIntoView({{behavior:'smooth'}})">Explore World</button>
      </div>
    </div>
  </div>
</section>

<section id="mission" class="tc-section reveal">
  <div class="section-inner">
    <p class="section-label">Mission</p>
    <h2 class="section-title">AI literacy for the real world</h2>
    <p class="section-desc">TrustCraft trains you to spot hallucinations, verify claims, and build judgment — through an immersive village where information behaves like a living system.</p>
    <div class="mission-grid">
      <div class="mission-card reveal-child"><h4 style="font-family:'Inter Tight',sans-serif;margin-bottom:.5rem">Judge</h4><p style="font-size:.9rem;color:rgba(250,250,250,.55)">Every encounter presents a claim. You decide: trust, verify, or reject.</p></div>
      <div class="mission-card reveal-child"><h4 style="font-family:'Inter Tight',sans-serif;margin-bottom:.5rem">Learn</h4><p style="font-size:.9rem;color:rgba(250,250,250,.55)">ML concepts taught through story — not textbooks.</p></div>
      <div class="mission-card reveal-child"><h4 style="font-family:'Inter Tight',sans-serif;margin-bottom:.5rem">Grow</h4><p style="font-size:.9rem;color:rgba(250,250,250,.55)">Earn archetypes, scores, and a trust profile that reflects how you think.</p></div>
    </div>
  </div>
</section>

<section id="world" class="tc-section reveal">
  <div class="section-inner">
    <p class="section-label">Product</p>
    <h2 class="section-title">Explore the world</h2>
    <p class="section-desc">Six destinations. One literacy journey. Progress: {progress}/10 training rounds completed.</p>
    <div class="saas-grid">{world_cards}</div>
  </div>
</section>

<section id="characters" class="tc-section reveal">
  <div class="section-inner">
    <p class="section-label">Characters</p>
    <h2 class="section-title">Voices you will meet</h2>
    <p class="section-desc">Each character teaches a different failure mode of trust.</p>
    <div class="char-grid">{char_cards}</div>
  </div>
</section>

<section id="journey" class="tc-section reveal">
  <div class="section-inner">
    <p class="section-label">Learning Journey</p>
    <h2 class="section-title">How it works</h2>
    <div class="journey-grid">{journey_steps}</div>
  </div>
</section>

<section id="final-cta" class="tc-section reveal">
  <div class="final-box">
    <h2>Ready to train your judgment?</h2>
    <p>Enter the village. Face hallucinations. Build AI literacy that lasts.</p>
    <button class="btn-primary magnetic" id="final-start">Start Journey</button>
  </div>
</section>
<footer>Designed &amp; Developed by Gaurav Suthar</footer>

<script>
(function(){{
  function startJourney() {{
    try {{
      const u = new URL(window.parent.location.href);
      u.searchParams.set('tc_enter', '1');
      window.parent.location.href = u.toString();
    }} catch(e) {{ console.error(e); }}
  }}
  function openLoc(loc) {{
    try {{
      const u = new URL(window.parent.location.href);
      u.searchParams.set('tc_enter', '1');
      u.searchParams.set('tc_loc', loc);
      window.parent.location.href = u.toString();
    }} catch(e) {{ startJourney(); }}
  }}
  ['hero-start','nav-start','final-start'].forEach(id => {{
    const el = document.getElementById(id);
    if(el) el.addEventListener('click', startJourney);
  }});
  document.querySelectorAll('.saas-card-btn').forEach(btn => {{
    btn.addEventListener('click', () => openLoc(btn.dataset.loc));
  }});

  const nav = document.getElementById('tc-nav');
  window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 40));

  const reveals = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver(entries => {{
    entries.forEach(e => {{ if(e.isIntersecting) e.target.classList.add('visible'); }});
  }}, {{ threshold: 0.12 }});
  reveals.forEach(el => io.observe(el));

  document.querySelectorAll('.tilt-card').forEach(card => {{
    card.addEventListener('mousemove', e => {{
      const r = card.getBoundingClientRect();
      const x = (e.clientX - r.left) / r.width - 0.5;
      const y = (e.clientY - r.top) / r.height - 0.5;
      card.style.transform = `perspective(800px) rotateY(${{x*8}}deg) rotateX(${{-y*8}}deg) scale(1.02)`;
      card.style.boxShadow = `${{-x*20}}px ${{y*20}}px 50px rgba(0,0,0,.45)`;
    }});
    card.addEventListener('mouseleave', () => {{
      card.style.transform = '';
      card.style.boxShadow = '';
    }});
  }});

  document.querySelectorAll('.magnetic').forEach(btn => {{
    btn.addEventListener('mousemove', e => {{
      const r = btn.getBoundingClientRect();
      const x = e.clientX - r.left - r.width/2;
      const y = e.clientY - r.top - r.height/2;
      btn.style.transform = `translate(${{x*0.15}}px,${{y*0.15}}px)`;
    }});
    btn.addEventListener('mouseleave', () => btn.style.transform = '');
  }});

  let mx=.5, my=.5;
  const pbg = document.getElementById('parallax-bg');
  const prays = document.getElementById('parallax-rays');
  const plogo = document.getElementById('parallax-logo');
  document.getElementById('hero').addEventListener('mousemove', e => {{
    const r = document.getElementById('hero').getBoundingClientRect();
    mx = (e.clientX-r.left)/r.width; my = (e.clientY-r.top)/r.height;
    if(pbg) pbg.style.transform = `scale(1.04) translate(${{(mx-.5)*10}}px,${{(my-.5)*6}}px)`;
    if(prays) prays.style.transform = `translate(${{(mx-.5)*6}}px,${{(my-.5)*4}}px)`;
    if(plogo) {{
      const dx=(mx-.5)*12, dy=(my-.5)*8;
      plogo.style.transform = `translate(${{dx}}px,${{dy}}px)`;
      const wm = plogo.querySelector('.hero-wordmark');
      if(wm) wm.style.textShadow = `0 0 ${{40+mx*30}}px rgba(255,255,255,.25), 0 0 ${{80+my*40}}px rgba(231,139,60,.2)`;
    }}
  }});

  let audioOn=false, audioCtx=null;
  const audioBtn = document.getElementById('audio-toggle');
  function startAmbient(){{
    if(audioCtx) return;
    try {{
      audioCtx = new (window.AudioContext||window.webkitAudioContext)();
      const g = audioCtx.createGain(); g.gain.value=0.03; g.connect(audioCtx.destination);
      [180,240,320].forEach((f,i)=>{{
        const o=audioCtx.createOscillator(); o.type='sine'; o.frequency.value=f;
        o.connect(g); o.start(); setTimeout(()=>o.stop(), 8000+i*2000);
      }});
    }} catch(e) {{}}
  }}
  if(audioBtn) audioBtn.addEventListener('click', ()=>{{
    audioOn=!audioOn; audioBtn.textContent = audioOn ? 'Audio on' : 'Ambient audio';
    if(audioOn) startAmbient(); else if(audioCtx){{ try{{audioCtx.close();}}catch(e){{}} audioCtx=null; }}
  }});

  const canvas = document.getElementById('fx-canvas');
  const ctx = canvas.getContext('2d');
  const parts = [];
  for(let i=0;i<90;i++) parts.push({{x:Math.random(),y:Math.random(),s:Math.random()*2+.5,sp:.0001+Math.random()*.0003,t:Math.random()>.75?'p':Math.random()>.5?'f':'d'}});
  function resize(){{ canvas.width=window.innerWidth; canvas.height=window.innerHeight; }}
  resize(); window.addEventListener('resize', resize);
  let t=0;
  function anim(){{
    t+=.01; ctx.clearRect(0,0,canvas.width,canvas.height);
    parts.forEach(p=>{{
      p.y-=p.sp; if(p.y<0){{p.y=1;p.x=Math.random()}}
      const x=p.x*canvas.width, y=p.y*canvas.height;
      ctx.globalAlpha=.35;
      if(p.t==='p'){{ ctx.fillStyle='#F2A6C8'; ctx.beginPath(); ctx.ellipse(x,y,p.s,p.s*.5,t,0,7); ctx.fill(); }}
      else if(p.t==='f'){{ ctx.fillStyle='#9AE6B4'; ctx.shadowBlur=8; ctx.shadowColor='#9AE6B4'; ctx.beginPath(); ctx.arc(x,y,p.s*.8,0,7); ctx.fill(); ctx.shadowBlur=0; }}
      else{{ ctx.fillStyle='#E8C97D'; ctx.beginPath(); ctx.arc(x,y,p.s,0,7); ctx.fill(); }}
    }});
    requestAnimationFrame(anim);
  }}
  anim();
}})();
</script></body></html>"""


def hero_enter_from_query() -> bool:
    """Start game from landing CTA or world card."""
    try:
        qp = st.query_params
        if qp.get("tc_enter") == "1":
            load_save_into_session()
            st.session_state.game_started = True
            loc = qp.get("tc_loc", "village_square")
            if loc in ("village_square", "library", "forest", "watchtower", "training", "castle"):
                st.session_state.location = loc
            else:
                st.session_state.location = "village_square"
            visited = list(set(st.session_state.get("visited_locs", [])))
            visited.append(st.session_state.location)
            st.session_state.visited_locs = list(set(visited))
            try:
                qp.clear()
            except Exception:
                pass
            return True
    except Exception:
        pass
    return False
def compute_scores():
    answers = st.session_state.answers
    if not answers:
        return st.session_state.scores

    total = len(answers)
    correct = sum(1 for a in answers if a["correct"])
    trust_actions = [a for a in answers if a["choice"] == "trust"]
    verify_actions = [a for a in answers if a["choice"] == "verify"]
    reject_actions = [a for a in answers if a["choice"] == "reject"]
    hall_qs = [a for a in answers if a.get("hallucination")]

    trust_correct = sum(1 for a in answers if a["correct_action"] == "trust" and a["choice"] == "trust")
    trust_opps = sum(1 for a in answers if a["correct_action"] == "trust")
    trust_score = int(100 * trust_correct / trust_opps) if trust_opps else 50

    verify_correct = sum(1 for a in answers if a["correct_action"] == "verify" and a["choice"] == "verify")
    verify_opps = sum(1 for a in answers if a["correct_action"] == "verify")
    verify_wrong_miss = sum(1 for a in answers if a["correct_action"] == "verify" and a["choice"] != "verify")
    verify_score = int(100 * verify_correct / verify_opps) if verify_opps else int(
        max(0, 70 - 15 * verify_wrong_miss)
    )

    hall_correct = sum(1 for a in hall_qs if a["correct"])
    hall_score = int(100 * hall_correct / len(hall_qs)) if hall_qs else 0

    false_trust = sum(1 for a in answers if a.get("hallucination") and a["choice"] == "trust")
    false_reject = sum(1 for a in answers if not a.get("hallucination") and a["correct_action"] == "trust" and a["choice"] == "reject")

    literacy = int(100 * correct / total)
    critical = int(max(0, literacy - 8 * false_trust - 5 * false_reject))

    st.session_state.scores = {
        "literacy": min(100, literacy),
        "trust": min(100, trust_score),
        "verification": min(100, verify_score),
        "hallucination": min(100, hall_score),
        "critical": min(100, critical),
    }
    return st.session_state.scores


def pick_archetype(scores):
    s = scores
    if s["hallucination"] >= 75 and s["verification"] >= 65:
        return "golem"
    if s["verification"] >= 80:
        return "verifier"
    if s["literacy"] >= 75 and s["trust"] >= 60:
        return "librarian"
    if s["literacy"] >= 65:
        return "scholar"
    if s["trust"] < 40 or (s["hallucination"] < 40 and s["literacy"] < 50):
        return "zombie"
    if s["trust"] < 50 and s["critical"] < 55:
        return "chicken"
    if s["verification"] >= s["trust"]:
        return "verifier"
    return "scholar"


def confusion_matrix_chart():
    cm = st.session_state.get("cm_history", {})
    tp, fp, fn, tn = cm.get("tp", 0), cm.get("fp", 0), cm.get("fn", 0), cm.get("tn", 0)
    if tp + fp + fn + tn == 0:
        tp = fp = fn = tn = 0
    cm_df = pd.DataFrame(
        [[tp, fp], [fn, tn]],
        index=["Actually Yes", "Actually No"],
        columns=["Predicted Yes", "Predicted No"],
    )
    fig = go.Figure(
        data=go.Heatmap(
            z=cm_df.values.tolist(),
            x=["Predicted Yes", "Predicted No"],
            y=["Actually Yes", "Actually No"],
            colorscale=[[0, "#0D1A0F"], [0.45, "#2D4A2D"], [1, "#E8C97D"]],
            text=[[f"TP {tp}", f"FP {fp}"], [f"FN {fn}", f"TN {tn}"]],
            texttemplate="%{text}",
            textfont={"size": 14, "color": "#f5e6c8"},
            showscale=False,
        )
    )
    return plotly_theme(fig, "Judgment Map", 300)


def travel_to(loc: str):
    load_save_into_session()
    visited = list(set(st.session_state.get("visited_locs", []) + [loc]))
    st.session_state.visited_locs = visited
    if loc == "castle" and not castle_unlocked():
        st.session_state.location = "castle"
        st.session_state.castle_locked_msg = True
    else:
        st.session_state.location = loc
        st.session_state.castle_locked_msg = False
        if loc == "castle":
            unlock_achievement("ai_guardian")
    save_session_to_disk()
    st.rerun()


def render_app_navbar():
    pass


def render_landing():
    render_native_landing()


def render_village_square():
    """Central hub with back navigation."""
    # Back button
    c1, c2 = st.columns([8, 1])
    with c1:
        st.markdown("")
    with c2:
        if st.button("Back to Hub", key="back_main"):
            st.session_state.location = "landing"
            st.rerun()
    
    inner = f"""
    <p class="world-title">🏘️ Village Square</p>
    <p class="location-sub">Information travels here. Some seeds grow truth, some grow weeds.</p>
    """
    st.markdown(cinematic_scene("grade-square", inner, "min(280px)"), unsafe_allow_html=True)

    st.markdown('''
    <div style="max-width:1200px;margin:2rem auto;padding:0 1rem">
      <p style="font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:1rem">Encounters</p>
      <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.5rem;color:#F5ECD7;margin-bottom:2rem">Meet the villagers</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    for i, enc in enumerate(VILLAGE_TUTORIAL):
        ch = CHARACTERS[enc["npc"]]
        st.markdown(f'''
        <div style="max-width:1200px;margin:0 auto 1.5rem;padding:0 1rem">
          <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:1.5rem">
            <div style="display:flex;gap:1rem;margin-bottom:1rem">
              <div style="font-size:3rem">{ch['emoji']}</div>
              <div>
                <h4 style="font-family:'Inter Tight',sans-serif;color:var(--gold);margin:0 0 0.5rem">{ch['name']}</h4>
                <p style="color:rgba(245,236,215,0.75);margin:0">{enc['text']}</p>
              </div>
            </div>
          </div>
        </div>
        ''', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        for col, act, lbl in zip([c1, c2, c3], ["trust", "verify", "reject"], ["Trust", "Verify", "Reject"]):
            with col:
                if st.button(lbl, key=f"sq_{i}_{act}", use_container_width=True):
                    correct = enc["answer"] == act
                    record_decision(act, correct, enc["answer"], enc["npc"] == "zombie", enc["why"], 12)
                    st.rerun()

    st.markdown('''
    <div style="max-width:1200px;margin:3rem auto 2rem;padding:0 1rem">
      <p style="font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:1rem">Guides</p>
      <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.5rem;color:#F5ECD7;margin-bottom:2rem">Character profiles</h3>
    </div>
    ''', unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    for col, key in zip([m1, m2, m3], ["golem", "librarian", "villager"]):
        with col:
            render_mentor_panel(key)

    render_kingdom_map()


def render_watchtower():
    """Confidence Calibration"""

    if st.button("Back", key="back_watchtower"):
        st.session_state.location = "village_square"
        st.rerun()

    inner = """
    <p class="world-title">🏰 Confidence Calibration</p>
    <p class="location-sub">Confidence doesn't always mean correctness. Learn to calibrate.</p>
    """

    st.markdown(
        cinematic_scene("grade-tower", inner, "min(42vh,420px)"),
        unsafe_allow_html=True,
    )

    score = st.session_state.get("trust_score", 50)

    st.markdown(f"""
    <div style="
    max-width:1150px;
    margin:2rem auto;
    padding:3rem;
    border-radius:36px;
    background:
    radial-gradient(circle at top left, rgba(232,201,125,.18), transparent 35%),
    radial-gradient(circle at bottom right, rgba(232,201,125,.12), transparent 35%),
    rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.10);
    backdrop-filter:blur(40px);
    -webkit-backdrop-filter:blur(40px);
    box-shadow:0 40px 120px rgba(0,0,0,.45);
    ">

    <div style="
    letter-spacing:.22em;
    text-transform:uppercase;
    color:#E8C97D;
    font-size:.8rem;
    ">
    Calibration Analytics
    </div>

    <h1 style="
    font-size:5rem;
    color:#F5ECD7;
    margin:.5rem 0;
    ">
    {score}%
    </h1>

    <p style="
    color:rgba(245,236,215,.75);
    font-size:1.1rem;
    ">
    Confidence Alignment Score
    </p>

    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="glass-card">
        <h3>🎯 Evidence First</h3>
        <p>Strong decisions come from evidence not certainty.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
        <h3>📈 Decision Quality</h3>
        <p>Good analysts update beliefs when new facts appear.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="glass-card">
        <h3>⚖️ Calibration</h3>
        <p>Match confidence to reality instead of intuition.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="margin-top:1.5rem;">
    <h2>🧠 Calibration Principle</h2>
    <p>
    The best decision makers are not the most confident.
    They are the most accurate at estimating uncertainty and adjusting confidence when evidence changes.
    </p>
    </div>
    """, unsafe_allow_html=True)

    render_mentor_panel("golem")
def render_forest():
    """Premium Hallucination Detection"""

    if st.button("Back", key="back_forest"):
        st.session_state.location = "village_square"
        st.rerun()

    inner = """
    <p class="world-title">🌲 Hallucination Detection</p>
    <p class="location-sub">Can you tell when AI sounds right but is actually wrong?</p>
    """

    st.markdown(
        cinematic_scene("grade-forest", inner, "min(38vh,380px)"),
        unsafe_allow_html=True,
    )

    if st.session_state.forest_stage == "intro":

        st.markdown("""
        <div style="
        max-width:900px;
        margin:2rem auto;
        padding:2rem;
        border-radius:24px;
        background:rgba(255,255,255,.04);
        border:1px solid rgba(255,255,255,.08);
        backdrop-filter:blur(20px);
        ">

        <p style="
        font-size:.8rem;
        letter-spacing:.15em;
        text-transform:uppercase;
        color:rgba(232,201,125,.8);
        ">
        Hallucination Challenge
        </p>

        <h2 style="color:#F5ECD7;">
        Can you spot misleading AI answers?
        </h2>

        <p style="color:rgba(245,236,215,.82)">
        You will see an AI response.
        Decide whether to Trust it Verify it or Reject it.
        </p>

        <p style="color:rgba(245,236,215,.65)">
        Some answers are correct.
        Some only sound correct.
        </p>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Start Challenge", use_container_width=True):
            st.session_state.forest_question = 0
            st.session_state.forest_score = 0
            st.session_state.forest_feedback = None
            st.session_state.forest_stage = "question"
            st.rerun()

        return

    if st.session_state.forest_stage == "question":

        q = HALLUCINATION_SCENARIOS[
            st.session_state.forest_question
        ]

        st.markdown(f"""
        <div style="
        max-width:900px;
        margin:2rem auto;
        padding:2rem;
        border-radius:24px;
        background:rgba(255,255,255,.04);
        border:1px solid rgba(255,255,255,.08);
        backdrop-filter:blur(20px);
        ">

        <p style="
        font-size:.8rem;
        letter-spacing:.15em;
        text-transform:uppercase;
        color:rgba(232,201,125,.8);
        ">
        Question {st.session_state.forest_question + 1}/{len(HALLUCINATION_SCENARIOS)}
        </p>

        <h2 style="color:#F5ECD7;">
        {q["question"]}
        </h2>

        <p style="
        color:rgba(245,236,215,.6);
        text-transform:uppercase;
        letter-spacing:.1em;
        ">
        AI Response
        </p>

        <p style="
        color:rgba(245,236,215,.85);
        font-size:1.05rem;
        line-height:1.8;
        ">
        {q["response"]}
        </p>

        </div>
        """, unsafe_allow_html=True)

        c1,c2,c3 = st.columns(3)

        with c1:
            trust = st.button("Trust", use_container_width=True)

        with c2:
            verify = st.button("Verify", use_container_width=True)

        with c3:
            reject = st.button("Reject", use_container_width=True)

        choice = None

        if trust:
            choice = 0

        if verify:
            choice = 1

        if reject:
            choice = 2

        if choice is not None:

            correct = choice == q["correct"]

            if correct:
                st.session_state.forest_score += 1

            st.session_state.forest_answers.append({
                "question": q["question"],
                "choice": choice,
                "correct": correct
            })

            st.session_state.forest_feedback = {
                "correct": correct,
                "feedback": q["feedback"]
            }

            st.session_state.forest_stage = "feedback"
            st.rerun()

        return

    if st.session_state.forest_stage == "feedback":

        fb = st.session_state.forest_feedback

        if fb["correct"]:
            st.success("Correct Decision")
        else:
            st.error("Not Quite")

        st.info(fb["feedback"])

        if st.button("Next Question", use_container_width=True):

            st.session_state.forest_question += 1

            if st.session_state.forest_question >= len(HALLUCINATION_SCENARIOS):
                st.session_state.forest_stage = "report"
            else:
                st.session_state.forest_stage = "question"

            st.rerun()

        return


    if st.session_state.forest_stage == "report":

        total = len(HALLUCINATION_SCENARIOS)
        score = st.session_state.forest_score
        pct = round(score / total * 100)

        rank = (
            "Truth Guardian" if pct >= 90 else
            "Sharp Verifier" if pct >= 75 else
            "Careful Thinker" if pct >= 60 else
            "Needs Verification Training"
        )

        st.markdown(f"""
        <style>
        @keyframes glow {{
            0% {{opacity:.7;transform:scale(1);}}
            50% {{opacity:1;transform:scale(1.04);}}
            100% {{opacity:.7;transform:scale(1);}}
        }}

        @keyframes fill {{
            from {{width:0%;}}
            to {{width:{pct}%;}}
        }}
        </style>

        <div style="
        position:relative;
        overflow:hidden;
        max-width:1100px;
        margin:2rem auto;
        padding:3.5rem;
        border-radius:42px;
        background:
        radial-gradient(circle at top left, rgba(232,201,125,.18), transparent 35%),
        radial-gradient(circle at bottom right, rgba(232,201,125,.12), transparent 40%),
        rgba(255,255,255,.05);
        backdrop-filter:blur(60px);
        -webkit-backdrop-filter:blur(60px);
        border:1px solid rgba(255,255,255,.12);
        box-shadow:
        0 0 120px rgba(232,201,125,.15),
        0 40px 120px rgba(0,0,0,.45);
        ">

        <div style="
        font-size:.8rem;
        letter-spacing:.25em;
        text-transform:uppercase;
        color:#E8C97D;">
        ✦ Hallucination Intelligence Dashboard
        </div>

        <div style="
        font-size:6rem;
        font-weight:800;
        color:#F5ECD7;">
        {pct}%
        </div>

        <div style="color:rgba(245,236,215,.75);">
        Detection Accuracy
        </div>

        <div style="
        height:14px;
        margin-top:2rem;
        border-radius:999px;
        background:rgba(255,255,255,.08);
        overflow:hidden;">
        <div style="
        height:100%;
        width:0%;
        animation:fill 2s forwards;
        background:linear-gradient(90deg,#E8C97D,#F5ECD7);
        "></div>
        </div>

        <div style="
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:18px;
        margin-top:2rem;">

        <div style="padding:1.5rem;border-radius:22px;background:rgba(255,255,255,.05);text-align:center;">
        <h2 style="color:#F5ECD7;">{score}</h2>
        <p>Correct</p>
        </div>

        <div style="padding:1.5rem;border-radius:22px;background:rgba(255,255,255,.05);text-align:center;">
        <h2 style="color:#F5ECD7;">{total-score}</h2>
        <p>Missed</p>
        </div>

        <div style="padding:1.5rem;border-radius:22px;background:rgba(255,255,255,.05);text-align:center;">
        <h2 style="color:#F5ECD7;">{rank}</h2>
        <p>Rank</p>
        </div>

        </div>

        <div style="
        margin-top:1.8rem;
        display:inline-block;
        padding:.8rem 1.4rem;
        border-radius:999px;
        background:rgba(232,201,125,.12);
        border:1px solid rgba(232,201,125,.25);
        color:#F5ECD7;">
        XP SCORE • {score}/{total}
        </div>

        </div>
        """, unsafe_allow_html=True)

        if st.button("Play Again", use_container_width=True):
            st.session_state.forest_stage = "intro"
            st.session_state.forest_score = 0
            st.session_state.forest_question = 0
            st.session_state.forest_feedback = None
            st.session_state.forest_answers = []
            st.rerun()
def render_library():
    """Evidence Verification - source validation and ML concepts."""
    if st.button("Back", key="back_library"):
        st.session_state.location = "village_square"
        st.rerun()
    
    inner = f"""
    <p class="world-title">📚 Evidence Verification</p>
    <p class="location-sub">Learn which sources to trust and which to question.</p>
    """
    st.markdown(cinematic_scene("grade-library", inner, "min(36vh,360px)"), unsafe_allow_html=True)
    
    st.markdown('''
    <div style="max-width:720px;margin:2rem auto">
      <p style="font-size:0.75rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8)">AI Concepts</p>
    </div>
    ''', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, concept in enumerate(ML_CONCEPTS):
        card = f"""
        <div class="glass-card" style="height:100%">
          <p style="font-size:0.8rem;letter-spacing:0.1em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:0.5rem">{concept.get('emoji', '🤖')} Concept</p>
          <h3 style="margin:0 0 0.75rem;color:#F5ECD7">{concept['title']}</h3>
          <p style="font-size:0.9rem;color:rgba(245,236,215,0.75);margin:0.5rem 0"><strong>Imagine:</strong> {concept['analogy']}</p>
          <p style="font-size:0.85rem;color:rgba(245,236,215,0.65);margin:0.5rem 0"><strong>Example:</strong> {concept['example']}</p>
          <p style="font-size:0.82rem;color:rgba(232,201,125,0.7);margin-top:0.6rem">{concept['story']}</p>
        </div>"""
        with cols[i % 2]:
            st.markdown(card, unsafe_allow_html=True)


def start_training_session():
    if not st.session_state.question_order:
        order = list(range(len(QUESTIONS)))
        random.shuffle(order)
        st.session_state.question_order = order[:10]
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.session_state.show_feedback = False


def render_training():
    """Training Simulator - live scenarios."""
    if st.button("Back", key="back_training"):
        st.session_state.location = "village_square"
        st.rerun()
    
    start_training_session()
    idx = st.session_state.question_index
    order = st.session_state.question_order
    total = len(order) if order else 0

    inner = f"""
    <p class="world-title">⚔️ Training Simulator</p>
    <p class="location-sub">Live encounters. Make real choices.</p>
    """
    st.markdown(cinematic_scene("grade-training", inner, "min(32vh,320px)"), unsafe_allow_html=True)

    if total:
        progress_text = f"Question {idx + 1} of {total}"
        st.markdown(f'<p style="text-align:center;color:rgba(245,236,215,0.6);margin-bottom:1.5rem">{progress_text}</p>', unsafe_allow_html=True)

    st.markdown('''
    <div style="max-width:1200px;margin:2rem auto;padding:0 1rem">
      <p style="font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:1rem">Complexity Model</p>
      <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.3rem;color:#F5ECD7;margin-bottom:0.75rem">How well is the model trained?</h3>
    </div>
    ''', unsafe_allow_html=True)
    

    if idx >= total and total > 0:
        st.session_state.questions_answered = len(st.session_state.answers)
        compute_scores()
        st.markdown('''
        <div style="max-width:720px;margin:2rem auto;padding:2rem;text-align:center;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px">
          <p style="font-size:1.2rem;color:#E8C97D;margin-bottom:0.5rem">Training Complete</p>
          <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.5rem;color:#F5ECD7;margin-bottom:1.5rem">The village honors your judgment</h3>
          <p style="color:rgba(245,236,215,0.7);margin-bottom:0">Reach 180 XP total to unlock Results Dashboard</p>
        </div>
        ''', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("New training", key="train_again"):
                st.session_state.question_order = []
                st.session_state.question_index = 0
                st.session_state.answers = []
                st.session_state.show_feedback = False
                st.rerun()
        with c2:
            if castle_unlocked() and st.button("Results Dashboard", key="train_castle"):
                st.session_state.location = "castle"
                st.rerun()
        with c3:
            if st.button("Village Square", key="train_back"):
                st.session_state.location = "village_square"
                st.rerun()
        return

    q = QUESTIONS[order[idx]]
    ch = CHARACTERS[q["character"]]

    st.markdown(f'''
    <div style="max-width:720px;margin:2rem auto;padding:2rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px">
      <div style="display:flex;gap:1rem;margin-bottom:1.5rem;align-items:flex-start">
        <div style="font-size:2.5rem">{ch['emoji']}</div>
        <div>
          <h3 style="font-family:'Inter Tight',sans-serif;font-size:1.2rem;color:var(--gold);margin:0 0 0.25rem">{ch['name']}</h3>
          <p style="font-size:0.8rem;color:rgba(245,236,215,0.5);margin:0;letter-spacing:0.08em;text-transform:uppercase">{q['category']}</p>
        </div>
      </div>
      <p style="font-size:1.05rem;line-height:1.7;color:rgba(245,236,215,0.85);margin:0">{q['statement']}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.session_state.show_feedback and st.session_state.last_feedback:
        fb = st.session_state.last_feedback
        status = "Correct" if fb["correct"] else "Not quite"
        st.markdown(f'''
        <div style="max-width:720px;margin:1.5rem auto;padding:1.5rem;background:{'rgba(45,74,45,0.5)' if fb['correct'] else 'rgba(60,28,28,0.45)'};border:1px solid {'rgba(106,176,76,0.5)' if fb['correct'] else 'rgba(201,74,74,0.45)'};border-radius:12px">
          <p style="color:{'#b8e0a8' if fb['correct'] else '#f0b0b0'};font-weight:600;margin:0 0 0.75rem">{status}</p>
          <p style="color:rgba(245,236,215,0.8);line-height:1.6;margin:0">{fb['explanation']}</p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("Next question", key="train_continue", use_container_width=True):
            st.session_state.show_feedback = False
            st.session_state.question_index += 1
            st.session_state.last_feedback = None
            st.rerun()
    else:
        st.markdown('''
        <div style="max-width:1200px;margin:2rem auto 1.5rem;padding:0 1rem">
          <p style="font-size:0.85rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8)">Your judgment</p>
          <p style="font-size:0.95rem;color:rgba(245,236,215,0.7)">Trust = accept it | Verify = check sources | Reject = call it out</p>
        </div>
        ''', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        for col, action, label in zip(
            [c1, c2, c3],
            ["trust", "verify", "reject"],
            ["Trust", "Verify", "Reject"],
        ):
            with col:
                if st.button(label, key=f"choice_{idx}_{action}", use_container_width=True):
                    correct = q["correct"] == action
                    record_decision(
                        action, correct, q["correct"], q["hallucination"], q["explanation"], 15
                    )
                    st.session_state.last_feedback = {
                        "correct": correct,
                        "explanation": q["explanation"],
                    }
                    st.session_state.show_feedback = True
                    st.rerun()


def render_castle():
    """Results Dashboard - final assessment."""
    if st.button("Back", key="back_castle"):
        st.session_state.location = "village_square"
        st.rerun()
    
    compute_scores()
    scores = st.session_state.scores
    answers = st.session_state.answers
    archetype_key = pick_archetype(scores)
    arch = ARCHETYPES[archetype_key]

    if not castle_unlocked():
        inner = f"""
        <p class="world-title">👑 Results Dashboard</p>
        <p class="location-sub">Gates sealed. Earn 180 XP and complete 5 training rounds.</p>
        """
        st.markdown(cinematic_scene("grade-castle", inner, "min(40vh,400px)"), unsafe_allow_html=True)
        
        xp = st.session_state.get("knowledge_xp", 0)
        q_answered = st.session_state.get("questions_answered", 0)
        st.markdown(f'''
        <div style="max-width:720px;margin:2rem auto;padding:1.5rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px">
          <p style="color:rgba(245,236,215,0.7);margin:0">Progress: {xp} / 180 XP · {q_answered} / 5 training rounds</p>
        </div>
        ''', unsafe_allow_html=True)
        
        if st.button("Continue training", key="castle_go_train"):
            st.session_state.location = "training"
            st.rerun()
        return

    inner = f"""
    <p class="world-title">👑 Results Dashboard</p>
    <p class="location-sub">Your legend is written on the wall.</p>
    """
    st.markdown(cinematic_scene("grade-castle", inner, "min(34vh,340px)"), unsafe_allow_html=True)

    st.markdown(f'''
    <div style="text-align:center;max-width:720px;margin:2rem auto;padding:2rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:16px">
      <p style="font-size:0.75rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:0.5rem">Your Archetype</p>
      <h2 style="font-family:'Inter Tight',sans-serif;font-size:2.2rem;font-weight:700;color:#F5ECD7;margin:0">{arch['name']}</h2>
      <p style="color:rgba(245,236,215,0.75);line-height:1.65;margin:1.5rem 0 0">{arch['desc']}</p>
    </div>
    ''', unsafe_allow_html=True)

    # Scores
    st.markdown('''
    <div style="max-width:1200px;margin:2rem auto;padding:0 1rem">
      <p style="font-size:0.75rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:1rem">Scores</p>
    </div>
    ''', unsafe_allow_html=True)
    
    cols = st.columns(5)
    for col, key, label in zip(cols, ["literacy", "trust", "verification", "hallucination", "critical"], ["Literacy", "Trust", "Verify", "Hallucination", "Critical"]):
        with col:
            v = scores.get(key, 0)
            st.markdown(f'''
            <div style="text-align:center;padding:1rem;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px">
              <div style="font-size:1.5rem;font-weight:700;color:var(--gold)">{v}</div>
              <div style="font-size:0.75rem;color:rgba(245,236,215,0.5);margin-top:0.5rem">{label}</div>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Analysis
    st.markdown(f'''
    <div style="max-width:1200px;margin:2rem auto;padding:0 1rem">
      <p style="font-size:0.75rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(232,201,125,0.8);margin-bottom:1rem">Analysis</p>
      <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:1.5rem">
        <p style="margin:0 0 1rem"><strong style="color:var(--gold)">Strengths</strong></p>
        <p style="margin:0 0 1.5rem;color:rgba(245,236,215,0.75)">{arch['strengths']}</p>
        <p style="margin:0 0 1rem"><strong style="color:var(--blossom)">Growth opportunities</strong></p>
        <p style="margin:0 0 1.5rem;color:rgba(245,236,215,0.75)">{arch['weaknesses']}</p>
        <p style="margin:0 0 1rem"><strong style="color:var(--blue)">Next steps</strong></p>
        <p style="margin:0;color:rgba(245,236,215,0.75)">{arch['advice']}</p>
      </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start new journey", key="castle_reset"):
            st.session_state.question_order = []
            st.session_state.question_index = 0
            st.session_state.answers = []
            st.session_state.show_feedback = False
            st.session_state.questions_answered = 0
            st.session_state.scores = {k: 0 for k in ["literacy", "trust", "verification", "hallucination", "critical"]}
            st.session_state.location = "landing"
            st.session_state.game_started = False
            st.rerun()
    with c2:
        if st.button("Village Square", key="castle_sq"):
            st.session_state.location = "village_square"
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    init_state()
    load_save_into_session()
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(ENHANCEMENT_CSS, unsafe_allow_html=True)

    if hero_enter_from_query():
        st.rerun()

    loc = st.session_state.location
    if not st.session_state.game_started:
        render_landing()
    else:
        st.markdown('<div class="world-zone">', unsafe_allow_html=True)
        render_progress_hud()
        render_app_navbar()
        if loc == "village_square":
            render_village_square()
        elif loc == "library":
            render_library()
        elif loc == "forest":
            render_forest()
        elif loc == "watchtower":
            render_watchtower()
        elif loc == "training":
            render_training()
        elif loc == "castle":
            render_castle()
        else:
            render_village_square()
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

GLOBAL_CSS += """
.brand-name{
color:#FFE8B1;
font-weight:600;
letter-spacing:.22em;
text-transform:uppercase;
}

.hero-version{
color:#FFE8B1;
opacity:.75;
margin-left:20px;
font-size:.82rem;
letter-spacing:.16em;
text-transform:uppercase;
}

.footer-brand{
display:flex;
flex-direction:column;
align-items:center;
gap:16px;
}

.footer-links{
display:flex;
gap:12px;
justify-content:center;
}

.footer-links a{
padding:10px 18px;
border-radius:999px;
background:rgba(255,255,255,.05);
border:1px solid rgba(255,255,255,.10);
backdrop-filter:blur(20px);
-webkit-backdrop-filter:blur(20px);
text-decoration:none!important;
color:rgba(245,236,215,.92)!important;
font-size:.82rem;
transition:.25s ease;
}

.footer-links a:hover{
background:rgba(255,255,255,.08);
transform:translateY(-2px);
color:#fff!important;
}
"""

GLOBAL_CSS += """
.creator-card{
max-width:520px;
margin:40px auto 0;
padding:28px;
border-radius:28px;
background:rgba(255,255,255,.04);
border:1px solid rgba(255,255,255,.08);
backdrop-filter:blur(20px);
-webkit-backdrop-filter:blur(20px);
text-align:center;
box-shadow:0 20px 60px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.05);
}

.creator-label{
font-size:.78rem;
letter-spacing:.18em;
text-transform:uppercase;
color:rgba(245,236,215,.45);
margin-bottom:8px;
}

.creator-name{
font-size:1.2rem;
font-weight:600;
color:#F5ECD7;
margin-bottom:20px;
}

.creator-links{
display:flex;
justify-content:center;
gap:12px;
}

.creator-links a{
padding:10px 18px;
border-radius:999px;
text-decoration:none!important;
background:rgba(255,255,255,.05);
border:1px solid rgba(255,255,255,.08);
color:#F5ECD7!important;
transition:.25s ease;
}

.creator-links a:hover{
transform:translateY(-2px);
background:rgba(255,255,255,.08);
}
"""
