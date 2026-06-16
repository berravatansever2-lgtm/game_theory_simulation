# Finansal Veri ile Oyun Teorisi Simülasyonu 📊🐍

Bu proje, finansal piyasa verilerini kullanarak oyun teorisi stratejilerini ve matematiksel modelleri simüle eden gelişmiş bir Python uygulamasıdır. `yfinance` entegrasyonu sayesinde borsa endeksleri (S&P 500 vb.) üzerinde istatistiksel analizler gerçekleştirir.

## 🔥 Özellikler
- **Gerçek Zamanlı Entegrasyon:** Yahoo Finance API kullanarak güncel finansal veri çekimi.
- **İstatistiksel Modelleme:** `SciPy` ve `NumPy` ile rastsal yürüyüş (random walk) ve olasılık dağılımları analizi.
- **Görsel Analiz:** Strateji sonuçlarının `Matplotlib` kütüphanesi yardımıyla grafiksel olarak çizdirilmesi.

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edin:

1. Bu depoyu bilgisayarınıza klonlayın veya indirin.
2. Projenin bulunduğu klasörde bir terminal açın ve gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Simülasyonu başlatın:
   ```bash
   python simulation.py
   ```

## 📦 Kullanılan Teknolojiler
- **Python 3**
- **yfinance** (Finansal Veri Çekimi)
- **NumPy & SciPy** (Matematik ve İstatistik Hesaplamaları)
- **Matplotlib** (Veri Görselleştirme)
