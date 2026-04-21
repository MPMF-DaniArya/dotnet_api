import os
import subprocess
from google import genai

# KONFIGURASI
# Jika di GitHub Action, API Key diambil dari Environment Variable
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "models/gemini-flash-latest"
client = genai.Client(api_key=API_KEY)

def get_git_diff():
    """Mengambil perubahan kode. Jika commit pertama, ambil semua file .cs."""
    try:
        # Cek apakah ini commit pertama (apakah HEAD~1 ada?)
        subprocess.check_output(["git", "rev-parse", "HEAD~1"], stderr=subprocess.DEVNULL)
        
        # JIKA BUKAN COMMIT PERTAMA: Ambil perbedaan normal
        print("🔄 Mengambil perbedaan dari commit sebelumnya...")
        return subprocess.check_output(
            ["git", "diff", "HEAD~1", "HEAD", "--", "*.cs"]
        ).decode("utf-8")

    except subprocess.CalledProcessError:
        # JIKA COMMIT PERTAMA: Ambil isi semua file .cs yang ada di folder source_code_be
        print("🐣 Commit pertama terdeteksi! Mengambil semua kode untuk inisialisasi...")
        all_code = ""
        source_dir = "source_code_be" # Sesuaikan dengan folder kodinganmu
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith(".cs"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        all_code += f"\n--- FILE: {file} ---\n"
                        all_code += f.read()
        return all_code

def generate_incremental_docs():
    print("🚀 Memulai AI Documentation Generator...")

    # 1. Persiapan Folder Output (Wajib ada agar tidak error saat git push)
    output_dir = "output_docs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Folder '{output_dir}' berhasil dibuat.")
        # Buat file kosong agar folder tidak diabaikan Git jika masih kosong
        with open(os.path.join(output_dir, ".gitkeep"), "w") as f:
            pass

    # 2. Ambil Perubahan Kode
    print("🔍 Memeriksa perubahan kode di Git...")
    diff_content = get_git_diff()

    # Cek apakah ada perubahan yang berarti (minimal 10 karakter)
    if not diff_content or len(diff_content.strip()) < 10:
        print("✅ Tidak ada perubahan kode C# yang perlu didokumentasikan.")
        return

    prompt = f"""
    Tugas: Buat dokumentasi teknis HANYA untuk fitur/endpoint baru yang ada dalam 'Git Diff' di bawah ini.
    Target: IT Developer (Backend, Mobile, Web).
    
    GIT DIFF TERBARU:
    {diff_content}
    
    Instruksi:
    1. Identifikasi nama fungsi/endpoint baru.
    2. Jelaskan Business Logic singkat dari perubahan tersebut.
    3. Berikan contoh Request & Response JSON (Success/Error).
    4. Format harus rapi menggunakan Markdown.
    5. JANGAN menulis ulang dokumentasi yang sudah ada. Cukup fokus pada apa yang baru di Diff ini.
    """

    print(f"🤖 Menghubungi AI ({MODEL_NAME})...")
    
    try:
        # 4. Panggil Gemini API
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=prompt
        )

        # 5. Simpan Hasil (Mode 'a' untuk Menambah ke bawah/Append)
        file_path = os.path.join(output_dir, "Dokumentasi_API.md")
        
        # Mengambil info waktu untuk header (Format Ubuntu/Linux)
        try:
            timestamp = subprocess.check_output(['date']).decode().strip()
        except:
            timestamp = "Auto Update"

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n")
            f.write(f"### 🆕 Update: {timestamp}\n")
            f.write(response.text)
            f.write(f"\n")
        
        print(f"✅ BERHASIL: Dokumentasi ditambahkan ke {file_path}")

    except Exception as e:
        print(f"❌ ERROR: Gagal memproses AI. Detail: {e}")

if __name__ == "__main__":
    generate_incremental_docs()