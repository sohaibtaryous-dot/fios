"""
ui.py
Composants d'interface Streamlit pour Packing List Extractor Pro.
CSS, cartes de stats, tableaux HTML par client, total général.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime

import streamlit as st

from export_engine import calculate_summary, fmt_num


# ─────────────────────────────────────────────────────────────
#  CSS GLOBAL
# ─────────────────────────────────────────────────────────────

def inject_css() -> None:
    st.markdown(
        """
<style>
/* ── Variables ── */
:root {
  --pri:  #1a3a5c;
  --sec:  #2e6da4;
  --acc:  #e67e22;
  --ok:   #27ae60;
  --err:  #e74c3c;
  --bg:   #eef2f7;
  --card: #ffffff;
  --lgt:  #f0f5fb;
  --bdr:  #c8d8ea;
  --gray: #6c757d;
  --gt-bg:#fff3cd;
  --gt-b: #f39c12;
}

/* ── Layout ── */
.block-container { max-width: 1400px !important; padding: 1.5rem 2rem !important; }
header[data-testid="stHeader"] { background: var(--pri) !important; }

/* ── Hero ── */
.hero-banner {
  background: linear-gradient(135deg, var(--pri) 0%, var(--sec) 100%);
  border-radius: 14px;
  padding: 2rem 2.5rem;
  margin-bottom: 1.5rem;
  color: white;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.hero-icon { font-size: 3rem; }
.hero-title { font-size: 1.6rem; font-weight: 700; margin-bottom: 0.3rem; }
.hero-sub   { font-size: 0.92rem; opacity: 0.78; }

/* ── Stat cards ── */
.stats-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.9rem;
  margin: 1.2rem 0;
}
.stat-card {
  background: var(--card);
  border-radius: 12px;
  padding: 1.1rem 1rem;
  text-align: center;
  border-top: 3px solid var(--sec);
  box-shadow: 0 3px 14px rgba(26,58,92,.09);
}
.stat-v { font-size: 1.65rem; font-weight: 700; color: var(--pri); display: block; }
.stat-l { font-size: 0.73rem; color: var(--gray); text-transform: uppercase; letter-spacing: .05em; }

/* ── Section client ── */
.client-section { margin-bottom: 1.6rem; }
.client-header {
  background: var(--sec);
  color: white;
  padding: 0.75rem 1.2rem;
  border-radius: 10px 10px 0 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-weight: 700;
  font-size: 0.95rem;
}
.client-badge {
  background: white;
  color: var(--sec);
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  font-size: 0.76rem;
  font-weight: 700;
}

