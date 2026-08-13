import streamlit as st

# Pengaturan Halaman Website
st.set_page_config(page_title="Generator RPP Madrasah", layout="wide")

# Judul Website
st.title("🤖 Generator RPP Madrasah Berbasis AI")
st.write("Isi formulir di bawah ini. Biarkan AI menyusun RPP utuh Anda!")

# Bagian Identitas
with st.expander("📝 BAGIAN A: IDENTITAS (Wajib)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        nama_madrasah = st.text_input("Nama Madrasah")
        nama_guru = st.text_input("Nama Guru")
        mata_pelajaran = st.text_input("Mata Pelajaran")
        fase_kelas = st.text_input("Fase / Kelas")
    with col2:
        semester = st.text_input("Semester")
        tahun_pelajaran = st.text_input("Tahun Pelajaran")
        alokasi_waktu = st.text_input("Alokasi Waktu")
        jumlah_pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, step=1)

# Bagian Kompetensi
with st.expander("📚 BAGIAN B, C, & D: KOMPETENSI (Wajib)", expanded=True):
    cp = st.text_area("Capaian Pembelajaran (CP)")
    tp = st.text_area("Tujuan Pembelajaran (TP)")
    materi = st.text_area("Materi Pembelajaran (IKTP/Materi)")

# Bagian Model Pembelajaran
with st.expander("🛠️ BAGIAN E: MODEL PEMBELAJARAN", expanded=True):
    st.info("💡 TIPS: Kosongkan kolom ini jika Anda ingin AI menganalisis dan memberikan 3 rekomendasi model terbaik terlebih dahulu.")
    model_pembelajaran = st.text_input("Ketik Model Pembelajaran (Opsional)")

# Bagian Tambahan
with st.expander("📌 BAGIAN F: INFORMASI TAMBAHAN (Opsional)", expanded=False):
    karakteristik = st.text_area("Karakteristik Murid")
    media = st.text_area("Media Pembelajaran yang Tersedia")
    lingkungan = st.text_area("Lingkungan Belajar")
    catatan = st.text_area("Catatan Tambahan Guru")

# Tombol untuk memproses
st.markdown("---")
if st.button("🚀 Proses RPP Sekarang", type="primary"):
    st.success("Tampilan Web berhasil dibuat! Logika AI akan ditambahkan pada langkah berikutnya.")
