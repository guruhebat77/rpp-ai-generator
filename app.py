import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
import io
import re

# Pengaturan Halaman
st.set_page_config(page_title="Generator RPP Madrasah", layout="wide")

# Konfigurasi Kunci API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Kunci API Gemini belum diatur di Streamlit Secrets!")

# --- FUNGSI WORD (TIMES NEW ROMAN 12) ---
def markdown_to_docx(markdown_text):
    doc = Document()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    lines = markdown_text.split('\n')
    for line in lines:
        if line.strip():
            p = doc.add_paragraph()
            run = p.add_run(line.replace("**", "").replace("#", ""))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
    
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

# --- FUNGSI LOGIN ---
def check_password():
    def password_entered():
        if st.session_state["email"] in st.secrets["passwords"] and st.secrets["passwords"][st.session_state["email"]] == st.session_state["password"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("🔒 Login Generator RPP")
        st.text_input("Email", key="email")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered, type="primary")
        return False
    return True

# --- APLIKASI UTAMA ---
if check_password():
    if st.button("🚪 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    st.title("🤖 Generator RPP Madrasah AI")
    
    nama_madrasah = st.text_input("Nama Madrasah")
    nama_guru = st.text_input("Nama Guru")
    mata_pelajaran = st.text_input("Mata Pelajaran")
    fase_kelas = st.text_input("Fase / Kelas")
    jumlah_pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, step=1)
    cp = st.text_area("Capaian Pembelajaran (CP)")
    tp = st.text_area("Tujuan Pembelajaran (TP)")
    materi = st.text_area("Materi Pembelajaran")
    model_pembelajaran = st.text_input("Model Pembelajaran (Kosongkan untuk rekomendasi)")

    if st.button("🚀 Proses RPP"):
        with st.spinner("AI sedang memproses..."):
            model = genai.GenerativeModel('gemini-3-flash-preview')
            
            if model_pembelajaran.strip() == "":
                prompt = f"""
                Berikan 3 rekomendasi model pembelajaran untuk materi {materi} dan TP {tp}.
                Jelaskan kelebihan dan kekurangannya.
                Setelah memberikan rekomendasi, TULISKAN PERINTAH INI: 
                'Silakan salin nama model yang Anda pilih, masukkan ke dalam kolom Model Pembelajaran di web ini, lalu klik kembali tombol Proses RPP.'
                """
            else:
                prompt = f"""
                Buat RPP Madrasah lengkap dengan format tabel untuk:
                Identitas: {nama_madrasah}, {nama_guru}, {mata_pelajaran}
                TP: {tp}
                Materi: {materi}
                Model: {model_pembelajaran}
                Gunakan narasi KBC (Kurikulum Berbasis Cinta) dan pastikan formatnya rapi.
                """

            response = model.generate_content(prompt)
            st.session_state["hasil_rpp"] = response.text

    if "hasil_rpp" in st.session_state:
        st.markdown(st.session_state["hasil_rpp"])
        st.download_button("📥 Unduh Hasil RPP (.docx)", data=markdown_to_docx(st.session_state["hasil_rpp"]), file_name="RPP.docx")
