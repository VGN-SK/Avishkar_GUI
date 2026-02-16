import streamlit as st
import pandas as pd
import pydeck as pdk
import time

from backend.auth_service import authenticate_user
from backend.pod_service import get_all_pods, get_pod_by_name
from backend.telemetry_service import (
    get_latest_telemetry,
    get_all_latest_snapshots
)
from integration.weather import get_route_weather
from integration.energy_tips import get_energy_tip
from integration.fun_facts import get_fun_fact
from analysis.safety_limits import compute_safety_limits
from tracking.mapper import get_all_pod_coordinates
from tracking.default_tracks import get_track



# PAGE CONFIG

st.set_page_config(
    page_title="Hyperloop Operations",
    layout="wide"
)


# SESSION STATE FOR USER LOGIN

if "user" not in st.session_state:
    st.session_state.user = None



# LOGIN PAGE

def login_page():

    # Center layout using columnsm-- also using html to add padding and proper text aliignent
    left_spacer, center_col, right_spacer = st.columns([1, 2, 1])

    with center_col:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="
                background-color: #f8f9fa;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            ">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            "<h2 style='text-align: center;'> Hyperloop Operations</h2>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<p style='text-align: center; color: gray;'>Secure Access Portal</p>",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        login_clicked = st.button("Login", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if login_clicked:
            user = authenticate_user(username, password)

            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")



# VIEWER DASHBOARD

def viewer_dashboard():

    if "map_view" not in st.session_state:
        st.session_state.map_view = None  # For storing the viewstate created for map .. to avoid recentering dueing reruns

    st.title(" Hyperloop Dashboard")

    pods = get_all_pods()
    snapshots = get_all_latest_snapshots()


