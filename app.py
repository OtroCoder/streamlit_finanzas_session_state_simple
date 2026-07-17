"""
Aplicación financiera monolítica en Streamlit.

Toda la interfaz visible se construye con HTML, CSS y JavaScript:
- No utiliza widgets visuales nativos de Streamlit.
- Incluye navegación por módulos, validaciones y botones animados.
- Conserva los valores mediante localStorage del navegador.
- Los cálculos financieros se ejecutan en JavaScript.

Ejecución:
    streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# 1. CONFIGURACIÓN GENERAL DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Finanzas Corporativas",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Oculta completamente la interfaz visual propia de Streamlit.
st.markdown(
    """
    <style>
        #MainMenu, header, footer,
        [data-testid="stSidebar"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"],
        [data-testid="stStatusWidget"] {
            display: none !important;
        }

        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stMain"], .stApp {
            margin: 0 !important;
            padding: 0 !important;
            background: #f4f7fb !important;
        }

        [data-testid="stMainBlockContainer"], .block-container {
            width: 100% !important;
            max-width: none !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        iframe {
            display: block;
            width: 100% !important;
            border: 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 2. APLICACIÓN COMPLETA: HTML + CSS + JAVASCRIPT
# ============================================================

app_html = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="color-scheme" content="light" />
    <title>Finanzas Corporativas</title>

    <style>
        :root {
            --navy-950: #07152e;
            --navy-900: #0b1f3a;
            --navy-800: #12345b;
            --blue-700: #155eef;
            --blue-600: #2878ff;
            --blue-100: #dbeafe;
            --cyan-500: #19b8c9;
            --cyan-100: #dff9fb;
            --green-600: #079455;
            --green-100: #dcfae6;
            --amber-600: #dc6803;
            --amber-100: #fef0c7;
            --red-600: #d92d20;
            --red-100: #fee4e2;
            --slate-900: #101828;
            --slate-700: #344054;
            --slate-600: #475467;
            --slate-500: #667085;
            --slate-400: #98a2b3;
            --slate-300: #d0d5dd;
            --slate-200: #e4e7ec;
            --slate-100: #f2f4f7;
            --surface: #ffffff;
            --surface-soft: #f7f9fc;
            --shadow-sm: 0 2px 8px rgba(16, 24, 40, 0.06);
            --shadow-md: 0 14px 38px rgba(16, 24, 40, 0.11);
            --shadow-lg: 0 24px 70px rgba(7, 21, 46, 0.18);
            --radius-sm: 10px;
            --radius-md: 16px;
            --radius-lg: 24px;
            --transition: 220ms cubic-bezier(.2, .8, .2, 1);
        }

        * {
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            margin: 0;
            min-height: 100vh;
            color: var(--slate-900);
            background:
                radial-gradient(circle at 8% 2%, rgba(25, 184, 201, 0.12), transparent 25%),
                radial-gradient(circle at 94% 8%, rgba(21, 94, 239, 0.13), transparent 28%),
                #f4f7fb;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
            -webkit-font-smoothing: antialiased;
        }

        button, input {
            font: inherit;
        }

        button {
            -webkit-tap-highlight-color: transparent;
        }

        .app-shell {
            width: min(1480px, 100%);
            min-height: 100vh;
            margin: 0 auto;
            padding: 24px;
        }

        .topbar {
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            padding: 22px 26px;
            color: white;
            background: linear-gradient(135deg, var(--navy-950), var(--navy-800));
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-lg);
        }

        .topbar::before {
            content: "";
            position: absolute;
            width: 330px;
            height: 330px;
            right: -110px;
            top: -190px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(25,184,201,.38), transparent 67%);
            pointer-events: none;
        }

        .brand {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .brand-mark {
            display: grid;
            place-items: center;
            width: 48px;
            height: 48px;
            flex: 0 0 48px;
            border-radius: 15px;
            background: linear-gradient(145deg, var(--blue-600), var(--cyan-500));
            box-shadow: 0 12px 28px rgba(25, 184, 201, 0.28);
        }

        .brand-mark svg {
            width: 25px;
            height: 25px;
        }

        .brand-copy h1 {
            margin: 0;
            font-size: clamp(1.15rem, 2.3vw, 1.55rem);
            letter-spacing: -0.03em;
        }

        .brand-copy p {
            margin: 4px 0 0;
            color: rgba(255,255,255,.68);
            font-size: .88rem;
        }

        .top-actions {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            min-height: 38px;
            padding: 0 14px;
            color: #e8ffff;
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 999px;
            font-size: .82rem;
            font-weight: 700;
            backdrop-filter: blur(12px);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #6ce9a6;
            box-shadow: 0 0 0 5px rgba(108,233,166,.12);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(.76); opacity: .72; }
        }

        .layout {
            display: grid;
            grid-template-columns: 278px minmax(0, 1fr);
            gap: 22px;
            margin-top: 22px;
        }

        .sidebar {
            position: sticky;
            top: 20px;
            align-self: start;
            padding: 20px;
            background: rgba(255,255,255,.88);
            border: 1px solid rgba(208,213,221,.74);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            backdrop-filter: blur(18px);
        }

        .sidebar-label {
            margin: 2px 8px 12px;
            color: var(--slate-500);
            font-size: .72rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .nav-list {
            display: grid;
            gap: 8px;
        }

        .nav-button {
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 12px;
            width: 100%;
            min-height: 54px;
            padding: 10px 13px;
            color: var(--slate-600);
            background: transparent;
            border: 1px solid transparent;
            border-radius: 14px;
            cursor: pointer;
            text-align: left;
            transition: color var(--transition), background var(--transition),
                        transform var(--transition), border-color var(--transition);
        }

        .nav-button::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(100deg, transparent 30%, rgba(255,255,255,.68), transparent 70%);
            transform: translateX(-115%);
            transition: transform 500ms ease;
        }

        .nav-button:hover::after {
            transform: translateX(115%);
        }

        .nav-button:hover {
            color: var(--navy-900);
            background: var(--slate-100);
            transform: translateX(3px);
        }

        .nav-button.active {
            color: white;
            background: linear-gradient(135deg, var(--blue-700), var(--blue-600));
            border-color: rgba(255,255,255,.16);
            box-shadow: 0 10px 24px rgba(21,94,239,.24);
        }

        .nav-icon {
            display: grid;
            place-items: center;
            width: 35px;
            height: 35px;
            flex: 0 0 35px;
            color: currentColor;
            background: rgba(255,255,255,.14);
            border-radius: 10px;
        }

        .nav-button:not(.active) .nav-icon {
            background: var(--blue-100);
            color: var(--blue-700);
        }

        .nav-icon svg {
            width: 18px;
            height: 18px;
        }

        .nav-copy strong {
            display: block;
            font-size: .92rem;
        }

        .nav-copy span {
            display: block;
            margin-top: 2px;
            opacity: .72;
            font-size: .74rem;
        }

        .sidebar-divider {
            height: 1px;
            margin: 18px 0;
            background: var(--slate-200);
        }

        .storage-card {
            padding: 15px;
            color: var(--slate-700);
            background: linear-gradient(145deg, #f8fbff, #eef5ff);
            border: 1px solid #d5e5ff;
            border-radius: 14px;
        }

        .storage-card strong {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: .84rem;
        }

        .storage-card p {
            margin: 8px 0 0;
            color: var(--slate-500);
            font-size: .76rem;
            line-height: 1.5;
        }

        .main-content {
            min-width: 0;
        }

        .hero {
            position: relative;
            overflow: hidden;
            display: grid;
            grid-template-columns: minmax(0, 1fr) auto;
            gap: 20px;
            align-items: center;
            padding: 26px 28px;
            background: rgba(255,255,255,.92);
            border: 1px solid rgba(208,213,221,.76);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-sm);
        }

        .hero::after {
            content: "";
            position: absolute;
            width: 230px;
            height: 230px;
            right: -85px;
            bottom: -150px;
            border-radius: 50%;
            background: rgba(25,184,201,.08);
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 9px;
            color: var(--blue-700);
            font-size: .74rem;
            font-weight: 800;
            letter-spacing: .11em;
            text-transform: uppercase;
        }

        .eyebrow::before {
            content: "";
            width: 22px;
            height: 3px;
            border-radius: 99px;
            background: var(--cyan-500);
        }

        .hero h2 {
            margin: 0;
            color: var(--navy-950);
            font-size: clamp(1.7rem, 3vw, 2.35rem);
            letter-spacing: -0.045em;
            line-height: 1.05;
        }

        .hero p {
            max-width: 720px;
            margin: 12px 0 0;
            color: var(--slate-500);
            font-size: .96rem;
            line-height: 1.65;
        }

        .hero-badge {
            position: relative;
            z-index: 1;
            display: grid;
            place-items: center;
            width: 108px;
            height: 108px;
            border-radius: 30px;
            background: linear-gradient(145deg, var(--navy-900), var(--blue-700));
            box-shadow: 0 20px 34px rgba(11,31,58,.22);
            animation: float 5s ease-in-out infinite;
        }

        .hero-badge svg {
            width: 52px;
            height: 52px;
            color: white;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0); }
            50% { transform: translateY(-7px) rotate(2deg); }
        }

        .workspace {
            display: grid;
            grid-template-columns: minmax(0, 1.35fr) minmax(300px, .65fr);
            gap: 20px;
            margin-top: 20px;
        }

        .panel {
            background: rgba(255,255,255,.94);
            border: 1px solid rgba(208,213,221,.76);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-sm);
        }

        .form-panel {
            padding: 26px;
        }

        .panel-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 22px;
        }

        .panel-title {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .panel-icon {
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            border-radius: 13px;
            color: var(--blue-700);
            background: var(--blue-100);
        }

        .panel-icon svg {
            width: 21px;
            height: 21px;
        }

        .panel-title h3 {
            margin: 0;
            color: var(--navy-950);
            font-size: 1.08rem;
        }

        .panel-title p {
            margin: 4px 0 0;
            color: var(--slate-500);
            font-size: .78rem;
        }

        .module-chip {
            padding: 7px 11px;
            color: var(--blue-700);
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 999px;
            font-size: .72rem;
            font-weight: 800;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 16px;
        }

        .field-group.full {
            grid-column: 1 / -1;
        }

        .field-group label {
            display: block;
            margin: 0 0 8px;
            color: var(--slate-700);
            font-size: .8rem;
            font-weight: 750;
        }

        .field-shell {
            position: relative;
            display: flex;
            align-items: center;
            min-height: 54px;
            background: var(--surface);
            border: 1.5px solid var(--slate-300);
            border-radius: 13px;
            transition: border-color var(--transition), box-shadow var(--transition),
                        transform var(--transition);
        }

        .field-shell:focus-within {
            border-color: var(--blue-600);
            box-shadow: 0 0 0 4px rgba(40,120,255,.12);
            transform: translateY(-1px);
        }

        .field-prefix,
        .field-suffix {
            display: grid;
            place-items: center;
            min-width: 46px;
            height: 100%;
            color: var(--slate-500);
            font-size: .84rem;
            font-weight: 750;
        }

        .field-prefix {
            border-right: 1px solid var(--slate-200);
        }

        .field-suffix {
            min-width: 65px;
            border-left: 1px solid var(--slate-200);
        }

        .field-shell input {
            width: 100%;
            min-width: 0;
            height: 52px;
            padding: 0 14px;
            color: var(--slate-900);
            background: transparent;
            border: 0;
            outline: 0;
            font-weight: 700;
        }

        .field-shell input::-webkit-inner-spin-button,
        .field-shell input::-webkit-outer-spin-button {
            opacity: .45;
        }

        .helper-text {
            min-height: 18px;
            margin-top: 6px;
            color: var(--slate-500);
            font-size: .72rem;
        }

        .helper-text.error {
            color: var(--red-600);
            font-weight: 700;
        }

        .action-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 22px;
        }

        .btn {
            position: relative;
            overflow: hidden;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 9px;
            min-height: 50px;
            padding: 0 19px;
            border-radius: 13px;
            border: 0;
            cursor: pointer;
            font-size: .84rem;
            font-weight: 800;
            transition: transform var(--transition), box-shadow var(--transition),
                        filter var(--transition), background var(--transition);
        }

        .btn::before {
            content: "";
            position: absolute;
            width: 0;
            height: 0;
            left: var(--ripple-x, 50%);
            top: var(--ripple-y, 50%);
            border-radius: 50%;
            background: rgba(255,255,255,.42);
            transform: translate(-50%, -50%);
            transition: width 500ms ease, height 500ms ease, opacity 600ms ease;
            opacity: 0;
        }

        .btn.ripple::before {
            width: 360px;
            height: 360px;
            opacity: 1;
        }

        .btn:hover {
            transform: translateY(-2px);
        }

        .btn:active {
            transform: translateY(0) scale(.985);
        }

        .btn-primary {
            color: white;
            background: linear-gradient(135deg, var(--blue-700), var(--blue-600));
            box-shadow: 0 12px 25px rgba(21,94,239,.25);
        }

        .btn-primary:hover {
            box-shadow: 0 16px 30px rgba(21,94,239,.34);
            filter: saturate(1.08);
        }

        .btn-secondary {
            color: var(--slate-700);
            background: var(--slate-100);
            border: 1px solid var(--slate-200);
        }

        .btn-secondary:hover {
            background: #e9edf3;
        }

        .btn-ghost {
            min-height: 38px;
            padding: 0 13px;
            color: rgba(255,255,255,.9);
            background: rgba(255,255,255,.08);
            border: 1px solid rgba(255,255,255,.14);
        }

        .btn svg {
            width: 17px;
            height: 17px;
        }

        .result-panel {
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            min-height: 100%;
            padding: 26px;
            color: white;
            background:
                linear-gradient(155deg, rgba(255,255,255,.06), transparent 38%),
                linear-gradient(145deg, var(--navy-950), var(--navy-800));
            border-color: rgba(11,31,58,.42);
            box-shadow: var(--shadow-md);
        }

        .result-panel::before {
            content: "";
            position: absolute;
            width: 260px;
            height: 260px;
            right: -110px;
            top: -130px;
            border-radius: 50%;
            background: rgba(25,184,201,.14);
        }

        .result-label {
            position: relative;
            z-index: 1;
            display: flex;
            align-items: center;
            gap: 8px;
            color: rgba(255,255,255,.68);
            font-size: .74rem;
            font-weight: 800;
            letter-spacing: .11em;
            text-transform: uppercase;
        }

        .result-main {
            position: relative;
            z-index: 1;
            margin-top: 22px;
        }

        .result-main .caption {
            color: rgba(255,255,255,.66);
            font-size: .82rem;
        }

        .result-main .value {
            margin-top: 7px;
            font-size: clamp(2rem, 5vw, 3.1rem);
            font-weight: 850;
            letter-spacing: -0.055em;
            line-height: 1;
        }

        .result-main .value.pop {
            animation: resultPop 520ms cubic-bezier(.2,.9,.2,1);
        }

        @keyframes resultPop {
            0% { transform: translateY(12px) scale(.94); opacity: 0; }
            100% { transform: translateY(0) scale(1); opacity: 1; }
        }

        .result-grid {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 10px;
            margin-top: 24px;
        }

        .result-item {
            min-width: 0;
            padding: 14px;
            background: rgba(255,255,255,.07);
            border: 1px solid rgba(255,255,255,.1);
            border-radius: 14px;
            backdrop-filter: blur(10px);
        }

        .result-item span {
            display: block;
            color: rgba(255,255,255,.62);
            font-size: .72rem;
        }

        .result-item strong {
            display: block;
            overflow: hidden;
            margin-top: 6px;
            color: white;
            font-size: .98rem;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .meter-wrap {
            position: relative;
            z-index: 1;
            margin-top: auto;
            padding-top: 24px;
        }

        .meter-head {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
            color: rgba(255,255,255,.65);
            font-size: .72rem;
        }

        .meter {
            overflow: hidden;
            height: 8px;
            background: rgba(255,255,255,.12);
            border-radius: 999px;
        }

        .meter-fill {
            width: 0;
            height: 100%;
            background: linear-gradient(90deg, var(--cyan-500), #7cf5dc);
            border-radius: inherit;
            transition: width 900ms cubic-bezier(.2,.8,.2,1);
        }

        .info-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin-top: 20px;
        }

        .info-card {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            min-width: 0;
            padding: 17px;
            background: rgba(255,255,255,.9);
            border: 1px solid rgba(208,213,221,.74);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            transition: transform var(--transition), box-shadow var(--transition);
        }

        .info-card:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
        }

        .info-icon {
            display: grid;
            place-items: center;
            width: 36px;
            height: 36px;
            flex: 0 0 36px;
            color: var(--green-600);
            background: var(--green-100);
            border-radius: 11px;
        }

        .info-icon.blue {
            color: var(--blue-700);
            background: var(--blue-100);
        }

        .info-icon.amber {
            color: var(--amber-600);
            background: var(--amber-100);
        }

        .info-icon svg {
            width: 18px;
            height: 18px;
        }

        .info-card strong {
            display: block;
            color: var(--navy-950);
            font-size: .84rem;
        }

        .info-card p {
            margin: 5px 0 0;
            color: var(--slate-500);
            font-size: .75rem;
            line-height: 1.48;
        }

        .toast-stack {
            position: fixed;
            z-index: 50;
            right: 22px;
            bottom: 22px;
            display: grid;
            gap: 10px;
            width: min(360px, calc(100vw - 44px));
            pointer-events: none;
        }

        .toast {
            display: flex;
            align-items: center;
            gap: 11px;
            padding: 14px 15px;
            color: var(--slate-700);
            background: rgba(255,255,255,.96);
            border: 1px solid var(--slate-200);
            border-left: 4px solid var(--green-600);
            border-radius: 13px;
            box-shadow: var(--shadow-md);
            animation: toastIn 280ms ease both;
        }

        .toast.error {
            border-left-color: var(--red-600);
        }

        .toast.hide {
            animation: toastOut 240ms ease both;
        }

        @keyframes toastIn {
            from { opacity: 0; transform: translateY(12px) scale(.96); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes toastOut {
            to { opacity: 0; transform: translateY(10px) scale(.96); }
        }

        .modal-backdrop {
            position: fixed;
            z-index: 40;
            inset: 0;
            display: grid;
            place-items: center;
            padding: 20px;
            background: rgba(7,21,46,.58);
            backdrop-filter: blur(7px);
            opacity: 0;
            pointer-events: none;
            transition: opacity var(--transition);
        }

        .modal-backdrop.open {
            opacity: 1;
            pointer-events: auto;
        }

        .modal {
            width: min(760px, 100%);
            max-height: min(760px, 88vh);
            overflow: auto;
            background: white;
            border: 1px solid rgba(255,255,255,.8);
            border-radius: 22px;
            box-shadow: var(--shadow-lg);
            transform: translateY(15px) scale(.97);
            transition: transform var(--transition);
        }

        .modal-backdrop.open .modal {
            transform: translateY(0) scale(1);
        }

        .modal-head {
            position: sticky;
            top: 0;
            z-index: 2;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            padding: 19px 21px;
            background: rgba(255,255,255,.94);
            border-bottom: 1px solid var(--slate-200);
            backdrop-filter: blur(14px);
        }

        .modal-head h3 {
            margin: 0;
            font-size: 1rem;
        }

        .icon-button {
            display: grid;
            place-items: center;
            width: 38px;
            height: 38px;
            color: var(--slate-600);
            background: var(--slate-100);
            border: 1px solid var(--slate-200);
            border-radius: 11px;
            cursor: pointer;
            transition: transform var(--transition), background var(--transition);
        }

        .icon-button:hover {
            background: var(--slate-200);
            transform: rotate(5deg);
        }

        .modal-body {
            padding: 21px;
        }

        .state-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
        }

        .state-card {
            padding: 15px;
            background: var(--surface-soft);
            border: 1px solid var(--slate-200);
            border-radius: 14px;
        }

        .state-card h4 {
            margin: 0 0 12px;
            color: var(--navy-950);
            font-size: .85rem;
        }

        .state-row {
            display: flex;
            justify-content: space-between;
            gap: 12px;
            padding: 7px 0;
            border-top: 1px dashed var(--slate-200);
            color: var(--slate-500);
            font-size: .73rem;
        }

        .state-row strong {
            color: var(--slate-700);
            text-align: right;
        }

        .modal-actions {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-top: 18px;
        }

        .danger-button {
            color: white;
            background: var(--red-600);
            box-shadow: 0 10px 20px rgba(217,45,32,.2);
        }

        .module-view {
            display: none;
        }

        .module-view.active {
            display: contents;
        }

        .shake {
            animation: shake 360ms ease;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            50% { transform: translateX(5px); }
            75% { transform: translateX(-3px); }
        }

        @media (max-width: 1060px) {
            .layout {
                grid-template-columns: 1fr;
            }

            .sidebar {
                position: static;
            }

            .nav-list {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }

            .nav-button {
                min-height: 66px;
            }

            .nav-copy span,
            .storage-card,
            .sidebar-divider,
            .sidebar-label {
                display: none;
            }
        }

        @media (max-width: 820px) {
            .app-shell {
                padding: 14px;
            }

            .topbar {
                padding: 18px;
            }

            .status-pill {
                display: none;
            }

            .hero {
                grid-template-columns: 1fr;
                padding: 22px;
            }

            .hero-badge {
                display: none;
            }

            .workspace {
                grid-template-columns: 1fr;
            }

            .result-panel {
                min-height: 360px;
            }

            .info-strip {
                grid-template-columns: 1fr;
            }

            .state-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 580px) {
            .brand-copy p {
                display: none;
            }

            .top-actions .btn-ghost span {
                display: none;
            }

            .nav-list {
                grid-template-columns: 1fr;
            }

            .nav-button {
                min-height: 52px;
            }

            .nav-copy span {
                display: block;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            .field-group.full {
                grid-column: auto;
            }

            .form-panel,
            .result-panel {
                padding: 20px;
            }

            .panel-head {
                align-items: flex-start;
            }

            .module-chip {
                display: none;
            }

            .action-row .btn {
                width: 100%;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: .001ms !important;
                animation-iteration-count: 1 !important;
                scroll-behavior: auto !important;
                transition-duration: .001ms !important;
            }
        }
    </style>
</head>

<body>
    <div class="app-shell">
        <header class="topbar">
            <div class="brand">
                <div class="brand-mark" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 19V9m6 10V5m6 14v-7m4 7H2" stroke-linecap="round" />
                    </svg>
                </div>
                <div class="brand-copy">
                    <h1>Finanzas Corporativas</h1>
                    <p>Simuladores financieros con persistencia automática</p>
                </div>
            </div>

            <div class="top-actions">
                <div class="status-pill">
                    <span class="status-dot"></span>
                    Sesión protegida
                </div>
                <button class="btn btn-ghost" id="openStateButton" type="button">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 6h16M4 12h16M4 18h10" stroke-linecap="round" />
                    </svg>
                    <span>Datos guardados</span>
                </button>
            </div>
        </header>

        <div class="layout">
            <aside class="sidebar">
                <div class="sidebar-label">Módulos financieros</div>

                <nav class="nav-list" aria-label="Módulos financieros">
                    <button class="nav-button active" data-module="simple" type="button">
                        <span class="nav-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 3v18M17 7.5c0-1.66-2.24-3-5-3s-5 1.34-5 3 2.24 3 5 3 5 1.34 5 3-2.24 3-5 3-5-1.34-5-3" stroke-linecap="round"/>
                            </svg>
                        </span>
                        <span class="nav-copy">
                            <strong>Interés simple</strong>
                            <span>Crecimiento lineal</span>
                        </span>
                    </button>

                    <button class="nav-button" data-module="compound" type="button">
                        <span class="nav-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M4 16l5-5 4 4 7-8" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M14 7h6v6" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </span>
                        <span class="nav-copy">
                            <strong>Interés compuesto</strong>
                            <span>Crecimiento acumulativo</span>
                        </span>
                    </button>

                    <button class="nav-button" data-module="loan" type="button">
                        <span class="nav-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="5" width="18" height="14" rx="3"/>
                                <path d="M3 10h18M7 15h3" stroke-linecap="round"/>
                            </svg>
                        </span>
                        <span class="nav-copy">
                            <strong>Pago mensual</strong>
                            <span>Cuota de préstamo</span>
                        </span>
                    </button>
                </nav>

                <div class="sidebar-divider"></div>

                <div class="storage-card">
                    <strong>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                            <path d="m9 12 2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        Persistencia activa
                    </strong>
                    <p>Los valores se conservan al cambiar de módulo o actualizar la página.</p>
                </div>
            </aside>

            <main class="main-content">
                <section class="hero">
                    <div>
                        <div class="eyebrow" id="heroEyebrow">Simulador financiero</div>
                        <h2 id="heroTitle">Interés simple</h2>
                        <p id="heroDescription">
                            Calcule el rendimiento generado por un capital cuando el interés no se acumula sobre periodos anteriores.
                        </p>
                    </div>

                    <div class="hero-badge" aria-hidden="true">
                        <svg id="heroIcon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
                            <path d="M12 3v18M17 7.5c0-1.66-2.24-3-5-3s-5 1.34-5 3 2.24 3 5 3 5 1.34 5 3-2.24 3-5 3-5-1.34-5-3" stroke-linecap="round"/>
                        </svg>
                    </div>
                </section>

                <!-- MÓDULO: INTERÉS SIMPLE -->
                <section class="module-view active" data-view="simple">
                    <div class="workspace">
                        <article class="panel form-panel" id="simpleFormPanel">
                            <div class="panel-head">
                                <div class="panel-title">
                                    <div class="panel-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <path d="M5 12h14M12 5v14" stroke-linecap="round"/>
                                        </svg>
                                    </div>
                                    <div>
                                        <h3>Datos de inversión</h3>
                                        <p>Complete los valores para realizar la simulación.</p>
                                    </div>
                                </div>
                                <span class="module-chip">Cálculo lineal</span>
                            </div>

                            <div class="form-grid">
                                <div class="field-group full">
                                    <label for="simpleCapital">Capital inicial</label>
                                    <div class="field-shell">
                                        <span class="field-prefix">$</span>
                                        <input id="simpleCapital" type="number" min="0" step="100" inputmode="decimal" />
                                        <span class="field-suffix">USD</span>
                                    </div>
                                    <div class="helper-text" id="simpleCapitalHelp">Monto que se invertirá inicialmente.</div>
                                </div>

                                <div class="field-group">
                                    <label for="simpleRate">Tasa anual</label>
                                    <div class="field-shell">
                                        <input id="simpleRate" type="number" min="0" step="0.5" inputmode="decimal" />
                                        <span class="field-suffix">%</span>
                                    </div>
                                    <div class="helper-text" id="simpleRateHelp">Porcentaje anual esperado.</div>
                                </div>

                                <div class="field-group">
                                    <label for="simpleMonths">Tiempo</label>
                                    <div class="field-shell">
                                        <input id="simpleMonths" type="number" min="1" step="1" inputmode="numeric" />
                                        <span class="field-suffix">meses</span>
                                    </div>
                                    <div class="helper-text" id="simpleMonthsHelp">Duración mínima: 1 mes.</div>
                                </div>
                            </div>

                            <div class="action-row">
                                <button class="btn btn-primary calculate-button" data-action="calculate-simple" type="button">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 19V9m6 10V5m6 14v-7m4 7H2" stroke-linecap="round"/>
                                    </svg>
                                    Calcular interés simple
                                </button>
                                <button class="btn btn-secondary" data-action="clear-simple" type="button">
                                    Limpiar módulo
                                </button>
                            </div>
                        </article>

                        <aside class="panel result-panel">
                            <div class="result-label">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" stroke-linecap="round"/>
                                </svg>
                                Resultado estimado
                            </div>

                            <div class="result-main">
                                <div class="caption">Monto final</div>
                                <div class="value" id="simpleMainResult">$0.00</div>
                            </div>

                            <div class="result-grid">
                                <div class="result-item">
                                    <span>Capital inicial</span>
                                    <strong id="simpleCapitalResult">$0.00</strong>
                                </div>
                                <div class="result-item">
                                    <span>Interés generado</span>
                                    <strong id="simpleInterestResult">$0.00</strong>
                                </div>
                                <div class="result-item">
                                    <span>Tasa anual</span>
                                    <strong id="simpleRateResult">0.00%</strong>
                                </div>
                                <div class="result-item">
                                    <span>Plazo</span>
                                    <strong id="simpleTimeResult">0 meses</strong>
                                </div>
                            </div>

                            <div class="meter-wrap">
                                <div class="meter-head">
                                    <span>Proporción del rendimiento</span>
                                    <strong id="simpleMeterLabel">0%</strong>
                                </div>
                                <div class="meter">
                                    <div class="meter-fill" id="simpleMeter"></div>
                                </div>
                            </div>
                        </aside>
                    </div>
                </section>

                <!-- MÓDULO: INTERÉS COMPUESTO -->
                <section class="module-view" data-view="compound">
                    <div class="workspace">
                        <article class="panel form-panel" id="compoundFormPanel">
                            <div class="panel-head">
                                <div class="panel-title">
                                    <div class="panel-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <path d="M4 16l5-5 4 4 7-8" stroke-linecap="round" stroke-linejoin="round"/>
                                            <path d="M14 7h6v6" stroke-linecap="round" stroke-linejoin="round"/>
                                        </svg>
                                    </div>
                                    <div>
                                        <h3>Datos de crecimiento</h3>
                                        <p>El rendimiento se reinvierte al finalizar cada año.</p>
                                    </div>
                                </div>
                                <span class="module-chip">Capitalización anual</span>
                            </div>

                            <div class="form-grid">
                                <div class="field-group full">
                                    <label for="compoundCapital">Capital inicial</label>
                                    <div class="field-shell">
                                        <span class="field-prefix">$</span>
                                        <input id="compoundCapital" type="number" min="0" step="100" inputmode="decimal" />
                                        <span class="field-suffix">USD</span>
                                    </div>
                                    <div class="helper-text" id="compoundCapitalHelp">Monto base de la inversión.</div>
                                </div>

                                <div class="field-group">
                                    <label for="compoundRate">Tasa anual</label>
                                    <div class="field-shell">
                                        <input id="compoundRate" type="number" min="0" step="0.5" inputmode="decimal" />
                                        <span class="field-suffix">%</span>
                                    </div>
                                    <div class="helper-text" id="compoundRateHelp">Tasa utilizada en cada periodo anual.</div>
                                </div>

                                <div class="field-group">
                                    <label for="compoundYears">Tiempo</label>
                                    <div class="field-shell">
                                        <input id="compoundYears" type="number" min="1" step="1" inputmode="numeric" />
                                        <span class="field-suffix">años</span>
                                    </div>
                                    <div class="helper-text" id="compoundYearsHelp">Duración mínima: 1 año.</div>
                                </div>
                            </div>

                            <div class="action-row">
                                <button class="btn btn-primary calculate-button" data-action="calculate-compound" type="button">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 16l5-5 4 4 7-8" stroke-linecap="round" stroke-linejoin="round"/>
                                        <path d="M14 7h6v6" stroke-linecap="round" stroke-linejoin="round"/>
                                    </svg>
                                    Calcular interés compuesto
                                </button>
                                <button class="btn btn-secondary" data-action="clear-compound" type="button">
                                    Limpiar módulo
                                </button>
                            </div>
                        </article>

                        <aside class="panel result-panel">
                            <div class="result-label">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M3 17l6-6 4 4 8-9" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                                Proyección acumulada
                            </div>

                            <div class="result-main">
                                <div class="caption">Monto final</div>
                                <div class="value" id="compoundMainResult">$0.00</div>
                            </div>

                            <div class="result-grid">
                                <div class="result-item">
                                    <span>Capital inicial</span>
                                    <strong id="compoundCapitalResult">$0.00</strong>
                                </div>
                                <div class="result-item">
                                    <span>Interés generado</span>
                                    <strong id="compoundInterestResult">$0.00</strong>
                                </div>
                                <div class="result-item">
                                    <span>Tasa anual</span>
                                    <strong id="compoundRateResult">0.00%</strong>
                                </div>
                                <div class="result-item">
                                    <span>Plazo</span>
                                    <strong id="compoundTimeResult">0 años</strong>
                                </div>
                            </div>

                            <div class="meter-wrap">
                                <div class="meter-head">
                                    <span>Proporción del rendimiento</span>
                                    <strong id="compoundMeterLabel">0%</strong>
                                </div>
                                <div class="meter">
                                    <div class="meter-fill" id="compoundMeter"></div>
                                </div>
                            </div>
                        </aside>
                    </div>
                </section>

                <!-- MÓDULO: PAGO MENSUAL -->
                <section class="module-view" data-view="loan">
                    <div class="workspace">
                        <article class="panel form-panel" id="loanFormPanel">
                            <div class="panel-head">
                                <div class="panel-title">
                                    <div class="panel-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <rect x="3" y="5" width="18" height="14" rx="3"/>
                                            <path d="M3 10h18M7 15h3" stroke-linecap="round"/>
                                        </svg>
                                    </div>
                                    <div>
                                        <h3>Datos del préstamo</h3>
                                        <p>Calcule la cuota bajo el sistema de pagos iguales.</p>
                                    </div>
                                </div>
                                <span class="module-chip">Cuota fija mensual</span>
                            </div>

                            <div class="form-grid">
                                <div class="field-group full">
                                    <label for="loanAmount">Monto del préstamo</label>
                                    <div class="field-shell">
                                        <span class="field-prefix">$</span>
                                        <input id="loanAmount" type="number" min="0.01" step="500" inputmode="decimal" />
                                        <span class="field-suffix">USD</span>
                                    </div>
                                    <div class="helper-text" id="loanAmountHelp">Capital que será financiado.</div>
                                </div>

                                <div class="field-group">
                                    <label for="loanRate">Tasa anual</label>
                                    <div class="field-shell">
                                        <input id="loanRate" type="number" min="0" step="0.5" inputmode="decimal" />
                                        <span class="field-suffix">%</span>
                                    </div>
                                    <div class="helper-text" id="loanRateHelp">Se convertirá a tasa mensual.</div>
                                </div>

                                <div class="field-group">
                                    <label for="loanYears">Plazo</label>
                                    <div class="field-shell">
                                        <input id="loanYears" type="number" min="1" step="1" inputmode="numeric" />
                                        <span class="field-suffix">años</span>
                                    </div>
                                    <div class="helper-text" id="loanYearsHelp">Duración mínima: 1 año.</div>
                                </div>
                            </div>

                            <div class="action-row">
                                <button class="btn btn-primary calculate-button" data-action="calculate-loan" type="button">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <rect x="3" y="5" width="18" height="14" rx="3"/>
                                        <path d="M3 10h18M7 15h3" stroke-linecap="round"/>
                                    </svg>
                                    Calcular pago mensual
                                </button>
                                <button class="btn btn-secondary" data-action="clear-loan" type="button">
                                    Limpiar módulo
                                </button>
                            </div>
                        </article>

                        <aside class="panel result-panel">
                            <div class="result-label">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M12 2v20M17 6H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" stroke-linecap="round"/>
                                </svg>
                                Obligación estimada
                            </div>

                            <div class="result-main">
                                <div class="caption">Cuota mensual</div>
                                <div class="value" id="loanMainResult">$0.00</div>
                            </div>

                            <div class="result-grid">
                                <div class="result-item">
                                    <span>Monto solicitado</span>
                                    <strong id="loanAmountResult">$0.00</strong>
                                </div>
                                <div class="result-item">
                                    <span>Total pagado</span>
                                    <strong id="loanTotalResult">$0.00</strong>
                                </div>
                                <div class="result-item">
                                    <span>Total intereses</span>
                                    <strong id="loanInterestResult">$0.00</strong>
                                </div>
                                <div class="result-item">
                                    <span>Número de cuotas</span>
                                    <strong id="loanPaymentsResult">0</strong>
                                </div>
                            </div>

                            <div class="meter-wrap">
                                <div class="meter-head">
                                    <span>Intereses sobre el total pagado</span>
                                    <strong id="loanMeterLabel">0%</strong>
                                </div>
                                <div class="meter">
                                    <div class="meter-fill" id="loanMeter"></div>
                                </div>
                            </div>
                        </aside>
                    </div>
                </section>

                <section class="info-strip">
                    <article class="info-card">
                        <div class="info-icon">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="m5 12 4 4L19 6" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <div>
                            <strong>Validación inmediata</strong>
                            <p>Los campos se revisan antes de ejecutar cualquier cálculo.</p>
                        </div>
                    </article>

                    <article class="info-card">
                        <div class="info-icon blue">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                                <path d="m9 12 2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <div>
                            <strong>Datos persistentes</strong>
                            <p>Cambie de módulo sin perder los valores previamente ingresados.</p>
                        </div>
                    </article>

                    <article class="info-card">
                        <div class="info-icon amber">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M12 3v18M17 7.5c0-1.66-2.24-3-5-3s-5 1.34-5 3 2.24 3 5 3 5 1.34 5 3-2.24 3-5 3-5-1.34-5-3" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div>
                            <strong>Resultados claros</strong>
                            <p>Las cifras se presentan con formato monetario y métricas relevantes.</p>
                        </div>
                    </article>
                </section>
            </main>
        </div>
    </div>

    <div class="toast-stack" id="toastStack" aria-live="polite"></div>

    <div class="modal-backdrop" id="stateModal" role="dialog" aria-modal="true" aria-labelledby="stateModalTitle">
        <div class="modal">
            <div class="modal-head">
                <div>
                    <h3 id="stateModalTitle">Datos guardados en la sesión</h3>
                </div>
                <button class="icon-button" id="closeStateButton" type="button" aria-label="Cerrar">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M18 6 6 18M6 6l12 12" stroke-linecap="round"/>
                    </svg>
                </button>
            </div>

            <div class="modal-body">
                <div class="state-grid" id="stateGrid"></div>
                <div class="modal-actions">
                    <button class="btn btn-secondary" id="closeStateSecondary" type="button">Cerrar</button>
                    <button class="btn danger-button" id="resetAllButton" type="button">Restablecer toda la aplicación</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        "use strict";

        // ====================================================
        // 1. ESTADO DE LA APLICACIÓN
        // ====================================================

        const STORAGE_KEY = "finanzas_corporativas_monolitica_v1";

        const DEFAULT_STATE = {
            activeModule: "simple",
            simple: {
                capital: 1000,
                rate: 5,
                months: 12,
                result: null
            },
            compound: {
                capital: 1000,
                rate: 5,
                years: 5,
                result: null
            },
            loan: {
                amount: 10000,
                rate: 10,
                years: 3,
                result: null
            }
        };

        const MODULE_CONTENT = {
            simple: {
                eyebrow: "Simulador financiero",
                title: "Interés simple",
                description: "Calcule el rendimiento generado por un capital cuando el interés no se acumula sobre periodos anteriores.",
                icon: '<path d="M12 3v18M17 7.5c0-1.66-2.24-3-5-3s-5 1.34-5 3 2.24 3 5 3 5 1.34 5 3-2.24 3-5 3-5-1.34-5-3" stroke-linecap="round"/>'
            },
            compound: {
                eyebrow: "Proyección de inversión",
                title: "Interés compuesto",
                description: "Proyecte el crecimiento de una inversión cuando cada rendimiento se incorpora al capital del siguiente periodo.",
                icon: '<path d="M4 16l5-5 4 4 7-8" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 7h6v6" stroke-linecap="round" stroke-linejoin="round"/>'
            },
            loan: {
                eyebrow: "Planificación crediticia",
                title: "Pago mensual",
                description: "Estime la cuota fija, el total pagado y los intereses de un préstamo con pagos mensuales constantes.",
                icon: '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M3 10h18M7 15h3" stroke-linecap="round"/>'
            }
        };

        let state = loadState();


        // ====================================================
        // 2. UTILIDADES GENERALES
        // ====================================================

        function deepClone(value) {
            return JSON.parse(JSON.stringify(value));
        }

        function mergeState(base, saved) {
            return {
                ...base,
                ...saved,
                simple: { ...base.simple, ...(saved?.simple || {}) },
                compound: { ...base.compound, ...(saved?.compound || {}) },
                loan: { ...base.loan, ...(saved?.loan || {}) }
            };
        }

        function loadState() {
            try {
                const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
                return saved ? mergeState(deepClone(DEFAULT_STATE), saved) : deepClone(DEFAULT_STATE);
            } catch (error) {
                console.warn("No se pudo leer el estado guardado:", error);
                return deepClone(DEFAULT_STATE);
            }
        }

        function saveState() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
            } catch (error) {
                console.warn("No se pudo guardar el estado:", error);
            }
        }

        function byId(id) {
            return document.getElementById(id);
        }

        function toNumber(value) {
            if (value === "" || value === null || value === undefined) return NaN;
            return Number(value);
        }

        function formatMoney(value) {
            const safeValue = Number.isFinite(value) ? value : 0;
            return new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD",
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(safeValue);
        }

        function formatPercent(value) {
            const safeValue = Number.isFinite(value) ? value : 0;
            return `${safeValue.toLocaleString("es-PE", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            })}%`;
        }

        function clamp(value, min, max) {
            return Math.min(Math.max(value, min), max);
        }

        function animateValue(element) {
            element.classList.remove("pop");
            void element.offsetWidth;
            element.classList.add("pop");
        }

        function showToast(message, type = "success") {
            const toast = document.createElement("div");
            toast.className = `toast ${type === "error" ? "error" : ""}`;
            toast.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    ${type === "error"
                        ? '<circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01" stroke-linecap="round"/>'
                        : '<circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9" stroke-linecap="round" stroke-linejoin="round"/>'}
                </svg>
                <span>${message}</span>
            `;

            byId("toastStack").appendChild(toast);

            setTimeout(() => toast.classList.add("hide"), 2800);
            setTimeout(() => toast.remove(), 3100);
        }

        function addRipple(button, event) {
            const rect = button.getBoundingClientRect();
            button.style.setProperty("--ripple-x", `${event.clientX - rect.left}px`);
            button.style.setProperty("--ripple-y", `${event.clientY - rect.top}px`);
            button.classList.remove("ripple");
            void button.offsetWidth;
            button.classList.add("ripple");
            setTimeout(() => button.classList.remove("ripple"), 550);
        }

        function triggerShake(element) {
            element.classList.remove("shake");
            void element.offsetWidth;
            element.classList.add("shake");
        }

        function requestFrameHeight() {
            const height = Math.max(
                document.documentElement.scrollHeight,
                document.body.scrollHeight
            );

            window.parent.postMessage(
                {
                    isStreamlitMessage: true,
                    type: "streamlit:setFrameHeight",
                    height: height + 12
                },
                "*"
            );
        }


        // ====================================================
        // 3. NAVEGACIÓN ENTRE MÓDULOS
        // ====================================================

        function switchModule(moduleName) {
            if (!MODULE_CONTENT[moduleName]) return;

            state.activeModule = moduleName;
            saveState();

            document.querySelectorAll(".nav-button").forEach(button => {
                button.classList.toggle("active", button.dataset.module === moduleName);
            });

            document.querySelectorAll(".module-view").forEach(view => {
                view.classList.toggle("active", view.dataset.view === moduleName);
            });

            const content = MODULE_CONTENT[moduleName];
            byId("heroEyebrow").textContent = content.eyebrow;
            byId("heroTitle").textContent = content.title;
            byId("heroDescription").textContent = content.description;
            byId("heroIcon").innerHTML = content.icon;

            requestAnimationFrame(requestFrameHeight);
        }


        // ====================================================
        // 4. VALIDACIONES
        // ====================================================

        function resetHelper(helperId, defaultMessage) {
            const helper = byId(helperId);
            helper.textContent = defaultMessage;
            helper.classList.remove("error");
        }

        function setFieldError(helperId, message) {
            const helper = byId(helperId);
            helper.textContent = message;
            helper.classList.add("error");
        }

        function validatePositive(value, helperId, fieldLabel, allowZero = false) {
            const minimumValid = allowZero ? value >= 0 : value > 0;

            if (!Number.isFinite(value)) {
                setFieldError(helperId, `Ingrese un valor válido para ${fieldLabel}.`);
                return false;
            }

            if (!minimumValid) {
                setFieldError(
                    helperId,
                    allowZero
                        ? `${fieldLabel} no puede ser negativo.`
                        : `${fieldLabel} debe ser mayor que cero.`
                );
                return false;
            }

            return true;
        }


        // ====================================================
        // 5. CÁLCULOS FINANCIEROS
        // ====================================================

        function calculateSimple() {
            resetHelper("simpleCapitalHelp", "Monto que se invertirá inicialmente.");
            resetHelper("simpleRateHelp", "Porcentaje anual esperado.");
            resetHelper("simpleMonthsHelp", "Duración mínima: 1 mes.");

            const capital = toNumber(byId("simpleCapital").value);
            const rate = toNumber(byId("simpleRate").value);
            const months = toNumber(byId("simpleMonths").value);

            const validations = [
                validatePositive(capital, "simpleCapitalHelp", "el capital"),
                validatePositive(rate, "simpleRateHelp", "la tasa", true),
                validatePositive(months, "simpleMonthsHelp", "el tiempo")
            ];

            if (validations.includes(false)) {
                triggerShake(byId("simpleFormPanel"));
                showToast("Revise los valores ingresados.", "error");
                return;
            }

            const interest = capital * (rate / 100) * (months / 12);
            const finalAmount = capital + interest;

            state.simple = {
                capital,
                rate,
                months,
                result: { interest, finalAmount }
            };
            saveState();
            renderSimpleResult();
            showToast("Interés simple calculado correctamente.");
        }

        function calculateCompound() {
            resetHelper("compoundCapitalHelp", "Monto base de la inversión.");
            resetHelper("compoundRateHelp", "Tasa utilizada en cada periodo anual.");
            resetHelper("compoundYearsHelp", "Duración mínima: 1 año.");

            const capital = toNumber(byId("compoundCapital").value);
            const rate = toNumber(byId("compoundRate").value);
            const years = toNumber(byId("compoundYears").value);

            const validations = [
                validatePositive(capital, "compoundCapitalHelp", "el capital"),
                validatePositive(rate, "compoundRateHelp", "la tasa", true),
                validatePositive(years, "compoundYearsHelp", "el tiempo")
            ];

            if (validations.includes(false)) {
                triggerShake(byId("compoundFormPanel"));
                showToast("Revise los valores ingresados.", "error");
                return;
            }

            const finalAmount = capital * Math.pow(1 + rate / 100, years);
            const interest = finalAmount - capital;

            state.compound = {
                capital,
                rate,
                years,
                result: { interest, finalAmount }
            };
            saveState();
            renderCompoundResult();
            showToast("Interés compuesto calculado correctamente.");
        }

        function calculateLoan() {
            resetHelper("loanAmountHelp", "Capital que será financiado.");
            resetHelper("loanRateHelp", "Se convertirá a tasa mensual.");
            resetHelper("loanYearsHelp", "Duración mínima: 1 año.");

            const amount = toNumber(byId("loanAmount").value);
            const rate = toNumber(byId("loanRate").value);
            const years = toNumber(byId("loanYears").value);

            const validations = [
                validatePositive(amount, "loanAmountHelp", "el monto"),
                validatePositive(rate, "loanRateHelp", "la tasa", true),
                validatePositive(years, "loanYearsHelp", "el plazo")
            ];

            if (validations.includes(false)) {
                triggerShake(byId("loanFormPanel"));
                showToast("Revise los valores ingresados.", "error");
                return;
            }

            const payments = Math.round(years * 12);
            const monthlyRate = rate / 100 / 12;

            let payment;
            if (monthlyRate === 0) {
                payment = amount / payments;
            } else {
                payment = amount * (
                    monthlyRate * Math.pow(1 + monthlyRate, payments)
                ) / (
                    Math.pow(1 + monthlyRate, payments) - 1
                );
            }

            const totalPaid = payment * payments;
            const totalInterest = totalPaid - amount;

            state.loan = {
                amount,
                rate,
                years,
                result: { payment, totalPaid, totalInterest, payments }
            };
            saveState();
            renderLoanResult();
            showToast("Pago mensual calculado correctamente.");
        }


        // ====================================================
        // 6. RENDERIZADO DE RESULTADOS
        // ====================================================

        function renderSimpleResult() {
            const data = state.simple;
            const result = data.result;

            byId("simpleCapitalResult").textContent = formatMoney(data.capital);
            byId("simpleRateResult").textContent = formatPercent(data.rate);
            byId("simpleTimeResult").textContent = `${data.months} ${data.months === 1 ? "mes" : "meses"}`;

            if (!result) {
                byId("simpleMainResult").textContent = "$0.00";
                byId("simpleInterestResult").textContent = "$0.00";
                byId("simpleMeter").style.width = "0%";
                byId("simpleMeterLabel").textContent = "0%";
                return;
            }

            byId("simpleMainResult").textContent = formatMoney(result.finalAmount);
            byId("simpleInterestResult").textContent = formatMoney(result.interest);

            const proportion = result.finalAmount > 0
                ? (result.interest / result.finalAmount) * 100
                : 0;

            byId("simpleMeter").style.width = `${clamp(proportion, 0, 100)}%`;
            byId("simpleMeterLabel").textContent = formatPercent(proportion);
            animateValue(byId("simpleMainResult"));
        }

        function renderCompoundResult() {
            const data = state.compound;
            const result = data.result;

            byId("compoundCapitalResult").textContent = formatMoney(data.capital);
            byId("compoundRateResult").textContent = formatPercent(data.rate);
            byId("compoundTimeResult").textContent = `${data.years} ${data.years === 1 ? "año" : "años"}`;

            if (!result) {
                byId("compoundMainResult").textContent = "$0.00";
                byId("compoundInterestResult").textContent = "$0.00";
                byId("compoundMeter").style.width = "0%";
                byId("compoundMeterLabel").textContent = "0%";
                return;
            }

            byId("compoundMainResult").textContent = formatMoney(result.finalAmount);
            byId("compoundInterestResult").textContent = formatMoney(result.interest);

            const proportion = result.finalAmount > 0
                ? (result.interest / result.finalAmount) * 100
                : 0;

            byId("compoundMeter").style.width = `${clamp(proportion, 0, 100)}%`;
            byId("compoundMeterLabel").textContent = formatPercent(proportion);
            animateValue(byId("compoundMainResult"));
        }

        function renderLoanResult() {
            const data = state.loan;
            const result = data.result;

            byId("loanAmountResult").textContent = formatMoney(data.amount);

            if (!result) {
                byId("loanMainResult").textContent = "$0.00";
                byId("loanTotalResult").textContent = "$0.00";
                byId("loanInterestResult").textContent = "$0.00";
                byId("loanPaymentsResult").textContent = "0";
                byId("loanMeter").style.width = "0%";
                byId("loanMeterLabel").textContent = "0%";
                return;
            }

            byId("loanMainResult").textContent = formatMoney(result.payment);
            byId("loanTotalResult").textContent = formatMoney(result.totalPaid);
            byId("loanInterestResult").textContent = formatMoney(result.totalInterest);
            byId("loanPaymentsResult").textContent = result.payments.toLocaleString("es-PE");

            const proportion = result.totalPaid > 0
                ? (result.totalInterest / result.totalPaid) * 100
                : 0;

            byId("loanMeter").style.width = `${clamp(proportion, 0, 100)}%`;
            byId("loanMeterLabel").textContent = formatPercent(proportion);
            animateValue(byId("loanMainResult"));
        }


        // ====================================================
        // 7. SINCRONIZACIÓN DE CAMPOS Y LIMPIEZA
        // ====================================================

        function populateInputs() {
            byId("simpleCapital").value = state.simple.capital;
            byId("simpleRate").value = state.simple.rate;
            byId("simpleMonths").value = state.simple.months;

            byId("compoundCapital").value = state.compound.capital;
            byId("compoundRate").value = state.compound.rate;
            byId("compoundYears").value = state.compound.years;

            byId("loanAmount").value = state.loan.amount;
            byId("loanRate").value = state.loan.rate;
            byId("loanYears").value = state.loan.years;
        }

        function persistInputChanges() {
            state.simple.capital = toNumber(byId("simpleCapital").value);
            state.simple.rate = toNumber(byId("simpleRate").value);
            state.simple.months = toNumber(byId("simpleMonths").value);

            state.compound.capital = toNumber(byId("compoundCapital").value);
            state.compound.rate = toNumber(byId("compoundRate").value);
            state.compound.years = toNumber(byId("compoundYears").value);

            state.loan.amount = toNumber(byId("loanAmount").value);
            state.loan.rate = toNumber(byId("loanRate").value);
            state.loan.years = toNumber(byId("loanYears").value);

            saveState();
        }

        function clearModule(moduleName) {
            state[moduleName] = deepClone(DEFAULT_STATE[moduleName]);
            saveState();
            populateInputs();

            if (moduleName === "simple") renderSimpleResult();
            if (moduleName === "compound") renderCompoundResult();
            if (moduleName === "loan") renderLoanResult();

            showToast("El módulo fue restablecido.");
        }

        function resetAll() {
            state = deepClone(DEFAULT_STATE);
            saveState();
            populateInputs();
            renderSimpleResult();
            renderCompoundResult();
            renderLoanResult();
            switchModule("simple");
            closeStateModal();
            showToast("La aplicación fue restablecida.");
        }


        // ====================================================
        // 8. MODAL DE DATOS GUARDADOS
        // ====================================================

        function stateRow(label, value) {
            return `<div class="state-row"><span>${label}</span><strong>${value}</strong></div>`;
        }

        function renderStateModal() {
            const simpleResult = state.simple.result;
            const compoundResult = state.compound.result;
            const loanResult = state.loan.result;

            byId("stateGrid").innerHTML = `
                <article class="state-card">
                    <h4>Interés simple</h4>
                    ${stateRow("Capital", formatMoney(state.simple.capital))}
                    ${stateRow("Tasa", formatPercent(state.simple.rate))}
                    ${stateRow("Meses", state.simple.months)}
                    ${stateRow("Monto final", simpleResult ? formatMoney(simpleResult.finalAmount) : "Sin calcular")}
                </article>

                <article class="state-card">
                    <h4>Interés compuesto</h4>
                    ${stateRow("Capital", formatMoney(state.compound.capital))}
                    ${stateRow("Tasa", formatPercent(state.compound.rate))}
                    ${stateRow("Años", state.compound.years)}
                    ${stateRow("Monto final", compoundResult ? formatMoney(compoundResult.finalAmount) : "Sin calcular")}
                </article>

                <article class="state-card">
                    <h4>Pago mensual</h4>
                    ${stateRow("Préstamo", formatMoney(state.loan.amount))}
                    ${stateRow("Tasa", formatPercent(state.loan.rate))}
                    ${stateRow("Años", state.loan.years)}
                    ${stateRow("Cuota", loanResult ? formatMoney(loanResult.payment) : "Sin calcular")}
                </article>
            `;
        }

        function openStateModal() {
            persistInputChanges();
            renderStateModal();
            byId("stateModal").classList.add("open");
            document.body.style.overflow = "hidden";
        }

        function closeStateModal() {
            byId("stateModal").classList.remove("open");
            document.body.style.overflow = "";
        }


        // ====================================================
        // 9. EVENTOS DE LA INTERFAZ
        // ====================================================

        document.querySelectorAll(".nav-button").forEach(button => {
            button.addEventListener("click", () => switchModule(button.dataset.module));
        });

        document.querySelectorAll(".btn").forEach(button => {
            button.addEventListener("click", event => addRipple(button, event));
        });

        document.querySelectorAll("input[type='number']").forEach(input => {
            input.addEventListener("input", persistInputChanges);
            input.addEventListener("keydown", event => {
                if (event.key !== "Enter") return;

                const activeModule = state.activeModule;
                if (activeModule === "simple") calculateSimple();
                if (activeModule === "compound") calculateCompound();
                if (activeModule === "loan") calculateLoan();
            });
        });

        document.addEventListener("click", event => {
            const actionButton = event.target.closest("[data-action]");
            if (!actionButton) return;

            const action = actionButton.dataset.action;

            if (action === "calculate-simple") calculateSimple();
            if (action === "calculate-compound") calculateCompound();
            if (action === "calculate-loan") calculateLoan();
            if (action === "clear-simple") clearModule("simple");
            if (action === "clear-compound") clearModule("compound");
            if (action === "clear-loan") clearModule("loan");
        });

        byId("openStateButton").addEventListener("click", openStateModal);
        byId("closeStateButton").addEventListener("click", closeStateModal);
        byId("closeStateSecondary").addEventListener("click", closeStateModal);
        byId("resetAllButton").addEventListener("click", resetAll);

        byId("stateModal").addEventListener("click", event => {
            if (event.target === byId("stateModal")) closeStateModal();
        });

        document.addEventListener("keydown", event => {
            if (event.key === "Escape") closeStateModal();
        });


        // ====================================================
        // 10. INICIALIZACIÓN
        // ====================================================

        populateInputs();
        renderSimpleResult();
        renderCompoundResult();
        renderLoanResult();
        switchModule(state.activeModule || "simple");

        const resizeObserver = new ResizeObserver(requestFrameHeight);
        resizeObserver.observe(document.body);
        window.addEventListener("load", requestFrameHeight);
        window.addEventListener("resize", requestFrameHeight);
        setTimeout(requestFrameHeight, 120);
    </script>
</body>
</html>
"""


# La aplicación completa se renderiza como un único componente web.
components.html(
    app_html,
    height=1180,
    scrolling=True,
)
