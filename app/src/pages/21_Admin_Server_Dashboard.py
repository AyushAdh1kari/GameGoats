import streamlit as st

from modules.api_client import get_json
from modules.nav import SideBarLinks
from modules.personas import require_persona

st.set_page_config(layout="wide")
SideBarLinks()
require_persona("admin")

st.title("Server Dashboard")
st.write("Monitor live infrastructure data through `GET /servers` and `GET /servers/<server_id>`.")

servers, error, _ = get_json("/servers")
if error:
    st.error(error)
    st.stop()

status_filter = st.selectbox("Filter by status", ["All", "healthy", "degraded", "down"])
environment_filter = st.selectbox("Filter by environment", ["All", "production", "staging"])

filtered_servers = []
for server in servers:
    status_match = status_filter == "All" or server["status"] == status_filter
    environment_match = environment_filter == "All" or server["environment"] == environment_filter
    if status_match and environment_match:
        filtered_servers.append(server)

metric1, metric2, metric3 = st.columns(3)
metric1.metric("Servers In View", len(filtered_servers))
metric2.metric("Healthy Servers", sum(1 for server in filtered_servers if server["status"] == "healthy"))
metric3.metric("Degraded Or Down", sum(1 for server in filtered_servers if server["status"] != "healthy"))

st.dataframe(
    filtered_servers,
    use_container_width=True,
    hide_index=True,
    column_order=["server_id", "server_name", "region", "environment", "status", "capacity_percent"],
)

selected_server = st.selectbox(
    "Inspect a server",
    options=filtered_servers or servers,
    format_func=lambda server: f"#{server['server_id']} - {server['server_name']}",
)

server_detail, detail_error, _ = get_json(f"/servers/{selected_server['server_id']}")
if detail_error:
    st.error(detail_error)
else:
    st.subheader("Server Detail")
    st.json(server_detail)
