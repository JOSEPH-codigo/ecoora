from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Ecoora AI", page_icon="🌱")

st.title("Ecoora AI 🌱")

# ---------- SESSION STATE ----------

if "points" not in st.session_state:
    st.session_state.points = 0

if "missions_done" not in st.session_state:
    st.session_state.missions_done = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Ecoora AI. Help people protect the environment."}
    ]

# ---------- MENU ----------

menu = st.sidebar.selectbox(
    "Menu",
    ["Chat", "Missions", "Points", "Settings"]
)

# ---------- CHAT ----------

if menu == "Chat":

    st.header("Ecoora Chat 🌍")

    # mostrar historial
    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.write("👤:", msg["content"])

        elif msg["role"] == "assistant":
            st.write("🌱 Ecoora:", msg["content"])

    question = st.text_input("Ask Ecoora something about the environment:")

    if question:

        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except:
            st.error("OpenAI API key not found. Add it in Streamlit Secrets.")
            st.stop()

        client = OpenAI(api_key=api_key)

        # guardar mensaje usuario
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        response = client.responses.create(
            model="gpt-4o-mini",
            input=st.session_state.messages
        )

        answer = response.output_text

        # guardar respuesta IA
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.write("🌱 Ecoora:", answer)

# ---------- MISSIONS ----------

if menu == "Missions":

    st.header("Eco Missions 🌎")

    missions = [
        "Recycle one plastic item ♻️",
        "Turn off lights for 1 hour 💡",
        "Use a reusable bottle 🍼",
        "Pick up trash outside 🗑️",
        "Plant something 🌱"
    ]

    for mission in missions:

        if mission not in st.session_state.missions_done:

            if st.button(f"Complete: {mission}"):

                st.session_state.points += 10
                st.session_state.missions_done.append(mission)

                st.success("Mission complete! +10 points ⭐")

# ---------- POINTS ----------

if menu == "Points":

    st.header("Your Eco Points ⭐")

    st.write(f"Total Points: {st.session_state.points}")

# ---------- SETTINGS ----------

if menu == "Settings":

    st.header("Settings ⚙️")

    if st.button("Reset Points"):

        st.session_state.points = 0
        st.session_state.missions_done = []
        st.session_state.messages = [
            {"role": "system", "content": "You are Ecoora AI. Help people protect the environment."}
        ]

        st.success("Everything reset!")