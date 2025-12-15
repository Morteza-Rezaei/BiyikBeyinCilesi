


# Bıyık Bey'in Çilesi 🎮

**2D Arcade Survivor Oyunu**

Bıyık Bey'in Çilesi, pygame kütüphanesi kullanılarak geliştirilmiş bir 2D arcade survivor oyunudur. Oyuncu, Bıyık Bey karakterini kontrol ederek düşmanlardan kaçınmalı, bombalardan uzak durmalı ve mümkün olduğunca uzun süre hayatta kalmalıdır.

---


# 👨‍💻 Geliştirici

- **Morteza Rezaeı**

Proje, pygame kütüphanesi kullanılarak geliştirilmiştir.

Tanıtım videosu (2 dakika): [https://youtu.be/M1T_XHGh2f4](https://youtu.be/M1T_XHGh2f4)

---

## 📋 İçindekiler

- [Özellikler](#ozellikler)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanim)
- [Oyun Mekanikleri](#oyun-mekanikleri)
- [Kontroller](#kontroller)
- [Proje Yapısı](#proje-yapisi)
- [Teknik Detaylar](#teknik-detaylar)


---


<a name="ozellikler"></a>
## ✨ Özellikler

### Oyun Özellikleri
- **Level Sistemi**: Her level 60 saniye sürer, level arttıkça zorluk artar
- **Dinamik Zorluk**: Her levelde düşman sayısı, hızı ve spawn süreleri artar
- **Rekor Sistemi**: En yüksek level kaydı tutulur ve gösterilir
- **Level Seçimi**: İstediğiniz leveldan başlayabilirsiniz (Ctrl+Start)

### Düşmanlar
- **Bomba**: Belirli süre sonra patlar, yakındaki oyuncuya hasar verir
- **Sinsi Jilet**: Yavaşça yaklaşır, belirli mesafede hızla saldırır
- **Uçan Terlik**: Ekran kenarından fırlatılır, düz çizgide oyuncuya doğru gider

### Power-up'lar
- **Çay**: +1 can verir (nadir)
- **Hız Artışı**: Oyuncuyu %50 hızlandırır (10 saniye)
- **Hız Azalışı**: Oyuncuyu %50 yavaşlatır (10 saniye)

### Arayüz Özellikleri
- **Can Göstergesi**: Sol üstte kalp ikonları ile can durumu
- **Level ve Süre Göstergesi**: Üstte ortalanmış level ve kalan süre
- **Buff/Debuff Göstergesi**: Aktif buff/debuff durumu ve kalan süre
- **Hint Sistemi**: Oyun içi yardım kartları (H tuşu)
- **Pause Menüsü**: ESC ile oyunu duraklatma
- **Ses Kontrolü**: Sol alt köşede ses seviyesi kontrolü

### Ses ve Müzik
- Menü müziği (intro + loop)
- Çeşitli ses efektleri (bomba patlaması, hasar alma, buff toplama, vb.)
- 3 seviyeli ses kontrolü (100%, 50%, 0%)

---


<a name="gereksinimler"></a>
## 🔧 Gereksinimler

### Sistem Gereksinimleri
- **Python**: 3.8 veya üzeri
- **İşletim Sistemi**: Windows, Linux, macOS
- **Pygame**: 2.0.0 veya üzeri

### Python Kütüphaneleri
- `pygame` - Oyun motoru ve grafik işlemleri

---


<a name="kurulum"></a>
## 📦 Kurulum


### 1. Projeyi İndirin

Projeyi bilgisayarınıza indirin veya klonlayın:

```bash
git clone https://github.com/Morteza-Rezaei/BiyikBeyinCilesi
cd BiyikBeyinCilesi
```

GitHub Proje Linki: [https://github.com/Morteza-Rezaei/BiyikBeyinCilesi](https://github.com/Morteza-Rezaei/BiyikBeyinCilesi)

### 2. Python Kurulumu

Python'un kurulu olduğundan emin olun. Kontrol etmek için:

```bash
python --version
# veya
python3 --version
```

Eğer Python kurulu değilse, [python.org](https://www.python.org/downloads/) adresinden indirip kurabilirsiniz.

### 3. Pygame Kurulumu

Pygame'i pip ile kurun:

```bash
pip install pygame
# veya
pip3 install pygame
```

Alternatif olarak, `requirements.txt` dosyasını kullanarak:

```bash
pip install -r requirements.txt
```

### 4. Proje Dosyalarını Kontrol Edin

Aşağıdaki klasör ve dosyaların mevcut olduğundan emin olun:

```
BiyikBeyinCilesi/
├── main.py              # Ana giriş noktası
├── engine.py            # Oyun motoru
├── states.py            # Oyun durumları (menü, oyun)
├── player.py            # Oyuncu karakteri
├── game_objects.py      # Oyun nesneleri (düşmanlar, buff'lar)
├── ui.py                # Arayüz bileşenleri
├── settings.py          # Oyun ayarları
├── assets/              # Görseller ve sesler
│   ├── biyik_adam/     # Karakter animasyonları
│   ├── game/           # Oyun içi görseller
│   ├── hint/           # Hint kartları
│   └── music/          # Ses efektleri ve müzik
└── requirements.txt     # Python bağımlılıkları
```

### 5. Oyunu Çalıştırın

```bash
python main.py
# veya
python3 main.py
```

Oyun tam ekran modunda açılacaktır.

---


<a name="kullanim"></a>
## 🎮 Kullanım

### Oyunu Başlatma

1. `main.py` dosyasını çalıştırın
2. Ana menüde "BAŞLA" butonuna tıklayın veya Enter'a basın
3. Oyun Level 1'den başlayacaktır

### Level Seçimi

- Ana menüde **Ctrl + Start** tuşlarına basarak level seçim ekranını açabilirsiniz
- İstediğiniz level numarasını girin (1-9999)
- "BAŞLA" butonuna tıklayın veya Enter'a basın

**Not**: Level 1'den başlamayan oyunlar rekor olarak kaydedilmez.

---


<a name="oyun-mekanikleri"></a>
## 🎯 Oyun Mekanikleri

### Level Sistemi

- Her level **60 saniye** sürer
- Level tamamlandığında "Sonraki level için tıkla veya SPACE'e bas" mesajı görünür
- Level arttıkça:
  - Düşman sayısı artar
  - Düşman hızı artar
  - Spawn süreleri kısalır
  - Bomba fünye süresi kısalır
  - Jilet saldırı mesafesi artar

### Can Sistemi

- Oyuncunun **5 canı** vardır
- Her hasar **1 can** azaltır
- Hasar aldıktan sonra **1.5 saniye** dokunulmazlık süresi vardır
- Çay toplayarak **+1 can** kazanabilirsiniz (maksimum 5)

### Düşman Davranışları

#### Bomba 💣
- Haritada rastgele konumlarda spawn olur
- Belirli süre sonra patlar (level arttıkça süre kısalır)
- Patlama anında yakındaki oyuncuya hasar verir
- Patlamadan önce tick tick animasyonu gösterir

#### Sinsi Jilet 🔪
- Ekran kenarından spawn olur
- İki modu vardır:
  - **Sinsi Mod**: Yavaşça oyuncuya yaklaşır, hafif titreme efekti
  - **Saldırı Modu**: Belirli mesafede hızla saldırır, kovalar
- Saldırı mesafesi ve süresi level ile artar

#### Uçan Terlik 👟
- Ekran kenarından fırlatılır
- Oyuncuya doğru düz çizgide gider
- Ekran dışına çıkınca kaybolur
- Hızı level ile artar

### Power-up'lar

#### Çay ☕
- Nadir çıkar (ağırlık: 1)
- Toplandığında +1 can verir
- Haritada 8 saniye kalır, son 2 saniyede yanıp söner

#### Hız Artışı ⚡
- Toplandığında oyuncuyu %50 hızlandırır
- 10 saniye sürer
- Sol üstte yeşil ikon ve kalan süre çubuğu gösterilir

#### Hız Azalışı 🐌
- Toplandığında oyuncuyu %50 yavaşlatır
- 10 saniye sürer
- Sol üstte kırmızı ikon ve kalan süre çubuğu gösterilir

### Rekor Sistemi

- En yüksek level `highscore.json` dosyasında kaydedilir
- Sadece Level 1'den başlayan oyunlar rekor olarak kaydedilir
- Ana menüde sağ üstte rekor bilgisi gösterilir
- Rekoru sıfırlamak için ana menüde rekorun altındaki "[Rekoru Sıfırla]" linkine tıklayın

---


<a name="kontroller"></a>
## ⌨️ Kontroller

### Ana Menü
- **Fare**: Butonlara tıklama
- **ESC**: Oyundan çık
- **Sol Alt Köşe**: Ses kontrolü (tıklayarak ses seviyesini değiştir)
- **Ctrl + Start**: Level seçim ekranını aç

### Oyun İçi
- **W, A, S, D**: Karakteri hareket ettir
  - **W**: Yukarı
  - **A**: Sol
  - **S**: Aşağı
  - **D**: Sağ
- **ESC**: Pause menüsünü aç/kapat
- **H**: Hint popup'ını aç/kapat
- **Fare**: Oyun aktifken gizlidir (pause/hint açıkken görünür)

### Level Başlangıç/Tamamlanma Ekranı
- **SPACE** veya **Fare Tıklaması**: Sonraki leveli başlat

### Pause Menüsü
- **ESC**: Devam et
- **Fare**: Butonlara tıklama
- **Ses Kontrolü**: Ortada ses seviyesini değiştir

### Hint Popup
- **H** veya **ESC**: Kapat
- **SPACE**, **Enter** veya **→**: Sonraki hint
- **Fare**: Butonlara tıklama

---


<a name="proje-yapisi"></a>
## 📁 Proje Yapısı

```
BiyikBeyinCilesi/
│
├── main.py                 # Ana giriş noktası - Oyunu başlatır
├── engine.py               # Oyun motoru - GameEngine, Assets, Audio, GameState
├── states.py               # Oyun durumları - MenuState, PlayingState
├── player.py               # Oyuncu karakteri - Hareket, animasyon, can sistemi
├── game_objects.py          # Oyun nesneleri - Düşmanlar, buff'lar, spawn manager
├── ui.py                   # Arayüz bileşenleri - Butonlar, hint, pause menüsü
├── settings.py             # Oyun ayarları - Sabitler, rekor sistemi
│
├── assets/                 # Oyun varlıkları
│   ├── biyik_adam/        # Karakter animasyonları (4 yön)
│   ├── game/              # Oyun içi görseller
│   │   ├── bomb_tick_*.png      # Bomba animasyon kareleri
│   │   ├── explosion_*.png     # Patlama animasyon kareleri
│   │   ├── sinsi_jilet_*.png   # Jilet animasyon kareleri
│   │   ├── ucan_terlik_*.png   # Terlik animasyon kareleri
│   │   ├── tea.png             # Çay görseli
│   │   ├── speed_buff.png      # Hız artışı görseli
│   │   ├── speed_debuff.png    # Hız azalışı görseli
│   │   ├── heart.png           # Can ikonu
│   │   └── heart_broken.png    # Boş can ikonu
│   ├── hint/               # Hint kartları
│   ├── music/              # Ses efektleri ve müzik
│   ├── player/             # Oyuncu animasyonları
│   ├── button_*.png        # Menü butonları
│   ├── volume_*.png        # Ses kontrol ikonları
│   ├── title.png           # Oyun başlığı
│   ├── instruction.png     # Talimat görseli
│   ├── home_bg.jpg         # Ana menü arka planı
│   └── game_bg.png          # Oyun arka planı
│
├── highscore.json          # Rekor kaydı (otomatik oluşturulur)
├── requirements.txt        # Python bağımlılıkları
└── README.md               # Bu dosya
```

### Dosya Açıklamaları

#### `main.py`
- Oyunun ana giriş noktası
- `GameEngine` sınıfını başlatır ve çalıştırır

#### `engine.py`
- **GameEngine**: Ana oyun döngüsü, durum yönetimi
- **GameState**: Tüm oyun durumları için temel sınıf
- **Assets**: Görsel ve font yükleme, önbellekleme
- **Audio**: Müzik ve ses efektleri yönetimi

#### `states.py`
- **MenuState**: Ana menü ekranı
- **PlayingState**: Ana oyun ekranı, oyun mantığı

#### `player.py`
- **Player**: Oyuncu karakteri
- Hareket, animasyon, can sistemi, buff/debuff yönetimi

#### `game_objects.py`
- **Bomb**: Bomba nesnesi ve patlama mekaniği
- **SinsiJilet**: Sinsi jilet düşmanı
- **UcanTerlik**: Uçan terlik düşmanı
- **Tea**: Çay power-up'ı
- **SpeedPowerup**: Hız artışı/azalışı power-up'ları
- **HealthUI**: Can göstergesi
- **SpawnManager**: Nesne oluşturma ve level yönetimi

#### `ui.py`
- **ImageButton**: Görsel tabanlı buton
- **VolumeControl**: Ses seviyesi kontrolü
- **PauseMenu**: Pause menüsü
- **HintButton**: Hint butonu
- **HintPopup**: Hint kartları popup'ı
- **LevelSelector**: Level seçim dialogu

#### `settings.py`
- Tüm oyun sabitleri (renkler, hızlar, süreler, vb.)
- Rekor yükleme/kaydetme fonksiyonları

---


<a name="teknik-detaylar"></a>
## 🔧 Teknik Detaylar

### Oyun Motoru
- **FPS**: 60 (sabit)
- **Ekran Modu**: Tam ekran (otomatik çözünürlük)
- **Delta Time**: Frame başına geçen süre (saniye cinsinden)

### Performans Optimizasyonları
- **Asset Caching**: Tüm görseller ve fontlar önbellekte tutulur
- **Preloading**: Oyun asset'leri menüde önceden yüklenir
- **Sprite Groups**: Pygame sprite grupları ile verimli çarpışma kontrolü
- **Surface Caching**: UI overlay'leri önceden oluşturulur

### Ses Sistemi
- **Müzik**: Intro + loop yapısı (menü müziği)
- **Ses Efektleri**: 16 kanallı mixer
- **Ses Seviyeleri**: 3 seviye (100%, 50%, 0%)
- **Loop Sesler**: Buff/debuff için sürekli çalan sesler (opsiyonel)

### Çarpışma Sistemi
- Oyuncu için küçültülmüş collision rect (daha adil çarpışma)
- Bomba patlaması için mesafe tabanlı çarpışma kontrolü
- Düşmanlar için rect tabanlı çarpışma kontrolü

### Level Sistemi
- **Zorluk Artışı**: Exponential ve linear kombinasyonu
- **Spawn Yönetimi**: Level bazlı maksimum düşman sayıları
- **Hız Çarpanı**: Her levelde %12 hız artışı
- **Spawn Süreleri**: Her levelde %8 azalma (minimum sınır var)

### Veri Kaydetme
- **Rekor**: JSON formatında `highscore.json` dosyasına kaydedilir
- **Format**: `{"level": <level>, "date": "<tarih>"}`

---

## 🐛 Bilinen Sorunlar

- Oyun tam ekran modunda çalışır (pencere modu yok)
- Bazı sistemlerde ses çalışmayabilir (pygame mixer sorunları)

---

## 📝 Geliştirici Notları

### Yeni Özellik Ekleme
1. Yeni düşman eklemek için `game_objects.py` dosyasına yeni bir sınıf ekleyin
2. `SpawnManager` sınıfına spawn mantığını ekleyin
3. `PlayingState` sınıfında güncelleme ve çizim mantığını ekleyin

### Ayarları Değiştirme
- Tüm oyun sabitleri `settings.py` dosyasında tanımlıdır
- Değerleri değiştirerek oyun dengesini ayarlayabilirsiniz

### Yeni Ses Ekleme
1. Ses dosyasını `assets/music/` klasörüne ekleyin
2. `engine.py` dosyasındaki `Audio.SOUND_PATHS` dictionary'sine ekleyin
3. `Audio.play_sound('ses_adi')` ile çalın

---

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

---


## 👨‍💻 Geliştirici

- **Morteza Rezaeı**

Proje, pygame kütüphanesi kullanılarak geliştirilmiştir.

Tanıtım videosu (2 dakika): [https://youtu.be/M1T_XHGh2f4](https://youtu.be/M1T_XHGh2f4)

**Not**: Bu README dosyası projeyi sunmak için hazırlanmıştır. Tüm kurulum adımları ve kullanım talimatları detaylı olarak açıklanmıştır.

---

## 🎉 İyi Oyunlar!

Bıyık Bey'in Çilesi'nde başarılar dileriz! Mümkün olduğunca uzun süre hayatta kalmaya çalışın ve rekor kırmayı deneyin! 🏆
