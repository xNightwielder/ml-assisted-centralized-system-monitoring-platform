# 1. Adım: Temel imajı seçiyoruz. Python 3.9'un slim versiyonu iyi bir başlangıç.
FROM python:3.12-slim

# 2. Adım: Çalışma dizinini belirliyoruz. Konteyner içindeki varsayılan dizinimiz.
WORKDIR /app

# 3. Adım: Önce sadece gereksinimler dosyasını kopyalıyoruz.
# Bu sayede, kod değişse bile kütüphaneler değişmediyse Docker bu adımı tekrar çalıştırmaz, hız kazanırız.
COPY requirements.txt .

# 4. Adım: Gerekli Python kütüphanelerini kuruyoruz.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Adım: Uygulamanın geri kalan tüm kodlarını kopyalıyoruz.
COPY . .

# 6. Adım: Konteyner çalıştığında hangi komutun çalışacağını belirtiyoruz.
# Flask uygulamasını 0.0.0.0 adresi üzerinden yayınlıyoruz ki konteyner dışından erişilebilsin.
CMD ["flask", "run", "--host=0.0.0.0"]