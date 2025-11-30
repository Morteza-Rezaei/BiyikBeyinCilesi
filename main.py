"""
Bıyık Bey'in Çilesi - Ana Oyun Giriş Noktası
Pygame kullanılarak Python'da yazılmış 2D Arcade Oyunu
"""

import pygame
import sys
from settings import *
from menu import MainMenu


def main():
    """Ana oyun fonksiyonu"""
    # Pygame'i başlat
    pygame.init()
    
    # Tam ekran görüntü oluştur
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Bıyık Bey'in Çilesi")
    
    # Dinamik ekran boyutlarını al
    screen_width, screen_height = screen.get_size()
    print(f"Tam ekran modunda çalışıyor: {screen_width}x{screen_height}")
    
    # FPS kontrolü için saat oluştur
    clock = pygame.time.Clock()
    
    # Oyun durumu
    running = True
    game_state = "menu"
    
    # Ana oyun döngüsü
    while running:
        if game_state == "menu":
            menu = MainMenu(screen)
            result = menu.run()
            
            if result == "start":
                game_state = "playing"
                # TODO: Gerçek oyunu başlat
                show_game_placeholder(screen, clock)
                game_state = "menu"
            elif result == "quit":
                running = False
        
        elif game_state == "playing":
            # TODO: Gerçek oyun döngüsünü buraya ekle
            pass
    
    # Temizlik yap ve çık
    pygame.quit()
    sys.exit()


def show_game_placeholder(screen, clock):
    """
    Geçici oyun ekranı fonksiyonu
    Gerçek oyun implementasyonu ile değiştirilecek
    
    Parametreler:
        screen: Pygame görüntü yüzeyi
        clock: FPS kontrolü için Pygame saati
    """
    from ui import draw_text_centered
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Menüye dönmek için ESC tuşu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        screen.fill(DARK_GRAY)
        draw_text_centered(
            screen,
            "Oyun Ekranı (Geçici)",
            TITLE_FONT_SIZE,
            WHITE,
            screen.get_height() // 2 - 50
        )
        draw_text_centered(
            screen,
            "Menüye dönmek için ESC'ye basın",
            INSTRUCTION_FONT_SIZE,
            LIGHT_GRAY,
            screen.get_height() // 2 + 50
        )
        
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
