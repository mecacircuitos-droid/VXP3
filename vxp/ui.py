import time
from typing import Callable

import streamlit as st

from .sim import (
    BLADES,
    REGIMES,
    REGIME_LABEL,
    BO105_DISPLAY_RPM,
    default_adjustments,
    simulate_measurement,
)
from .reports import legacy_results_text
from .plots import plot_track_marker, plot_track_graph, plot_polar, plot_polar_compare
from .solver import all_ok


# ---------------------------
# Navigation / state
# ---------------------------

def go(screen: str, **kwargs) -> None:
    st.session_state.vxp_screen = screen
    for k, v in kwargs.items():
        st.session_state[k] = v


def init_state() -> None:
    st.session_state.setdefault("vxp_screen", "home")
    st.session_state.setdefault("vxp_run", 1)
    st.session_state.setdefault("vxp_runs", {1: {}})
    st.session_state.setdefault("vxp_completed_by_run", {1: set()})
    st.session_state.setdefault("vxp_view_run", 1)

    st.session_state.setdefault("vxp_adjustments", default_adjustments())
    st.session_state.setdefault("vxp_pending_regime", None)
    st.session_state.setdefault("vxp_acq_in_progress", False)


def current_run_data(run: int):
    return st.session_state.vxp_runs.setdefault(run, {})


def completed_set(run: int):
    return st.session_state.vxp_completed_by_run.setdefault(run, set())


def run_selector_inline(key: str = "run_selector") -> int:
    runs = sorted(st.session_state.vxp_runs.keys())
    cur = int(st.session_state.vxp_view_run)
    if cur not in runs:
        cur = runs[0]
        st.session_state.vxp_view_run = cur
    idx = runs.index(cur)
    r = st.selectbox("Run", runs, index=idx, key=key)
    st.session_state.vxp_view_run = int(r)
    return int(r)


# ---------------------------
# Window chrome helpers
# ---------------------------

def win_caption(title: str, active: bool) -> None:
    cls = "active" if active else "inactive"
    st.markdown(
        f"<div class='vxp-win-caption {cls}'>"
        f"<div>{title}</div>"
        "<div class='vxp-closebox'>✕</div>"
        "</div>",
        unsafe_allow_html=True,
    )


def right_close_button(label: str, on_click: Callable[[], None]) -> None:
    cols = st.columns([0.75, 0.25])
    with cols[1]:
        st.button(label, use_container_width=True, on_click=on_click)


"""UI rendering.

Nota importante sobre Streamlit:
  La superposición tipo MDI (varias ventanas apiladas) requiere CSS avanzado
  que no es consistente entre navegadores. Para evitar que la “ventana nueva”
  se abra debajo (en vez de superponerse), la UI se renderiza como UNA única
  ventana principal cuyo contenido cambia según la navegación.
"""


# ---------------------------
# Desktop (single-window)
# ---------------------------

def render_desktop() -> None:
    """Render a single main window (no overlapping popups)."""

    # IMPORTANT (Streamlit): we cannot "wrap" widgets inside an open <div>
    # created by st.markdown. Doing so produces empty boxes and pushes the
    # widgets below the intended frame (exactly what you saw).
    #
    # We instead use a real Streamlit container (optionally with border=True)
    # and skin that container via CSS.
    try:
        desk = st.container(border=True)
    except TypeError:
        desk = st.container()

    with desk:
        # Marker used by CSS (safe even if :has is not available).
        st.markdown("<div class='vxp-desktop-marker'></div>", unsafe_allow_html=True)

        if st.session_state.vxp_screen == "home":
            render_select_procedure_window(active=True)
        else:
            render_active_window()


def render_select_procedure_window(active: bool) -> None:
    win_caption("Select Procedure:", active=active)
    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # Left column holds the classic big buttons; right column stays empty like the original screenshots.
    left, _ = st.columns([0.72, 0.28], gap="small")
    # IMPORTANT: Avoid on_click callbacks here.
    # In some Streamlit builds, callbacks can update state after this function
    # starts rendering, causing the next screen to appear "below" instead of
    # replacing the current one. We navigate explicitly and force a rerun.
    with left:
        if st.button("Aircraft Info", use_container_width=True, key="home_aircraft_info"):
            go("aircraft_info")
            st.rerun()
        if st.button("Main Rotor Balance Run 1", use_container_width=True, key="home_mr_run1"):
            go("mr_menu")
            st.rerun()
        if st.button("Tail Rotor Balance Run 1", use_container_width=True, key="home_tr_run1"):
            go("not_impl")
            st.rerun()
        if st.button("T/R Driveshaft Balance Run 1", use_container_width=True, key="home_drv_run1"):
            go("not_impl")
            st.rerun()
        if st.button("Vibration Signatures", use_container_width=True, key="home_vib_sig"):
            go("not_impl")
            st.rerun()
        if st.button("Measurements Only", use_container_width=True, key="home_meas_only"):
            go("not_impl")
            st.rerun()
        if st.button("Setup / Utilities", use_container_width=True, key="home_setup_utils"):
            go("not_impl")
            st.rerun()


