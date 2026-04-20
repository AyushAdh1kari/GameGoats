import requests
import streamlit as st
import pandas as pd

from modules.nav import SideBarLinks

st.set_page_config(layout="wide", page_title="Server Dashboard", page_icon="🖥️")
SideBarLinks()

if not st.session_state.get("authenticated") or st.session_state.get("role") != "admin":
    st.warning("Please log in as an Admin from the Home page.")
    st.stop()

API = "http://web-api:4000"

st.title("Server Dashboard")

try:
    resp = requests.get(f"{API}/servers", timeout=5)
    servers = resp.json() if resp.status_code == 200 else []
except Exception:
    servers = []
    st.error("Could not reach the API.")

if servers:
    healthy = sum(1 for s in servers if s.get("status") == "healthy")
    degraded = sum(1 for s in servers if s.get("status") == "degraded")
    down = sum(1 for s in servers if s.get("status") == "down")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Servers", len(servers))
    col2.metric("Healthy", healthy)
    col3.metric("Degraded", degraded)
    col4.metric("Down", down)

    st.divider()

    STATUS_COLORS = {"healthy": "🟢", "degraded": "🟡", "down": "🔴"}

    df = pd.DataFrame([
        {
            "Status": STATUS_COLORS.get(s.get("status"), "⚪") + " " + s.get("status", "–"),
            "Server": s.get("server_name", "–"),
            "Region": s.get("region", "–"),
            "Environment": s.get("environment", "–"),
            "Capacity": f"{s.get('capacity_percent', 0)}%",
            "Last Heartbeat": str(s.get("last_heartbeat", "–"))[:19],
        }
        for s in servers
    ])

    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("Server Detail")
    server_options = {s["server_name"]: s["server_id"] for s in servers}
    selected_server = st.selectbox("Select a server", list(server_options.keys()))
    server_id = server_options[selected_server]

    server = next(s for s in servers if s["server_id"] == server_id)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**Name:** {server.get('server_name')}")
        st.markdown(f"**Region:** {server.get('region')}")
        st.markdown(f"**Environment:** {server.get('environment')}")
        st.markdown(f"**Status:** {STATUS_COLORS.get(server.get('status'), '')} {server.get('status')}")

    with col_b:
        st.subheader("Update Server")
        with st.form("update_server_form"):
            new_status = st.selectbox("Status", ["healthy", "degraded", "down"],
                                      index=["healthy", "degraded", "down"].index(server.get("status", "healthy")))
            cap = server.get("capacity_percent", 0)
            if isinstance(cap, str):
                cap = float(cap)
            new_cap = st.slider("Capacity %", 0.0, 100.0, float(cap))
            if st.form_submit_button("Update", type="primary"):
                try:
                    resp = requests.put(
                        f"{API}/servers/{server_id}",
                        json={"status": new_status, "capacity_percent": new_cap},
                        timeout=5,
                    )
                    if resp.status_code == 200:
                        st.success("Server updated!")
                        st.rerun()
                    else:
                        st.error(f"Failed: {resp.text}")
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.button("Delete Server", type="secondary"):
        try:
            resp = requests.delete(f"{API}/servers/{server_id}", timeout=5)
            if resp.status_code == 200:
                st.success("Server deleted.")
                st.rerun()
            else:
                st.error(f"Failed: {resp.text}")
        except Exception as e:
            st.error(f"Error: {e}")

else:
    st.info("No servers found.")

st.divider()

st.subheader("Register New Server")
with st.form("new_server_form", clear_on_submit=True):
    nc1, nc2, nc3 = st.columns(3)
    with nc1:
        new_name = st.text_input("Server Name", max_chars=64)
    with nc2:
        new_region = st.selectbox("Region", ["NA-East", "NA-West", "EU-Central", "EU-West", "AP-South", "LATAM"],
                                  key="new_srv_region")
    with nc3:
        new_env = st.selectbox("Environment", ["production", "staging"], key="new_srv_env")
    if st.form_submit_button("Register Server", type="primary"):
        if new_name.strip():
            try:
                resp = requests.post(
                    f"{API}/servers",
                    json={"server_name": new_name.strip(), "region": new_region, "environment": new_env},
                    timeout=5,
                )
                if resp.status_code == 201:
                    st.success(f"Server '{new_name}' registered!")
                    st.rerun()
                else:
                    st.error(f"Failed: {resp.text}")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Server name is required.")
