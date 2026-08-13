import streamlit as st
import google.generativeai as genai

# Pengaturan Halaman
st.set_page_config(page_title="Generator RPP Madrasah", layout="wide")

# Konfigurasi Kunci API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Kunci API Gemini belum terdeteksi di Streamlit Secrets.")

# --- FUNGSI LOGIN ---
def check_password():
    """Mengembalikan nilai True jika pengguna sudah memasukkan password yang benar."""
    def password_entered():
        # Mengecek apakah email ada di secrets dan passwordnya cocok
        email_input = st.session_state["email"]
        pass_input = st.session_state["password"]
        
        if email_input in st.secrets["passwords"] and st.secrets["passwords"][email_input] == pass_input:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Hapus password dari memori demi keamanan
        else:
            st.session_state["password_correct"] = False

    # Jika belum login, tampilkan form login
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.title("🔒 Halaman Login")
        st.write("Silakan masukkan Email dan Password untuk mengakses Generator RPP.")
        
        # Form Login
        st.text_input("Email", key="email")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered, type="primary")
        
        # Pesan Error jika salah
        if "password_correct" in st.session_state and st.session_state["password_correct"] == False:
            st.error("Email atau Password salah! Silakan coba lagi.")
        
        return False # Hentikan proses di sini jika belum login
    return True # Lanjut ke aplikasi utama jika login berhasil