def render_active_window() -> None:
    screen = st.session_state.vxp_screen
    if screen == "mr_menu":
        screen_mr_menu_window()
    elif screen == "collect":
        screen_collect_window()
    elif screen == "acquire":
        screen_acquire_window()
    elif screen == "meas_list":
        screen_meas_list_window()
    elif screen == "meas_graph":
        screen_meas_graph_window()
    elif screen == "settings":
        screen_settings_window()
    elif screen == "solution":
        screen_solution_window()
    elif screen == "solution_text":
        screen_solution_text_window()
    elif screen == "next_run_prompt":
        screen_next_run_window()
    elif screen == "aircraft_info":
        screen_aircraft_info_window()
    else:
        screen_not_impl_window()


# ---------------------------
# Procedure screens (inside the active window)
# ---------------------------

def _centered_buttons(labels_and_targets):
    """Helper to keep buttons from becoming too wide."""
    left, mid, right = st.columns([0.10, 0.80, 0.10])
    with mid:
        for label, target in labels_and_targets:
            st.button(label, use_container_width=True, on_click=lambda t=target: go(t))


def screen_mr_menu_window():
    run = int(st.session_state.vxp_run)
    win_caption(f"Main Rotor Balance Run {run}", active=True)
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='display:flex; justify-content:space-between; font-weight:900;'>"
        "<div>Tracking &amp; Balance – Option B</div>"
        f"<div>Run {run}</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    _centered_buttons(
        [
            ("COLLECT", "collect"),
            ("MEASUREMENTS LIST", "meas_list"),
            ("MEASUREMENTS GRAPH", "meas_graph"),
            ("SETTINGS", "settings"),
            ("SOLUTION", "solution"),
            ("NEXT RUN", "next_run_prompt"),
        ]
    )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    right_close_button("Close", on_click=lambda: go("home"))


