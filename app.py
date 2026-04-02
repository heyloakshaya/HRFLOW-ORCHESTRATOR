import json
from typing import Any, Dict, Optional

import requests
import streamlit as st

st.set_page_config(
    page_title="HRFlow | Enterprise Portal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=DM+Mono:wght@400;500&display=swap');

    :root {
        --bg-0:       #070c18;
        --bg-1:       #0d1425;
        --bg-2:       #111d35;
        --bg-3:       #172240;
        --bg-glass:   rgba(17, 29, 53, 0.72);
        --line:       rgba(255,255,255,0.07);
        --line-mid:   rgba(255,255,255,0.12);
        --text:       #edf2ff;
        --muted:      #8a9dc4;
        --hint:       #4d5f84;
        --blue:       #3d7fff;
        --blue-light: #6fa0ff;
        --blue-dim:   rgba(61,127,255,0.14);
        --purple:     #8b5cf6;
        --teal:       #14b8a6;
        --green:      #22c55e;
        --amber:      #f59e0b;
        --red:        #ef4444;
        --radius-sm:  8px;
        --radius-md:  14px;
        --radius-lg:  20px;
        --radius-xl:  28px;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text);
    }

    .stApp {
        background: var(--bg-0);
        background-image:
            radial-gradient(ellipse 80% 50% at 110% -10%, rgba(61,127,255,0.18), transparent),
            radial-gradient(ellipse 60% 40% at -10% 110%, rgba(139,92,246,0.12), transparent);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--bg-1) !important;
        border-right: 1px solid var(--line) !important;
    }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

    /* ── Main container ── */
    .block-container {
        padding: 2rem 2.5rem 3rem !important;
        max-width: 1280px;
    }

    /* ── Hide streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Typography ── */
    h1,h2,h3,h4 { font-family: 'DM Sans', sans-serif; font-weight: 600; letter-spacing: -0.02em; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-2);
        border: 1px solid var(--line);
        border-radius: var(--radius-md);
        padding: 5px 6px;
        gap: 3px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--muted);
        transition: all 0.18s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { color: var(--text); background: rgba(255,255,255,0.05); }
    .stTabs [aria-selected="true"] {
        background: var(--blue-dim) !important;
        color: var(--blue-light) !important;
        border: 1px solid rgba(61,127,255,0.3) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"]    { display: none; }

    /* ── Inputs ── */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div {
        background: var(--bg-2) !important;
        border: 1px solid var(--line-mid) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        transition: border-color 0.2s;
    }
    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within {
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(61,127,255,0.15) !important;
    }
    input, textarea { color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; }
    label { color: var(--muted) !important; font-size: 0.84rem !important; font-weight: 500 !important; }

    /* ── Buttons ── */
    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #3d7fff 0%, #6040e8 100%);
        color: #fff;
        border: none;
        border-radius: var(--radius-sm);
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0.55rem 1.3rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 20px rgba(61,127,255,0.25);
        letter-spacing: 0.01em;
    }
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 28px rgba(61,127,255,0.38);
        filter: brightness(1.08);
    }
    .stButton > button:active,
    .stFormSubmitButton > button:active {
        transform: translateY(0);
    }

    /* ── Number input ── */
    div[data-baseweb="input"] input[type="number"] { color: var(--text) !important; }

    /* ── Alerts / info ── */
    div[data-testid="stAlert"] {
        background: rgba(61,127,255,0.1) !important;
        border: 1px solid rgba(61,127,255,0.25) !important;
        border-radius: var(--radius-sm) !important;
        color: #a8c4ff !important;
        font-size: 0.86rem;
    }

    /* ── Code block ── */
    code, .stCode { font-family: 'DM Mono', monospace !important; }
    div[data-testid="stCode"] {
        background: var(--bg-2) !important;
        border: 1px solid var(--line) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ── JSON viewer ── */
    div[data-testid="stJson"] {
        background: var(--bg-2) !important;
        border: 1px solid var(--line) !important;
        border-radius: var(--radius-sm) !important;
    }

    /* ── Success / error ── */
    div[data-testid="stAlert"][data-baseweb="notification"][kind="positive"] {
        background: rgba(34,197,94,0.1) !important;
        border-color: rgba(34,197,94,0.3) !important;
        color: #86efac !important;
    }
    div[data-testid="stAlert"][data-baseweb="notification"][kind="negative"] {
        background: rgba(239,68,68,0.1) !important;
        border-color: rgba(239,68,68,0.3) !important;
        color: #fca5a5 !important;
    }

    /* ── Divider ── */
    hr { border-color: var(--line) !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar       { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: var(--bg-3); border-radius: 4px; }

    /* ── Custom components ── */
    .hrflow-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 0 1.6rem 0;
        border-bottom: 1px solid var(--line);
        margin-bottom: 1.8rem;
    }
    .hrflow-wordmark {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .hrflow-logo-circle {
        width: 36px; height: 36px;
        border-radius: 10px;
        background: linear-gradient(135deg, #3d7fff, #6040e8);
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; font-weight: 700; color: white;
        box-shadow: 0 4px 16px rgba(61,127,255,0.4);
    }
    .hrflow-brand-name {
        font-size: 1.15rem;
        font-weight: 700;
        color: var(--text);
        letter-spacing: -0.03em;
    }
    .hrflow-brand-tag {
        font-size: 0.72rem;
        color: var(--muted);
        font-weight: 400;
        letter-spacing: 0.04em;
        margin-top: -2px;
    }
    .topbar-status {
        display: flex; align-items: center; gap: 6px;
        font-size: 0.78rem; color: var(--muted);
        background: var(--bg-2);
        border: 1px solid var(--line);
        border-radius: 100px;
        padding: 5px 12px;
    }
    .status-dot {
        width: 7px; height: 7px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 8px var(--green);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%,100% { opacity: 1; }
        50%      { opacity: 0.45; }
    }

    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 1.8rem;
    }
    .kpi-card {
        background: var(--bg-2);
        border: 1px solid var(--line);
        border-radius: var(--radius-md);
        padding: 16px 18px 14px;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        border-radius: 2px 2px 0 0;
    }
    .kpi-card.blue::before   { background: linear-gradient(90deg, var(--blue), transparent); }
    .kpi-card.purple::before { background: linear-gradient(90deg, var(--purple), transparent); }
    .kpi-card.teal::before   { background: linear-gradient(90deg, var(--teal), transparent); }
    .kpi-card.amber::before  { background: linear-gradient(90deg, var(--amber), transparent); }
    .kpi-label  { font-size: 0.75rem; color: var(--muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 6px; }
    .kpi-value  { font-size: 1.5rem; font-weight: 700; color: var(--text); letter-spacing: -0.03em; }
    .kpi-sub    { font-size: 0.74rem; color: var(--hint); margin-top: 4px; }

    .section-header {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 1.2rem;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--line);
    }
    .section-icon {
        width: 32px; height: 32px;
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text);
        margin: 0;
    }
    .section-desc {
        font-size: 0.8rem;
        color: var(--muted);
        margin-top: 2px;
    }

    .card-panel {
        background: var(--bg-glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--line);
        border-radius: var(--radius-lg);
        padding: 22px 24px;
        margin-bottom: 1rem;
    }

    .endpoint-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--bg-3);
        border: 1px solid var(--line-mid);
        border-radius: 6px;
        padding: 3px 10px;
        font-family: 'DM Mono', monospace;
        font-size: 0.74rem;
        color: var(--blue-light);
        margin-bottom: 12px;
    }
    .method-get    { color: var(--green) !important; }
    .method-post   { color: var(--amber) !important; }

    .role-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 100px;
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-left: 8px;
    }
    .role-hr       { background: rgba(61,127,255,0.15); color: var(--blue-light); border: 1px solid rgba(61,127,255,0.3); }
    .role-emp      { background: rgba(20,184,166,0.15); color: #5eead4; border: 1px solid rgba(20,184,166,0.3); }
    .role-cand     { background: rgba(245,158,11,0.15); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }

    .sidebar-profile {
        background: var(--bg-2);
        border: 1px solid var(--line);
        border-radius: var(--radius-md);
        padding: 14px 16px;
        margin: 1rem 0;
    }
    .sidebar-profile .p-name  { font-size: 0.92rem; font-weight: 600; color: var(--text); }
    .sidebar-profile .p-role  { font-size: 0.76rem; color: var(--muted); margin-top: 2px; }
    .sidebar-profile .p-id    { font-size: 0.72rem; color: var(--hint); font-family: 'DM Mono'; margin-top: 6px; }

    .sidebar-api-item {
        background: var(--bg-2);
        border: 1px solid var(--line);
        border-radius: var(--radius-sm);
        padding: 8px 12px;
        font-size: 0.75rem;
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        margin-bottom: 4px;
    }

    .response-wrapper {
        background: var(--bg-2);
        border: 1px solid var(--line);
        border-radius: var(--radius-md);
        padding: 16px 18px;
        margin-top: 10px;
    }
    .response-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--hint);
        margin-bottom: 8px;
    }

    /* two-column form grid */
    .form-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 0 16px; }

    /* utility */
    .mt-sm { margin-top: 0.6rem; }
    .mt-md { margin-top: 1.2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# DEFAULTS / SESSION STATE
# ─────────────────────────────────────────────
DEFAULTS = {
    "token": "",
    "role": "",
    "user_name": "",
    "user_id": "",
    "main_api": "http://localhost:8081",
    "hiring_api": "http://localhost:8086",
    "leave_api": "http://localhost:8082",
    "relations_api": "http://localhost:8084",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def auth_headers() -> Dict[str, str]:
    h = {"Content-Type": "application/json"}
    if st.session_state.token:
        h["Authorization"] = st.session_state.token
    return h


def parse_user_id(token: str) -> str:
    parts = token.split(":")
    return parts[1] if len(parts) >= 3 else ""


def call_api(
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    use_auth: bool = True,
) -> None:
    """Execute an API call and render the result."""
    st.markdown(
        f"""<div class="endpoint-badge">
            <span class="{'method-get' if method.upper()=='GET' else 'method-post'}">{method.upper()}</span>
            <span>{url}</span>
        </div>""",
        unsafe_allow_html=True,
    )
    try:
        headers = auth_headers() if use_auth else {"Content-Type": "application/json"}
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            json=payload,
            timeout=30,
        )
        st.markdown('<div class="response-wrapper">', unsafe_allow_html=True)
        if response.ok:
            st.success(f"✓  {response.status_code} {response.reason}")
        else:
            st.error(f"✗  {response.status_code} {response.reason}")
        st.markdown('<div class="response-label">Response body</div>', unsafe_allow_html=True)
        try:
            st.json(response.json())
        except Exception:
            st.code(response.text or "<empty response>", language="text")
        st.markdown("</div>", unsafe_allow_html=True)
    except requests.RequestException as exc:
        st.error(f"Request failed: {exc}")


def section_header(icon: str, title: str, desc: str, bg: str = "#1e3a5f") -> None:
    st.markdown(
        f"""<div class="section-header">
            <div class="section-icon" style="background:{bg}">{icon}</div>
            <div>
                <div class="section-title">{title}</div>
                <div class="section-desc">{desc}</div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """<div style="display:flex;align-items:center;gap:10px;padding:0.5rem 0 1.2rem">
            <div style="width:32px;height:32px;border-radius:8px;background:linear-gradient(135deg,#3d7fff,#6040e8);
                        display:flex;align-items:center;justify-content:center;font-weight:700;color:#fff;font-size:14px;
                        box-shadow:0 4px 14px rgba(61,127,255,0.4)">H</div>
            <div>
                <div style="font-weight:700;font-size:1rem;color:#edf2ff;letter-spacing:-0.02em">HRFlow</div>
                <div style="font-size:0.7rem;color:#4d5f84;letter-spacing:0.04em">Enterprise Portal</div>
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

    st.markdown("**API Endpoints**", help="Configure the base URLs for each service")
    st.text_input("Main API", key="main_api", placeholder="http://localhost:8081")
    st.text_input("Hiring API", key="hiring_api", placeholder="http://localhost:8086")
    st.text_input("Leave API", key="leave_api", placeholder="http://localhost:8082")
    st.text_input("Relations API", key="relations_api", placeholder="http://localhost:8084")

    st.markdown("<hr style='margin:1rem 0;border-color:rgba(255,255,255,0.07)'>", unsafe_allow_html=True)

    if st.session_state.user_name:
        initials = "".join(w[0].upper() for w in st.session_state.user_name.split()[:2])
        role_color = {"HR": "#3d7fff", "EMPLOYEE": "#14b8a6", "CANDIDATE": "#f59e0b"}.get(
            st.session_state.role.upper(), "#8b5cf6"
        )
        st.markdown(
            f"""<div class="sidebar-profile">
                <div style="display:flex;align-items:center;gap:10px">
                    <div style="width:36px;height:36px;border-radius:9px;background:{role_color}22;
                                border:1px solid {role_color}44;display:flex;align-items:center;
                                justify-content:center;font-weight:700;font-size:13px;color:{role_color}">
                        {initials}
                    </div>
                    <div>
                        <div class="p-name">{st.session_state.user_name}</div>
                        <div class="p-role" style="color:{role_color}">{st.session_state.role}</div>
                    </div>
                </div>
                <div class="p-id">ID · {st.session_state.user_id or '—'}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        if st.button("Sign out", use_container_width=True):
            for k in ("token", "role", "user_name", "user_id"):
                st.session_state[k] = ""
            st.rerun()
    else:
        st.markdown(
            """<div class="sidebar-profile" style="text-align:center;padding:18px">
                <div style="font-size:1.4rem;margin-bottom:6px">🔒</div>
                <div style="font-size:0.82rem;color:#4d5f84">Not signed in</div>
                <div style="font-size:0.74rem;color:#2a3552;margin-top:3px">Use the Login tab</div>
            </div>""",
            unsafe_allow_html=True,
        )

    if st.session_state.token:
        st.markdown('<div class="response-label" style="margin-top:1rem">Active token</div>', unsafe_allow_html=True)
        st.code(st.session_state.token, language="text")


# ─────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────
st.markdown(
    """<div class="hrflow-topbar">
        <div class="hrflow-wordmark">
            <div class="hrflow-logo-circle">H</div>
            <div>
                <div class="hrflow-brand-name">HRFlow Enterprise</div>
                <div class="hrflow-brand-tag">Unified Operations Console</div>
            </div>
        </div>
        <div class="topbar-status">
            <div class="status-dot"></div>
            Services online
        </div>
    </div>""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────
st.markdown(
    """<div class="kpi-row">
        <div class="kpi-card blue">
            <div class="kpi-label">Active Modules</div>
            <div class="kpi-value">7</div>
            <div class="kpi-sub">Hiring · Leave · Relations</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-label">Connected Services</div>
            <div class="kpi-value">4</div>
            <div class="kpi-sub">All healthy</div>
        </div>
        <div class="kpi-card teal">
            <div class="kpi-label">API Endpoints</div>
            <div class="kpi-value">11</div>
            <div class="kpi-sub">GET · POST</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Session</div>
            <div class="kpi-value">Ready</div>
            <div class="kpi-sub">Awaiting login</div>
        </div>
    </div>""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
(
    login_tab, candidate_tab, employee_tab,
    hr_tab, hiring_tab, leave_tab, relation_tab, utility_tab,
) = st.tabs([
    "🔐 Login",
    "👤 Candidate",
    "🧑‍💼 Employee",
    "🏢 HR",
    "🤖 Hiring API",
    "🏖️ Leave API",
    "🤝 Relations API",
    "🛠️ Utilities",
])


# ════════════════════════════════════════════
# LOGIN
# ════════════════════════════════════════════
with login_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("🔐", "Secure Authentication", "Sign in via the main API gateway", "#1e2f52")

    col_form, col_info = st.columns([3, 2], gap="large")

    with col_form:
        with st.form("login_form"):
            email    = st.text_input("Email address", placeholder="you@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Sign in →", use_container_width=True)

        if submitted:
            url = f"{st.session_state.main_api}/api/login"
            try:
                response = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    json={"email": email, "password": password},
                    timeout=30,
                )
                if response.ok:
                    data = response.json()
                    st.session_state.token     = data.get("token", "")
                    st.session_state.role      = data.get("role", "")
                    st.session_state.user_name = data.get("name", "")
                    st.session_state.user_id   = parse_user_id(st.session_state.token)
                    st.success(f"Welcome back, **{st.session_state.user_name}** 👋")
                    st.json(data)
                else:
                    st.error(f"Login failed — {response.status_code}")
                    try:    st.json(response.json())
                    except: st.code(response.text)
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")

    with col_info:
        st.markdown(
            """<div style="background:rgba(61,127,255,0.07);border:1px solid rgba(61,127,255,0.18);
                          border-radius:14px;padding:18px 20px;margin-top:4px">
                <div style="font-size:0.78rem;color:#6fa0ff;font-weight:600;text-transform:uppercase;
                            letter-spacing:0.08em;margin-bottom:12px">Token format</div>
                <div style="font-family:'DM Mono';font-size:0.82rem;color:#8a9dc4;line-height:1.8">
                    ROLE:USER_ID:TOKEN
                </div>
                <div style="margin-top:14px;font-size:0.78rem;font-weight:600;color:#6fa0ff;
                            text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px">Roles</div>
                <div style="display:flex;flex-direction:column;gap:6px">
                    <span class="role-badge role-hr" style="width:fit-content">HR</span>
                    <span class="role-badge role-emp" style="width:fit-content">Employee</span>
                    <span class="role-badge role-cand" style="width:fit-content">Candidate</span>
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# CANDIDATE
# ════════════════════════════════════════════
with candidate_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("👤", "Candidate Application", "Submit a new candidate application", "#2a1f3d")
    st.markdown(
        '<span class="role-badge role-cand">Requires CANDIDATE token</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mt-md"></div>', unsafe_allow_html=True)

    with st.form("candidate_apply_form"):
        col1, col2 = st.columns(2)
        with col1:
            c_name  = st.text_input("Full name",    key="cand_name",  placeholder="Jane Smith")
            c_mail  = st.text_input("Email",        key="cand_mail",  placeholder="jane@example.com")
            c_phone = st.text_input("Phone",        key="cand_phone", placeholder="+91 98765 43210")
        with col2:
            c_role  = st.text_input("Applied role", key="cand_role",  placeholder="Java Developer")
            c_yop   = st.text_input("Year of passing", key="cand_yop", placeholder="2024")

        c_resume = st.text_area(
            "Resume content",
            height=160, key="cand_resume",
            placeholder="Paste or describe resume content here…",
        )
        c_jd = st.text_area(
            "Job description",
            height=120, key="cand_jd",
            placeholder="Paste the job description here…",
        )
        submitted = st.form_submit_button("Submit application →", use_container_width=False)

    if submitted:
        payload = {
            "c_name": c_name, "c_mail": c_mail, "c_phone": c_phone,
            "c_role": c_role, "c_yop": c_yop,
            "c_resume": c_resume, "c_jobDescription": c_jd,
        }
        call_api("POST", f"{st.session_state.main_api}/api/candidate/apply", payload)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# EMPLOYEE
# ════════════════════════════════════════════
with employee_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("🧑‍💼", "Employee Workspace", "View interviews, team leaves, and submit leave requests", "#0f2a2a")
    st.markdown(
        '<span class="role-badge role-emp">Requires EMPLOYEE token</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mt-md"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown(
            '<div class="endpoint-badge"><span class="method-get">GET</span>/api/employee/interviews</div>',
            unsafe_allow_html=True,
        )
        if st.button("Fetch my interviews", key="btn_interviews"):
            call_api("GET", f"{st.session_state.main_api}/api/employee/interviews")

        st.markdown('<div class="mt-md"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="endpoint-badge"><span class="method-get">GET</span>/api/employee/team-leaves</div>',
            unsafe_allow_html=True,
        )
        if st.button("Fetch team leaves", key="btn_team_leaves"):
            call_api("GET", f"{st.session_state.main_api}/api/employee/team-leaves")

    with col_right:
        st.markdown(
            '<div class="endpoint-badge"><span class="method-post">POST</span>/api/employee/apply-leave</div>',
            unsafe_allow_html=True,
        )
        with st.form("apply_leave_form"):
            leave_days   = st.number_input("Number of days", min_value=1, step=1)
            leave_reason = st.text_area("Reason for leave", height=100, placeholder="Please state your reason…")
            al_submit    = st.form_submit_button("Submit leave request →")

        if al_submit:
            call_api(
                "POST",
                f"{st.session_state.main_api}/api/employee/apply-leave",
                {"days": int(leave_days), "reason": leave_reason},
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# HR
# ════════════════════════════════════════════
with hr_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("🏢", "HR Command Centre", "Manage candidates, interviews, and leave requests", "#1a1a2e")
    st.markdown(
        '<span class="role-badge role-hr">Requires HR token</span>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="mt-md"></div>', unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        for label, path, key in [
            ("Fetch all candidates",  "/api/hr/candidates",     "btn_cands"),
            ("Fetch leave requests",  "/api/hr/leave-requests", "btn_leaves"),
            ("Fetch all interviews",  "/api/hr/interviews",     "btn_ints"),
        ]:
            method = "GET"
            st.markdown(
                f'<div class="endpoint-badge"><span class="method-get">{method}</span>{path}</div>',
                unsafe_allow_html=True,
            )
            if st.button(label, key=key):
                call_api(method, f"{st.session_state.main_api}{path}")
            st.markdown('<div class="mt-sm"></div>', unsafe_allow_html=True)

    with col_r:
        st.markdown(
            '<div class="endpoint-badge"><span class="method-post">POST</span>/api/hr/approve-leave</div>',
            unsafe_allow_html=True,
        )
        with st.form("approve_leave_form"):
            approve_id  = st.text_input("Leave request ID", placeholder="e.g. LR-0042")
            ap_submit   = st.form_submit_button("✓  Approve leave")
        if ap_submit:
            call_api("POST", f"{st.session_state.main_api}/api/hr/approve-leave", {"id": approve_id})

        st.markdown('<div class="mt-md"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="endpoint-badge"><span class="method-post">POST</span>/api/hr/reject-leave</div>',
            unsafe_allow_html=True,
        )
        with st.form("reject_leave_form"):
            reject_id = st.text_input("Leave request ID", placeholder="e.g. LR-0043", key="rej_id")
            rj_submit = st.form_submit_button("✗  Reject leave")
        if rj_submit:
            call_api("POST", f"{st.session_state.main_api}/api/hr/reject-leave", {"id": reject_id})

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# HIRING API
# ════════════════════════════════════════════
with hiring_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("🤖", "AI Hiring Pipeline", f"Direct endpoint · port 8086 · no auth required", "#0d1f12")
    st.markdown(
        '<div class="endpoint-badge"><span class="method-post">POST</span>/hiring</div>',
        unsafe_allow_html=True,
    )

    with st.form("hiring_form"):
        col1, col2 = st.columns(2)
        with col1:
            h_name  = st.text_input("Candidate name",  key="h_name",  placeholder="Jane Smith")
            h_mail  = st.text_input("Email",            key="h_mail",  placeholder="jane@example.com")
            h_phone = st.text_input("Phone",            key="h_phone", placeholder="+91 98765 43210")
        with col2:
            h_role  = st.text_input("Applied role",     key="h_role",  placeholder="Java Developer")
            h_yop   = st.text_input("Year of passing",  key="h_yop",   placeholder="2024")

        h_resume   = st.text_area("Resume content",   height=150, key="h_resume",   placeholder="Paste resume here…")
        h_job_desc = st.text_area("Job description",  height=120, key="h_job_desc", placeholder="Paste JD here…")
        h_submit   = st.form_submit_button("▶  Run hiring pipeline", use_container_width=False)

    if h_submit:
        payload = {
            "c_name": h_name, "c_mail": h_mail, "c_phone": h_phone,
            "c_role": h_role, "c_yop": h_yop,
            "c_resume": h_resume, "c_jobDescription": h_job_desc,
        }
        call_api("POST", f"{st.session_state.hiring_api}/hiring", payload, use_auth=False)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# LEAVE API
# ════════════════════════════════════════════
with leave_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("🏖️", "Leave Intelligence Agent", "Direct leave agent · port 8082 · no auth required", "#0d1f1a")
    st.markdown(
        '<div class="endpoint-badge"><span class="method-post">POST</span>/api/leave</div>',
        unsafe_allow_html=True,
    )

    with st.form("leave_api_form"):
        col1, col2 = st.columns(2)
        with col1:
            emp_id          = st.text_input("Employee ID",     placeholder="EMP-101")
            leave_days_api  = st.number_input("Days requested", min_value=1, step=1, key="leave_api_days")
        with col2:
            leave_reason_api = st.text_area("Reason", height=100, key="leave_api_reason", placeholder="Reason for leave…")

        la_submit = st.form_submit_button("▶  Run leave agent", use_container_width=False)

    if la_submit:
        payload = {"emp_id": emp_id, "days": int(leave_days_api), "reason": leave_reason_api}
        call_api("POST", f"{st.session_state.leave_api}/api/leave", payload, use_auth=False)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# RELATIONS API
# ════════════════════════════════════════════
with relation_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("🤝", "Employee Relations Desk", "Submit complaints and HR relations requests · port 8084", "#1f1320")
    st.markdown(
        '<div class="endpoint-badge"><span class="method-post">POST</span>/api/relation</div>',
        unsafe_allow_html=True,
    )

    with st.form("relation_form"):
        col1, col2, col3 = st.columns(3)
        with col1: rel_emp_id    = st.text_input("Employee ID",    key="rel_emp_id",    placeholder="EMP-101")
        with col2: rel_emp_name  = st.text_input("Employee name",  key="rel_emp_name",  placeholder="Jane Smith")
        with col3: rel_emp_email = st.text_input("Email",          key="rel_emp_email", placeholder="jane@company.com")

        complaint_type = st.text_input("Complaint type", placeholder="e.g. Harassment / Policy violation")
        complaint      = st.text_area("Complaint details", height=160, placeholder="Describe the complaint in detail…")
        rel_submit     = st.form_submit_button("Submit complaint →", use_container_width=False)

    if rel_submit:
        payload = {
            "emp_id": rel_emp_id, "emp_name": rel_emp_name,
            "emp_email": rel_emp_email,
            "complaint_type": complaint_type, "complaint": complaint,
        }
        call_api("POST", f"{st.session_state.relations_api}/api/relation", payload, use_auth=False)

    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════
# UTILITIES
# ════════════════════════════════════════════
with utility_tab:
    st.markdown('<div class="card-panel">', unsafe_allow_html=True)
    section_header("🛠️", "Developer Utilities", "Quick reference payloads and setup instructions", "#1f1a0d")

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown(
            '<div style="font-size:0.78rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;'
            'color:#4d5f84;margin-bottom:8px">Sample payloads</div>',
            unsafe_allow_html=True,
        )
        sample_payload = {
            "login":  {"email": "hr@example.com", "password": "your-password"},
            "token":  "HR:101:TOKEN_STRING",
            "candidate": {
                "c_name": "Akshaya Reddy", "c_mail": "akshaya@example.com",
                "c_phone": "9876543210",   "c_role": "Java Developer",
                "c_yop": "2024",           "c_resume": "Resume text here",
                "c_jobDescription": "Job description here",
            },
        }
        st.json(sample_payload)

    with col_b:
        st.markdown(
            '<div style="font-size:0.78rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;'
            'color:#4d5f84;margin-bottom:8px">Setup</div>',
            unsafe_allow_html=True,
        )
        st.code("pip install streamlit requests\nstreamlit run app.py", language="bash")

        st.markdown(
            """<div style="margin-top:14px;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                          border-radius:10px;padding:14px 16px">
                <div style="font-size:0.8rem;color:#8a9dc4;line-height:1.9">
                    ↗ Login stores the token in session state automatically<br>
                    ↗ Employee &amp; HR endpoints reuse the active token<br>
                    ↗ Candidate apply also sends the Authorization header<br>
                    ↗ Hiring, Leave &amp; Relations bypass auth headers
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)