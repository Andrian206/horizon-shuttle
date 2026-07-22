
# Create sample knowledge base documents for the user

import os
os.makedirs('/home/aeuvro/Code/horizon-shuttle/data', exist_ok=True)

documents = {
    "01_company_profile.txt": """HORIZON SHUTTLE — COMPANY PROFILE

Tentang Kami
Horizon Shuttle adalah perusahaan jasa transportasi shuttle antar kota yang berdiri sejak tahun 2018. Didirikan oleh Bapak Ahmad Rizky di Bandung, Jawa Barat, dengan visi menjadi penyedia layanan shuttle terpercaya dan nyaman di Indonesia.

Visi
Menjadi perusahaan shuttle antar kota terdepan yang mengutamakan keselamatan, kenyamanan, dan kepuasan pelanggan.

Misi
1. Memberikan layanan transportasi yang aman, nyaman, dan tepat waktu.
2. Menggunakan armada berkualitas dengan perawatan rutin.
3. Mengutamakan kepuasan pelanggan melalui pelayanan profesional.
4. Terus berinovasi dalam teknologi dan layanan untuk kemudahan pelanggan.

Nilai Perusahaan
- Safety First: Keselamatan adalah prioritas utama.
- Customer Centric: Pelanggan adalah pusat dari setiap keputusan.
- Integrity: Jujur dan transparan dalam setiap layanan.
- Excellence: Selalu berusaha memberikan yang terbaik.

Kontak
- Telepon: 022-1234-5678
- WhatsApp: 0812-3456-7890
- Email: info@horizonshuttle.id
- Website: www.horizonshuttle.id

Jam Operasional
- Senin – Jumat: 05.00 – 22.00 WIB
- Sabtu: 05.00 – 20.00 WIB
- Minggu & Hari Libur Nasional: 06.00 – 18.00 WIB

Kantor Pusat
Jl. Soekarno-Hatta No. 123, Bandung, Jawa Barat 40266
""",

    "02_service_catalog.txt": """HORIZON SHUTTLE — SERVICE CATALOG

Kami menyediakan tiga kelas layanan untuk memenuhi kebutuhan perjalanan Anda:

1. ECONOMY CLASS
Harga: Rp 150.000 per orang per trip
Fasilitas:
- AC (Air Conditioner)
- Kursi konfigurasi 2-2 (4 kursi per baris)
- Snack dan air mineral
- USB charging port per kursi
- Bagasi kabin 7 kg + bagasi 20 kg
- Musik dan hiburan ringan

2. BUSINESS CLASS
Harga: Rp 250.000 per orang per trip
Fasilitas:
- AC premium dengan filter udara
- Kursi konfigurasi 2-1 (3 kursi per baris, lebih lega)
- Kursi reclining dengan footrest
- TV layar sentuh per kursi
- Meal box (makanan ringan + minum)
- USB charging port + colokan listrik
- WiFi onboard
- Bagasi kabin 10 kg + bagasi 30 kg
- Prioritas boarding

3. EXECUTIVE CLASS
Harga: Rp 400.000 per orang per trip
Fasilitas:
- AC premium dengan ionizer
- Kursi konfigurasi 1-1 (2 kursi per baris, sangat lega)
- Kursi full reclining (hampir flat)
- TV layar besar per kursi dengan konten premium
- Meal box lengkap (makanan berat + minum + dessert)
- USB charging + colokan listrik + wireless charging
- WiFi onboard high-speed
- Selimut dan bantal
- Bagasi kabin 15 kg + bagasi 40 kg
- Priority boarding + priority check-in
- Lounge access (di terminal tertentu)
- Gratis snack dan minum sepanjang perjalanan

Ketentuan Umum
- Anak di bawah 3 tahun: gratis (tidak mendapat kursi)
- Anak 3-10 tahun: diskon 30% dari harga dewasa
- Pemesanan minimal 2 jam sebelum keberangkatan
- Reschedule bisa dilakukan maksimal 1x dengan biaya administrasi Rp 25.000
""",

    "03_route_schedule.txt": """HORIZON SHUTTLE — ROUTE & SCHEDULE

Rute dan Jadwal Keberangkatan Horizon Shuttle:

1. BANDUNG ↔ JAKARTA
Estimasi perjalanan: 3 jam
Jadwal keberangkatan dari Bandung:
- 06.00 WIB — Terminal Leuwi Panjang
- 09.00 WIB — Terminal Leuwi Panjang
- 12.00 WIB — Terminal Leuwi Panjang
- 15.00 WIB — Terminal Leuwi Panjang
- 18.00 WIB — Terminal Leuwi Panjang

Jadwal keberangkatan dari Jakarta:
- 06.00 WIB — Terminal Kampung Rambutan
- 09.00 WIB — Terminal Kampung Rambutan
- 12.00 WIB — Terminal Kampung Rambutan
- 15.00 WIB — Terminal Kampung Rambutan
- 18.00 WIB — Terminal Kampung Rambutan

Titik jemput (door-to-door) tersedia untuk kelas Business dan Executive.

2. BANDUNG ↔ CIREBON
Estimasi perjalanan: 2.5 jam
Jadwal keberangkatan dari Bandung:
- 07.00 WIB — Terminal Leuwi Panjang
- 13.00 WIB — Terminal Leuwi Panjang
- 17.00 WIB — Terminal Leuwi Panjang

Jadwal keberangkatan dari Cirebon:
- 07.00 WIB — Terminal Harjamukti
- 13.00 WIB — Terminal Harjamukti
- 17.00 WIB — Terminal Harjamukti

3. BANDUNG ↔ YOGYAKARTA
Estimasi perjalanan: 8 jam
Jadwal keberangkatan dari Bandung:
- 20.00 WIB — Terminal Leuwi Panjang (night trip)

Jadwal keberangkatan dari Yogyakarta:
- 20.00 WIB — Terminal Giwangan (night trip)

4. BANDUNG ↔ SEMARANG
Estimasi perjalanan: 7 jam
Jadwal keberangkatan dari Bandung:
- 19.00 WIB — Terminal Leuwi Panjang (night trip)

Jadwal keberangkatan dari Semarang:
- 19.00 WIB — Terminal Terboyo (night trip)

Catatan Penting:
- Waktu keberangkatan bisa berubah karena kondisi lalu lintas.
- Penumpang diharapkan datang 30 menit sebelum jadwal.
- Untuk night trip, penumpang disarankan membawa selimut sendiri (tersedia di kelas Executive).
""",

    "04_fleet_info.txt": """HORIZON SHUTTLE — FLEET INFORMATION

Armada Horizon Shuttle selalu dalam kondisi prima dengan perawatan rutin setiap 5.000 km.

1. TOYOTA HIACE
Kapasitas: 15 penumpang
Kelas: Economy, Business
Fasilitas:
- AC double blower
- Kursi reclining
- Audio system
- Bagasi belakang luas
- USB charging port

2. ISUZU ELF (LONG)
Kapasitas: 20 penumpang
Kelas: Economy, Business
Fasilitas:
- AC powerful
- Kursi reclining dengan footrest
- TV LED 32 inch
- Audio system premium
- Bagasi samping dan belakang
- USB charging port per kursi

3. MEDIUM BUS (MERCEDES-BENZ)
Kapasitas: 33 penumpang
Kelas: Business, Executive
Fasilitas:
- AC premium dengan ionizer
- Kursi reclining full (Executive)
- TV LED per kursi (Executive) / TV LED besar (Business)
- WiFi onboard
- Toilet onboard (Executive)
- Mini pantry (Executive)
- Bagasi luas di bawah dan belakang

4. PREMIUM COASTER (TOYOTA)
Kapasitas: 25 penumpang
Kelas: Executive
Fasilitas:
- AC premium
- Kursi full reclining dengan leg rest
- TV layar sentuh per kursi
- WiFi high-speed
- Toilet onboard
- Mini pantry
- Bagasi luas

Kebijakan Armada:
- Umur armada maksimal 5 tahun
- Perawatan rutin setiap 5.000 km
- Pemeriksaan keamanan harian sebelum keberangkatan
- Sopir berpengalaman minimal 5 tahun
- Semua armada dilengkapi GPS tracking
""",

    "05_faq.txt": """HORIZON SHUTTLE — FREQUENTLY ASKED QUESTIONS (FAQ)

BAGASI
Q: Berapa batas bagasi yang diperbolehkan?
A: Batas bagasi bervariasi sesuai kelas:
   - Economy: 20 kg + kabin 7 kg
   - Business: 30 kg + kabin 10 kg
   - Executive: 40 kg + kabin 15 kg

Q: Bagaimana jika bagasi melebihi batas?
A: Biaya kelebihan bagasi Rp 15.000 per kg.

Q: Apakah boleh membawa barang pecah belah?
A: Boleh, asalkan dikemas dengan aman. Horizon Shuttle tidak bertanggung jawab atas kerusakan barang pecah belah.

REFUND
Q: Bagaimana cara refund tiket?
A: Refund dapat diajukan minimal 24 jam sebelum keberangkatan melalui:
   - WhatsApp: 0812-3456-7890
   - Email: refund@horizonshuttle.id
   - Aplikasi/website (jika tersedia)

Q: Berapa biaya refund?
A: Biaya administrasi refund 20% dari harga tiket. Dana dikembalikan dalam 3-5 hari kerja.

Q: Apakah bisa refund setelah keberangkatan?
A: Tidak bisa. Refund hanya untuk tiket yang belum digunakan.

RESCHEDULE
Q: Bagaimana cara reschedule?
A: Reschedule bisa dilakukan maksimal 4 jam sebelum keberangkatan dengan biaya administrasi Rp 25.000.

Q: Berapa kali reschedule diperbolehkan?
A: Maksimal 1x per tiket.

PEMBAYARAN
Q: Metode pembayaran apa saja yang diterima?
A: Transfer bank, QRIS, e-wallet (GoPay, OVO, DANA, LinkAja), dan kartu kredit.

Q: Apakah ada DP (uang muka)?
A: Ya, DP minimal 50% dari total harga. Pelunasan maksimal 2 jam sebelum keberangkatan.

PEMBATALAN
Q: Bagaimana jika bus dibatalkan oleh Horizon Shuttle?
A: Penumpang akan mendapat:
   - Refund 100% tanpa biaya administrasi, ATAU
   - Reschedule gratis ke jadwal lain.

CHECK-IN
Q: Kapan harus check-in?
A: Penumpang diharapkan datang 30 menit sebelum jadwal keberangkatan.

Q: Apa yang perlu dibawa saat check-in?
A: Kode booking (digital/print) dan identitas diri (KTP/SIM/Passport).

BARANG HILANG
Q: Bagaimana jika ada barang tertinggal?
A: Hubungi customer service segera:
   - Telepon: 022-1234-5678
   - WhatsApp: 0812-3456-7890
   Barang yang ditemukan akan disimpan selama 30 hari.

HEWAN PELIHARAAN
Q: Boleh membawa hewan peliharaan?
A: Hewan kecil dalam kandang (kucing, kelinci) diperbolehkan dengan biaya tambahan Rp 50.000. Anjing hanya diperbolehkan dalam kandang ukuran kecil.
""",

    "06_company_policies.txt": """HORIZON SHUTTLE — COMPANY POLICIES

KEBIJAKAN REFUND
1. Refund dapat diajukan minimal 24 jam sebelum jadwal keberangkatan.
2. Biaya administrasi refund: 20% dari harga tiket.
3. Dana refund akan dikembalikan dalam 3-5 hari kerja ke rekening/rekening e-wallet asal pembayaran.
4. Refund tidak berlaku untuk tiket yang sudah digunakan atau melewati jadwal keberangkatan.
5. Dalam kasus pembatalan dari pihak Horizon Shuttle, refund 100% tanpa biaya administrasi.

KEBIJAKAN RESCHEDULE
1. Reschedule dapat dilakukan maksimal 4 jam sebelum keberangkatan.
2. Biaya administrasi reschedule: Rp 25.000 per tiket.
3. Reschedule hanya diperbolehkan 1x per tiket.
4. Reschedule ke hari yang sama atau berbeda diperbolehkan, tergantung ketersediaan kursi.
5. Reschedule tidak berlaku untuk tiket promo tertentu (akan diinformasikan saat pembelian).

KEBIJAKAN BAGASI
1. Bagasi gratis sesuai kelas layanan (lihat Service Catalog).
2. Kelebihan bagasi dikenakan biaya Rp 15.000 per kg.
3. Barang berharga (emas, perhiasan, uang tunai) disarankan tidak dimasukkan ke bagasi.
4. Horizon Shuttle tidak bertanggung jawab atas kehilangan barang berharga di bagasi.
5. Barang terlarang: senjata, bahan peledak, narkoba, dan barang ilegal lainnya.

KEBIJAKAN KETERLAMBATAN
1. Keterlambatan keberangkatan karena faktor cuaca atau lalu lintas:
   - Horizon Shuttle akan memberikan informasi terkini melalui WhatsApp/SMS.
   - Penumpang berhak reschedule gratis atau refund penuh.
2. Keterlambatan penumpang:
   - Penumpang yang terlambat lebih dari 15 menit dianggap no-show.
   - Tiket hangus dan tidak bisa refund.
3. Keterlambatan kedatangan:
   - Estimasi waktu hanya perkiraan. Horizon Shuttle tidak bertanggung jawab atas kerugian akibat keterlambatan kedatangan.

KEBIJAKAN KOMPENSASI
1. Kompensasi diberikan dalam bentuk:
   - Voucher perjalanan (nominal sesuai ketentuan)
   - Refund parsial (untuk kasus tertentu)
   - Upgrade kelas gratis (jika tersedia)
2. Kompensasi tidak berlaku untuk keterlambatan akibat force majeure (bencana alam, kerusuhan, dll).
3. Klaim kompensasi harus diajukan dalam 7 hari setelah kejadian.

KEBIJAKAN KEAMANAN
1. Setiap penumpang wajib menunjukkan identitas saat check-in.
2. Bagasi akan diperiksa secara acak untuk keamanan.
3. Dilarang membawa barang terlarang (senjata, bahan peledak, narkoba).
4. Pelanggaran keamanan akan dilaporkan ke pihak berwenang.
""",

    "07_cs_sop.txt": """HORIZON SHUTTLE — CUSTOMER SERVICE SOP

STANDAR PELAYANAN CUSTOMER SERVICE

1. TONE OF VOICE
- Ramah dan sopan dalam setiap interaksi.
- Gunakan bahasa Indonesia yang baik dan benar.
- Hindari bahasa gaul yang berlebihan, kecuali sesuai konteks pelanggan.
- Selalu sapa pelanggan: "Selamat [pagi/siang/sore/malam], Horizon Shuttle siap membantu."
- Akhiri dengan: "Terima kasih telah memilih Horizon Shuttle. Ada yang lain bisa kami bantu?"

2. WAKTU RESPON
- Chat/WhatsApp: maksimal 5 menit pada jam operasional.
- Email: maksimal 24 jam.
- Telepon: diangkat dalam 3 dering.

3. MENANGANI KOMPLAIN
Langkah-langkah:
   a. Dengarkan keluhan pelanggan dengan penuh perhatian.
   b. Ucapkan permintaan maaf atas ketidaknyamanan.
   c. Konfirmasi pemahaman: "Jadi yang Bapak/Ibu maksud adalah..."
   d. Tawarkan solusi sesuai kebijakan perusahaan.
   e. Jika solusi tidak memungkinkan, eskalasi ke supervisor.
   f. Follow up dalam 24 jam setelah penyelesaian.

4. MENANGANI REFUND REQUEST
   a. Verifikasi data pemesanan (kode booking, nama, tanggal).
   b. Periksa apakah masih dalam batas waktu refund (24 jam sebelum keberangkatan).
   c. Jelaskan biaya administrasi 20%.
   d. Konfirmasi rekening pengembalian dana.
   e. Proses refund dan berikan estimasi waktu (3-5 hari kerja).
   f. Kirimkan bukti pengajuan refund via email/WhatsApp.

5. MENANGANI RESCHEDULE REQUEST
   a. Verifikasi data pemesanan.
   b. Periksa ketersediaan kursi di jadwal baru.
   c. Jelaskan biaya administrasi Rp 25.000.
   d. Konfirmasi jadwal baru dengan pelanggan.
   e. Kirimkan tiket baru via email/WhatsApp.

6. MENANGANI BARANG HILANG
   a. Catat detail barang (jenis, warna, ciri khas, perkiraan lokasi tertinggal).
   b. Hubungi tim operasional untuk pengecekan armada.
   c. Berikan estimasi waktu pengecekan (2-4 jam).
   d. Jika ditemukan, informasikan cara pengambilan:
      - Ambil di kantor pusat, atau
      - Kirim via kurir (biaya ditanggung pemilik).
   e. Jika tidak ditemukan, berikan surat keterangan kehilangan.

7. ESCALATION MATRIX
   - Level 1: Customer Service (komplain umum, refund, reschedule)
   - Level 2: Supervisor (komplain berat, kompensasi, kecelakaan)
   - Level 3: Manager (kasus hukum, media, kebijakan khusus)

8. JAM OPERASIONAL CS
   - Senin–Jumat: 05.00–22.00 WIB
   - Sabtu: 05.00–20.00 WIB
   - Minggu & Libur: 06.00–18.00 WIB
   - Luar jam operasional: auto-reply + follow up pagi hari.
""",

    "08_marketing_guideline.txt": """HORIZON SHUTTLE — MARKETING GUIDELINE

BRAND IDENTITY

Brand Personality
- Trustworthy: Pelanggan bisa percaya pada keselamatan dan kenyamanan.
- Friendly: Pendekatan yang hangat dan tidak kaku.
- Professional: Layanan berkualitas dengan standar tinggi.
- Innovative: Selalu mengadopsi teknologi terbaru untuk kenyamanan.

Tone of Voice
- Bahasa: Indonesia (utama), English (opsional untuk turis).
- Gaya: Conversational, tidak terlalu formal tapi tetap profesional.
- Hindari: bahasa yang menyinggung, klaim berlebihan, perbandingan negatif dengan kompetitor.

Warna Brand
- Primary: #0050CB (Biru Horizon)
- Secondary: #00DBE9 (Cyan)
- Accent: #A33200 (Oranye hangat)
- Neutral: #F7F9FB (Putih kebiruan)

CALL TO ACTION (CTA)
- Primary: "Pesan Sekarang", "Booking Tiket"
- Secondary: "Cek Jadwal", "Hubungi Kami"
- Soft: "Pelajari Lebih Lanjut", "Lihat Rute"

TARGET MARKET
1. Primary: Pelajar & mahasiswa (18-25 tahun) — harga terjangkau, rute Bandung-Jakarta.
2. Secondary: Pekerja kantoran (25-40 tahun) — kelas Business, door-to-door.
3. Tertiary: Keluarga & turis (30-50 tahun) — kelas Executive, rute wisata.

CHANNEL MARKETING
1. Instagram: Konten visual armada, rute, testimoni. Posting 1x/hari.
2. TikTok: Video pendek perjalanan, tips traveling, behind the scenes. Posting 3x/minggu.
3. WhatsApp Broadcast: Promo, pengumuman, reminder. Kirim 2x/minggu.
4. Email Newsletter: Update bulanan, promo eksklusif.
5. Google My Business: Update jam, foto, respon review.

JENIS KONTEN
1. Edukasi: Tips traveling, packing tips, info rute.
2. Promosi: Diskon, bundle, early bird.
3. Testimoni: Review pelanggan, before-after.
4. Behind the Scenes: Perawatan armada, training sopir.
5. Interactive: Poll, quiz, giveaway.

KEBIJAKAN PROMO
- Promo tidak boleh lebih dari 50% dari harga normal.
- Periode promo minimal 3 hari, maksimal 14 hari.
- Promo tidak berlaku untuk hari libur nasional (kecuali dinyatakan).
- Promo tidak bisa digabung dengan promo lain.
""",

    "09_promotional_campaign.txt": """HORIZON SHUTTLE — PROMOTIONAL CAMPAIGNS

PROMO AKTIF

1. PROMO LIBURAN (Musim Libur Sekolah & Lebaran)
Periode: 15 Juni – 15 Juli, 1–15 Ramadhan
Diskon: 20% untuk semua kelas
Kode Promo: LIBURAN20
Syarat:
- Pemesanan minimal 3 hari sebelum keberangkatan
- Berlaku untuk rute Bandung-Jakarta dan Bandung-Cirebon
- Tidak berlaku untuk hari H keberangkatan

2. PROMO MAHASISWA
Periode: Berlaku terus (ongoing)
Diskon: 25% untuk kelas Economy
Kode Promo: MAHASISWA25
Syarat:
- Menunjukkan kartu mahasiswa aktif saat check-in
- Berlaku untuk rute Bandung-Jakarta
- Maksimal 2 tiket per mahasiswa per trip
- Tidak berlaku saat peak season (Lebaran, Natal)

3. PROMO WEEKEND
Periode: Setiap Jumat–Minggu
Diskon: 15% untuk kelas Business
Kode Promo: WEEKEND15
Syarat:
- Pemesanan minimal 1 hari sebelum keberangkatan
- Berlaku untuk semua rute
- Berlaku untuk keberangkatan Jumat, Sabtu, Minggu

4. PROMO AKHIR TAHUN
Periode: 20 Desember – 5 Januari
Diskon: 30% untuk semua kelas
Kode Promo: TAHUNBARU30
Syarat:
- Pemesanan minimal 7 hari sebelum keberangkatan
- Berlaku untuk semua rute
- Kuota terbatas (500 tiket)

5. PROMO BUNDLE KELUARGA
Periode: Berlaku terus
Diskon: Beli 4 tiket, bayar 3 (kelas Economy & Business)
Kode Promo: KELUARGA4PAY3
Syarat:
- Minimal 4 penumpang dalam 1 pemesanan
- Berlaku untuk semua rute
- Anak di atas 3 tahun dihitung sebagai 1 penumpang

6. PROMO EARLY BIRD
Periode: Berlaku terus
Diskon: 10% untuk pemesanan 14 hari sebelum keberangkatan
Kode Promo: EARLYBIRD10
Syarat:
- Pemesanan minimal 14 hari sebelum keberangkatan
- Berlaku untuk semua kelas dan rute
- Tidak bisa digabung dengan promo lain

7. PROMO ULANG TAHUN HORIZON
Periode: 15 Agustus (HUT Horizon Shuttle)
Diskon: 50% untuk 50 penumpang pertama
Kode Promo: HUT50
Syarat:
- Kuota sangat terbatas (50 tiket)
- Berlaku untuk semua kelas dan rute
- 1 tiket per orang

CARA MENGGUNAKAN PROMO
1. Pilih tiket di website/aplikasi.
2. Masukkan kode promo saat checkout.
3. Diskon akan otomatis terpotong.
4. Selesaikan pembayaran.

CATATAN
- Promo tidak berlaku untuk hari libur nasional (kecuali dinyatakan).
- Promo tidak bisa digabung dengan promo lain.
- Horizon Shuttle berhak mengubah atau menghentikan promo sewaktu-waktu.
""",

    "10_business_reports.txt": """HORIZON SHUTTLE — BUSINESS REPORTS (DATA DUMMY)

LAPORAN PENJUALAN BULANAN (JANUARI – JUNI 2026)

Bulan    | Total Tiket | Pendapatan    | Rata-rata per Tiket
---------|-------------|---------------|--------------------
Januari  | 2.450       | Rp 612.500.000| Rp 250.000
Februari | 2.180       | Rp 545.000.000| Rp 250.000
Maret    | 2.890       | Rp 722.500.000| Rp 250.000
April    | 3.120       | Rp 780.000.000| Rp 250.000
Mei      | 3.450       | Rp 862.500.000| Rp 250.000
Juni     | 3.680       | Rp 920.000.000| Rp 250.000

Total Semester 1: 17.770 tiket, Rp 4.442.500.000

OKUPANSI PER RUTE (JUNI 2026)

Rute              | Kapasitas/Bulan | Terisi | Okupansi
------------------|-----------------|--------|----------
Bandung-Jakarta   | 4.500           | 3.890  | 86.4%
Bandung-Cirebon   | 2.700           | 2.340  | 86.7%
Bandung-Yogyakarta| 900             | 720    | 80.0%
Bandung-Semarang  | 900             | 680    | 75.6%

OKUPANSI PER KELAS (JUNI 2026)

Kelas      | Total Penjualan | Persentase
-----------|-----------------|------------
Economy    | 2.208 tiket     | 60.0%
Business   | 1.104 tiket     | 30.0%
Executive  | 368 tiket       | 10.0%

RUTE PALING RAMAI (TOP 3 JUNI 2026)
1. Bandung-Jakarta (pukul 18.00 WIB) — 780 penumpang
2. Bandung-Jakarta (pukul 06.00 WIB) — 720 penumpang
3. Bandung-Cirebon (pukul 07.00 WIB) — 650 penumpang

RUTE PALING SEPI (BOTTOM 2 JUNI 2026)
1. Bandung-Semarang (night trip) — 680 penumpang (75.6% okupansi)
2. Bandung-Yogyakarta (night trip) — 720 penumpang (80.0% okupansi)

PROMO PALING EFEKTIF (JUNI 2026)
1. Promo Mahasiswa — 520 tiket terjual
2. Promo Weekend — 480 tiket terjual
3. Promo Early Bird — 350 tiket terjual

KELUHAN PELANGGAN (JUNI 2026)
Kategori          | Jumlah | Persentase
------------------|--------|------------
Keterlambatan     | 45     | 35%
AC tidak dingin   | 28     | 22%
Kursi tidak nyaman| 20     | 16%
Sopir kurang ramah| 15     | 12%
Lainnya           | 19     | 15%
Total             | 127    | 100%

REKOMENDASI STRATEGIS
1. Tambah 1 trip Bandung-Jakarta pukul 15.00 (demand tinggi).
2. Evaluasi rute night trip — pertimbangkan diskon tambahan.
3. Perbaiki maintenance AC (22% keluhan).
4. Training sopir customer service (12% keluhan).
5. Promo Mahasiswa efektif — perluas ke rute Cirebon.
""",

    "11_customer_reviews.txt": """HORIZON SHUTTLE — CUSTOMER REVIEWS (DATA DUMMY)

ULASAN POSITIF

1. "Perjalanan Bandung-Jakarta sangat nyaman. Sopirnya ramah dan profesional. AC dingin, kursi bersih. Pasti naik lagi!" — Rina, 24 tahun, Mahasiswa

2. "Saya sering pakai Horizon Shuttle untuk business trip. Kelas Business worth it banget — reclining seat, WiFi, dan meal box. Recommended!" — Budi, 35 tahun, Karyawan Swasta

3. "Pertama kali coba kelas Executive ke Yogyakarta. Pengalaman luar biasa! Kursi hampir flat, ada selimut dan bantal. Tidur nyenyak sepanjang perjalanan." — Siti, 42 tahun, Ibu Rumah Tangga

4. "Promo mahasiswa sangat membantu. Harga terjangkau tapi kualitas tetap oke. Terima kasih Horizon Shuttle!" — Andi, 20 tahun, Mahasiswa

5. "Door-to-door service-nya sangat membantu. Saya tinggal di Cimahi, dijemput di rumah dan diantar sampai tujuan di Jakarta. Praktis!" — Dedi, 38 tahun, Wiraswasta

6. "Armadanya bersih dan wangi. Terlihat terawat dengan baik. Suka banget sama kebersihannya." — Maya, 29 tahun, Desainer

7. "Customer service responsif. Saya reschedule via WhatsApp dan langsung diproses dalam 10 menit." — Fajar, 31 tahun, Karyawan

8. "Anak saya suka naik Horizon Shuttle. Ada TV dan snack, jadi dia tidak rewel sepanjang perjalanan." — Lina, 36 tahun, Ibu Rumah Tangga

ULASAN KONSTRUKTIF / NEGATIF

1. "Bus terlambat 30 menit dari jadwal. Tidak ada informasi yang jelas. Mohon diperbaiki komunikasinya." — Ahmad, 28 tahun, Karyawan

2. "AC di kursi saya tidak terlalu dingin. Mungkin perlu dicek maintenance-nya." — Putri, 26 tahun, Freelancer

3. "Sopirnya agak ugal-ugalan. Kecepatan stabil saja sudah cukup, tidak perlu ngebut." — Hendra, 45 tahun, PNS

4. "Toilet di bus tidak bersih. Bau dan tidak ada tissue. Mohon diperhatikan kebersihannya." — Nina, 33 tahun, Karyawan

5. "WiFi di kelas Business lemot banget. Tidak bisa dipakai kerja. Harap diperbaiki." — Rudi, 30 tahun, Programmer

6. "Tempat duduk agak sempit untuk saya yang bertubuh besar. Mungkin perlu pertimbangkan kursi yang lebih lebar." — Bayu, 40 tahun, Pengusaha

7. "Proses refund lama. Sudah 7 hari belum masuk ke rekening. Mohon dipercepat." — Citra, 27 tahun, Guru

8. "Pengumuman keterlambatan baru diberitahu 1 jam sebelum keberangkatan. Saya sudah di jalan. Sebaiknya diberitahu lebih awal." — Yoga, 32 tahun, Karyawan

RINGKASAN SENTIMEN
- Positif: 78%
- Netral: 12%
- Negatif: 10%

TOPIK PALING SERING DIBICARAKAN
1. Kenyamanan kursi (positif)
2. Keterlambatan (negatif)
3. Kebersihan armada (positif & negatif)
4. Sopir (positif & negatif)
5. Harga/promo (positif)
""",

    "12_internal_sop.txt": """HORIZON SHUTTLE — INTERNAL SOP

SOP 1: BUS TERLAMBAT
1. Identifikasi penyebab keterlambatan (lalu lintas, cuaca, armada rusak).
2. Informasikan ke penumpang via WhatsApp/SMS minimal 30 menit sebelum jadwal.
3. Berikan estimasi waktu keberangkatan baru.
4. Tawarkan opsi:
   a. Tunggu keberangkatan baru
   b. Reschedule gratis ke jadwal lain
   c. Refund penuh (jika keterlambatan > 2 jam)
5. Dokumentasikan insiden untuk laporan.
6. Berikan kompensasi sesuai kebijakan:
   - 30-60 menit: voucher Rp 25.000
   - 1-2 jam: voucher Rp 50.000
   - >2 jam: refund penuh + voucher Rp 50.000

SOP 2: ARMADA RUSAK DI TENGAH PERJALANAN
1. Sopir segera berhenti di tempat aman.
2. Hubungi tim operasional untuk bantuan.
3. Informasikan penumpang dengan tenang dan jelas.
4. Tawarkan:
   a. Tunggu armada pengganti (estimasi 1-2 jam)
   b. Refund penuh + transportasi alternatif
5. Dokumentasikan kerusakan untuk maintenance.
6. Pastikan penumpang aman dan nyaman selama menunggu.

SOP 3: PROSES REFUND INTERNAL
1. CS terima request refund dari pelanggan.
2. Verifikasi data pemesanan di sistem.
3. Periksa apakah masih dalam batas waktu (24 jam sebelum keberangkatan).
4. Jika lolos verifikasi:
   a. Hitung refund: harga tiket - 20% biaya admin
   b. Input ke sistem refund
   c. Proses ke finance dalam 24 jam
   d. Finance transfer dalam 3-5 hari kerja
   e. Kirimkan bukti transfer ke pelanggan
5. Jika tidak lolos verifikasi:
   a. Jelaskan alasan penolakan
   b. Tawarkan opsi reschedule

SOP 4: KEHILANGAN BARANG PENUMPANG
1. CS catat detail barang dan data penumpang.
2. Hubungi sopir dan tim cleaning untuk pengecekan armada.
3. Berikan estimasi waktu pengecekan (2-4 jam).
4. Jika ditemukan:
   a. Foto barang dan kirim ke penumpang untuk konfirmasi
   b. Simpan di kantor pusat (maksimal 30 hari)
   c. Informasikan cara pengambilan atau pengiriman
5. Jika tidak ditemukan:
   a. Berikan surat keterangan kehilangan
   b. Tawarkan kompensasi sesuai kebijakan (jika berlaku)

SOP 5: MENANGANI KOMPLAIN BERAT
1. Dengarkan dengan empati, jangan interupsi.
2. Ucapkan permintaan maaf yang tulus.
3. Konfirmasi pemahaman keluhan.
4. Tawarkan solusi sesuai kebijakan.
5. Jika penumpang tidak puas dengan solusi:
   a. Eskalasi ke supervisor dalam 15 menit
   b. Supervisor ambil alih penanganan
   c. Jika masih tidak puas, eskalasi ke manager
6. Follow up dalam 24 jam.
7. Dokumentasikan seluruh insiden.

SOP 6: KECELAKAAN / EMERGENCY
1. Prioritaskan keselamatan penumpang dan crew.
2. Hubungi emergency services (119 / 110).
3. Hubungi tim operasional dan manajemen.
4. Dokumentasikan kejadian (foto, video, saksi).
5. Berikan pernyataan resmi sesuai arahan manajemen.
6. Koordinasi dengan asuransi.
7. Berikan support psikologis kepada penumpang (jika diperlukan).
8. Lakukan investigasi internal.
9. Update SOP berdasarkan lesson learned.

SOP 7: PERAWATAN ARMADA
1. Pemeriksaan harian (pre-trip):
   - Ban, oli, rem, lampu
   - AC, audio, TV
   - Kebersihan interior
   - Kelengkapan safety (APAR, P3K, palu pemecah kaca)
2. Perawatan rutin (setiap 5.000 km):
   - Ganti oli dan filter
   - Periksa rem dan kopling
   - Periksa sistem kelistrikan
   - Cuci AC
3. Perawatan besar (setiap 50.000 km):
   - Overhaul mesin
   - Ganti sparepart yang aus
   - Pengecekan sistem keseluruhan
4. Dokumentasikan semua perawatan.
"""
}

# Write all files
for filename, content in documents.items():
    filepath = f'/home/aeuvro/Code/horizon-shuttle/data/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {filename} — {len(content)} chars, ~{content.count(chr(10))} lines")

print(f"\n🎉 Total 12 files created in /home/aeuvro/Code/horizon-shuttle/data")