/* ── Tableau résultat ── */
.rt-wrap {
  background: var(--card);
  border-radius: 0 0 10px 10px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(26,58,92,.09);
  overflow-x: auto;
}
table.rt {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.84rem;
  font-family: 'Inter', sans-serif;
}
table.rt thead th {
  background: var(--lgt);
  padding: 0.65rem 0.9rem;
  text-align: left;
  font-size: 0.74rem;
  font-weight: 700;
  color: var(--pri);
  border-bottom: 2px solid var(--bdr);
  text-transform: uppercase;
  letter-spacing: .04em;
  white-space: nowrap;
}
table.rt thead th.r { text-align: right; }
table.rt tbody td {
  padding: 0.6rem 0.9rem;
  border-bottom: 1px solid var(--bdr);
  vertical-align: middle;
}
table.rt tbody td.r { text-align: right; font-variant-numeric: tabular-nums; }
table.rt tbody tr:nth-child(even) { background: #f5f9fd; }
table.rt tbody tr:hover { background: #e8f0fa; }

/* ── Total client ── */
table.rt .tr-total td {
  background: #d4e6f1;
  font-weight: 700;
  border-top: 2px solid var(--sec);
  color: var(--pri);
}

/* ── Total général ── */
.grand-total-section { margin-top: 0.5rem; }
.grand-total-header {
  background: #7d5a00;
  color: white;
  padding: 0.75rem 1.2rem;
  border-radius: 10px 10px 0 0;
  font-weight: 700;
  font-size: 0.95rem;
}
table.rt .tr-grand td {
  background: var(--gt-bg);
  font-weight: 700;
  border-top: 3px solid var(--gt-b);
  color: #7d5a00;
  font-size: 0.9rem;
}

/* ── Badge devise ── */
.cbadge {
  display: inline-block;
  padding: 0.08rem 0.38rem;
  border-radius: 4px;
  font-size: 0.72rem;
  font-weight: 700;
  background: var(--lgt);
  color: var(--sec);
  border: 1px solid var(--bdr);
  margin-left: 3px;
}

/* ── Alerte / avertissement ── */
.warn-chip {
  display: inline-block;
  background: #fff3cd;
  color: #7d5a00;
  border: 1px solid #f39c12;
  border-radius: 4px;
  padding: 0.1rem 0.45rem;
  font-size: 0.72rem;
  font-weight: 600;
  margin: 1px 2px;
}
.err-chip {
  background: #fde8e8;
  color: #c0392b;
  border-color: #e74c3c;
}

/* ── Séparateur ── */
.section-divider {
  border: none;
  border-top: 2px solid var(--bdr);
  margin: 1.2rem 0;
}

/* ── Bouton Streamlit override ── */
div[data-testid="stDownloadButton"] button,
div[data-testid="stButton"] > button[kind="primary"] {
  border-radius: 8px !important;
  font-weight: 600 !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
#  ENTÊTE
# ─────────────────────────────────────────────────────────────

def render_header() -> None:
    st.markdown(
        """
<div class="hero-banner">
  <div class="hero-icon">📦</div>
  <div>
    <div class="hero-title">Packing List Extractor Pro</div>
    <div class="hero-sub">
      Importez vos PDF Packing Lists — extraction automatique des données,
      regroupement par client, rapport bordereau PDF paysage.
    </div>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
#  CARTES DE STATISTIQUES
# ─────────────────────────────────────────────────────────────

def render_stat_cards(summary: dict) -> None:
    imp_str = " / ".join(
        f"{fmt_num(v)} {k}"
        for k, v in summary.get("total_importe_by_currency", {}).items()
    ) or "—"

    st.markdown(
        f"""
<div class="stats-row">
  <div class="stat-card">
    <span class="stat-v">{summary.get('total_files', summary.get('total_pls', 0))}</span>
    <span class="stat-l">PDF Traités</span>
  </div>
  <div class="stat-card">
    <span class="stat-v">{summary.get('total_clients', 0)}</span>
    <span class="stat-l">Clients</span>
  </div>
  <div class="stat-card">
    <span class="stat-v">{fmt_num(summary.get('total_bultos', 0), 0)}</span>
    <span class="stat-l">Total Bultos</span>
  </div>
  <div class="stat-card">
    <span class="stat-v">{fmt_num(summary.get('total_pb', 0))}</span>
    <span class="stat-l">Poids Brut (KG)</span>
  </div>
  <div class="stat-card">
    <span class="stat-v">{fmt_num(summary.get('total_pn', 0))}</span>
    <span class="stat-l">Poids Net (KG)</span>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
#  TABLEAU PAR CLIENT
# ─────────────────────────────────────────────────────────────

def _badges(warnings: list[str]) -> str:
    if not warnings:
        return ""
    return "".join(f'<span class="warn-chip">⚠ {w}</span>' for w in warnings)


def render_client_table(client_name: str, items: list[dict]) -> None:
    rows_html = ""
    c_bultos = 0
    c_pb     = 0.0
    c_pn     = 0.0
    c_imp: dict = defaultdict(float)

    for it in items:
        cur  = it.get("currency", "EUR")
        b    = it.get("bultos",     0)
        pb   = it.get("peso_bruto", 0.0)
        pn   = it.get("peso_neto",  0.0)
        imp  = it.get("importe",    0.0)
        warns = it.get("warnings", [])

        c_bultos += b
        c_pb     += pb
        c_pn     += pn
        c_imp[cur] += imp

        imp_cell = (
            f'{fmt_num(imp)} <span class="cbadge">{cur}</span>' if imp else "—"
        )
        warn_html = _badges(warns)
        err = it.get("error")
        if err:
            warn_html += f'<span class="warn-chip err-chip">❌ {err[:50]}</span>'

        rows_html += f"""
<tr>
  <td>{it.get('bl_number', 'N/A')}</td>
  <td>{it.get('filename', '')}<br>{warn_html}</td>
  <td>{it.get('date', '—')}</td>
  <td class="r">{fmt_num(b, 0)}</td>
  <td class="r">{fmt_num(pb)} KG</td>
  <td class="r">{fmt_num(pn)} KG</td>
  <td class="r">{imp_cell}</td>
</tr>
"""

    # Ligne total client
    imp_total = " | ".join(
        f'{fmt_num(v)} <span class="cbadge">{k}</span>'
        for k, v in c_imp.items()
    ) or "—"

    rows_html += f"""
<tr class="tr-total">
  <td colspan="3"><strong>TOTAL CLIENT : {client_name.upper()}</strong></td>
  <td class="r"><strong>{fmt_num(c_bultos, 0)}</strong></td>
  <td class="r"><strong>{fmt_num(c_pb)} KG</strong></td>
  <td class="r"><strong>{fmt_num(c_pn)} KG</strong></td>
  <td class="r"><strong>{imp_total}</strong></td>
</tr>
"""

    html = f"""
<div class="client-section">
  <div class="client-header">
    <span>👤 {client_name}</span>
    <span class="client-badge">{len(items)} Packing List{'s' if len(items) > 1 else ''}</span>
  </div>
  <div class="rt-wrap">
    <table class="rt">
      <thead>
        <tr>
          <th>N° BL / PKL</th>
          <th>Fichier PDF</th>
          <th>Date</th>
          <th class="r">Bultos (Colis)</th>
          <th class="r">Poids Brut</th>
          <th class="r">Poids Net</th>
          <th class="r">Importe HT</th>
        </tr>
      </thead>
      <tbody>
        {rows_html}
      </tbody>
    </table>
  </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  TOTAL GÉNÉRAL
# ─────────────────────────────────────────────────────────────

def render_grand_total(summary: dict) -> None:
    n_clients = summary.get("total_clients", 0)
    n_pls     = summary.get("total_pls", 0)
    bultos    = summary.get("total_bultos", 0)
    pb        = summary.get("total_pb", 0.0)
    pn        = summary.get("total_pn", 0.0)
    imp_dict  = summary.get("total_importe_by_currency", {})

    imp_str = " | ".join(
        f'{fmt_num(v)} <span class="cbadge" style="background:#fff3cd;color:#7d5a00;border-color:#f39c12">{k}</span>'
        for k, v in imp_dict.items()
    ) or "—"

    html = f"""
<div class="grand-total-section">
  <div class="grand-total-header">🏆 TOTAL GÉNÉRAL — TOUS LES PACKING LISTS</div>
  <div class="rt-wrap">
    <table class="rt">
      <thead>
        <tr>
          <th>—</th>
          <th class="r">CLIENTS</th>
          <th class="r">PACKING LISTS</th>
          <th class="r">TOTAL BULTOS</th>
          <th class="r">TOTAL POIDS BRUT</th>
          <th class="r">TOTAL POIDS NET</th>
          <th class="r">TOTAL IMPORTE HT</th>
        </tr>
      </thead>
      <tbody>
        <tr class="tr-grand">
          <td><strong>🏆 TOTAUX GÉNÉRAUX</strong></td>
          <td class="r"><strong>{n_clients}</strong></td>
          <td class="r"><strong>{n_pls}</strong></td>
          <td class="r"><strong>{fmt_num(bultos, 0)}</strong></td>
          <td class="r"><strong>{fmt_num(pb)} KG</strong></td>
          <td class="r"><strong>{fmt_num(pn)} KG</strong></td>
          <td class="r"><strong>{imp_str}</strong></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  PAGE RÉSULTATS COMPLÈTE
# ─────────────────────────────────────────────────────────────

def render_results(results: list[dict], grouped: dict) -> None:
    summary = calculate_summary(grouped)
    summary["total_files"] = len(results)

    # Avertissements globaux
    all_warns = [
        f"{r['filename']}: {', '.join(r['warnings'])}"
        for r in results
        if r.get("warnings")
    ]
    if all_warns:
        with st.expander(f"⚠️ {len(all_warns)} avertissement(s) — données partiellement extraites"):
            for w in all_warns:
                st.caption(w)

    # Stats
    render_stat_cards(summary)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### Détail par client")

    # Tableaux clients
    for client_name, items in grouped.items():
        render_client_table(client_name, items)

    # Total général
    render_grand_total(summary)


# ─────────────────────────────────────────────────────────────
#  INSTRUCTIONS D'UTILISATION
# ─────────────────────────────────────────────────────────────

def render_instructions() -> None:
    st.markdown(
        """
<div style="background:#f0f5fb;border-radius:10px;padding:1.2rem 1.5rem;
            border-left:4px solid #2e6da4;margin-bottom:1rem;">
  <strong style="color:#1a3a5c;">📋 Comment utiliser :</strong>
  <ol style="margin:0.5rem 0 0 1rem;color:#444;font-size:0.9rem;line-height:1.8">
    <li>Importez un ou plusieurs fichiers PDF Packing List</li>
    <li>Cliquez sur <strong>« Extraire & Analyser »</strong></li>
    <li>Vérifiez les données extraites par client</li>
    <li>Téléchargez le rapport PDF paysage avec bordereaux</li>
  </ol>
  <p style="margin-top:0.6rem;font-size:0.82rem;color:#666;">
    ⚡ L'extraction est automatique. Les données manquantes sont signalées par des avertissements.
  </p>
</div>
        """,
        unsafe_allow_html=True,
    )