# --- APLIKASI UTAMA (Hanya berjalan jika check_password() True) ---
if check_password():
    # Tombol Logout
    if st.button("🚪 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

    st.title("🤖 Generator RPP Madrasah AI")
    st.write("Selamat datang! Silakan isi formulir di bawah ini untuk menyusun RPP utuh Anda.")

    # Form Input Data
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

    with st.expander("📚 BAGIAN B, C, & D: KOMPETENSI (Wajib)", expanded=True):
        cp = st.text_area("Capaian Pembelajaran (CP)")
        tp = st.text_area("Tujuan Pembelajaran (TP)")
        materi = st.text_area("Materi Pembelajaran (IKTP/Materi)")

    with st.expander("🛠️ BAGIAN E: MODEL PEMBELAJARAN", expanded=True):
        st.info("💡 TIPS: Kosongkan kolom ini jika Anda ingin AI memberikan 3 rekomendasi model terlebih dahulu (Tahap 1).")
        model_pembelajaran = st.text_input("Model Pembelajaran (Opsional)")

    with st.expander("📌 BAGIAN F: INFORMASI TAMBAHAN (Opsional)", expanded=False):
        karakteristik = st.text_area("Karakteristik Murid")
        media = st.text_area("Media Pembelajaran yang Tersedia")
        lingkungan = st.text_area("Lingkungan Belajar")
        catatan = st.text_area("Catatan Tambahan Guru")

    st.markdown("---")

    # Data Gabungan
    data_input = f"""
    INFORMASI AWAL PEMBELAJARAN
    A. IDENTITAS
    Nama Madrasah: {nama_madrasah}
    Nama Guru: {nama_guru}
    Mata Pelajaran: {mata_pelajaran}
    Fase/Kelas: {fase_kelas}
    Semester: {semester}
    Tahun Pelajaran: {tahun_pelajaran}
    Alokasi Waktu: {alokasi_waktu}
    Jumlah Pertemuan: {jumlah_pertemuan}

    B. CAPAIAN PEMBELAJARAN: {cp}
    C. TUJUAN PEMBELAJARAN: {tp}
    D. MATERI PEMBELAJARAN: {materi}
    E. MODEL PEMBELAJARAN: {model_pembelajaran}
    F. INFORMASI TAMBAHAN:
    - Karakteristik Murid: {karakteristik}
    - Media Pembelajaran: {media}
    - Lingkungan Belajar: {lingkungan}
    - Catatan Guru: {catatan}
    """

    if st.button("🚀 Proses RPP Sekarang", type="primary"):
        if not cp or not tp or not materi:
            st.warning("Mohon isi Capaian Pembelajaran, Tujuan Pembelajaran, dan Materi terlebih dahulu.")
        else:
            with st.spinner("AI sedang berpikir dan menyusun dokumen Anda..."):
                model = genai.GenerativeModel('gemini-3-flash-preview')
                
                if model_pembelajaran.strip() == "":
                    prompt = f"""
                    Anda bertindak sebagai Tim Pengembang Kurikulum Madrasah.
                    Berikut adalah data pembelajaran:
                    {data_input}
                    
                    # TAHAP 1 (Model Pembelajaran Kosong)
                    Analisis terlebih dahulu:
                    1. Karakteristik materi.
                    2. Tingkat kompleksitas Tujuan Pembelajaran.
                    3. Karakteristik murid berdasarkan fase dan kelas.
                    
                    Selanjutnya berikan minimal 3 rekomendasi model pembelajaran yang paling sesuai.
                    Untuk setiap model jelaskan:
                    - Alasan pedagogis.
                    - Kelebihan.
                    - Kekurangan.
                    - Alasan model tersebut paling sesuai dengan TP.
                    
                    Setelah itu BERHENTI. Jangan membuat RP.
                    """
                else:
                    prompt = f"""
                    Anda bertindak sebagai Tim Pengembang Kurikulum Madrasah (Ahli Kurikulum, Pedagogi, Guru Berprestasi, Praktisi Kurikulum Berbasis Cinta/KBC).
                    
                    Berikut adalah data pembelajaran:
                    {data_input}
                    
                    # TAHAP 2
                    Lakukan analisis internal terhadap hubungan CP dengan TP, materi, karakteristik murid, model pembelajaran, asesmen, DPL, dan KBC.
                    Lalu susun Rencana Pembelajaran (RP) UTUH menggunakan format TABEL MARKDOWN STANDAR.
                    
                    ## A. IDENTITAS
                    Tulis ulang identitas di atas.
                    
                    ## B. IDENTIFIKASI
                    Susun dalam tabel yang memuat: Kesiapan Murid, Materi Pelajaran (Faktual, Konseptual, dll), Dimensi Profil Lulusan (DPL), Topik Panca Cinta (WAJIB memuat Cinta kepada Allah dan Rasul-Nya serta Cinta kepada Ilmu), dan Materi Integrasi KBC secara naratif.
                    
                    ## C. DESAIN PEMBELAJARAN
                    Susun dalam tabel yang memuat: Capaian Pembelajaran, Lintas Disiplin Ilmu, Tujuan Pembelajaran, Topik, Praktik Pedagogis, Kemitraan, Lingkungan (fisik, budaya, digital), dan Pemanfaatan Digital beserta fungsi pedagogisnya.
                    
                    ## D. PENGALAMAN BELAJAR
                    Buat sejumlah {jumlah_pertemuan} tabel TERPISAH untuk setiap pertemuan.
                    Format WAJIB:
                    Tabel hanya memiliki dua kolom yaitu: "Tahapan Pembelajaran" dan "Pengalaman Belajar".
                    Tahapan meliputi: Awal (Berkesadaran), Inti: Memahami (Bermakna), Inti: Mengaplikasi (Menggembirakan), Refleksi, Penutup.
                    Pada kolom Pengalaman Belajar tuliskan SATU NARASI UTUH yang memuat aktivitas guru, murid, tujuan pedagogis, hubungan TP, dan integrasi KBC. Jangan pisahkan elemen ini ke dalam kolom berbeda.
                    
                    ## E. ASESMEN
                    Susun dalam tabel yang berisi Asesmen Awal, Proses, dan Akhir.
                    
                    ATURAN KHUSUS:
                    - Format TP: KKO + Materi + Kondisi + Kriteria + Penguatan Nilai KBC.
                    - Konsistensi Nilai KBC wajib dijaga dari awal hingga Refleksi.
                    - Hindari kalimat pasif/membosankan seperti "Guru menjelaskan materi". Jelaskan APA, MENGAPA, dan Bagaimana.
                    - Jangan tampilkan validasi internal di hasil akhir.
                    """
                
                try:
                    response = model.generate_content(prompt)
                    st.success("Selesai diproses!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