def screen_collect_window():
    run = int(st.session_state.vxp_run)
    win_caption(f"Main Rotor: Run {run}    Day Mode", active=True)
    st.markdown(
        f"<div style='display:flex; justify-content:space-between; font-weight:900; margin-top:6px;'>"
        f"<div>RPM&nbsp;&nbsp;{BO105_DISPLAY_RPM:.1f}</div><div></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    done = completed_set(run)
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # Regime buttons with checkmarks like the original
    for r in REGIMES:
        cols = st.columns([0.84, 0.16])
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
        st.markdown(
            "<div class='vxp-label' style='margin-top:10px;'>✓ RUN 3 COMPLETE — PARAMETERS OK</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    right_close_button("Close", on_click=lambda: go("mr_menu"))


def screen_acquire_window():
    win_caption("ACQUIRING …", active=True)
    run = int(st.session_state.vxp_run)
    regime = st.session_state.get("vxp_pending_regime")
    if not regime:
        right_close_button("Close", on_click=lambda: go("collect"))
        return

    st.markdown(f"<div class='vxp-label' style='margin-top:8px;'>{REGIME_LABEL[regime]}</div>", unsafe_allow_html=True)
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

    right_close_button("Close", on_click=lambda: go("collect"))


def screen_meas_list_window():
    win_caption("MEASUREMENTS LIST", active=True)
    view_run = run_selector_inline(key="run_selector_generic")
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet. Go to COLLECT.")
        right_close_button("Close", on_click=lambda: go("mr_menu"))
        return
    st.markdown(
        f"<div class='vxp-mono' style='height:380px; overflow:auto; margin-top:8px;'>{legacy_results_text(view_run, data)}</div>",
        unsafe_allow_html=True,
    )
    right_close_button("Close", on_click=lambda: go("mr_menu"))


def screen_meas_graph_window():
    win_caption("MEASUREMENTS GRAPH", active=True)

    # Compact controls row (like the original)
    ctrl = st.columns([0.22, 0.78], gap="small")
    with ctrl[0]:
        view_run = run_selector_inline(key="run_selector_meas_graph")

    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet. Go to COLLECT.")
        right_close_button("Close", on_click=lambda: go("mr_menu"))
        return

    available = [r for r in REGIMES if r in data]
    with ctrl[1]:
        sel = st.selectbox(
            "Select Measurement",
            available,
            format_func=lambda rr: REGIME_LABEL[rr],
            key="meas_sel",
        )

    m = data[sel]

    # Data for comparison graphs (up to the 3 regimes)
    compare = {r: data[r] for r in REGIMES if r in data}

    left, right = st.columns([0.56, 0.44], gap="medium")
    with left:
        st.markdown(
            f"<div class='vxp-mono' style='height:330px; overflow:auto;'>{legacy_results_text(view_run, data)}</div>",
            unsafe_allow_html=True,
        )
    with right:
        # Smaller charts + comparison plots (track marker, track over regimes, polar compare)
        st.pyplot(plot_track_marker(m), clear_figure=True)
        st.pyplot(plot_track_graph(compare), clear_figure=True)
        st.pyplot(plot_polar_compare(compare), clear_figure=True)

    right_close_button("Close", on_click=lambda: go("mr_menu"))


def screen_settings_window():
    win_caption("SETTINGS", active=True)
    run_selector_inline(key="run_selector_settings")

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
        adj["pitch_turns"][b] = float(
            row[1].number_input("", value=float(adj["pitch_turns"][b]), step=0.25, key=f"pl_{regime}_{b}")
        )
        adj["trim_mm"][b] = float(
            row[2].number_input("", value=float(adj["trim_mm"][b]), step=0.5, key=f"tt_{regime}_{b}")
        )
        adj["bolt_g"][b] = float(
            row[3].number_input("", value=float(adj["bolt_g"][b]), step=5.0, key=f"wt_{regime}_{b}")
        )

    right_close_button("Close", on_click=lambda: go("mr_menu"))


def screen_solution_window():
    win_caption("SOLUTION", active=True)
    view_run = run_selector_inline(key="run_selector_solution")
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet. Go to COLLECT.")
        right_close_button("Close", on_click=lambda: go("mr_menu"))
        return

    st.selectbox("", options=["BALANCE ONLY", "TRACK ONLY", "TRACK + BALANCE"], index=2, key="sol_type")
    _centered_buttons(
        [
            ("SHOW SOLUTION", "solution_text"),
            ("Close", "mr_menu"),
        ]
    )


def screen_solution_text_window():
    win_caption("SOLUTION", active=True)
    view_run = run_selector_inline(key="run_selector_solution_text")
    data = current_run_data(view_run)
    if not data:
        st.write("No measurements for this run yet. Go to COLLECT.")
        right_close_button("Close", on_click=lambda: go("mr_menu"))
        return
    st.markdown(
        f"<div class='vxp-mono' style='height:380px; overflow:auto; margin-top:8px;'>"
        f"{legacy_results_text(view_run, data)}"
        "</div>",
        unsafe_allow_html=True,
    )
    right_close_button("Close", on_click=lambda: go("mr_menu"))


def screen_next_run_window():
    run = int(st.session_state.vxp_run)
    win_caption("NEXT RUN", active=True)
    st.write(f"Current run: {run}. This simulator supports up to 3 runs.")
    cols = st.columns([0.5, 0.5])

    with cols[0]:
        if st.button("Start Next Run", use_container_width=True, disabled=(run >= 3)):
            st.session_state.vxp_run = run + 1
            st.session_state.vxp_runs.setdefault(run + 1, {})
            st.session_state.vxp_completed_by_run.setdefault(run + 1, set())
            go("mr_menu")
            st.rerun()
    with cols[1]:
        st.button("Cancel", use_container_width=True, on_click=lambda: go("mr_menu"))


def screen_aircraft_info_window():
    win_caption("Aircraft Info", active=True)
    st.write("(Placeholder) Aircraft information screen.")
    right_close_button("Close", on_click=lambda: go("home"))


def screen_not_impl_window():
    win_caption("VXP", active=True)
    st.write("Solo se implementa **Main Rotor – Tracking & Balance (Option B)** para el BO105.")
    right_close_button("Close", on_click=lambda: go("home"))
