import time
import streamlit as st
from .sim import (
    BLADES, REGIMES, REGIME_LABEL,
    BO105_DISPLAY_RPM,
    default_adjustments,
    simulate_measurement
)
from .reports import legacy_results_text
from .plots import plot_track_marker, plot_track_graph, plot_polar
from .solver import all_ok, suggest_pitchlink, suggest_trimtabs, suggest_weight


def go(screen: str, **kwargs) -> None:
    st.session_state.vxp_screen = screen
    for k, v in kwargs.items():
        st.session_state[k] = v

def _win_begin(
    *,
    win_id: str,
    title: str,
    x: int,
    y: int,
    w: int,
    h: int,
    active: bool = True,
    modal: bool = False,
) -> None:
    """Dibuja una ventana estilo WinXP dentro del 'desktop' (MDI)."""
    cls = "vxp-win vxp-modal" if modal else "vxp-win"
    cap_cls = "active" if active else "inactive"
    st.markdown(
        (
            f"<div id='{win_id}' class='{cls}' style='left:{x}px; top:{y}px; width:{w}px; height:{h}px;'>"
            f"<div class='vxp-win-caption {cap_cls}'>"
            f"<div>{title}</div>"
            "<div class='vxp-closebox'>✕</div>"
            "</div>"
            "<div class='vxp-win-content'>"
        ),
        unsafe_allow_html=True,
    )


def _win_end() -> None:
    st.markdown("</div></div>", unsafe_allow_html=True)


def _dim() -> None:
    st.markdown("<div class='vxp-dim'></div>", unsafe_allow_html=True)


def _select_procedure_window(active: bool) -> None:
    # Ventana “Select Procedure” (siempre visible, como el original)
    _win_begin(
        win_id="proc",
        title="Select Procedure:",
        x=10,
        y=10,
        w=820,
        h=660,
        active=active,
    )
    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

    # Botones (imitación del original). Se pueden ajustar más adelante por aeronave.
    st.button("Aircraft Info", use_container_width=True, on_click=go, args=("aircraft_info",), key="proc_aircraft")
    st.button("Main Rotor Balance Run 1", use_container_width=True, on_click=go, args=("mr_menu",), key="proc_mr1")
    st.button("Tail Rotor Balance Run 1", use_container_width=True, on_click=go, args=("not_impl",), key="proc_tr1")
    st.button("T/R Driveshaft Balance Run 1", use_container_width=True, on_click=go, args=("not_impl",), key="proc_dr")
    st.button("Vibration Signatures", use_container_width=True, on_click=go, args=("not_impl",), key="proc_vib")
    st.button("Measurements Only", use_container_width=True, on_click=go, args=("not_impl",), key="proc_meas")
    st.button("Setup / Utilities", use_container_width=True, on_click=go, args=("not_impl",), key="proc_setup")

    _win_end()


def init_state() -> None:
    st.session_state.setdefault("vxp_screen", "home")
    st.session_state.setdefault("vxp_run", 1)
    st.session_state.setdefault("vxp_runs", {1: {}})
    st.session_state.setdefault("vxp_completed_by_run", {1: set()})
    st.session_state.setdefault("vxp_view_run", 1)

    st.session_state.setdefault("vxp_adjustments", default_adjustments())
    st.session_state.setdefault("vxp_pending_regime", None)
    st.session_state.setdefault("vxp_acq_in_progress", False)

    st.session_state.setdefault("vxp_applied_changes", {})  # run -> list[str]
    st.session_state.setdefault("vxp_edit_item", "pitch")
    st.session_state.setdefault("vxp_edit_values", {})


def current_run_data(run: int):
    return st.session_state.vxp_runs.setdefault(run, {})


def completed_set(run: int):
    return st.session_state.vxp_completed_by_run.setdefault(run, set())


def run_selector_inline() -> int:
    runs = sorted(st.session_state.vxp_runs.keys())
    cur = int(st.session_state.vxp_view_run)
    if cur not in runs:
        cur = runs[0]
        st.session_state.vxp_view_run = cur
    idx = runs.index(cur)
    r = st.selectbox("Run", runs, index=idx, key="run_selector")
    st.session_state.vxp_view_run = int(r)
    return int(r)


def screen_home():
    # Solo el “desktop”: la ventana principal ya está en app.py
    _select_procedure_window(active=True)


