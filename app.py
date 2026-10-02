import datetime
import pandas as pd
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(
    page_title="Lecturer Task Prioritizer", page_icon="📑", layout="centered"
)

st.title("📑 Smart Task Prioritizer for Lecturers")
st.write(
    "Aplikasi sederhana untuk mengurutkan prioritas tugas mengajar, memeriksa berkas, dan riset berdasarkan **Weighted Scoring Algorithm** & **Eisenhower Matrix**."
)

# Inisialisasi State Penyimpanan Tugas
if "task_list" not in st.session_state:
    st.session_state.task_list = []

# --- FORM INPUT TUGAS ---
with st.form("task_form", clear_on_submit=True):
    st.subheader("➕ Tambah Tugas Baru")

    task_name = st.text_input(
        "Nama Tugas", placeholder="Contoh: Koreksi UTS Kelas A"
    )

    col1, col2 = st.columns(2)
    with col1:
        urgency = st.slider(
            "Tingkat Urgensi (Mendesak)",
            1,
            5,
            3,
            help="1 = Sangat Santai, 5 = Sangat Mendesak / H-1",
        )
    with col2:
        importance = st.slider(
            "Tingkat Kepentingan (Dampak)",
            1,
            5,
            3,
            help="1 = Dampak Kecil, 5 = Sangat Penting (Wajib)",
        )

    deadline = st.date_input("Deadline", datetime.date.today())

    submitted = st.form_submit_button("Hitung & Tambahkan")

    if submitted and task_name:
        # Algoritma Weighted Scoring: Hitung Skor Prioritas
        # Rumus: (Urgensi x 0.4) + (Kepentingan x 0.4) + (Faktor Deadline x 0.2)
        days_left = (deadline - datetime.date.today()).days
        deadline_score = max(
            1, 5 - max(0, days_left)
        )  # Makin dekat deadline, skor makin tinggi (max 5)

        priority_score = (
            (urgency * 0.4) + (importance * 0.4) + (deadline_score * 0.2)
        )

        # Penentuan Kuadran Eisenhower
        if urgency >= 3 and importance >= 3:
            quadrant = "🔴 Do First (Sangat Penting & Mendesak)"
        elif urgency < 3 and importance >= 3:
            quadrant = "🔵 Schedule (Penting, Tidak Mendesak)"
        elif urgency >= 3 and importance < 3:
            quadrant = "🟡 Delegate (Mendesak, Kurang Penting)"
        else:
            quadrant = "⚪ Don't Do / Later (Bisa Ditunda)"

        st.session_state.task_list.append({
            "Tugas": task_name,
            "Deadline": deadline.strftime("%Y-%m-%d"),
            "Skor Prioritas": round(priority_score, 2),
            "Kategori Kuadran": quadrant,
        })
        st.success(f"Tugas '{task_name}' berhasil ditambahkan!")

# --- DISPLAY & SORTING TUGAS ---
st.divider()
st.subheader("📋 Daftar Prioritas Tugas")

if st.session_state.task_list:
    # Ubah data ke Pandas DataFrame & Urutkan berdasar Skor Prioritas (Descending)
    df = pd.DataFrame(st.session_state.task_list)
    df = df.sort_values(by="Skor Prioritas", ascending=False).reset_index(
        drop=True
    )

    # Tampilkan Tabel Hasil Sorting
    st.dataframe(df, use_container_width=True)

    # Tombol Reset
    if st.button("Hapus Semua Data"):
        st.session_state.task_list = []
        st.rerun()
else:
    st.info("Belum ada tugas yang dimasukkan. Silakan isi form di atas!")