# COLLECT ALERTS

    all_alerts = []

    for pod in pods:

        telemetry = get_latest_telemetry(pod["name"])
        if not telemetry:
            continue

        weather = get_route_weather(pod["track_id"])
        safety = compute_safety_limits(telemetry, weather)

        if safety["alerts"]:
            for alert in safety["alerts"]:
                all_alerts.append({
                    "pod": pod["name"],
                    "message": alert,
                    "severity": safety["severity"]
                })


             # TOP ROW: SUMMARY + INFO PANEL

    col_left, col_right = st.columns([3, 1])


            # TOP DASHBOARD SECTION


    left_col, right_col = st.columns([3, 1])

                #LEFT SIDE 
    with left_col:

        st.markdown("##  Pod Overview")

        summary_data = []

        for pod in pods:
            name = pod["name"]
            status = pod["status"]

            if name not in snapshots:
                continue

            telemetry = snapshots[name]
            track_id = pod["track_id"]

            speed_kmh = float(telemetry["velocity"]) * 3.6
            battery = float(telemetry["battery"])

            weather = get_route_weather(track_id)
            weather_risk = weather["risk_level"].capitalize()

            safety = compute_safety_limits(telemetry, weather)
            safe_speed_kmh = safety["safe_velocity"] * 3.6
            
            summary_data.append({
                "Pod": name,
                "Speed (km/h)": round(speed_kmh, 1),
                "Safe Speed (km/h)": round(safe_speed_kmh, 1),
                "Battery (%)": round(battery, 1),
                "Status": status.capitalize(),
                "Weather Risk": weather_risk
        })


        df_summary = pd.DataFrame(summary_data)

        if not df_summary.empty:

        # Compact filter row
            f1, f2, f3 = st.columns([1.5, 1.5, 1])

            with f1:
                selected_status = st.selectbox(
                "Status",
                ["All"] + sorted(df_summary["Status"].unique())
            )

            with f2:
                sort_by = st.selectbox(
                "Sort By",
                ["None", "Speed (km/h)", "Battery (%)"]
                )

            with f3:
                sort_order = st.selectbox(
                "Order",
                ["Descending", "Ascending"]
            )

            if selected_status != "All":
                df_summary = df_summary[df_summary["Status"] == selected_status]

            if sort_by != "None":
                df_summary = df_summary.sort_values(
                by=sort_by,
                ascending=(sort_order == "Ascending")
            )

                                 #TABLE
            def highlight_status(val):
                if val == "Operational":
                    return "background-color: #d4edda; color: #155724; font-weight:600"
                elif val == "Maintenance":
                    return "background-color: #fff3cd; color: #856404; font-weight:600"
                elif val == "Docked":
                    return "background-color: #d1ecf1; color: #0c5460; font-weight:600"
                return ""


            def highlight_weather(val):
                if val == "Low":
                    return "background-color: #d4edda; color: #155724; font-weight:600"
                elif val == "Medium":
                    return "background-color: #fff3cd; color: #856404; font-weight:600"
                elif val == "High":
                    return "background-color: #f8d7da; color: #721c24; font-weight:600"
                return ""
                
            def highlight_speed(row):
                if row["Speed (km/h)"] > row["Safe Speed (km/h)"]:
                    return ["background-color: #f8d7da"] * len(row)
                return [""] * len(row)

            styled_df = df_summary.style

            if "Status" in df_summary.columns:
                styled_df = styled_df.map(highlight_status, subset=["Status"])

            if "Weather Risk" in df_summary.columns:
                styled_df = styled_df.map(highlight_weather, subset=["Weather Risk"])
            
            if "Speed (km/h)" in df_summary.columns and "Safe Speed (km/h)" in df_summary.columns:
                styled_df = styled_df.apply(highlight_speed, axis=1)

            st.dataframe(
            styled_df,
            width="stretch",
            height=260
        )

                # RIGHT SIDE

    with right_col:

        st.markdown("##  System Alerts")

        if all_alerts:

            for alert in all_alerts:

                if alert["severity"] == "critical":
                    st.error(f"{alert['pod']}: {alert['message']}")

                elif alert["severity"] == "warning":
                    st.warning(f"{alert['pod']}: {alert['message']}")

                else:
                    st.info(f"{alert['pod']}: {alert['message']}")

        else:
            st.success("All Pods Operating Within Safe Limits")

        st.divider()

        st.markdown("### ⚡ Energy Optimization")
        st.info(get_energy_tip())

        st.markdown("###  Did You Know?")
        st.success(get_fun_fact())



    # LIVE MAP SECTION
 

    st.subheader("Live Network View")

    pod_locations = get_all_pod_coordinates()

    if pod_locations:

        enriched_data = []

        for pod in pod_locations:

            telemetry = get_latest_telemetry(pod["pod_name"])
            if not telemetry:
                continue

            pod_meta = get_pod_by_name(pod["pod_name"])
            track_id = pod_meta["track_id"]

            weather = get_route_weather(track_id)
            safety = compute_safety_limits(telemetry, weather)

            severity = safety["severity"]

            if severity == "normal":
                color = [0, 200, 0]
            elif severity == "warning":
                color = [255, 165, 0]
            else:
                color = [255, 0, 0]

            track = get_track(track_id)

            current_pos = float(telemetry["position_m"])
            next_pos = current_pos + 50

            lat1, lon1 = track.get_coordinates(current_pos)
            lat2, lon2 = track.get_coordinates(next_pos)

            enriched_data.append({
                "pod_name": pod["pod_name"],
                "lat": pod["lat"],
                "lon": pod["lon"],
                "color": color,
                "severity": severity,
                "arrow_path": [[lon1, lat1], [lon2, lat2]]
            })

        df = pd.DataFrame(enriched_data)

        if not df.empty:
            st.markdown("### Map Controls")

            c1, c2, c3 = st.columns([2, 1, 1])

            with c1:
                st.markdown("Focus Pod")
                selected_pod = st.selectbox(
                    label="Focus Pod",
                    label_visibility = "collapsed",
                    options=["None"] + df["pod_name"].tolist()
                )

            with c2:
                st.markdown("Follow")
                follow_mode = st.toggle("Follow", value=True, label_visibility = "collapsed")

            with c3:
                st.markdown("Zoom")
                zoom_level = st.slider("Zoom", 10, 18, 13, label_visibility = "collapsed")
                st.caption("Zoom affects camera only in Follow Mode.")



            # Default center
            default_lat = df["lat"].mean()
            default_lon = df["lon"].mean()

            if selected_pod != "None":
                pod_row = df[df["pod_name"] == selected_pod].iloc[0]
                focus_lat = pod_row["lat"]
                focus_lon = pod_row["lon"]
            else:
                focus_lat = default_lat
                focus_lon = default_lon


            # Follow mode behavior
            if follow_mode:
                st.session_state.map_view = pdk.ViewState(
                    latitude=focus_lat,
                    longitude=focus_lon,
                    zoom=zoom_level,
                    pitch=0
                )
            else:
                # Keep previous view if exists
                if st.session_state.map_view is None:
                    st.session_state.map_view = pdk.ViewState(
                        latitude=default_lat,
                        longitude=default_lon,
                        zoom=zoom_level,
                        pitch=0
                    )

            view_state = st.session_state.map_view


            track_layers = []

            unique_tracks = [
                get_pod_by_name(name)["track_id"]
                for name in df["pod_name"]
            ]

            for track_id in set(unique_tracks):

                track = get_track(track_id)

                track_path = [
                    [wp.lon, wp.lat]
                    for wp in track.waypoints
                ]

                track_layers.append(
                pdk.Layer(
                        "PathLayer",
                        data=[{"path": track_path}],
                        get_path="path",
                        get_width=15,
                        get_color=[0, 0, 200],
                    )
                )


            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position="[lon, lat]",
                get_radius=80,
                get_fill_color="color",
                pickable=True,
            )

            arrow_layer = pdk.Layer(
                "PathLayer",     # Not very visible .. should reduce scatter plot radius too 
                data=df,
                get_path="arrow_path",
                get_width=40,
                get_color="color",
            )

            deck = pdk.Deck(
                layers=track_layers + [scatter_layer, arrow_layer],
                initial_view_state=view_state,
                map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                tooltip={"text": "Pod: {pod_name}\nSeverity: {severity}"}
            )

            st.pydeck_chart(deck)

    else:
        st.warning("No live location data available.")

    st.divider()

    # POD COMPARISON TOOL

    st.subheader("Pod Health Comparison")

    pod_names = [pod["name"] for pod in pods]

    col1, col2 = st.columns(2)

    with col1:
        pod_a = st.selectbox("Select First Pod", pod_names)

    with col2:
        pod_b = st.selectbox("Select Second Pod", pod_names)

    if pod_a and pod_b and pod_a != pod_b:

        def get_battery(pod_name):
            telemetry = get_latest_telemetry(pod_name)
            if not telemetry:
                return 0
            return float(telemetry["battery"])

        comparison_df = pd.DataFrame({
            "Metric": ["Battery (%)"],
            pod_a: [round(get_battery(pod_a), 1)],
            pod_b: [round(get_battery(pod_b), 1)]
        })

        st.table(comparison_df)

 
    # AUTO REFRESH
 

    st.experimental_rerun() if False else time.sleep(1)
    st.rerun()


# ROUTING

def main():

    if st.session_state.user is None:
        login_page()
        return

    role = st.session_state.user["role"]

    st.sidebar.markdown("### Logged In")
    st.sidebar.write(role.capitalize())

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    if role == "viewer":
        viewer_dashboard()

    elif role == "operator":
        st.header("Operator Dashboard (PLS be patient ... under cooking)")

    elif role == "controller":
        st.header("Controller Dashboard (PLS be patient ... under cooking)")


if __name__ == "__main__":
    main()

