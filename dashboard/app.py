import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from src.hybrid_algorithm import hybrid_schedule
from src.ppc_solver import solve_scheduling

st.title("🚀 Ordonnancement Hybride (PPC + ML)")

tasks = [("A", 3), ("B", 5), ("C", 2)]
st.write("Tâches :", tasks)

if st.button("Lancer l’algorithme hybride"):
    order, total = hybrid_schedule(tasks)
    st.success(f"Ordre choisi : {[t[0] for t in order]}")
    st.info(f"Durée totale : {total}")

if st.button("Lancer PPC seul"):
    total = solve_scheduling(tasks)
    st.info(f"Durée totale (PPC seul) : {total}")
