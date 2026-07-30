import streamlit as st
import requests
import json

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Hive Mind Research", page_icon="🐝")
st.title("🐝 Hive Mind Research")

query = st.text_input("Research question")

if st.button("Run") and query.strip():
    try:
        resp = requests.post(
            f"{BACKEND_URL}/research",
            json={"userquery": query},
            stream=True,
            timeout=300,
        )
        resp.raise_for_status()

        writerAgent_data = []
        status = st.status("🐝 Running agents...", expanded=True)
        for line in resp.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue
            event = json.loads(line[6:])
            node_name = event.get("node", "")
            node_data = event.get("data", {})

            status.update(label=f"Running {node_name}...")
            status.write(f"✅ {node_name}")

            if node_name == "WriterAgent":
                writerAgent_data.append(node_data.get("draft", ""))

        status.update(label="✅ All agents complete!", state="complete", expanded=False)

        if writerAgent_data:
            st.markdown("# Final Report\n")
            st.markdown(writerAgent_data[-1])
        else:
            st.warning("No report was generated.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")