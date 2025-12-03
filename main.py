"""
Bıyık Bey'in Çilesi - Ana Giriş Noktası
2D Arcade Oyunu

Dosya Yapısı:
    main.py      - Oyunu başlatır
    engine.py    - Oyun motoru (GameEngine, Assets, Audio, GameState)
    states.py    - Oyun durumları (MenuState, PlayingState)
    player.py    - Oyuncu karakteri
    ui.py        - Arayüz bileşenleri (butonlar, ses kontrolü)
    settings.py  - Oyun ayarları ve sabitler
    assets/      - Görseller ve sesler
"""

from engine import GameEngine


def main():
    engine = GameEngine()
    engine.run()


if __name__ == "__main__":
    main()