def screen_not_impl():
    _select_procedure_window(active=False)
    _win_begin(win_id="dlg_notimpl", title="VXP", x=220, y=180, w=520, h=260, active=True, modal=True)
    st.write("Solo se implementa **Main Rotor – Tracking & Balance (Option B)** para el BO105.")
    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("home",), key="notimpl_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_mr_menu():
    _select_procedure_window(active=False)

    _win_begin(
        win_id="mr_menu",
        title=f"Main Rotor Balance Run {st.session_state.vxp_run}",
        x=140,
        y=30,
        w=760,
        h=630,
        active=True,
    )

    st.markdown(
        "<div class='vxp-strip'><div>Tracking &amp; Balance – Option B</div>"
        f"<div>Run {st.session_state.vxp_run}</div></div>",
        unsafe_allow_html=True,
    )

    def btn(label: str, scr: str):
        st.button(label, use_container_width=True, on_click=go, args=(scr,), key=f"mr_{scr}")

    btn("COLLECT", "collect")
    btn("MEASUREMENTS LIST", "meas_list")
    btn("MEASUREMENTS GRAPH", "meas_graph")
    btn("SETTINGS", "settings")
    btn("SOLUTION", "solution")
    btn("NEXT RUN", "next_run_prompt")

    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("home",), key="mr_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_collect():
    _select_procedure_window(active=False)
    _win_begin(
        win_id="collect",
        title=f"RPM {BO105_DISPLAY_RPM:.1f}",
        x=220,
        y=70,
        w=660,
        h=560,
        active=True,
    )
    run = int(st.session_state.vxp_run)
    st.markdown(
        f"<div class='vxp-strip'><div>Main Rotor: Run {run} &nbsp;&nbsp; Day Mode</div><div>Run {run}</div></div>",
        unsafe_allow_html=True,
    )

    done = completed_set(run)
    for r in REGIMES:
        cols = st.columns([0.86, 0.14])
        with cols[0]:
            if st.button(REGIME_LABEL[r], use_container_width=True, key=f"reg_{run}_{r}"):
                st.session_state.vxp_pending_regime = r
                go("acquire")
                st.rerun()
        with cols[1]:
            st.markdown(
                f"<div style='font-size:22px; font-weight:900; padding-top:10px;'>{'✓' if r in done else ''}</div>",
                unsafe_allow_html=True,
            )

    if run == 3 and len(done) == 3 and all_ok(current_run_data(3)):
        st.markdown("<div class='vxp-label' style='margin-top:10px;'>✓ RUN 3 COMPLETE — PARAMETERS OK</div>", unsafe_allow_html=True)

    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("mr_menu",), key="collect_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_acquire():
    _select_procedure_window(active=False)
    _dim()
    _win_begin(win_id="acq", title="ACQUIRING ...", x=240, y=140, w=560, h=380, active=True, modal=True)
    run = int(st.session_state.vxp_run)
    regime = st.session_state.get("vxp_pending_regime")
    if not regime:
        st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
        st.button("Close", on_click=go, args=("collect",), key="acq_close1")
        st.markdown("</div>", unsafe_allow_html=True)
        _win_end()
        return

    st.markdown(f"<div class='vxp-label'>{REGIME_LABEL[regime]}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='vxp-label'>RPM {BO105_DISPLAY_RPM:.1f}</div>", unsafe_allow_html=True)
    st.markdown("<div class='vxp-mono'>M/R LAT\t\tACQUIRING\n\nM/R OBT\t\tACQUIRING</div>", unsafe_allow_html=True)

    if not st.session_state.get("vxp_acq_in_progress", False):
        st.session_state.vxp_acq_in_progress = True
        p = st.progress(0)
        for i in range(80):
            time.sleep(0.01)
            p.progress(i + 1)

        meas = simulate_measurement(run, regime, st.session_state.vxp_adjustments)
        current_run_data(run)[regime] = meas
        completed_set(run).add(regime)

        st.session_state.vxp_pending_regime = None
        st.session_state.vxp_acq_in_progress = False
        go("collect")
        st.rerun()

    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("collect",), key="acq_close2")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_meas_list():
    _select_procedure_window(active=False)
    _win_begin(win_id="meas_list", title="MEASUREMENTS LIST", x=170, y=60, w=760, h=630, active=True)
    view_run = run_selector_inline()
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet. Go to COLLECT.")
        st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
        st.button("Close", on_click=go, args=("mr_menu",), key="ml_close_empty")
        st.markdown("</div>", unsafe_allow_html=True)
        _win_end()
        return
    st.markdown(f"<div class='vxp-mono' style='height:520px; overflow:auto;'>{legacy_results_text(view_run, data)}</div>", unsafe_allow_html=True)
    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("mr_menu",), key="ml_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_meas_graph():
    _select_procedure_window(active=False)
    _win_begin(win_id="meas_graph", title="MEASUREMENTS GRAPH", x=140, y=40, w=820, h=650, active=True)
    view_run = run_selector_inline()
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet. Go to COLLECT.")
        st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
        st.button("Close", on_click=go, args=("mr_menu",), key="mg_close_empty")
        st.markdown("</div>", unsafe_allow_html=True)
        _win_end()
        return

    available = [r for r in REGIMES if r in data]
    sel = st.selectbox("Select Measurement", available, format_func=lambda rr: REGIME_LABEL[rr])
    m = data[sel]

    left, right = st.columns([0.50, 0.50], gap="medium")
    with left:
        st.markdown(f"<div class='vxp-mono' style='height:520px; overflow:auto;'>{legacy_results_text(view_run, data)}</div>", unsafe_allow_html=True)
    with right:
        st.pyplot(plot_track_marker(m), clear_figure=True)
        st.pyplot(plot_polar(m), clear_figure=True)

    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("mr_menu",), key="mg_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_settings():
    _select_procedure_window(active=False)
    _win_begin(win_id="settings", title="SETTINGS", x=240, y=120, w=560, h=520, active=True)
    run_selector_inline()

    regime = st.selectbox("Regime", options=REGIMES, format_func=lambda r: REGIME_LABEL[r])
    adj = st.session_state.vxp_adjustments[regime]

    hdr = st.columns([0.20, 0.27, 0.27, 0.26])
    hdr[0].markdown("**Blade**")
    hdr[1].markdown("**Pitch link (turns)**")
    hdr[2].markdown("**Trim tab (mm)**")
    hdr[3].markdown("**Bolt weight (g)**")

    for b in BLADES:
        row = st.columns([0.20, 0.27, 0.27, 0.26])
        row[0].markdown(b)
        adj["pitch_turns"][b] = float(row[1].number_input("", value=float(adj["pitch_turns"][b]), step=0.25, key=f"pl_{regime}_{b}"))
        adj["trim_mm"][b] = float(row[2].number_input("", value=float(adj["trim_mm"][b]), step=0.5, key=f"tt_{regime}_{b}"))
        adj["bolt_g"][b] = float(row[3].number_input("", value=float(adj["bolt_g"][b]), step=5.0, key=f"wt_{regime}_{b}"))

    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("mr_menu",), key="set_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_solution():
    _select_procedure_window(active=False)
    _win_begin(win_id="solution", title="SOLUTION", x=240, y=90, w=560, h=580, active=True)
    view_run = run_selector_inline()
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet. Go to COLLECT.")
        st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
        st.button("Close", on_click=go, args=("mr_menu",), key="sol_close_empty")
        st.markdown("</div>", unsafe_allow_html=True)
        _win_end()
        return

    st.selectbox("", options=["BALANCE ONLY", "TRACK ONLY", "TRACK + BALANCE"], index=2, key="sol_type")
    st.button("GRAPHICAL SOLUTION", use_container_width=True, on_click=go, args=("solution_graph",))
    st.button("SHOW SOLUTION", use_container_width=True, on_click=go, args=("solution_text",))
    st.button("EDIT SOLUTION", use_container_width=True, on_click=go, args=("edit_solution",))
    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("mr_menu",), key="sol_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_solution_graph():
    _select_procedure_window(active=False)
    _win_begin(win_id="sol_graph", title="RESULTS", x=110, y=30, w=860, h=660, active=True)
    view_run = run_selector_inline()
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet.")
        st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
        st.button("Close", on_click=go, args=("solution",), key="sg_close_empty")
        st.markdown("</div>", unsafe_allow_html=True)
        _win_end()
        return

    available = [r for r in REGIMES if r in data]
    sel = st.selectbox("Select Bal Meas", available, format_func=lambda rr: REGIME_LABEL[rr])
    m = data[sel]

    left, right = st.columns([0.50, 0.50], gap="medium")
    with left:
        st.markdown(f"<div class='vxp-mono' style='height:590px; overflow:auto;'>{legacy_results_text(view_run, data)}</div>", unsafe_allow_html=True)
        applied = st.session_state.vxp_applied_changes.get(view_run, [])
        st.markdown("<div class='vxp-label' style='margin-top:10px;'>APPLIED CHANGES (THIS RUN)</div>", unsafe_allow_html=True)
        st.markdown("<div class='vxp-mono' style='height:120px; overflow:auto;'>" + ("\n".join(applied) if applied else "NONE") + "</div>", unsafe_allow_html=True)

    with right:
        st.pyplot(plot_track_marker(m), clear_figure=True)
        st.pyplot(plot_track_graph(data), clear_figure=True)
        st.pyplot(plot_polar(m), clear_figure=True)

    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("solution",), key="sg_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_solution_text():
    _select_procedure_window(active=False)
    _win_begin(win_id="sol_text", title="SHOW SOLUTION", x=140, y=40, w=820, h=650, active=True)
    view_run = run_selector_inline()
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet.")
        st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
        st.button("Close", on_click=go, args=("solution",), key="st_close_empty")
        st.markdown("</div>", unsafe_allow_html=True)
        _win_end()
        return

    lines = []
    lines.append(legacy_results_text(view_run, data))
    lines.append("----- Suggested Next Action (Training) -----")

    if view_run == 1:
        sug = suggest_pitchlink(data)
        lines.append("RUN 1: Correct TRACKING using Pitch Link (flats).")
        for b in BLADES:
            flats = sug[b] * 6.0
            if abs(flats) >= 0.5:
                lines.append(f"  {b}: {flats:+.1f} flats (≈ {sug[b]:+.2f} turns)")
    elif view_run == 2:
        sug = suggest_trimtabs(data)
        lines.append("RUN 2: Correct FORWARD FLIGHT TRACK using Trim Tabs (Tab Sta 5/6).")
        for b in BLADES:
            if abs(sug[b]) >= 0.25:
                lines.append(f"  {b}: {sug[b]:+.2f} mm (equiv)")
    else:
        blade, grams = suggest_weight(data)
        lines.append("RUN 3: Correct 1/REV VIBRATION using Weight (plqts).")
        lines.append(f"  Add ~{grams:.0f} g at {blade} bolt (≈ {grams/10:.1f} plqts)")
        if len(completed_set(3)) == 3 and all_ok(current_run_data(3)):
            lines.append("")
            lines.append("✓ PARAMETERS OK — TRAINING COMPLETE")

    st.markdown(f"<div class='vxp-mono' style='height:680px; overflow:auto;'>{chr(10).join(lines)}</div>", unsafe_allow_html=True)
    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("solution",), key="st_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def screen_next_run_prompt():
    _select_procedure_window(active=False)
    _win_begin(win_id="next", title="NEXT RUN", x=210, y=170, w=620, h=420, active=True)

    def start_next():
        cur = int(st.session_state.vxp_run)
        if cur >= 3:
            go("mr_menu")
            return
        nxt = cur + 1
        st.session_state.vxp_runs.setdefault(nxt, {})
        st.session_state.vxp_completed_by_run.setdefault(nxt, set())
        st.session_state.vxp_run = nxt
        st.session_state.vxp_view_run = nxt
        go("mr_menu")
        st.rerun()

    st.button("UPDATE SETTINGS - START NEXT RUN", use_container_width=True, on_click=start_next)
    st.button("NO CHANGES MADE - START NEXT RUN", use_container_width=True, on_click=start_next)
    st.button("CANCEL - STAY ON RUN", use_container_width=True, on_click=go, args=("mr_menu",))
    st.markdown("<div class='vxp-smallbtn'>", unsafe_allow_html=True)
    st.button("Close", on_click=go, args=("mr_menu",), key="next_close")
    st.markdown("</div>", unsafe_allow_html=True)
    _win_end()


