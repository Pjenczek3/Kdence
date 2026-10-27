import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Kdence", page_icon="🏃‍♂️", layout="wide")

# =====================================================================
# DESIGN
# =====================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }

    /* --- Suppression de la bande blanche / éléments Streamlit --- */
    header[data-testid="stHeader"], [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"],
    #MainMenu, footer { display: none !important; visibility: hidden !important; height: 0 !important; }

    .stApp {
        background:
            radial-gradient(circle at 15% 0%, rgba(56,189,248,0.14) 0%, transparent 40%),
            radial-gradient(circle at 90% 15%, rgba(59,130,246,0.14) 0%, transparent 45%),
            linear-gradient(135deg, #0b132b 0%, #1c2541 50%, #28385e 100%);
        background-attachment: fixed;
        color: #F8FAFC;
    }
    .block-container { padding-top: 1.2rem !important; padding-bottom: 3rem; max-width: 1280px; }

    /* --- Cartes (containers avec bordure) --- */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(17, 30, 56, 0.72);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(56,189,248,0.18) !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 28px rgba(0,0,0,0.30);
    }
    [class*="st-key-card_s_"] {
        border-left: 4px solid #334155 !important;
        transition: transform .15s ease, border-color .2s ease;
    }
    [class*="st-key-card_s_"]:hover { transform: translateX(3px); }

    /* --- Navigation (radio transformé en onglets) --- */
    [data-testid="stRadio"] > label { display: none; }
    [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 6px; background: rgba(17,30,56,0.75); padding: 6px;
        border-radius: 16px; border: 1px solid rgba(56,189,248,0.2);
        justify-content: center; flex-wrap: wrap;
    }
    [data-testid="stRadio"] label[data-baseweb="radio"] {
        padding: 9px 18px; border-radius: 12px; cursor: pointer;
        transition: all .2s ease; margin: 0;
    }
    [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child { display: none; }
    [data-testid="stRadio"] label[data-baseweb="radio"] p {
        font-size: .82rem; font-weight: 700; letter-spacing: .8px; color: #94A3B8;
    }
    [data-testid="stRadio"] label[data-baseweb="radio"]:hover { background: rgba(56,189,248,0.12); }
    [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(135deg, #0EA5E9, #3B82F6);
        box-shadow: 0 4px 16px rgba(14,165,233,0.45);
    }
    [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p { color: #fff; }

    /* --- KPI --- */
    .kpi-card {
        background: linear-gradient(160deg, rgba(17,30,56,0.92), rgba(28,37,65,0.85));
        border: 1.5px solid #1E3A8A; padding: 20px 22px; border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35); transition: transform .2s ease, box-shadow .2s ease;
        height: 128px; position: relative; overflow: hidden;
    }
    .kpi-card:hover { transform: translateY(-4px); box-shadow: 0 14px 32px rgba(0,0,0,0.45); }
    .kpi-card::after {
        content: ""; position: absolute; right: -30px; top: -30px; width: 100px; height: 100px;
        border-radius: 50%; background: var(--glow, #38BDF8); opacity: .12; filter: blur(8px);
    }
    .kpi-title { font-size: .7rem; color: #94A3B8; text-transform: uppercase;
        letter-spacing: 1.3px; margin-bottom: 10px; font-weight: 700; }
    .kpi-value { font-size: 2rem; font-weight: 800; color: #38BDF8; line-height: 1.1; }
    .kpi-sub { font-size: .75rem; color: #94A3B8; margin-top: 6px; }

    /* --- Hero --- */
    .hero {
        display: flex; align-items: center; gap: 28px; padding: 6px 4px;
    }
    .ring {
        --p: 0; width: 112px; height: 112px; border-radius: 50%; flex-shrink: 0;
        background: conic-gradient(#38BDF8 calc(var(--p) * 1%), rgba(51,65,85,0.6) 0);
        display: grid; place-items: center; box-shadow: 0 0 30px rgba(56,189,248,0.35);
    }
    .ring::before { content: ""; position: absolute; width: 88px; height: 88px; border-radius: 50%; background: #111e38; }
    .ring span { position: relative; font-size: 1.35rem; font-weight: 800; color: #F8FAFC; }
    .hero h2 { margin: 0; font-size: 1.5rem; font-weight: 800; color: #F8FAFC; }
    .hero p { margin: 4px 0 0; color: #94A3B8; font-size: .9rem; }

    .bar-bg { background: rgba(51,65,85,.6); border-radius: 99px; height: 10px; overflow: hidden; margin-top: 12px; }
    .bar-fg { height: 100%; border-radius: 99px; background: linear-gradient(90deg,#38BDF8,#4ADE80,#FACC15); }

    .logo { font-size: 1.9rem; font-weight: 900; letter-spacing: -.5px;
        background: linear-gradient(90deg,#FFFFFF,#38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .profile { color:#F8FAFC; font-size:.85rem; background: rgba(30,41,59,.8); padding: 9px 14px;
        border-radius: 12px; border: 1px solid #334155; text-align:center; }
    .section-title { font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin: 0 0 4px; }
    .muted { color: #94A3B8; font-size: .8rem; }
    .pill { display:inline-block; padding: 2px 10px; border-radius: 99px; font-size: .72rem; font-weight: 700;
        background: rgba(56,189,248,.15); color: #38BDF8; margin-left: 6px; }
    .pill.ok { background: rgba(74,222,128,.15); color: #4ADE80; }
    .seance-name { font-size: .95rem; font-weight: 700; color: #F8FAFC; }
    .seance-desc { font-size: .78rem; color: #94A3B8; margin-top: 2px; }

    /* --- Widgets --- */
    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        border-radius: 12px; font-weight: 700; border: 1px solid rgba(56,189,248,.35);
        background: rgba(30,41,59,.8); color: #F8FAFC; transition: all .2s ease;
    }
    .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        border-color: #38BDF8; background: linear-gradient(135deg,#0EA5E9,#3B82F6); color:#fff;
        transform: translateY(-1px); box-shadow: 0 6px 18px rgba(14,165,233,.4);
    }
    [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"],
    .stButton > button[kind="primary"] { background: linear-gradient(135deg,#0EA5E9,#3B82F6); border: none; }
    [data-testid="stNumberInput"] input, [data-testid="stTextInput"] input,
    [data-baseweb="select"] > div { border-radius: 10px !important; }
    [data-testid="stForm"] { border: 1px solid rgba(56,189,248,.18); border-radius: 16px; background: rgba(11,19,43,.4); }
    [data-testid="stExpander"] { border: 1px solid rgba(56,189,248,.2) !important; border-radius: 14px !important; background: rgba(17,30,56,.5); }
    h1,h2,h3,h4 { color: #F8FAFC !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# DONNÉES (une seule source de vérité : la liste de séances)
# =====================================================================
if "seances" not in st.session_state:
    st.session_state.seances = [
        dict(id=1, semaine=9, nom="S1 (VMA)", desc="15' EF + 10x400m@3'07 (R:1') + 10' EF", prevus=10.0, realises=10.2, validee=True),
        dict(id=2, semaine=9, nom="S2 (Seuil)", desc="15' EF + 3x2000m@3'45 + 10' EF", prevus=12.0, realises=0.0, validee=False),
        dict(id=3, semaine=9, nom="S3 (Endurance)", desc="50' EF", prevus=8.0, realises=0.0, validee=False),
        dict(id=4, semaine=9, nom="S4 (Sortie longue)", desc="1h30 EF allure marathon", prevus=18.0, realises=0.0, validee=False),
        dict(id=5, semaine=10, nom="S1 (VMA)", desc="15' EF + 12x400m@3'07 + 10' EF", prevus=11.0, realises=0.0, validee=False),
        dict(id=6, semaine=10, nom="S2 (Sortie longue)", desc="1h40 EF", prevus=20.0, realises=0.0, validee=False),
    ]
    st.session_state.next_id = 7

st.session_state.setdefault("duree_plan", 12)
st.session_state.setdefault("semaine_active", 9)
st.session_state.setdefault("page", "📊 TABLEAU DE BORD")

CHAUSSURES = {"nom": "Hoka Mach X3", "km": 70.6, "km_max": 800}
PAGES = ["📊 TABLEAU DE BORD", "📅 MES PLANS", "📈 MES STATISTIQUES", "👟 MES ÉQUIPEMENTS"]


def df_seances() -> pd.DataFrame:
    cols = ["id", "semaine", "nom", "desc", "prevus", "realises", "validee"]
    return pd.DataFrame(st.session_state.seances, columns=cols)


def get(sid):
    return next(s for s in st.session_state.seances if s["id"] == sid)


def add_seance(semaine, nom, desc, prevus, realises=0.0, validee=False):
    st.session_state.seances.append(
        dict(id=st.session_state.next_id, semaine=semaine, nom=nom, desc=desc,
             prevus=prevus, realises=realises, validee=validee)
    )
    st.session_state.next_id += 1


# --- callbacks : mises à jour instantanées, sans st.rerun() ---
def cb_check(sid):
    get(sid)["validee"] = st.session_state[f"chk_{sid}"]


def cb_km(sid):
    s = get(sid)
    s["realises"] = float(st.session_state[f"km_{sid}"])
    if s["realises"] > 0 and not s["validee"]:  # des km saisis = séance faite
        s["validee"] = True
        st.session_state[f"chk_{sid}"] = True


def cb_delete(sid):
    st.session_state.seances = [s for s in st.session_state.seances if s["id"] != sid]


def cb_copy_week(src, dst):
    for s in [x for x in st.session_state.seances if x["semaine"] == src]:
        add_seance(dst, s["nom"], s["desc"], s["prevus"])


# =====================================================================
# EN-TÊTE + NAVIGATION
# =====================================================================
c_logo, c_nav, c_prof = st.columns([1.1, 3.6, 1.2], vertical_alignment="center")
with c_logo:
    st.markdown("<div class='logo'>🥇 Kdence</div>", unsafe_allow_html=True)
with c_nav:
    st.radio("Navigation", PAGES, key="page", horizontal=True, label_visibility="collapsed")
with c_prof:
    st.markdown(
        "<div class='profile'>👤 Profil du coureur<br><span class='muted'>Cooper 1920 m</span></div>",
        unsafe_allow_html=True,
    )
st.write("")

page = st.session_state.page
df = df_seances()
semaines_dispo = list(range(1, st.session_state.duree_plan + 1))
if st.session_state.semaine_active not in semaines_dispo:
    st.session_state.semaine_active = semaines_dispo[-1]


def seance_card(s):
    """Une ligne de séance : case, infos, saisie des km, suppression."""
    sid = s["id"]
    with st.container(border=True, key=f"card_s_{sid}"):
        if s["validee"]:
            st.markdown(f"<style>.st-key-card_s_{sid}{{border-left-color:#10B981 !important;}}</style>", unsafe_allow_html=True)
        c_chk, c_info, c_km, c_del = st.columns([0.07, 0.55, 0.28, 0.10], vertical_alignment="center")
        with c_chk:
            st.checkbox("ok", value=s["validee"], key=f"chk_{sid}", on_change=cb_check, args=(sid,), label_visibility="collapsed")
        with c_info:
            icon = "🟢" if s["validee"] else "⚪"
            pill = "<span class='pill ok'>Faite</span>" if s["validee"] else "<span class='pill'>À faire</span>"
            st.markdown(
                f"<div class='seance-name'>{icon} {s['nom']} <span class='pill'>{s['prevus']:.1f} km</span>{pill}</div>"
                f"<div class='seance-desc'>{s['desc']}</div>",
                unsafe_allow_html=True,
            )
        with c_km:
            st.number_input("Km réalisés", min_value=0.0, step=0.5, value=float(s["realises"]),
                            key=f"km_{sid}", on_change=cb_km, args=(sid,), format="%.1f",
                            help="Saisis les km réellement courus")
        with c_del:
            st.button("🗑️", key=f"del_{sid}", on_click=cb_delete, args=(sid,), help="Supprimer cette séance")


# =====================================================================
# PAGE 1 : TABLEAU DE BORD
# =====================================================================
if page == PAGES[0]:
    sem = st.session_state.semaine_active
    d_sem = df[df.semaine == sem]
    prevus_sem = d_sem.prevus.sum()
    reels_sem = d_sem[d_sem.validee].realises.sum()
    nb_faites = int(d_sem.validee.sum())
    nb_total = len(d_sem)
    pct_km = min(reels_sem / prevus_sem * 100, 100) if prevus_sem else 0
    taux = nb_faites / nb_total * 100 if nb_total else 0
    restants = max(df.prevus.sum() - df[df.validee].realises.sum(), 0)

    # --- Hero ---
    with st.container(border=True):
        c_h, c_sel = st.columns([3, 1], vertical_alignment="center")
        with c_h:
            msg = "Semaine terminée, bravo 🔥" if nb_total and nb_faites == nb_total else "Continue, chaque km compte 💪"
            st.markdown(
                f"""<div class="hero">
                    <div class="ring" style="--p:{pct_km:.0f}; position:relative;"><span>{pct_km:.0f}%</span></div>
                    <div><h2>Préparation Marathon · Semaine {sem}</h2>
                    <p>{reels_sem:.1f} km courus sur {prevus_sem:.1f} km prévus · {nb_faites}/{nb_total} séances validées</p>
                    <p style="color:#38BDF8;font-weight:600;">{msg}</p></div></div>""",
                unsafe_allow_html=True,
            )
        with c_sel:
            st.selectbox("Semaine affichée", semaines_dispo, key="semaine_active")

    st.write("")

    # --- KPI ---
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"<div class='kpi-card' style='border-color:#0EA5E9;--glow:#0EA5E9'><div class='kpi-title'>Km réalisés · sem. {sem}</div>"
                    f"<div class='kpi-value'>{reels_sem:.1f} km</div><div class='kpi-sub'>sur {prevus_sem:.1f} km prévus</div></div>", unsafe_allow_html=True)
    with k2:
        st.markdown(f"<div class='kpi-card' style='border-color:#3B82F6;--glow:#3B82F6'><div class='kpi-title'>Kms restants (plan)</div>"
                    f"<div class='kpi-value' style='color:#F8FAFC'>{restants:.1f} km</div><div class='kpi-sub'>plan total : {df.prevus.sum():.0f} km</div></div>", unsafe_allow_html=True)
    with k3:
        st.markdown(f"<div class='kpi-card' style='border-color:#10B981;--glow:#10B981'><div class='kpi-title'>Respect du plan</div>"
                    f"<div class='kpi-value' style='color:#4ADE80'>{taux:.0f}%</div><div class='kpi-sub'>{nb_faites} séance(s) sur {nb_total}</div></div>", unsafe_allow_html=True)
    with k4:
        use = CHAUSSURES["km"] / CHAUSSURES["km_max"] * 100
        st.markdown(f"<div class='kpi-card' style='border-color:#F59E0B;--glow:#F59E0B'><div class='kpi-title'>Chaussures · {CHAUSSURES['km']} km</div>"
                    f"<div style='font-size:.9rem;color:#4ADE80;font-weight:600;'>🟢 Bon état <span style='color:#F8FAFC'>&nbsp;{CHAUSSURES['nom']}</span></div>"
                    f"<div class='bar-bg'><div class='bar-fg' style='width:{use:.0f}%'></div></div></div>", unsafe_allow_html=True)

    st.write("")
    col_graph, col_seances = st.columns([1.15, 1], gap="large")

    # --- Graphique ---
    with col_graph:
        with st.container(border=True):
            st.markdown("<div class='section-title'>Kilométrage hebdomadaire · Prévu vs Réel</div>"
                        "<div class='muted'>Mis à jour en direct à chaque séance validée</div>", unsafe_allow_html=True)
            agg = pd.DataFrame({"semaine": semaines_dispo})
            prev = df.groupby("semaine").prevus.sum()
            reel = df[df.validee].groupby("semaine").realises.sum()
            agg["prevu"] = agg.semaine.map(prev).fillna(0)
            agg["reel"] = agg.semaine.map(reel).fillna(0)
            agg = agg[(agg.prevu > 0) | (agg.reel > 0) | (agg.semaine == sem)]
            labels = [f"S{w}" for w in agg.semaine]
            fig = go.Figure([
                go.Bar(name="Réel", x=labels, y=agg.reel, marker_color="#0EA5E9", marker_cornerradius=6),
                go.Bar(name="Prévu", x=labels, y=agg.prevu, marker_color="#38BDF8", opacity=0.45, marker_cornerradius=6),
            ])
            fig.update_layout(
                barmode="group", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94A3B8", size=11), margin=dict(l=0, r=0, t=30, b=0), height=330,
                legend=dict(orientation="h", y=1.12, x=0),
                xaxis=dict(showgrid=False, linecolor="#334155"),
                yaxis=dict(gridcolor="rgba(148,163,184,0.12)", ticksuffix=" km"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # --- Séances ---
    with col_seances:
        st.markdown(f"<div class='section-title'>🏃 Séances · Semaine {sem}</div>"
                    "<div class='muted'>Coche la séance et/ou saisis tes km à droite</div>", unsafe_allow_html=True)
        st.write("")
        if d_sem.empty:
            st.info("Aucune séance cette semaine. Crée-en une ci-dessous ou dans « Mes plans ».")
        for s in [x for x in st.session_state.seances if x["semaine"] == sem]:
            seance_card(s)

        with st.expander("➕ Ajouter une séance"):
            with st.form("form_dash_add", clear_on_submit=True):
                n_nom = st.text_input("Nom", placeholder="S5 (Footing)")
                n_desc = st.text_input("Description", placeholder="45' footing facile")
                n_prev = st.number_input("Km prévus", min_value=0.0, value=8.0, step=0.5)
                if st.form_submit_button("Ajouter à la semaine " + str(sem), use_container_width=True):
                    add_seance(sem, n_nom or "Séance", n_desc, n_prev)
                    st.rerun()

# =====================================================================
# PAGE 2 : MES PLANS
# =====================================================================
elif page == PAGES[1]:
    st.markdown("<h3>📅 Construis ton plan d'entraînement</h3>", unsafe_allow_html=True)
    st.caption("Tout ce que tu crées ici apparaît automatiquement dans ton tableau de bord.")

    with st.container(border=True):
        st.markdown("<div class='section-title'>⏱️ Durée du plan</div>", unsafe_allow_html=True)
        st.slider("Nombre de semaines", 4, 24, key="duree_plan")

    c_left, c_right = st.columns([1, 1.3], gap="large")

    with c_left:
        with st.container(border=True):
            st.markdown("<div class='section-title'>➕ Créer une séance</div>", unsafe_allow_html=True)
            with st.form("form_plan_add"):
                sc = st.selectbox("Semaine", semaines_dispo, index=min(8, len(semaines_dispo) - 1))
                p_nom = st.text_input("Nom de la séance", value="S1 (VMA)")
                p_desc = st.text_input("Description", value="15' EF + 10x400m + 10' EF")
                p_km = st.number_input("Distance prévue (km)", min_value=0.0, value=10.0, step=0.5)
                if st.form_submit_button("Enregistrer dans le plan", use_container_width=True):
                    add_seance(sc, p_nom, p_desc, p_km)
                    st.success(f"Séance ajoutée à la semaine {sc} ✅")
                    st.rerun()

        with st.container(border=True):
            st.markdown("<div class='section-title'>📋 Dupliquer une semaine</div>"
                        "<div class='muted'>Copie toutes les séances d'une semaine vers une autre</div>", unsafe_allow_html=True)
            d1, d2 = st.columns(2)
            src = d1.selectbox("Depuis", semaines_dispo, key="copy_src", index=min(8, len(semaines_dispo) - 1))
            dst = d2.selectbox("Vers", semaines_dispo, key="copy_dst", index=min(9, len(semaines_dispo) - 1))
            st.button("Dupliquer", on_click=cb_copy_week, args=(src, dst), disabled=(src == dst), use_container_width=True)

    with c_right:
        with st.container(border=True):
            st.markdown("<div class='section-title'>🗓️ Vue d'ensemble</div>", unsafe_allow_html=True)
            tot = df.groupby("semaine").prevus.sum()
            mx = max(tot.max(), 1) if len(tot) else 1
            chips = ""
            for w in semaines_dispo:
                v = tot.get(w, 0)
                h = int(v / mx * 100)
                chips += (f"<div style='flex:1;min-width:28px;text-align:center'>"
                          f"<div style='height:60px;display:flex;align-items:flex-end'><div style='width:100%;height:{max(h,4)}%;"
                          f"background:{'linear-gradient(180deg,#38BDF8,#0EA5E9)' if v else 'rgba(51,65,85,.6)'};border-radius:5px'></div></div>"
                          f"<div class='muted' style='font-size:.65rem'>S{w}</div></div>")
            st.markdown(f"<div style='display:flex;gap:4px;align-items:flex-end'>{chips}</div>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("<div class='section-title'>📋 Détail d'une semaine</div>", unsafe_allow_html=True)
            sw = st.selectbox("Semaine", semaines_dispo, key="plan_week_view", index=min(8, len(semaines_dispo) - 1))
            liste = [s for s in st.session_state.seances if s["semaine"] == sw]
            st.markdown(f"<p style='color:#38BDF8;font-weight:700'>Objectif semaine {sw} : {sum(s['prevus'] for s in liste):.1f} km · {len(liste)} séance(s)</p>", unsafe_allow_html=True)
            if not liste:
                st.info("Aucune séance : utilise le formulaire pour en ajouter.")
            for s in liste:
                a, b = st.columns([0.88, 0.12], vertical_alignment="center")
                a.markdown(
                    f"<div style='background:rgba(30,41,59,.55);border-left:3px solid #38BDF8;padding:10px 14px;border-radius:10px;'>"
                    f"<div class='seance-name'>{s['nom']} <span class='pill'>{s['prevus']:.1f} km</span></div>"
                    f"<div class='seance-desc'>{s['desc']}</div></div>", unsafe_allow_html=True)
                b.button("🗑️", key=f"pdel_{s['id']}", on_click=cb_delete, args=(s["id"],))
            if st.button("🎯 Voir cette semaine dans le tableau de bord", use_container_width=True):
                st.session_state.semaine_active = sw
                st.session_state.page = PAGES[0]
                st.rerun()

# =====================================================================
# PAGE 3 : STATISTIQUES
# =====================================================================
elif page == PAGES[2]:
    st.markdown("<h3>📈 Mes statistiques</h3>", unsafe_allow_html=True)
    faites = df[df.validee]
    total = faites.realises.sum()
    nb = len(faites)
    moy = total / nb if nb else 0
    best = faites.realises.max() if nb else 0

    s1, s2, s3, s4 = st.columns(4)
    for col, titre, val, color in [
        (s1, "Km totaux courus", f"{total:.1f} km", "#38BDF8"),
        (s2, "Séances validées", f"{nb}", "#4ADE80"),
        (s3, "Km moyens / séance", f"{moy:.1f} km", "#FACC15"),
        (s4, "Plus longue séance", f"{best:.1f} km", "#F472B6"),
    ]:
        col.markdown(f"<div class='kpi-card' style='--glow:{color}'><div class='kpi-title'>{titre}</div>"
                     f"<div class='kpi-value' style='color:{color}'>{val}</div></div>", unsafe_allow_html=True)
    st.write("")
    with st.container(border=True):
        st.markdown("<div class='section-title'>Progression cumulée des km</div>", unsafe_allow_html=True)
        if nb:
            cum = faites.sort_values(["semaine", "id"]).reset_index(drop=True)
            cum["cumul"] = cum.realises.cumsum()
            fig = go.Figure(go.Scatter(x=list(range(1, nb + 1)), y=cum.cumul, mode="lines+markers", fill="tozeroy",
                                       line=dict(color="#38BDF8", width=3), fillcolor="rgba(56,189,248,0.15)"))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=320,
                              font=dict(color="#94A3B8"), margin=dict(l=0, r=0, t=10, b=0),
                              xaxis=dict(title="Séance n°", showgrid=False), yaxis=dict(gridcolor="rgba(148,163,184,.12)", ticksuffix=" km"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Valide une séance pour voir ta progression.")

# =====================================================================
# PAGE 4 : ÉQUIPEMENTS
# =====================================================================
else:
    st.markdown("<h3>👟 Mes équipements</h3>", unsafe_allow_html=True)
    use = CHAUSSURES["km"] / CHAUSSURES["km_max"] * 100
    with st.container(border=True):
        st.markdown(
            f"<div class='hero'><div style='font-size:3rem'>👟</div><div style='flex:1'>"
            f"<h2>{CHAUSSURES['nom']}</h2><p>{CHAUSSURES['km']} km parcourus sur ~{CHAUSSURES['km_max']} km de durée de vie</p>"
            f"<div class='bar-bg'><div class='bar-fg' style='width:{use:.0f}%'></div></div>"
            f"<p style='color:#4ADE80;font-weight:600'>🟢 Bon état · encore {CHAUSSURES['km_max'] - CHAUSSURES['km']:.0f} km avant remplacement</p>"
            f"</div></div>", unsafe_allow_html=True)