import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date, timedelta
import math

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🔥 FireMuscle · StephanoEl",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
def get_data_file(username):
    return f"data/firemuscle_data_{username}.json"

def load_users():
    if os.path.exists("data/users.json"):
        with open("data/users.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"StephanoEl": {"password": "111003", "email": "stephanoescobar2004@gmail.com"}}

def save_users(users):
    with open("data/users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

# ─── RUTINA PRECARGADA ─────────────────────────────────────────────────────────
RUTINA_BASE = {
    "Día 1": {
        "titulo": "Espalda",
        "ejercicios": [
            {"musculo": "Abdomen",   "nombre": "Pre Entreno",              "series": 2, "reps": "20, 20, 7, 15, 15", "descanso": "30 seg"},
            {"musculo": "Espalda",   "nombre": "Superman",                 "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Dumbbell Row",             "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Prone Cobra",              "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Dumbbell Pullover",        "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Seal Flaps",               "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Reverse Fly",              "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Reverse Snow Angels",      "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Remo",                     "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Prone Thoracic Rotation",  "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Peso muerto",              "series": 2, "reps": "1 min",             "descanso": "10 seg"},
            {"musculo": "Espalda",   "nombre": "Lat Pulldown",             "series": 6, "reps": "20, 16",            "descanso": "10 seg"},
        ]
    },
    "Día 2": {
        "titulo": "Abdominales",
        "ejercicios": [
            {"musculo": "Abdomen", "nombre": "Pre Entreno",          "series": 3, "reps": "20, 20, 7, 15, 20", "descanso": "30 seg"},
            {"musculo": "Abdomen", "nombre": "Abdomen Crunch lvl 1", "series": 2, "reps": "20, 20",            "descanso": "10 seg"},
            {"musculo": "Abdomen", "nombre": "Abdomen Crunch lvl 2", "series": 2, "reps": "20, 20",            "descanso": "10 seg"},
            {"musculo": "Abdomen", "nombre": "Abdomen Crunch lvl 3", "series": 2, "reps": "20, 20",            "descanso": "10 seg"},
            {"musculo": "Abdomen", "nombre": "Abdomen Crunch lvl 4", "series": 2, "reps": "20, 20",            "descanso": "15 seg"},
        ]
    },
    "Día 3": {
        "titulo": "Pierna",
        "ejercicios": [
            {"musculo": "Abdomen", "nombre": "Pre Entreno",           "series": 3, "reps": "20, 20, 10-9, 20, 20", "descanso": "30 seg"},
            {"musculo": "Pierna",  "nombre": "Goblet Squat",          "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Pierna",  "nombre": "Single‑Leg Calf Raise", "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Pierna",  "nombre": "Curtsy Lunge",          "series": 4, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Pierna",  "nombre": "Dumbbell Sumo Squat",   "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Pierna",  "nombre": "Cossack Squat",         "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Pierna",  "nombre": "Hip Thrust",            "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Pierna",  "nombre": "Kneeling Squat",        "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
        ]
    },
    "Día 4": {
        "titulo": "Pecho y Abdominales",
        "ejercicios": [
            {"musculo": "Abdomen", "nombre": "Pre Entreno",              "series": 2, "reps": "20, 20, 10-9, 20, 20", "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Dumbbell Forward Press",   "series": 2, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Triple Remo",              "series": 2, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Dumbbell Front Raise",     "series": 2, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Remo Cerrado",             "series": 2, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Dumbbell Floor Press",     "series": 2, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Dumbbell Pullover",        "series": 2, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Dumbbell Floor Press",     "series": 4, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Push-up",                  "series": 2, "reps": "1 min. 1 min",         "descanso": "30 seg"},
            {"musculo": "Pecho",   "nombre": "Maquina",                  "series": 3, "reps": "10, 10, Fallo",        "descanso": "20 seg"},
        ]
    },
    "Día 5": {
        "titulo": "Bíceps y Tríceps",
        "ejercicios": [
            {"musculo": "Abdomen",  "nombre": "Pre Entreno",                          "series": 2, "reps": "20, 20, 10-9, 20, 20", "descanso": "30 seg"},
            {"musculo": "Bíceps",   "nombre": "Curl de bíceps con rotación",          "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Triceps",  "nombre": "Extensión de tríceps",                 "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Bíceps",   "nombre": "Curl de bíceps con giro",              "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Triceps",  "nombre": "Patada de tríceps",                    "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Bíceps",   "nombre": "Curl martillo",                        "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Triceps",  "nombre": "Curl martillo inclinado",              "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Bíceps",   "nombre": "Curl lateral alterno",                 "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Triceps",  "nombre": "Martillo acostado hasta el pecho",     "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Triceps",  "nombre": "Extensión de tríceps alterna",         "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
            {"musculo": "Triceps",  "nombre": "Remo con mancuerna sentado",           "series": 2, "reps": "1 min, 1 min",         "descanso": "30 seg"},
        ]
    },
    "Día 6": {
        "titulo": "Recuperación Activa - Semi Descanso",
        "ejercicios": [
            {"musculo": "Abdomen",       "nombre": "Pre Entreno",  "series": 2, "reps": "20, 20, 10-9, 20, 20",       "descanso": "10 seg"},
            {"musculo": "Pecho",         "nombre": "Planchas",     "series": 0, "reps": "-",                           "descanso": "-"},
            {"musculo": "Triceps",       "nombre": "Planchas",     "series": 0, "reps": "-",                           "descanso": "-"},
            {"musculo": "Pecho",         "nombre": "Maquina",      "series": 6, "reps": "12, 12, 12, 12, 15, Fallo",  "descanso": "1 min"},
            {"musculo": "Espalda/Brazos","nombre": "Dead Hang",    "series": 2, "reps": "5, 5",                        "descanso": "30 seg"},
        ]
    },
}

DIA_SEMANA_MAP = {0: "Día 1", 1: "Día 2", 2: "Día 3", 3: "Día 4", 4: "Día 5", 5: "Día 6"}

NUTRI_OBJETIVOS_EXCEL = {
    "calorias": 1800, "grasas": 55, "colesterol": 300,
    "sodio": 1750, "carbohidratos": 180, "proteinas": 130, "azucar": 25, "fibra": 25,
}

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg:#0a0e17; --surface:#111827; --surface2:#1a2332;
    --accent:#00e5a0; --accent2:#ff6b35; --accent3:#4facfe; --accent4:#a78bfa;
    --text:#e8f0fe; --muted:#6b7a99;
    --good:#00e5a0; --warn:#ffd166; --bad:#ff4757; --border:#1e2d45;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background-color:var(--bg);color:var(--text);}
#MainMenu,footer{visibility:hidden;}
.block-container{padding-top:1rem!important;}

.app-header{background:linear-gradient(135deg,#0a0e17 0%,#1a0d05 50%,#0d0a00 100%);border-bottom:1px solid rgba(255,107,53,.3);padding:1.2rem 2rem;margin:-1rem -1rem 2rem -1rem;display:flex;align-items:center;gap:1rem;position:relative;overflow:hidden;}
.app-title{font-family:'Bebas Neue',sans-serif;font-size:2.2rem;letter-spacing:3px;background:linear-gradient(135deg,#ff6b35 0%,#ff4500 50%,#ffd166 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:0;line-height:1;filter:drop-shadow(0 0 12px rgba(255,100,0,.4));}
.app-subtitle{font-size:.75rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;font-weight:500;}
.user-badge{margin-left:auto;background:var(--surface2);border:1px solid var(--border);border-radius:50px;padding:.4rem 1rem;font-size:.8rem;color:var(--accent);font-family:'JetBrains Mono',monospace;letter-spacing:1px;}

.card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:1.5rem;margin-bottom:1rem;position:relative;overflow:hidden;}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#ff6b35,#ffd166);}
.card-orange::before{background:linear-gradient(90deg,var(--accent2),var(--warn));}
.card-blue::before{background:linear-gradient(90deg,var(--accent3),#a78bfa);}
.card-purple::before{background:linear-gradient(90deg,#a78bfa,#ec4899);}
.card-title{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;letter-spacing:2px;color:var(--accent);margin-bottom:1rem;display:flex;align-items:center;gap:.5rem;}
.card-orange .card-title{color:var(--accent2);}
.card-blue .card-title{color:var(--accent3);}
.card-purple .card-title{color:var(--accent4);}

.pill{display:inline-block;padding:.2rem .7rem;border-radius:50px;font-size:.7rem;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.pill-good{background:rgba(0,229,160,.15);color:var(--good);border:1px solid rgba(0,229,160,.3);}
.pill-warn{background:rgba(255,209,102,.15);color:var(--warn);border:1px solid rgba(255,209,102,.3);}
.pill-bad{background:rgba(255,71,87,.15);color:var(--bad);border:1px solid rgba(255,71,87,.3);}
.pill-info{background:rgba(79,172,254,.15);color:var(--accent3);border:1px solid rgba(79,172,254,.3);}
.pill-purple{background:rgba(167,139,250,.15);color:var(--accent4);border:1px solid rgba(167,139,250,.3);}

.prog-wrap{margin:.4rem 0;}
.prog-label{display:flex;justify-content:space-between;font-size:.72rem;color:var(--muted);margin-bottom:.25rem;}
.prog-bar{height:6px;background:var(--border);border-radius:99px;overflow:hidden;}
.prog-fill{height:100%;border-radius:99px;transition:width .4s ease;}
.prog-good{background:linear-gradient(90deg,#00e5a0,#00c07d);}
.prog-warn{background:linear-gradient(90deg,#ffd166,#ffb347);}
.prog-bad{background:linear-gradient(90deg,#ff4757,#ff1f3a);}

.ex-entry{background:var(--surface2);border:1px solid var(--border);border-radius:12px;padding:.8rem 1rem;margin:.4rem 0;display:flex;align-items:center;gap:1rem;}
.ex-icon{font-size:1.4rem;}
.ex-info{flex:1;}
.ex-name{font-weight:600;font-size:.9rem;}
.ex-detail{font-size:.75rem;color:var(--muted);margin-top:.1rem;}

.food-row{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:.7rem 1rem;margin:.4rem 0;display:flex;justify-content:space-between;align-items:center;}
.food-name{font-weight:500;font-size:.9rem;}
.food-cal{font-family:'JetBrains Mono',monospace;color:var(--accent);font-size:.85rem;}

.stTextInput input,.stNumberInput input,.stSelectbox select{background:var(--surface2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:10px!important;}
.stButton>button{background:linear-gradient(135deg,var(--accent),#00c07d)!important;color:var(--bg)!important;font-weight:700!important;border:none!important;border-radius:10px!important;letter-spacing:1px!important;transition:opacity .2s!important;}
.stButton>button:hover{opacity:.85!important;}
.stSidebar{background:var(--surface)!important;border-right:1px solid var(--border);}

.metric-box{background:var(--surface2);border:1px solid var(--border);border-radius:14px;padding:1rem 1.2rem;text-align:center;}
.metric-val{font-family:'Bebas Neue',sans-serif;font-size:2rem;color:var(--accent);line-height:1;}
.metric-label{font-size:.68rem;color:var(--muted);text-transform:uppercase;letter-spacing:1.5px;margin-top:.3rem;}

.alert-good{background:rgba(0,229,160,.08);border:1px solid rgba(0,229,160,.25);border-radius:10px;padding:.8rem 1rem;color:var(--good);font-size:.85rem;margin:.5rem 0;}
.alert-warn{background:rgba(255,209,102,.08);border:1px solid rgba(255,209,102,.25);border-radius:10px;padding:.8rem 1rem;color:var(--warn);font-size:.85rem;margin:.5rem 0;}
.alert-bad{background:rgba(255,71,87,.08);border:1px solid rgba(255,71,87,.25);border-radius:10px;padding:.8rem 1rem;color:var(--bad);font-size:.85rem;margin:.5rem 0;}
.alert-info{background:rgba(79,172,254,.08);border:1px solid rgba(79,172,254,.25);border-radius:10px;padding:.8rem 1rem;color:var(--accent3);font-size:.85rem;margin:.5rem 0;}

.section-sep{border:none;border-top:1px solid var(--border);margin:1.5rem 0;}

.db-week-header{font-family:'Bebas Neue',sans-serif;font-size:1.6rem;letter-spacing:3px;background:linear-gradient(90deg,var(--accent4),#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:1.5rem 0 .5rem;}
.db-ex-row{display:flex;gap:1rem;padding:.4rem .3rem;border-bottom:1px solid var(--border);font-size:.82rem;align-items:center;}
.db-ex-row:last-child{border-bottom:none;}
.db-musculo{color:var(--accent3);font-weight:600;min-width:80px;}
.db-nombre{flex:1;color:var(--text);}
.db-detail{color:var(--muted);font-family:'JetBrains Mono',monospace;font-size:.75rem;}

.routine-badge{display:inline-flex;align-items:center;gap:.3rem;background:rgba(0,229,160,.1);border:1px solid rgba(0,229,160,.3);border-radius:6px;padding:.15rem .6rem;font-size:.7rem;color:var(--accent);font-weight:600;letter-spacing:.5px;}

/* Ocultar "Press Enter to submit" */
[data-testid="stForm"] small,
[data-testid="stForm"] .st-emotion-cache-1gulkj5,
[data-testid="stForm"] .eyeqlp53,
small.eyeqlp53,
div[data-testid="InputInstructions"],
[data-testid="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}
/* Ocultar barra superior de Streamlit */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
header[data-testid="stHeader"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ─── DATA HELPERS ──────────────────────────────────────────────────────────────
def load_data(username):
    data_file = get_data_file(username)
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data, username):
    data_file = get_data_file(username)
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_today_key():
    return date.today().isoformat()

def init_day(data, day_key):
    if day_key not in data:
        data[day_key] = {"foods": [], "exercises": [], "profile": {}}
    if "profile" not in data[day_key]:
        data[day_key]["profile"] = {}
    return data

# ─── NUTRIENT CALCULATOR ───────────────────────────────────────────────────────
def calc_limits(age, weight_kg, height_cm, sex="Masculino", activity="Moderado", use_excel=False):
    if use_excel:
        return NUTRI_OBJETIVOS_EXCEL.copy()
    if sex == "Masculino":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    activity_factors = {"Sedentario": 1.2, "Ligero": 1.375, "Moderado": 1.55, "Activo": 1.725, "Muy activo": 1.9}
    factor = activity_factors.get(activity, 1.55)
    tdee = bmr * factor
    protein_g = weight_kg * 1.6
    fat_g = (tdee * 0.25) / 9
    carbs_g = (tdee - protein_g * 4 - fat_g * 9) / 4
    return {
        "calorias": round(tdee), "proteinas": round(protein_g),
        "carbohidratos": round(carbs_g), "grasas": round(fat_g),
        "azucar": round(carbs_g * 0.10), "fibra": 30 if sex == "Masculino" else 25,
        "sodio": 2300, "colesterol": 300,
    }

def get_status(consumed, limit, nutrient):
    pct = (consumed / limit * 100) if limit > 0 else 0
    if nutrient == "fibra":
        if consumed >= limit:       return "✅ Excelente", "good", "Meta alcanzada"
        elif consumed >= limit*0.6: return "⚠️ Moderado",  "warn", f"Faltan {limit-consumed:.0f}g"
        else:                       return "❌ Bajo",       "bad",  "Muy poca fibra"
    if pct <= 80:   return "✅ Bien",     "good", "Dentro del límite"
    elif pct <= 100: return "⚠️ Moderado", "warn", "Cerca del límite"
    elif pct <= 130: return "⚠️ Excedido", "warn", f"Superado en {pct-100:.0f}%"
    else:            return "❌ Exceso",   "bad",  f"¡Muy alto! ({pct:.0f}%)"

def overall_diet_status(foods, limits):
    if not foods: return None
    totals = sum_nutrients(foods)
    issues, warns = 0, 0
    for k in ["grasas", "colesterol", "sodio", "carbohidratos", "azucar"]:
        if k in limits and limits[k] > 0:
            pct = totals.get(k, 0) / limits[k] * 100
            if pct > 130:   issues += 1
            elif pct > 100: warns  += 1
    fibra_pct = totals.get("fibra", 0) / limits.get("fibra", 30) * 100
    if fibra_pct < 60: warns += 1
    if issues == 0 and warns == 0: return "good", "🌟 Excelente alimentación hoy"
    elif issues == 0:              return "warn", "⚡ Alimentación moderada — pequeños ajustes"
    else:                          return "bad",  f"⚠️ {issues} nutriente(s) muy excedido(s) hoy"

def sum_nutrients(foods):
    keys = ["calorias","proteinas","carbohidratos","grasas","azucar","fibra","sodio","colesterol"]
    total = {k: 0 for k in keys}
    for f in foods:
        for k in keys:
            total[k] += float(f.get(k, 0))
    return total

# ─── DATABASE HELPERS ──────────────────────────────────────────────────────────
def get_all_weeks(data):
    if "db_semanas" not in data:
        data["db_semanas"] = {}
    return data["db_semanas"]

def get_next_semana_num(data):
    weeks = get_all_weeks(data)
    if not weeks:
        return 1
    nums = []
    for k in weeks.keys():
        parts = k.split()
        if parts and parts[-1].isdigit():
            nums.append(int(parts[-1]))
    return (max(nums) + 1) if nums else 1

def get_musculo_from_exercise(ex):
    return ex.get("grupo") or ex.get("musculo") or "—"

def guardar_dia_en_db(data, semana_num, dia_label, exercises, foods, notas=""):
    weeks = get_all_weeks(data)
    sem_key = f"Semana {semana_num}"

    if sem_key not in weeks:
        weeks[sem_key] = {"dias": {}, "fecha_inicio": date.today().isoformat()}

    exercises_normalized = []
    for ex in exercises:
        ex_copy = dict(ex)
        if "grupo" in ex_copy and "musculo" not in ex_copy:
            ex_copy["musculo"] = ex_copy.pop("grupo")
        elif "grupo" in ex_copy:
            ex_copy["musculo"] = ex_copy.pop("grupo")
        exercises_normalized.append(ex_copy)

    weeks[sem_key]["dias"][dia_label] = {
        "fecha":        date.today().isoformat(),
        "ejercicios":   exercises_normalized,
        "alimentos":    foods,
        "notas":        notas,
        "guardado_en":  datetime.now().strftime("%H:%M:%S"),
    }
    data["db_semanas"] = weeks
    return data

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "data" not in st.session_state:
    st.session_state.data = {}
if "selected_day" not in st.session_state:
    dow = date.today().weekday()
    st.session_state.selected_day = DIA_SEMANA_MAP.get(dow, "Día 1")
if "editing_food_idx" not in st.session_state:
    st.session_state.editing_food_idx = None

if "food_form_counter" not in st.session_state:
    st.session_state.food_form_counter = 0

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    all_users = load_users()

    # ─── FONDO LOGIN ─────────────────────────────────────────────────────────
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://png.pngtree.com/background/20230528/original/pngtree-gym-is-reflected-in-an-odd-light-picture-image_2773779.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background: linear-gradient(
            135deg,
            rgba(5, 8, 15, 0.90) 0%,
            rgba(20, 8, 3, 0.88) 50%,
            rgba(5, 8, 15, 0.92) 100%
        );
        z-index: 0;
        pointer-events: none;
    }
    [data-testid="stHeader"] {
        background: transparent !important;
    }
    .block-container {
        position: relative;
        z-index: 1;
    }
    /* Animación de entrada del card */
    .login-card-anim {
        animation: fadeSlideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
    }
    @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(28px) scale(0.97); }
        to   { opacity: 1; transform: translateY(0)    scale(1);    }
    }
    /* Glow pulsante en el título */
    @keyframes flamePulse {
        0%, 100% { filter: drop-shadow(0 0 12px rgba(255,100,0,.5)); }
        50%       { filter: drop-shadow(0 0 28px rgba(255,150,0,.8)); }
    }
    .fire-title-glow {
        animation: flamePulse 2.8s ease-in-out infinite;
    }
    /* Mejora tabs en login */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,.04) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,107,53,.2) !important;
        padding: 3px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #6b7a99 !important;
        font-weight: 600 !important;
        letter-spacing: .5px !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(255,107,53,.18) !important;
        color: #ff8c55 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    # ─────────────────────────────────────────────────────────────────────────

    col1, col2, col3 = st.columns([1, 1.8, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="login-card-anim" style="text-align:center;padding:1rem 0 .5rem;">
            <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:4px;
                        background:linear-gradient(135deg,#ff6b35,#ffd166);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        filter:drop-shadow(0 0 16px rgba(255,100,0,.5));">
                🔥 FIREMUSCLE
            </div>
            <div style="font-size:.75rem;color:#6b7a99;letter-spacing:3px;text-transform:uppercase;margin-top:.3rem;">
                Forja tu mejor versión
            </div>
        </div>
        """, unsafe_allow_html=True)

        login_tab, register_tab = st.tabs(["🔑 Iniciar sesión", "✨ Crear cuenta"])

        with login_tab:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form(key="login_form", clear_on_submit=False):
                username = st.text_input("👤 Usuario", placeholder="Nombre de usuario")
                password = st.text_input("🔑 Contraseña", type="password", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted_login = st.form_submit_button("INICIAR SESIÓN", use_container_width=True)

            if submitted_login:
                if username in all_users and all_users[username]["password"] == password:
                    st.session_state.logged_in  = True
                    st.session_state.username   = username
                    st.session_state.data       = load_data(username)
                    st.rerun()
                else:
                    st.markdown('<div class="alert-bad">❌ Usuario o contraseña incorrectos</div>', unsafe_allow_html=True)

        with register_tab:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form(key="register_form", clear_on_submit=False):
                new_user  = st.text_input("👤 Nombre de usuario", placeholder="Ej: StephanoEl")
                new_email = st.text_input("📧 Email", placeholder="tu@correo.com")
                new_pass  = st.text_input("🔑 Contraseña", type="password", placeholder="Mínimo 6 caracteres")
                new_pass2 = st.text_input("🔒 Confirmar contraseña", type="password", placeholder="Repite tu contraseña")
                st.markdown("<br>", unsafe_allow_html=True)
                submitted_register = st.form_submit_button("CREAR CUENTA", use_container_width=True)

            if submitted_register:
                if not new_user.strip():
                    st.markdown('<div class="alert-bad">❌ Ingresa un nombre de usuario</div>', unsafe_allow_html=True)
                elif new_user in all_users:
                    st.markdown('<div class="alert-bad">❌ Ese usuario ya existe</div>', unsafe_allow_html=True)
                elif len(new_pass) < 6:
                    st.markdown('<div class="alert-warn">⚠️ La contraseña debe tener al menos 6 caracteres</div>', unsafe_allow_html=True)
                elif new_pass != new_pass2:
                    st.markdown('<div class="alert-bad">❌ Las contraseñas no coinciden</div>', unsafe_allow_html=True)
                else:
                    all_users[new_user] = {"password": new_pass, "email": new_email}
                    save_users(all_users)
                    st.markdown('<div class="alert-good">✅ ¡Cuenta creada! Ahora inicia sesión.</div>', unsafe_allow_html=True)

            st.markdown("""<div style="text-align:center;margin-top:1.5rem;font-size:.65rem;color:#3a4560;letter-spacing:1px;">🔥 FIREMUSCLE v2.0 · StephanoEl</div>""", unsafe_allow_html=True)

    st.stop()
# ═══════════════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.data and st.session_state.username:
    st.session_state.data = load_data(st.session_state.username)

current_user = st.session_state.username
data = st.session_state.data

st.markdown(f"""
<div class="app-header">
    <div>
        <div class="app-title">🔥 FIREMUSCLE</div>
        <div class="app-subtitle">Forja tu mejor versión · Salud & Rendimiento · v2.0</div>
    </div>
    <div class="user-badge">👤 {current_user}</div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:3px;color:#00e5a0;margin-bottom:1rem;">⚙️ PERFIL PERSONAL</div>""", unsafe_allow_html=True)

    today_key = get_today_key()
    data = init_day(data, today_key)

    if "global_profile" not in data:
        data["global_profile"] = {}
    gp = data["global_profile"]

    age      = st.number_input("🎂 Edad",       min_value=10,  max_value=100,  value=int(gp.get("age", 22)),      step=1)
    weight   = st.number_input("⚖️ Peso (kg)",  min_value=30.0, max_value=250.0, value=float(gp.get("weight", 63.0)), step=0.5)
    height   = st.number_input("📏 Altura (cm)", min_value=100.0, max_value=220.0, value=float(gp.get("height", 168.0)), step=0.5)
    sex      = st.selectbox("⚥ Sexo", ["Masculino","Femenino"],
                            index=0 if gp.get("sex","Masculino")=="Masculino" else 1)
    activity = st.selectbox("🏃 Nivel de actividad",
                            ["Sedentario","Ligero","Moderado","Activo","Muy activo"],
                            index=["Sedentario","Ligero","Moderado","Activo","Muy activo"].index(gp.get("activity","Moderado")))
    use_excel_limits = st.toggle("📊 Usar objetivos del Excel", value=gp.get("use_excel_limits", True))

    if st.button("💾 Guardar Perfil", use_container_width=True):
        data["global_profile"] = {
            "age": age, "weight": weight, "height": height,
            "sex": sex, "activity": activity, "use_excel_limits": use_excel_limits,
            "deficit": gp.get("deficit", 0),
        }
        save_data(data, current_user)
        st.session_state.data = data
        st.success("✅ Perfil guardado")

    limits = calc_limits(age, weight, height, sex, activity, use_excel=use_excel_limits)

    st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
    src_label = "📊 Del Excel" if use_excel_limits else "🧮 Calculado"
    st.markdown(f"""<div style="font-size:.7rem;color:#6b7a99;text-transform:uppercase;letter-spacing:2px;margin-bottom:.8rem;">Tus límites diarios <span class='pill pill-info'>{src_label}</span></div>""", unsafe_allow_html=True)

    for k, v in {
        "🔥 Calorías": f"{limits['calorias']} kcal",
        "💪 Proteínas": f"{limits['proteinas']}g",
        "🌾 Carbos": f"{limits['carbohidratos']}g",
        "🧈 Grasas": f"{limits['grasas']}g",
        "🍬 Azúcar": f"{limits['azucar']}g",
        "🌿 Fibra": f"{limits['fibra']}g",
        "🧂 Sodio": f"{limits['sodio']}mg",
        "🫀 Colesterol": f"{limits['colesterol']}mg",
    }.items():
        st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:.35rem 0;border-bottom:1px solid #1e2d45;font-size:.8rem;"><span style="color:#6b7a99;">{k}</span><span style="font-family:'JetBrains Mono',monospace;color:#e8f0fe;font-size:.78rem;">{v}</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style="font-size:.65rem;color:#6b7a99;text-transform:uppercase;letter-spacing:2px;margin-bottom:.5rem;">⚡ Déficit / Superávit calórico</div>""", unsafe_allow_html=True)
    deficit_saved = int(gp.get("deficit", 0))
    deficit_val   = st.slider("kcal ajuste diario", min_value=-800, max_value=500, value=deficit_saved, step=50,
                              help="Negativo = déficit · Positivo = superávit")
    meta_cal = limits["calorias"] + deficit_val
    if deficit_val < 0:
        d_color, d_label, d_tip = "#4facfe", f"Déficit de {abs(deficit_val)} kcal", "Ideal para pérdida de grasa"
    elif deficit_val > 0:
        d_color, d_label, d_tip = "#ff6b35", f"Superávit de {deficit_val} kcal", "Ideal para ganar masa muscular"
    else:
        d_color, d_label, d_tip = "#00e5a0", "Mantenimiento", "Sin ajuste calórico"

    st.markdown(f"""
    <div style="background:#1a2332;border:1px solid #1e2d45;border-radius:10px;padding:.8rem;margin-top:.3rem;text-align:center;">
        <div style="font-family:'JetBrains Mono',monospace;font-size:1.4rem;color:{d_color};font-weight:700;">{meta_cal} kcal</div>
        <div style="font-size:.72rem;color:{d_color};font-weight:600;margin-top:.2rem;">{d_label}</div>
        <div style="font-size:.65rem;color:#6b7a99;margin-top:.1rem;">{d_tip}</div>
        <div style="font-size:.6rem;color:#6b7a99;margin-top:.3rem;">Base: {limits['calorias']} kcal · Ajuste: {"+" if deficit_val>=0 else ""}{deficit_val}</div>
    </div>
    """, unsafe_allow_html=True)

    if deficit_val != deficit_saved:
        data["global_profile"]["deficit"] = deficit_val
        save_data(data, current_user)
        st.session_state.data = data
    limits["calorias"] = meta_cal

    st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:   bmi_label, bmi_color = "Bajo peso",   "#4facfe"
    elif bmi < 25:   bmi_label, bmi_color = "Normal ✅",    "#00e5a0"
    elif bmi < 30:   bmi_label, bmi_color = "Sobrepeso",   "#ffd166"
    else:            bmi_label, bmi_color = "Obesidad",    "#ff4757"

    st.markdown(f"""<div style="background:#1a2332;border:1px solid #1e2d45;border-radius:12px;padding:1rem;text-align:center;"><div style="font-size:.65rem;color:#6b7a99;letter-spacing:2px;text-transform:uppercase;">IMC</div><div style="font-family:'Bebas Neue',sans-serif;font-size:2.5rem;color:{bmi_color};line-height:1.1;">{bmi:.1f}</div><div style="font-size:.8rem;color:{bmi_color};">{bmi_label}</div></div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in  = False
        st.session_state.username   = ""
        st.session_state.data       = {}
        st.session_state.editing_food_idx = None
        st.rerun()

# ─── NAVIGATION ────────────────────────────────────────────────────────────────
tab_nutricion, tab_ejercicio, tab_resumen, tab_database, tab_chat = st.tabs([
    "🥗 Nutrición", "🏋️ Rutina", "📊 Resumen", "🗄️ Database", "🤖 AI Coach"
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 · NUTRICIÓN
# ═══════════════════════════════════════════════════════════════════════════════
with tab_nutricion:
    today_key = get_today_key()
    data = init_day(data, today_key)

    st.markdown(f"""<div class="card"><div class="card-title">🥗 REGISTRO DE ALIMENTOS</div><div style="font-size:.8rem;color:#6b7a99;">📅 Hoy: {date.today().strftime('%A %d de %B, %Y')}</div></div>""", unsafe_allow_html=True)

    with st.expander("➕ Agregar alimento", expanded=True):
        fk = st.session_state.food_form_counter  # sufijo único por envío
        c1, c2 = st.columns([2, 1])
    with c1:
        food_name = st.text_input("🍽️ Nombre del alimento", placeholder="Ej: Pechuga de pollo a la plancha", key=f"fn_{fk}")
        meal_type = st.selectbox("🕐 Momento del día", ["🌅 Desayuno","🌞 Almuerzo","🌙 Cena","🍎 Snack"], key=f"mt_{fk}")
    with c2:
        portion = st.text_input("📏 Porción", placeholder="200g / 1 taza", key=f"po_{fk}")

    st.markdown("**Información nutricional:**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cal  = st.number_input("🔥 Calorías (kcal)", min_value=0.0, step=1.0, key=f"ca_{fk}")
        prot = st.number_input("💪 Proteínas (g)",   min_value=0.0, step=0.1, key=f"pr_{fk}")
    with col2:
        carbs = st.number_input("🌾 Carbos (g)",  min_value=0.0, step=0.1, key=f"cb_{fk}")
        fat   = st.number_input("🧈 Grasas (g)",  min_value=0.0, step=0.1, key=f"fa_{fk}")
    with col3:
        sugar = st.number_input("🍬 Azúcar (g)", min_value=0.0, step=0.1, key=f"su_{fk}")
        fiber = st.number_input("🌿 Fibra (g)",  min_value=0.0, step=0.1, key=f"fi_{fk}")
    with col4:
        sodium = st.number_input("🧂 Sodio (mg)",      min_value=0.0, step=1.0, key=f"so_{fk}")
        chol   = st.number_input("🫀 Colesterol (mg)", min_value=0.0, step=1.0, key=f"ch_{fk}")

    if st.button("✅ Agregar Alimento", use_container_width=True):
        if food_name.strip():
            data[today_key]["foods"].append({
                "nombre": food_name, "porcion": portion, "comida": meal_type,
                "calorias": cal, "proteinas": prot, "carbohidratos": carbs,
                "grasas": fat, "azucar": sugar, "fibra": fiber,
                "sodio": sodium, "colesterol": chol,
                "hora": datetime.now().strftime("%H:%M"),
            })
            save_data(data, current_user)
            st.session_state.data = data
            st.session_state.food_form_counter += 1  # ← esto resetea todos los inputs
            st.success(f"✅ '{food_name}' agregado")
            st.rerun()
        else:
            st.error("Ingresa el nombre del alimento")

    st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)

    foods = data[today_key].get("foods", [])
    if foods:
        totals = sum_nutrients(foods)

        st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#4facfe;margin-bottom:.8rem;">📊 TOTALES DEL DÍA</div>""", unsafe_allow_html=True)
        cols = st.columns(4)
        for i, (label, val, lim, unit) in enumerate([
            ("🔥 Calorías",  totals["calorias"],       limits["calorias"],       "kcal"),
            ("💪 Proteínas", totals["proteinas"],      limits["proteinas"],      "g"),
            ("🌾 Carbos",    totals["carbohidratos"],  limits["carbohidratos"],  "g"),
            ("🧈 Grasas",    totals["grasas"],         limits["grasas"],         "g"),
        ]):
            with cols[i]:
                pct   = min(val / lim * 100, 100) if lim > 0 else 0
                color = "#00e5a0" if pct<=80 else "#ffd166" if pct<=100 else "#ff4757"
                st.markdown(f"""<div class="metric-box"><div style="font-size:.65rem;color:#6b7a99;letter-spacing:1.5px;text-transform:uppercase;">{label}</div><div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:{color};line-height:1.1;">{val:.0f}<span style="font-size:.9rem;">{unit}</span></div><div style="font-size:.65rem;color:#6b7a99;">/ {lim}{unit}</div><div style="margin-top:.5rem;height:4px;background:#1e2d45;border-radius:99px;"><div style="width:{pct:.0f}%;height:100%;border-radius:99px;background:{color};"></div></div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:.95rem;letter-spacing:2px;color:#4facfe;margin-bottom:.8rem;">🔍 DETALLE NUTRICIONAL</div>""", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        for i, (key, label, unit) in enumerate([
            ("azucar","🍬 Azúcar","g"), ("fibra","🌿 Fibra","g"),
            ("sodio","🧂 Sodio","mg"), ("colesterol","🫀 Colesterol","mg"),
        ]):
            val = totals[key]; lim = limits[key]
            pct = min(val/lim*100, 150) if lim>0 else 0
            status_txt, cls, msg = get_status(val, lim, key)
            bar_class = "prog-good" if cls=="good" else "prog-warn" if cls=="warn" else "prog-bad"
            target = col_a if i%2==0 else col_b
            with target:
                st.markdown(f"""<div class="prog-wrap"><div class="prog-label"><span>{label} <span class="pill pill-{cls}">{status_txt}</span></span><span>{val:.0f}/{lim}{unit}</span></div><div class="prog-bar"><div class="prog-fill {bar_class}" style="width:{min(pct,100):.0f}%"></div></div><div style="font-size:.68rem;color:#6b7a99;margin-top:.2rem;">{msg}</div></div>""", unsafe_allow_html=True)

        st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
        result = overall_diet_status(foods, limits)
        if result:
            cls, msg = result
            st.markdown(f'<div class="alert-{cls}"><strong>{msg}</strong></div>', unsafe_allow_html=True)

        st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
        st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:.95rem;letter-spacing:2px;color:#00e5a0;margin-bottom:.8rem;">🍽️ ALIMENTOS REGISTRADOS</div>""", unsafe_allow_html=True)

        for i, food in enumerate(foods):
            is_editing = (st.session_state.editing_food_idx == i)
            col_f, col_btns = st.columns([11, 1])
            with col_f:
                prot_v = float(food.get("proteinas",0))
                carb_v = float(food.get("carbohidratos",0))
                gras_v = float(food.get("grasas",0))
                macros = f"P:{prot_v:.0f}g  C:{carb_v:.0f}g  G:{gras_v:.0f}g" if (prot_v+carb_v+gras_v)>0 else ""
                parts  = [p for p in [food.get("porcion","").strip(), macros, f"⏰ {food.get('hora','—')}"] if p]
                border = "#4facfe" if is_editing else "var(--border)"
                st.markdown(f"""<div class="food-row" style="border-color:{border};"><div><div class="food-name">{food['comida']} &nbsp; {food['nombre']}</div><div style="font-size:.72rem;color:#6b7a99;margin-top:.15rem;">{"  |  ".join(parts)}</div></div><div class="food-cal">{food['calorias']:.0f} kcal</div></div>""", unsafe_allow_html=True)
            with col_btns:
                edit_label = "✏️" if not is_editing else "✖️"
                if st.button(edit_label, key=f"edit_food_{i}", use_container_width=True):
                    st.session_state.editing_food_idx = None if is_editing else i
                    st.rerun()
                if st.button("🗑️", key=f"del_food_{i}", use_container_width=True):
                    data[today_key]["foods"].pop(i)
                    if st.session_state.editing_food_idx == i:
                        st.session_state.editing_food_idx = None
                    save_data(data, current_user)
                    st.session_state.data = data
                    st.rerun()

            if is_editing:
                st.markdown(f"""<div style="background:#0d1b2e;border:1px solid #4facfe;border-radius:12px;padding:1rem;margin:.2rem 0 .5rem 0;"><div style="font-family:'Bebas Neue',sans-serif;letter-spacing:2px;color:#4facfe;font-size:.85rem;margin-bottom:.7rem;">✏️ EDITANDO: {food['nombre']}</div></div>""", unsafe_allow_html=True)
                ec1, ec2 = st.columns([2,1])
                with ec1:
                    e_name = st.text_input("🍽️ Nombre", value=food.get("nombre",""), key=f"e_name_{i}")
                    meal_opts = ["🌅 Desayuno","🌞 Almuerzo","🌙 Cena","🍎 Snack"]
                    e_meal = st.selectbox("🕐 Momento", meal_opts,
                        index=meal_opts.index(food.get("comida","🌅 Desayuno")) if food.get("comida") in meal_opts else 0,
                        key=f"e_meal_{i}")
                with ec2:
                    e_portion = st.text_input("📏 Porción", value=food.get("porcion",""), key=f"e_portion_{i}")
                ea,eb,ec_,ed = st.columns(4)
                with ea:
                    e_cal  = st.number_input("🔥 Kcal",   value=float(food.get("calorias",0)),  min_value=0.0, step=1.0,  key=f"e_cal_{i}")
                    e_prot = st.number_input("💪 Prot g",  value=float(food.get("proteinas",0)), min_value=0.0, step=0.1,  key=f"e_prot_{i}")
                with eb:
                    e_carb = st.number_input("🌾 Carbs g", value=float(food.get("carbohidratos",0)), min_value=0.0, step=0.1, key=f"e_carb_{i}")
                    e_fat  = st.number_input("🧈 Grasas g", value=float(food.get("grasas",0)),  min_value=0.0, step=0.1,  key=f"e_fat_{i}")
                with ec_:
                    e_sug  = st.number_input("🍬 Azúcar g", value=float(food.get("azucar",0)),  min_value=0.0, step=0.1,  key=f"e_sug_{i}")
                    e_fib  = st.number_input("🌿 Fibra g",  value=float(food.get("fibra",0)),   min_value=0.0, step=0.1,  key=f"e_fib_{i}")
                with ed:
                    e_sod  = st.number_input("🧂 Sodio mg", value=float(food.get("sodio",0)),   min_value=0.0, step=1.0,  key=f"e_sod_{i}")
                    e_cho  = st.number_input("🫀 Col mg",   value=float(food.get("colesterol",0)), min_value=0.0, step=1.0, key=f"e_cho_{i}")
                if st.button("💾 Guardar cambios", key=f"save_edit_{i}", use_container_width=True):
                    data[today_key]["foods"][i] = {
                        "nombre": e_name, "porcion": e_portion, "comida": e_meal,
                        "calorias": e_cal, "proteinas": e_prot, "carbohidratos": e_carb,
                        "grasas": e_fat, "azucar": e_sug, "fibra": e_fib,
                        "sodio": e_sod, "colesterol": e_cho,
                        "hora": food.get("hora", datetime.now().strftime("%H:%M")),
                        "editado": datetime.now().strftime("%H:%M"),
                    }
                    save_data(data, current_user)
                    st.session_state.data = data
                    st.session_state.editing_food_idx = None
                    st.rerun()
    else:
        st.markdown("""<div style="text-align:center;padding:3rem;color:#6b7a99;"><div style="font-size:3rem;margin-bottom:1rem;">🍽️</div><div>Sin alimentos registrados hoy</div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 · EJERCICIOS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_ejercicio:
    st.markdown("""<div class="card card-orange"><div class="card-title">🏋️ RUTINA SEMANAL · AUTOCARGADA</div><div style="font-size:.8rem;color:#6b7a99;">Rutina prellenada desde tu Excel · Lunes a Sábado · Domingo = Descanso 💤</div></div>""", unsafe_allow_html=True)

    day_cols = st.columns(6)
    for i, (dia_key, dia_data_rut) in enumerate(RUTINA_BASE.items()):
        with day_cols[i]:
            dow_today = date.today().weekday()
            is_today  = (DIA_SEMANA_MAP.get(dow_today) == dia_key)
            label     = f"{'📍 ' if is_today else ''}{dia_key}"
            if st.button(label, key=f"daybtn_{i}", use_container_width=True):
                st.session_state.selected_day = dia_key

    selected     = st.session_state.selected_day
    rutina_dia   = RUTINA_BASE.get(selected, RUTINA_BASE["Día 1"])
    storage_key  = f"exercises_{selected}"

    st.markdown(f"""<div style="display:flex;align-items:center;gap:1rem;margin:1rem 0 .5rem;"><div style="font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:3px;color:#ff6b35;">{selected.upper()}: {rutina_dia['titulo'].upper()}</div><span class="routine-badge">✨ Rutina cargada del Excel</span></div>""", unsafe_allow_html=True)

    if storage_key not in data:
        data[storage_key] = {"exercises": []}

    with st.expander("📋 Ver rutina del día (del Excel)", expanded=True):
        st.markdown(f"""<div class="alert-info">💡 Rutina oficial para <strong>{selected}: {rutina_dia['titulo']}</strong>. Guárdala con un clic o agrega ejercicios personalizados abajo.</div>""", unsafe_allow_html=True)

        for ej in rutina_dia["ejercicios"]:
            mc = {"Abdomen":"#ffd166","Espalda":"#00e5a0","Pecho":"#ff6b35",
                  "Pierna":"#4facfe","Bíceps":"#a78bfa","Triceps":"#ec4899",
                  "Cardio":"#ff4757","Core":"#ffd166","Espalda/Brazos":"#00e5a0"}.get(ej["musculo"],"#6b7a99")
            series_str = str(ej["series"]) if ej["series"]>0 else "-"
            st.markdown(f"""<div class="db-ex-row" style="padding:.5rem .3rem;"><span style="color:{mc};font-weight:600;min-width:90px;font-size:.78rem;">{ej['musculo']}</span><span style="flex:1;color:#e8f0fe;font-size:.85rem;">{ej['nombre']}</span><span style="color:#6b7a99;font-family:'JetBrains Mono',monospace;font-size:.72rem;">{series_str} series · {ej['reps']} · {ej['descanso']}</span></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_save, col_clear = st.columns(2)
        with col_save:
            if st.button(f"✅ Guardar rutina de hoy ({selected})", use_container_width=True, key="save_routine"):
                exercises_to_save = []
                for ej in rutina_dia["ejercicios"]:
                    exercises_to_save.append({
                        "nombre":       ej["nombre"],
                        "musculo":      ej["musculo"],
                        "tipo":         "Fuerza",
                        "duracion":     0,
                        "series":       ej["series"],
                        "reps":         ej["reps"],
                        "peso":         0.0,
                        "descanso_txt": ej["descanso"],
                        "notas":        "",
                        "hora":         datetime.now().strftime("%H:%M"),
                        "fuente":       "excel",
                    })
                data[storage_key]["exercises"] = exercises_to_save
                save_data(data, current_user)
                st.session_state.data = data
                st.success(f"✅ Rutina de {selected} guardada ({len(exercises_to_save)} ejercicios)")
                st.rerun()
        with col_clear:
            if st.button("🗑️ Borrar ejercicios del día", use_container_width=True, key="clear_exercises"):
                data[storage_key]["exercises"] = []
                save_data(data, current_user)
                st.session_state.data = data
                st.rerun()

    st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)

    with st.expander("➕ Agregar ejercicio personalizado"):
        ec1, ec2 = st.columns([2,1])
        with ec1:
            ex_name  = st.text_input("🏋️ Nombre del ejercicio", placeholder="Ej: Press de banca...")
            ex_group = st.selectbox("💪 Grupo muscular",
                ["Pecho","Espalda","Hombros","Bíceps","Tríceps","Piernas","Glúteos","Core/Abdomen","Cardio","Cuerpo completo"])
        with ec2:
            ex_type = st.selectbox("📌 Tipo", ["Fuerza","Cardio","Flexibilidad","HIIT","Funcional"])
            ex_dur  = st.number_input("⏱️ Duración (min)", min_value=0, max_value=300, value=0, step=5)
        ex1,ex2,ex3,ex4 = st.columns(4)
        with ex1: ex_sets    = st.number_input("📋 Series", min_value=0, max_value=20, value=0)
        with ex2: ex_reps_tx = st.text_input("🔁 Reps", placeholder="10, 10, 8")
        with ex3: ex_kg      = st.number_input("⚖️ Peso (kg)", min_value=0.0, max_value=500.0, value=0.0, step=0.5)
        with ex4: ex_rest    = st.text_input("😴 Descanso", placeholder="30 seg / 1 min")
        ex_notes = st.text_area("📝 Notas (opcional)", placeholder="RPE, sensaciones...", height=60)

        if st.button("✅ Agregar Ejercicio", use_container_width=True, key="add_custom_ex"):
            if ex_name.strip():
                data[storage_key]["exercises"].append({
                    "nombre":       ex_name,
                    "musculo":      ex_group,
                    "tipo":         ex_type,
                    "duracion":     ex_dur,
                    "series":       ex_sets,
                    "reps":         ex_reps_tx,
                    "peso":         ex_kg,
                    "descanso_txt": ex_rest,
                    "notas":        ex_notes,
                    "hora":         datetime.now().strftime("%H:%M"),
                    "fuente":       "manual",
                })
                save_data(data, current_user)
                st.session_state.data = data
                st.success(f"✅ '{ex_name}' agregado")
                st.rerun()
            else:
                st.error("Ingresa el nombre del ejercicio")

    exercises = data[storage_key].get("exercises", [])
    if exercises:
        total_sets  = sum(int(e.get("series",0) or 0) for e in exercises)
        grupos_uq   = len(set(get_musculo_from_exercise(e) for e in exercises))
        sc1,sc2,sc3 = st.columns(3)
        for col, val, label in zip([sc1,sc2,sc3],
                                   [len(exercises), total_sets, grupos_uq],
                                   ["Ejercicios","Series totales","Grupos musculares"]):
            with col:
                st.markdown(f"""<div class="metric-box"><div class="metric-val" style="color:#ff6b35;">{val}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

        st.markdown(f"""<br><div style="font-family:'Bebas Neue',sans-serif;font-size:.95rem;letter-spacing:2px;color:#ff6b35;margin-bottom:.8rem;">✅ EJERCICIOS REGISTRADOS HOY ({len(exercises)})</div>""", unsafe_allow_html=True)
        icon_map = {"Fuerza":"🏋️","Cardio":"🏃","Flexibilidad":"🧘","HIIT":"⚡","Funcional":"🤸"}

        for i, ex in enumerate(exercises):
            icon    = icon_map.get(ex.get("tipo","Fuerza"), "💪")
            musculo = get_musculo_from_exercise(ex)
            fuente_badge = '<span class="routine-badge" style="font-size:.6rem;">📊 Excel</span>' if ex.get("fuente")=="excel" else '<span class="pill pill-purple" style="font-size:.6rem;">✏️ Manual</span>'
            parts   = []
            if ex.get("series"): parts.append(f"{ex['series']} series")
            if ex.get("reps"):   parts.append(str(ex["reps"]))
            if ex.get("peso"):   parts.append(f"{ex['peso']}kg")
            desc = ex.get("descanso_txt","") or ""
            if desc: parts.append(f"Desc: {desc}")
            detail = "  |  ".join(parts) if parts else "—"

            col_ex, col_del = st.columns([10,1])
            with col_ex:
                st.markdown(f"""<div class="ex-entry"><div class="ex-icon">{icon}</div><div class="ex-info"><div class="ex-name">{ex['nombre']} <span style="font-size:.7rem;color:#6b7a99;font-weight:400;">[{musculo}]</span> {fuente_badge}</div><div class="ex-detail">{detail}</div>{f'<div class="ex-detail" style="color:#4facfe;">📝 {ex["notas"]}</div>' if ex.get("notas") else ""}</div><div style="font-size:.7rem;color:#6b7a99;">⏰ {ex.get('hora','—')}</div></div>""", unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_ex_{selected}_{i}"):
                    data[storage_key]["exercises"].pop(i)
                    save_data(data, current_user)
                    st.session_state.data = data
                    st.rerun()

        # ─── GUARDAR EN DATABASE ────────────────────────────────────────────
        st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
        st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:.9rem;letter-spacing:2px;color:#a78bfa;margin-bottom:.5rem;">🗄️ GUARDAR EN BASE DE DATOS</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="alert-info">💡 Guarda el día completo (ejercicios + nutrición) en la Database histórica.</div>""", unsafe_allow_html=True)

        coldb1, coldb2 = st.columns([2,1])
        with coldb1:
            suggested_week = get_next_semana_num(data)
            semana_num_input = st.number_input(
                "Número de semana", min_value=1, max_value=52,
                value=suggested_week, step=1,
                help="El sistema sugiere la siguiente semana disponible. Puedes cambiarlo para sobrescribir una existente."
            )
            dia_options  = ["DÍA 1","DÍA 2","DÍA 3","DÍA 4","DÍA 5","DÍA 6","DÍA 7"]
            suggested_dia_idx = ["Día 1","Día 2","Día 3","Día 4","Día 5","Día 6"].index(selected) if selected in ["Día 1","Día 2","Día 3","Día 4","Día 5","Día 6"] else 0
            dia_label_input  = st.selectbox("Día de la semana", dia_options, index=suggested_dia_idx)
            notas_db = st.text_input("Notas del día (opcional)", placeholder="Ej: Buen entrenamiento, aumenté peso...")

            sem_check = f"Semana {semana_num_input}"
            existing_weeks = get_all_weeks(data)
            if sem_check in existing_weeks and dia_label_input in existing_weeks[sem_check].get("dias",{}):
                st.markdown(f"""<div class="alert-warn">⚠️ <strong>Semana {semana_num_input} · {dia_label_input}</strong> ya existe. Se sobrescribirá.</div>""", unsafe_allow_html=True)

        with coldb2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            today_foods = data.get(today_key, {}).get("foods", [])
            st.markdown(f"""<div style="background:#1a2332;border:1px solid #1e2d45;border-radius:10px;padding:.8rem;font-size:.8rem;color:#6b7a99;"><div>💪 <strong style="color:#ff6b35;">{len(exercises)}</strong> ejercicios</div><div>🥗 <strong style="color:#00e5a0;">{len(today_foods)}</strong> alimentos</div><div style="margin-top:.3rem;font-size:.7rem;">Se guardarán ambos</div></div>""", unsafe_allow_html=True)

        if st.button("💾 Guardar en Database", use_container_width=True, key="save_to_db"):
            today_foods = data.get(today_key, {}).get("foods", [])
            data = guardar_dia_en_db(data, semana_num_input, dia_label_input, exercises, today_foods, notas_db)
            save_data(data, current_user)
            st.session_state.data = data
            st.success(f"✅ Guardado en Semana {semana_num_input} · {dia_label_input}")

    else:
        st.markdown(f"""<div style="text-align:center;padding:2rem;color:#6b7a99;"><div style="font-size:3rem;margin-bottom:1rem;">🏋️</div><div>Sin ejercicios guardados para {selected}</div><div style="font-size:.8rem;margin-top:.5rem;">Usa "Guardar rutina de hoy" para cargar desde el Excel, o agrega uno personalizado</div></div>""", unsafe_allow_html=True)

    st.markdown("""<div style="background:rgba(79,172,254,.08);border:1px solid rgba(79,172,254,.2);border-radius:12px;padding:1rem 1.2rem;margin-top:1rem;text-align:center;color:#4facfe;font-size:.85rem;">☀️ <strong>Domingo</strong> — Día de descanso y recuperación. 💤</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 · RESUMEN
# ═══════════════════════════════════════════════════════════════════════════════
with tab_resumen:
    st.markdown("""<div class="card card-blue"><div class="card-title">📊 RESUMEN DEL DÍA</div><div style="font-size:.8rem;color:#6b7a99;">Vista general de nutrición + entrenamiento de hoy</div></div>""", unsafe_allow_html=True)

    today_key   = get_today_key()
    data        = init_day(data, today_key)
    foods       = data[today_key].get("foods", [])
    dow         = date.today().weekday()
    today_dia_key = DIA_SEMANA_MAP.get(dow)
    ex_storage_key = f"exercises_{today_dia_key}" if today_dia_key else None
    exercises_today = data.get(ex_storage_key,{}).get("exercises",[]) if ex_storage_key else []

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#00e5a0;margin-bottom:.8rem;">🥗 NUTRICIÓN HOY</div>""", unsafe_allow_html=True)
        if foods:
            totals   = sum_nutrients(foods)
            pct_cal  = min(totals["calorias"]/limits["calorias"]*100, 100) if limits["calorias"]>0 else 0
            cal_col  = "#00e5a0" if pct_cal<=80 else "#ffd166" if pct_cal<=100 else "#ff4757"
            st.markdown(f"""<div class="metric-box" style="margin-bottom:.8rem;"><div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:{cal_col};">{totals['calorias']:.0f}</div><div class="metric-label">kcal consumidas de {limits['calorias']}</div></div>""", unsafe_allow_html=True)
            for key, label, unit in [
                ("proteinas","💪 Proteínas","g"),("carbohidratos","🌾 Carbos","g"),
                ("grasas","🧈 Grasas","g"),("azucar","🍬 Azúcar","g"),
                ("fibra","🌿 Fibra","g"),("sodio","🧂 Sodio","mg"),
            ]:
                val = totals[key]; lim = limits[key]
                pct = min(val/lim*100, 100) if lim>0 else 0
                st_txt,cls,_ = get_status(val,lim,key)
                bc = "prog-good" if cls=="good" else "prog-warn" if cls=="warn" else "prog-bad"
                st.markdown(f"""<div class="prog-wrap"><div class="prog-label"><span>{label} <span class="pill pill-{cls}">{st_txt}</span></span><span>{val:.0f}/{lim}{unit}</span></div><div class="prog-bar"><div class="prog-fill {bc}" style="width:{pct:.0f}%"></div></div></div>""", unsafe_allow_html=True)
            result = overall_diet_status(foods, limits)
            if result:
                cls,msg = result
                st.markdown(f'<div class="alert-{cls}" style="margin-top:.8rem;">{msg}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#6b7a99;padding:2rem;text-align:center;">Sin datos de nutrición hoy</div>', unsafe_allow_html=True)

    with r2:
        today_dia_label = RUTINA_BASE.get(today_dia_key,{}).get("titulo","Domingo") if today_dia_key else "Domingo"
        st.markdown(f"""<div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#ff6b35;margin-bottom:.8rem;">🏋️ ENTRENAMIENTO HOY {"("+today_dia_label+")" if today_dia_key else "(DOMINGO)"}</div>""", unsafe_allow_html=True)
        if not today_dia_key:
            st.markdown("""<div style="text-align:center;padding:2rem;color:#4facfe;"><div style="font-size:3rem;">😴</div><div>Hoy es Domingo · Día de descanso</div></div>""", unsafe_allow_html=True)
        elif exercises_today:
            total_sets = sum(int(e.get("series",0) or 0) for e in exercises_today)
            grupos     = list(set(get_musculo_from_exercise(e) for e in exercises_today))
            st.markdown(f"""<div class="metric-box" style="margin-bottom:.8rem;"><div class="metric-val" style="color:#ff6b35;">{len(exercises_today)}</div><div class="metric-label">ejercicios · {total_sets} series</div></div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style="font-size:.75rem;color:#6b7a99;margin-bottom:.5rem;">Grupos: {', '.join(grupos)}</div>""", unsafe_allow_html=True)
            for ex in exercises_today:
                parts = []
                if ex.get("series"): parts.append(f"{ex['series']} series")
                if ex.get("reps"):   parts.append(str(ex["reps"]))
                st.markdown(f"""<div style="background:#1a2332;border:1px solid #1e2d45;border-radius:8px;padding:.6rem .8rem;margin:.3rem 0;font-size:.82rem;"><strong>{ex['nombre']}</strong><span style="color:#6b7a99;margin-left:.5rem;">{' | '.join(parts)}</span></div>""", unsafe_allow_html=True)
        else:
            rutina_hoy = RUTINA_BASE.get(today_dia_key)
            if rutina_hoy:
                st.markdown(f"""<div class="alert-warn">⚡ Sin ejercicios registrados. Tu rutina de hoy: <strong>{rutina_hoy['titulo']}</strong> ({len(rutina_hoy['ejercicios'])} ejercicios). Ve a Rutina para cargarla.</div>""", unsafe_allow_html=True)

    st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
    st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;letter-spacing:2px;color:#4facfe;margin-bottom:.8rem;">📅 RESUMEN SEMANAL</div>""", unsafe_allow_html=True)
    week_cols = st.columns(7)
    dia_names = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
    for i in range(7):
        dia_key = DIA_SEMANA_MAP.get(i)
        exs     = data.get(f"exercises_{dia_key}",{}).get("exercises",[]) if dia_key else []
        is_tod  = (date.today().weekday()==i)
        color   = "#ff6b35" if is_tod else "#4facfe" if exs else "#6b7a99"
        icon    = "📍" if is_tod else "✅" if exs else ("😴" if i==6 else "○")
        with week_cols[i]:
            st.markdown(f"""<div style="text-align:center;background:#111827;border:1px solid {'#ff6b35' if is_tod else '#1e2d45'};border-radius:10px;padding:.8rem .3rem;"><div style="font-size:1.2rem;">{icon}</div><div style="font-family:'Bebas Neue',sans-serif;letter-spacing:1px;color:{color};font-size:.9rem;">{dia_names[i]}</div><div style="font-size:.65rem;color:#6b7a99;margin-top:.2rem;">{len(exs)} ej.</div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 · DATABASE
# ═══════════════════════════════════════════════════════════════════════════════
with tab_database:
    st.markdown("""<div class="card card-purple"><div class="card-title">🗄️ BASE DE DATOS HISTÓRICA</div><div style="font-size:.8rem;color:#6b7a99;">Historial completo por semana y día · Ejercicios + Nutrición + Notas</div></div>""", unsafe_allow_html=True)

    weeks_data = get_all_weeks(data)

    if not weeks_data:
        st.markdown("""
        <div style="text-align:center;padding:4rem;color:#6b7a99;">
            <div style="font-size:4rem;margin-bottom:1rem;">🗄️</div>
            <div style="font-size:1.2rem;font-weight:600;color:#a78bfa;">Base de datos vacía</div>
            <div style="font-size:.9rem;margin-top:.8rem;">
                Para guardar datos, ve a la pestaña <strong style="color:#ff6b35;">Rutina</strong>,<br>
                registra tus ejercicios del día y usa el botón<br>
                <strong>💾 Guardar en Database</strong> al final.
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        fcol1, fcol2, fcol3 = st.columns(3)
        with fcol1:
            all_week_keys = sorted(weeks_data.keys(),
                                   key=lambda x: int(x.split()[-1]) if x.split()[-1].isdigit() else 0)
            filter_week = st.selectbox("🗓️ Filtrar por semana", ["Todas"] + all_week_keys, key="db_filter_week")
        with fcol2:
            filter_dia = st.selectbox("📅 Filtrar por día",
                                      ["Todos","DÍA 1","DÍA 2","DÍA 3","DÍA 4","DÍA 5","DÍA 6","DÍA 7"],
                                      key="db_filter_dia")
        with fcol3:
            filter_tipo = st.selectbox("🔍 Mostrar", ["Todo","Solo ejercicios","Solo nutrición"],
                                       key="db_filter_tipo")

        st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)

        total_dias         = sum(len(s.get("dias",{})) for s in weeks_data.values())
        total_sem          = len(weeks_data)
        total_ex_global    = sum(len(d.get("ejercicios",[]))
                                 for s in weeks_data.values()
                                 for d in s.get("dias",{}).values())
        total_meals_global = sum(len(d.get("alimentos",[]))
                                 for s in weeks_data.values()
                                 for d in s.get("dias",{}).values())

        gs1, gs2, gs3, gs4 = st.columns(4)
        for col, val, label, color in zip(
            [gs1, gs2, gs3, gs4],
            [total_sem, total_dias, total_ex_global, total_meals_global],
            ["Semanas","Días registrados","Ejercicios totales","Comidas registradas"],
            ["#a78bfa","#4facfe","#ff6b35","#00e5a0"],
        ):
            with col:
                st.markdown(f"""<div class="metric-box"><div class="metric-val" style="color:{color};">{val}</div><div class="metric-label">{label}</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        weeks_to_show = {k: v for k, v in weeks_data.items()
                         if filter_week == "Todas" or k == filter_week}

        for sem_key in sorted(weeks_to_show.keys(),
                              key=lambda x: int(x.split()[-1]) if x.split()[-1].isdigit() else 0,
                              reverse=True):
            sem_obj = weeks_to_show[sem_key]
            dias    = sem_obj.get("dias", {})
            fecha_i = sem_obj.get("fecha_inicio", "")

            dias_to_show = {}
            for dk, dv in dias.items():
                if filter_dia == "Todos":
                    dias_to_show[dk] = dv
                else:
                    if dk.upper().replace(" ", "") == filter_dia.upper().replace(" ", ""):
                        dias_to_show[dk] = dv

            if not dias_to_show:
                continue

            st.markdown(f"""<div class="db-week-header">📅 {sem_key.upper()}</div>""", unsafe_allow_html=True)
            if fecha_i:
                try:
                    fi = date.fromisoformat(fecha_i)
                    st.markdown(f"""<div style="font-size:.75rem;color:#6b7a99;margin-bottom:.8rem;">Inicio: {fi.strftime('%d/%m/%Y')}</div>""", unsafe_allow_html=True)
                except Exception:
                    pass

            for dia_key in sorted(dias_to_show.keys()):
                dia_obj       = dias_to_show[dia_key]
                ejercicios    = dia_obj.get("ejercicios", [])
                alimentos     = dia_obj.get("alimentos", [])
                notas         = dia_obj.get("notas", "")
                fecha_dia     = dia_obj.get("fecha", "")
                hora_guardado = dia_obj.get("guardado_en", "")

                try:
                    fecha_fmt = date.fromisoformat(fecha_dia).strftime("%d/%m/%Y (%A)")
                except Exception:
                    fecha_fmt = fecha_dia

                nut_totals = sum_nutrients(alimentos) if alimentos else {}
                cal_dia    = nut_totals.get("calorias", 0)
                ex_count   = len([e for e in ejercicios if e.get("nombre", "") != "Descanso"])

                with st.expander(
                    f"{'📍 ' if fecha_dia == get_today_key() else ''}"
                    f"{dia_key} · {fecha_fmt} · "
                    f"{ex_count} ejercicios · {cal_dia:.0f} kcal"
                ):
                    if notas:
                        st.markdown(f"""<div class="alert-info">📝 {notas}</div>""", unsafe_allow_html=True)

                    grupos_dia = list(set(get_musculo_from_exercise(e)
                                         for e in ejercicios
                                         if e.get("nombre", "") != "Descanso"))
                    if grupos_dia:
                        badges = " ".join(f'<span class="pill pill-info">{g}</span>' for g in grupos_dia[:5])
                        st.markdown(f"<div style='margin-bottom:.8rem;'>{badges}</div>", unsafe_allow_html=True)

                    db_col1, db_col2 = st.columns(2)

                    with db_col1:
                        if filter_tipo != "Solo nutrición":
                            st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:.9rem;letter-spacing:2px;color:#ff6b35;margin-bottom:.5rem;">🏋️ EJERCICIOS</div>""", unsafe_allow_html=True)
                            if ejercicios:
                                for ex in ejercicios:
                                    if ex.get("nombre") == "Descanso":
                                        continue
                                    musculo = get_musculo_from_exercise(ex)
                                    mc = {"Abdomen":"#ffd166","Espalda":"#00e5a0","Pecho":"#ff6b35",
                                          "Pierna":"#4facfe","Bíceps":"#a78bfa","Triceps":"#ec4899",
                                          "Cardio":"#ff4757","Core":"#ffd166","Espalda/Brazos":"#00e5a0",
                                          }.get(musculo, "#6b7a99")
                                    series_str = str(ex.get("series", "-")) if ex.get("series") else "-"
                                    reps_str   = str(ex.get("reps",   "-")) if ex.get("reps")   else "-"
                                    fuente     = "📊" if ex.get("fuente") == "excel" else "✏️"
                                    st.markdown(f"""<div class="db-ex-row"><span style="color:{mc};font-weight:600;min-width:85px;font-size:.75rem;">{musculo}</span><span class="db-nombre">{fuente} {ex['nombre']}</span><span class="db-detail">{series_str}s · {reps_str}</span></div>""", unsafe_allow_html=True)
                            else:
                                st.markdown('<div style="color:#6b7a99;font-size:.8rem;padding:.5rem;">Sin ejercicios</div>', unsafe_allow_html=True)

                    with db_col2:
                        if filter_tipo != "Solo ejercicios":
                            st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:.9rem;letter-spacing:2px;color:#00e5a0;margin-bottom:.5rem;">🥗 NUTRICIÓN</div>""", unsafe_allow_html=True)
                            if alimentos:
                                prot_dia = nut_totals.get("proteinas", 0)
                                st.markdown(f"""<div style="background:#1a2332;border:1px solid #1e2d45;border-radius:8px;padding:.7rem;margin-bottom:.5rem;display:flex;gap:1rem;flex-wrap:wrap;"><span style="font-family:'JetBrains Mono',monospace;color:#00e5a0;font-size:.85rem;">🔥 {cal_dia:.0f} kcal</span><span style="color:#6b7a99;font-size:.8rem;">P:{prot_dia:.0f}g · C:{nut_totals.get('carbohidratos',0):.0f}g · G:{nut_totals.get('grasas',0):.0f}g</span></div>""", unsafe_allow_html=True)
                                for food in alimentos:
                                    st.markdown(f"""<div class="db-ex-row"><span style="color:#6b7a99;min-width:70px;font-size:.72rem;">{food.get('comida','—')[:10]}</span><span class="db-nombre" style="font-size:.8rem;">{food.get('nombre','—')}</span><span class="db-detail">{food.get('calorias',0):.0f} kcal</span></div>""", unsafe_allow_html=True)
                            else:
                                st.markdown('<div style="color:#6b7a99;font-size:.8rem;padding:.5rem;">Sin alimentos</div>', unsafe_allow_html=True)

                    st.markdown(f"""<div style="text-align:right;font-size:.65rem;color:#6b7a99;margin-top:.5rem;padding-top:.5rem;border-top:1px solid #1e2d45;">💾 Guardado a las {hora_guardado}</div>""", unsafe_allow_html=True)

                    if st.button(f"🗑️ Eliminar {dia_key} de {sem_key}", key=f"del_db_{sem_key}_{dia_key}"):
                        del data["db_semanas"][sem_key]["dias"][dia_key]
                        if not data["db_semanas"][sem_key]["dias"]:
                            del data["db_semanas"][sem_key]
                        save_data(data, current_user)
                        st.session_state.data = data
                        st.rerun()

# ── EXPORTAR EXCEL ────────────────────────────────────────────────────
        st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
        st.markdown("""<div style="font-family:'Bebas Neue',sans-serif;font-size:.9rem;letter-spacing:2px;color:#a78bfa;margin-bottom:.8rem;">📤 EXPORTAR DATOS</div>""", unsafe_allow_html=True)

        # Filtros de exportación
        ex1, ex2, ex3 = st.columns(3)
        with ex1:
            exp_semana = st.selectbox("📅 Semana a exportar", ["Todas"] + sorted(weeks_data.keys(), key=lambda x: int(x.split()[-1]) if x.split()[-1].isdigit() else 0), key="exp_semana")
        with ex2:
            exp_dia = st.selectbox("📋 Día a exportar", ["Todos","DÍA 1","DÍA 2","DÍA 3","DÍA 4","DÍA 5","DÍA 6","DÍA 7"], key="exp_dia")
        with ex3:
            st.markdown("<br>", unsafe_allow_html=True)
            generar = st.button("⚙️ Generar Excel", use_container_width=True, key="generar_excel")

        if generar:
            filas_ej_exp = []
            filas_al_exp = []

            for sem_key, sem_obj in weeks_data.items():
                if exp_semana != "Todas" and sem_key != exp_semana:
                    continue
                for dia_key, dia_obj in sem_obj.get("dias", {}).items():
                    if exp_dia != "Todos" and dia_key.upper().replace(" ","") != exp_dia.upper().replace(" ",""):
                        continue
                    fecha = dia_obj.get("fecha", "")
                    for ex in dia_obj.get("ejercicios", []):
                        if ex.get("nombre") != "Descanso":
                            filas_ej_exp.append({
                                "Semana": sem_key, "Día": dia_key, "Fecha": fecha,
                                "Músculo":   get_musculo_from_exercise(ex),
                                "Ejercicio": ex.get("nombre", ""),
                                "Series":    ex.get("series", ""),
                                "Reps":      ex.get("reps", ""),
                                "Peso (kg)": ex.get("peso", ""),
                                "Descanso":  ex.get("descanso_txt", ""),
                                "Notas":     ex.get("notas", ""),
                            })
                    for food in dia_obj.get("alimentos", []):
                        filas_al_exp.append({
                            "Semana": sem_key, "Día": dia_key, "Fecha": fecha,
                            "Comida":          food.get("comida", ""),
                            "Alimento":        food.get("nombre", ""),
                            "Porción":         food.get("porcion", ""),
                            "Calorías (kcal)": food.get("calorias", 0),
                            "Proteínas (g)":   food.get("proteinas", 0),
                            "Carbos (g)":      food.get("carbohidratos", 0),
                            "Grasas (g)":      food.get("grasas", 0),
                            "Azúcar (g)":      food.get("azucar", 0),
                            "Fibra (g)":       food.get("fibra", 0),
                            "Sodio (mg)":      food.get("sodio", 0),
                            "Colesterol (mg)": food.get("colesterol", 0),
                        })

            if not filas_ej_exp and not filas_al_exp:
                st.markdown('<div class="alert-warn">⚠️ No hay datos para los filtros seleccionados.</div>', unsafe_allow_html=True)
            else:
                import io
                from openpyxl import Workbook
                from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
                from openpyxl.utils import get_column_letter
                from openpyxl.formatting.rule import ColorScaleRule
                from openpyxl.drawing.image import Image as XLImage

                wb = Workbook()

                # ── Paleta suave y profesional ──
                C_WHITE   = "FFFFFF"
                C_LIGHT   = "F8F9FC"
                C_LIGHT2  = "F0F2F8"
                C_BORDER  = "E2E6F0"
                C_DARK    = "2D3452"
                C_MUTED   = "8B93B0"

                # Colores suaves tipo pastel profesional
                C_ORANGE  = "E8805A"
                C_ORANGE2 = "FDF0EB"
                C_GREEN   = "4CAF8A"
                C_GREEN2  = "EDF7F3"
                C_BLUE    = "5B8DEF"
                C_BLUE2   = "EEF3FD"
                C_PURPLE  = "8B72BE"
                C_PURPLE2 = "F3EFF9"
                C_YELLOW  = "D4A843"
                C_YELLOW2 = "FBF6E9"
                C_PINK    = "D472A0"
                C_RED     = "D46B6B"

                # Headers de tabla (versión más apagada)
                C_H_PURPLE = "A08CC8"
                C_H_BLUE   = "7AAAE8"
                C_H_GREEN  = "6BBD9E"
                C_H_ORANGE = "E8956A"
                C_H_YELLOW = "D4A843"
                C_H_PINK   = "D472A0"
                C_H_MUTED  = "9AA3BE"
                C_H_TEAL   = "4DADA0"
                C_H_SKY    = "5BAFD4"
                C_H_RED    = "D46B6B"
                C_DARK_HDR = "3D4466"

                th_s = Side(style="thin",   color=C_BORDER)
                tk_s = Side(style="medium", color="C8CEDF")
                thin_b  = Border(left=th_s, right=th_s, top=th_s, bottom=th_s)
                thick_b = Border(left=tk_s, right=tk_s, top=tk_s, bottom=tk_s)

                def sh(cell, bg, txt="FFFFFF", bold=True, size=11, align="center"):
                    cell.fill      = PatternFill("solid", fgColor=bg)
                    cell.font      = Font(bold=bold, color=txt, size=size, name="Calibri")
                    cell.alignment = Alignment(horizontal=align, vertical="center", wrap_text=True)
                    cell.border    = thick_b

                def sc(cell, row_num, fg=None, bold=False, left=False, bg_override=None):
                    bg = bg_override or (C_LIGHT2 if row_num % 2 == 0 else C_WHITE)
                    cell.fill      = PatternFill("solid", fgColor=bg)
                    cell.font      = Font(color=fg or C_DARK, size=10, bold=bold, name="Calibri")
                    cell.alignment = Alignment(horizontal="left" if left else "center", vertical="center")
                    cell.border    = thin_b
                    
                def aw(ws, min_w=10):
                    for col in ws.columns:
                        mx = max((len(str(c.value or "")) for c in col), default=min_w)
                        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max(mx+3, min_w), 50)

                filtro_label = f"{exp_semana}" + (f" · {exp_dia}" if exp_dia != "Todos" else " · Todos los días")
                total_ex_exp = len(filas_ej_exp)
                total_al_exp = len(filas_al_exp)

                # ══════════════════════════════════════════
                # HOJA 1 — PORTADA
                # ══════════════════════════════════════════
                wc = wb.active
                wc.title = "Portada"
                wc.sheet_view.showGridLines = False
                wc.sheet_view.showRowColHeaders = False

                # Ancho de columnas fijo para portada
                for ci, w in enumerate([2,18,18,18,18,18,18,18,2], 1):
                    wc.column_dimensions[get_column_letter(ci)].width = w

                # Fondo blanco general
                for r in range(1, 50):
                    for c in range(1, 10):
                        cell = wc.cell(row=r, column=c)
                        cell.fill = PatternFill("solid", fgColor=C_WHITE)

                # Banner superior
                banner_color  = "E8805A"  # naranja suave
                banner_color2 = "EF9E7A"  # naranja más claro

                for r in range(1, 7):
                    for c in range(1, 10):
                        cell = wc.cell(row=r, column=c)
                        cell.fill = PatternFill("solid", fgColor=banner_color if r <= 4 else banner_color2)
                    wc.row_dimensions[r].height = 18

                # Título principal centrado en el banner
                wc.merge_cells("B2:H4")
                t = wc["B2"]
                t.value     = "🔥  FIREMUSCLE"
                t.font      = Font(bold=True, size=32, color=C_WHITE, name="Calibri")
                t.alignment = Alignment(horizontal="center", vertical="center")
                t.fill      = PatternFill("solid", fgColor=C_ORANGE)

                # Subtítulo en banner
                wc.merge_cells("B5:H6")
                st2 = wc["B5"]
                st2.value     = "REPORTE DE PROGRESO PERSONAL"
                st2.font      = Font(bold=False, size=13, color="FFE0D0", name="Calibri")
                st2.alignment = Alignment(horizontal="center", vertical="center")
                st2.fill      = PatternFill("solid", fgColor="FF8050")

                # Espacio
                wc.row_dimensions[7].height = 10

                # Info del reporte
                wc.merge_cells("B8:H8")
                inf = wc["B8"]
                inf.value     = f"Usuario: {current_user}   ·   Exportado el {date.today().strftime('%d de %B del %Y')}   ·   Filtro: {filtro_label}"
                inf.font      = Font(size=10, color=C_MUTED, name="Calibri")
                inf.alignment = Alignment(horizontal="center", vertical="center")
                inf.fill      = PatternFill("solid", fgColor=C_WHITE)
                wc.row_dimensions[8].height = 20

                # Línea separadora naranja
                for c in range(2, 9):
                    cell = wc.cell(row=9, column=c)
                    cell.fill = PatternFill("solid", fgColor="E8805A")
                wc.row_dimensions[9].height = 3

                # Tarjetas de métricas (fila 11-14)
                card_data = [
                    ("Semanas",     str(total_sem),    C_PURPLE,  C_PURPLE2),
                    ("Días",        str(total_dias),   C_BLUE,    C_BLUE2),
                    ("Ejercicios",  str(total_ex_exp), C_ORANGE,  C_YELLOW2),
                    ("Comidas",     str(total_al_exp), C_GREEN,   C_GREEN2),
                ]

                card_cols = ["B", "D", "F", "H"]
                card_ends  = ["C", "E", "G", "I"]

                for idx, ((lbl, val, clr, bg2), (col_s, col_e)) in enumerate(zip(card_data, zip(card_cols, card_ends))):
                    wc.merge_cells(f"{col_s}11:{col_e}13")
                    vc = wc[f"{col_s}11"]
                    vc.value     = val
                    vc.font      = Font(bold=True, size=30, color=clr, name="Calibri")
                    vc.alignment = Alignment(horizontal="center", vertical="center")
                    vc.fill      = PatternFill("solid", fgColor=bg2)
                    vc.border    = Border(
                        left=Side(style="medium",   color=clr),
                        right=Side(style="medium",  color=clr),
                        top=Side(style="medium",    color=clr),
                        bottom=Side(style="thin",   color=C_BORDER),
                    )
                    wc.row_dimensions[11].height = 36
                    wc.row_dimensions[12].height = 36
                    wc.row_dimensions[13].height = 36

                    wc.merge_cells(f"{col_s}14:{col_e}14")
                    lc = wc[f"{col_s}14"]
                    lc.value     = lbl
                    lc.font      = Font(bold=True, size=10, color=clr, name="Calibri")
                    lc.alignment = Alignment(horizontal="center", vertical="center")
                    lc.fill      = PatternFill("solid", fgColor=bg2)
                    lc.border    = Border(
                        left=Side(style="medium",   color=clr),
                        right=Side(style="medium",  color=clr),
                        bottom=Side(style="medium", color=clr),
                        top=Side(style="thin",      color=C_BORDER),
                    )
                    wc.row_dimensions[14].height = 18

                wc.row_dimensions[15].height = 16

                # Sección "Contenido del archivo"
                wc.merge_cells("B16:H16")
                ct = wc["B16"]
                ct.value     = "CONTENIDO DEL ARCHIVO"
                ct.font      = Font(bold=True, size=11, color=C_WHITE, name="Calibri")
                ct.alignment = Alignment(horizontal="center", vertical="center")
                ct.fill      = PatternFill("solid", fgColor=C_DARK)
                wc.row_dimensions[16].height = 22

                contenido = [
                    ("💪  Hoja «Ejercicios»",  f"{total_ex_exp} ejercicios registrados con músculo, series, reps, peso y notas", C_ORANGE, C_YELLOW2),
                    ("🥗  Hoja «Nutricion»",   f"{total_al_exp} alimentos con macros completos + fila de totales automática",    C_GREEN,  C_GREEN2),
                ]
                for ri, (titulo, desc, clr, bg2) in enumerate(contenido, 17):
                    wc.merge_cells(f"B{ri}:C{ri}")
                    tc = wc[f"B{ri}"]
                    tc.value     = titulo
                    tc.font      = Font(bold=True, size=10, color=clr, name="Calibri")
                    tc.alignment = Alignment(horizontal="left", vertical="center")
                    tc.fill      = PatternFill("solid", fgColor=bg2)
                    tc.border    = thin_b

                    wc.merge_cells(f"D{ri}:H{ri}")
                    dc = wc[f"D{ri}"]
                    dc.value     = desc
                    dc.font      = Font(size=10, color=C_DARK, name="Calibri")
                    dc.alignment = Alignment(horizontal="left", vertical="center")
                    dc.fill      = PatternFill("solid", fgColor=C_LIGHT)
                    dc.border    = thin_b
                    wc.row_dimensions[ri].height = 22

                # Footer
                wc.row_dimensions[45].height = 16
                wc.merge_cells("B46:H46")
                fn = wc["B46"]
                fn.value     = "FireMuscle v2.0  ·  Forja tu mejor version  ·  Generado automaticamente"
                fn.font      = Font(size=9, color=C_MUTED, italic=True, name="Calibri")
                fn.alignment = Alignment(horizontal="center", vertical="center")
                fn.fill      = PatternFill("solid", fgColor=C_WHITE)
                # Línea naranja arriba del footer
                for c in range(2, 9):
                    wc.cell(row=45, column=c).fill = PatternFill("solid", fgColor=C_ORANGE)
                wc.row_dimensions[45].height = 3

                # ══════════════════════════════════════════
                # HOJA 2 — EJERCICIOS
                # ══════════════════════════════════════════
                we = wb.create_sheet("Ejercicios")
                we.sheet_view.showGridLines = False
                if filas_ej_exp:
                    df_e = pd.DataFrame(filas_ej_exp)
                    ncols = len(df_e.columns)

                    we.merge_cells(f"A1:{get_column_letter(ncols)}1")
                    t1 = we["A1"]
                    t1.value     = "💪  REGISTRO DE EJERCICIOS"
                    t1.font      = Font(bold=True, size=14, color=C_WHITE, name="Calibri")
                    t1.alignment = Alignment(horizontal="center", vertical="center")
                    t1.fill      = PatternFill("solid", fgColor=C_ORANGE)
                    we.row_dimensions[1].height = 28

                    hc = {
                        "Semana":    C_H_PURPLE, "Día":      C_H_PURPLE, "Fecha":    C_H_PURPLE,
                        "Músculo":   C_H_ORANGE, "Ejercicio":C_H_ORANGE,
                        "Series":    C_H_BLUE,   "Reps":     C_H_BLUE,
                        "Peso (kg)": C_H_GREEN,  "Descanso": C_H_YELLOW, "Notas":    C_H_MUTED,
                    }
                    for ci, h in enumerate(df_e.columns, 1):
                        cell = we.cell(row=2, column=ci, value=h)
                        sh(cell, hc.get(h, C_DARK))
                    we.row_dimensions[2].height = 22

                    mc = {
                        "Abdomen":"C49A2A","Espalda":"3D9E7A","Pecho":"C86845",
                        "Pierna":"4A78D4","Bíceps":"7A5CAE","Triceps":"B85A8A",
                        "Cardio":"B85555","Core":"C49A2A",
                    }
                    pill_bg = {
                        "Abdomen":"FBF6E9","Espalda":"EDF7F3","Pecho":"FBF0EB",
                        "Pierna":"EEF3FD","Bíceps":"F3EFF9","Triceps":"FAF0F6",
                        "Cardio":"FAF0F0","Core":"FBF6E9",
                    }
                    for ri, row in enumerate(df_e.itertuples(index=False), 3):
                        musc = str(row[3]) if len(row) > 3 else ""
                        acc  = mc.get(musc, C_DARK)
                        pbg  = pill_bg.get(musc, C_LIGHT)
                        for ci, v in enumerate(row, 1):
                            cell = we.cell(row=ri, column=ci, value=v)
                            if ci in (4, 5):
                                sc(cell, ri-2, fg=acc, bold=(ci==5), left=(ci==5), bg_override=pbg)
                            else:
                                sc(cell, ri-2)
                        we.row_dimensions[ri].height = 18

                    aw(we)
                    we.conditional_formatting.add(
                        f"F3:F{len(df_e)+2}",
                        ColorScaleRule(start_type="min", start_color="EBF3FF",
                                       end_type="max",   end_color="3B82F6"))

                # ══════════════════════════════════════════
                # HOJA 3 — NUTRICIÓN
                # ══════════════════════════════════════════
                wn = wb.create_sheet("Nutricion")
                wn.sheet_view.showGridLines = False
                if filas_al_exp:
                    df_a = pd.DataFrame(filas_al_exp)
                    ncols_a = len(df_a.columns)

                    wn.merge_cells(f"A1:{get_column_letter(ncols_a)}1")
                    t2 = wn["A1"]
                    t2.value     = "🥗  REGISTRO NUTRICIONAL"
                    t2.font      = Font(bold=True, size=14, color=C_WHITE, name="Calibri")
                    t2.alignment = Alignment(horizontal="center", vertical="center")
                    t2.fill      = PatternFill("solid", fgColor=C_GREEN)
                    wn.row_dimensions[1].height = 28

                    ha = {
                        "Semana":"A08CC8",   "Día":"A08CC8",      "Fecha":"A08CC8",
                        "Comida":"7AAAE8",   "Alimento":"6BBD9E", "Porción":"9AA3BE",
                        "Calorías (kcal)":"E8956A",
                        "Proteínas (g)":"6BBD9E", "Carbos (g)":"7AAAE8",
                        "Grasas (g)":"D4A843",    "Azúcar (g)":"D472A0",
                        "Fibra (g)":"4DADA0",     "Sodio (mg)":"5BAFD4",
                        "Colesterol (mg)":"D46B6B",
                    }
                    for ci, h in enumerate(df_a.columns, 1):
                        cell = wn.cell(row=2, column=ci, value=h)
                        sh(cell, ha.get(h, C_DARK))
                    wn.row_dimensions[2].height = 22

                    cc = {"Desayuno":"C49A2A","Almuerzo":"C86845","Cena":"7A5CAE","Snack":"3D9E7A"}
                    cb = {"Desayuno":"FBF6E9","Almuerzo":"FBF0EB","Cena":"F3EFF9","Snack":"EDF7F3"}
                    for ri, row in enumerate(df_a.itertuples(index=False), 3):
                        cv  = str(row[3]) if len(row) > 3 else ""
                        acc = next((v for k,v in cc.items() if k in cv), C_DARK)
                        pbg = next((v for k,v in cb.items() if k in cv), C_LIGHT)
                        for ci, v in enumerate(row, 1):
                            cell = wn.cell(row=ri, column=ci, value=v)
                            if ci in (4, 5):
                                sc(cell, ri-2, fg=acc, bold=(ci==5), left=(ci==5), bg_override=pbg)
                            else:
                                sc(cell, ri-2)
                        wn.row_dimensions[ri].height = 18

                    # Fila TOTALES
                    tr = len(df_a) + 3
                    wn.row_dimensions[tr].height = 22
                    for ci in range(1, ncols_a+1):
                        cell = wn.cell(row=tr, column=ci)
                        if ci == 5:
                            cell.value     = "TOTALES"
                            cell.font      = Font(bold=True, size=11, color=C_WHITE, name="Calibri")
                            cell.fill      = PatternFill("solid", fgColor=C_GREEN)
                            cell.alignment = Alignment(horizontal="center", vertical="center")
                            cell.border    = thick_b
                        elif ci >= 7:
                            cl = get_column_letter(ci)
                            cell.value         = f"=SUM({cl}3:{cl}{tr-1})"
                            cell.number_format = "0.0"
                            cell.font          = Font(bold=True, color=C_GREEN, size=11, name="Calibri")
                            cell.fill          = PatternFill("solid", fgColor="E6FAF4")
                            cell.alignment     = Alignment(horizontal="center", vertical="center")
                            cell.border        = thick_b
                        else:
                            cell.fill   = PatternFill("solid", fgColor=C_LIGHT2)
                            cell.border = thick_b

                    wn.conditional_formatting.add(
                        f"G3:G{tr-1}",
                        ColorScaleRule(
                            start_type="min",      start_color="EDF7F3",
                            mid_type="percentile", mid_value=50, mid_color="FBF6E9",
                            end_type="max",        end_color="E8956A"))

                # DESCARGAR
                buf = io.BytesIO()
                wb.save(buf)
                buf.seek(0)
                fname = f"firemuscle_{current_user}_{exp_semana.replace(' ','_')}_{exp_dia.replace(' ','_')}_{date.today().isoformat()}.xlsx"
                st.session_state["excel_buf"]   = buf
                st.session_state["excel_fname"] = fname
                st.success(f"✅ Excel listo — {total_ex_exp} ejercicios · {total_al_exp} alimentos")

        if "excel_buf" in st.session_state:
            st.download_button(
                label="📥 Descargar Excel",
                data=st.session_state["excel_buf"],
                file_name=st.session_state["excel_fname"],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
            
# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 · AI COACH
# ═══════════════════════════════════════════════════════════════════════════════
with tab_chat:

    st.markdown("""<div class="card card-purple"><div class="card-title">🤖 AI COACH · FIREMUSCLE</div>
    <div style="font-size:.8rem;color:#6b7a99;">Asistente personal con acceso a tu perfil, rutina y nutrición</div>
    </div>""", unsafe_allow_html=True)

    gp = data.get("global_profile", {})
    today_foods = data.get(get_today_key(), {}).get("foods", [])
    dow = date.today().weekday()
    today_dia_key = DIA_SEMANA_MAP.get(dow)
    exercises_today = data.get(f"exercises_{today_dia_key}", {}).get("exercises", []) if today_dia_key else []

    user_context = f"""
Eres el AI Coach personal de FireMuscle, un asistente experto en fitness y nutrición.
Tienes acceso al perfil completo del usuario y debes personalizar cada respuesta con sus datos.

PERFIL DEL USUARIO:
- Nombre: {current_user}
- Edad: {gp.get('age', '?')} años
- Peso: {gp.get('weight', '?')} kg
- Altura: {gp.get('height', '?')} cm
- Sexo: {gp.get('sex', '?')}
- Nivel de actividad: {gp.get('activity', '?')}
- Objetivos calóricos: {limits.get('calorias', '?')} kcal/día
- Proteínas meta: {limits.get('proteinas', '?')}g/día

RUTINA SEMANAL (6 días):
{chr(10).join([f"- {k}: {v['titulo']} ({len(v['ejercicios'])} ejercicios)" for k, v in RUTINA_BASE.items()])}

REGISTRO DE HOY:
- Día de entrenamiento: {RUTINA_BASE.get(today_dia_key, {}).get('titulo', 'Domingo/Descanso')}
- Ejercicios registrados: {len(exercises_today)}
- Alimentos registrados: {len(today_foods)}
- Calorías consumidas: {sum_nutrients(today_foods).get('calorias', 0):.0f} kcal de {limits.get('calorias', '?')} meta

Responde siempre en español. Sé directo, motivador y usa los datos del usuario para personalizar cada respuesta.
Usa emojis con moderación. Cuando sugieras rutinas, da series y reps concretas.
"""

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    st.markdown("""<div style="font-size:.75rem;color:#6b7a99;margin-bottom:.5rem;letter-spacing:1px;">💡 PREGUNTAS RÁPIDAS</div>""", unsafe_allow_html=True)
    quick_cols = st.columns(4)
    quick_prompts = [
        ("💪 ¿Cómo mejorar mi rutina?", "Analiza mi rutina actual y dime qué ejercicios podría mejorar o agregar para mejores resultados"),
        ("🥗 ¿Cómo está mi nutrición?", "Revisa mi alimentación de hoy y dime si estoy cumpliendo mis metas nutricionales"),
        ("🔥 Rutina de emergencia",      "Necesito una rutina rápida de 20 minutos para hacer en casa hoy"),
        ("📈 ¿Cómo progresar?",          "Dame consejos específicos para seguir progresando según mi nivel actual"),
    ]
    for i, (label, prompt) in enumerate(quick_prompts):
        with quick_cols[i]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": prompt})

    st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)

    for msg in st.session_state.chat_messages:
        role_label   = f"👤 {current_user}" if msg["role"] == "user" else "🔥 AI Coach"
        bubble_style = "background:#ff6b35;color:#fff;" if msg["role"] == "user" else "background:#1a2332;border:1px solid #1e2d45;color:#e8f0fe;"
        align        = "flex-end" if msg["role"] == "user" else "flex-start"
        st.markdown(f"""
        <div style="display:flex;justify-content:{align};margin:.4rem 0;">
            <div style="{bubble_style}border-radius:14px;padding:.7rem 1rem;max-width:80%;font-size:.88rem;line-height:1.5;">
                <div style="font-size:.65rem;opacity:.7;margin-bottom:.3rem;">{role_label}</div>
                {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.chat_messages and st.session_state.chat_messages[-1]["role"] == "user":
        with st.spinner("🔥 AI Coach pensando..."):
            try:
                from groq import Groq
                client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": user_context}] + st.session_state.chat_messages,
                    max_tokens=1024,
                )
                assistant_reply = response.choices[0].message.content
                st.session_state.chat_messages.append({"role": "assistant", "content": assistant_reply})
                st.rerun()
            except Exception as e:
                st.error(f"Error al conectar con AI Coach: {e}")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_btn, col_clear = st.columns([7, 1, 1])
        with col_input:
            user_input = st.text_input("", placeholder="Pregunta sobre tu entrenamiento, nutrición, rutinas...",
                                       label_visibility="collapsed")
        with col_btn:
            submitted = st.form_submit_button("Enviar", use_container_width=True)
        with col_clear:
            cleared = st.form_submit_button("🗑️ Limpiar", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        st.rerun()
    if cleared:
        st.session_state.chat_messages = []
        st.rerun()

# Footer
st.markdown(f"""<div style="text-align:center;font-size:.72rem;color:#6b7a99;letter-spacing:1px;padding:1.5rem;">🔥 FireMuscle · Auto-guardado {datetime.now().strftime("%H:%M:%S")} · {current_user}</div>""", unsafe_allow_html=True)