def route():
    scr = st.session_state.vxp_screen
    if scr == "home": return screen_home()
    if scr == "not_impl": return screen_not_impl()
    if scr == "mr_menu": return screen_mr_menu()
    if scr == "collect": return screen_collect()
    if scr == "acquire": return screen_acquire()
    if scr == "meas_list": return screen_meas_list()
    if scr == "meas_graph": return screen_meas_graph()
    if scr == "settings": return screen_settings()
    if scr == "solution": return screen_solution()
    if scr == "solution_graph": return screen_solution_graph()
    if scr == "solution_text": return screen_solution_text()
    if scr == "next_run_prompt": return screen_next_run_prompt()
    return screen_home()

# --- Navigation via querystring (Streamlit compat) ---

def _get_query_params() -> dict:
    """Compat: Streamlit <=1.26 (experimental_*) y Streamlit >=1.27 (query_params)."""
    if hasattr(st, "query_params"):
        try:
            return dict(st.query_params)
        except Exception:
            return st.query_params
    if hasattr(st, "experimental_get_query_params"):
        return st.experimental_get_query_params()
    return {}


def _clear_query_params() -> None:
    """Compat para limpiar la URL."""
    if hasattr(st, "query_params"):
        try:
            for k in list(st.query_params.keys()):
                del st.query_params[k]
        except Exception:
            pass
        return
    if hasattr(st, "experimental_set_query_params"):
        st.experimental_set_query_params()


def apply_nav():
    qp = _get_query_params()

    # qp puede devolver str o lista según versión
    nav = qp.get("nav", "")
    if isinstance(nav, list):
        nav = nav[0] if nav else ""
    nav = (nav or "").lower()

    if not nav:
        return

    # Limpia la URL para que no se quede “pegado”
    _clear_query_params()

    if nav in ("disconnect", "exit"):
        go("home")
    elif nav == "viewlog":
        go("meas_list")
    elif nav == "print_au":
        go("solution_text")
    elif nav in ("upload", "download", "help"):
        go("not_impl")
    elif nav == "settings":
        go("settings")
    else:
        go("home")

    # rerun compat
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()
