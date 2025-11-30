"""
Bıyık Bey'in Çilesi - Ana Menü
Başlık, talimatlar ve butonlar içeren ana menü ekranı
"""

import pygame
from settings import *
from ui import Button, draw_text_centered


class MainMenu:
    """Oyunun ana menü ekranı"""
    
    def __init__(self, screen):
        """
        Ana menüyü başlat
        
        Parametreler:
            screen: Pygame görüntü yüzeyi
        """
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        self._load_assets()
        self._calculate_layout()
        self._create_buttons()
        self._create_pixel_overlay()
        
        self.running = True
    
    def _load_assets(self):
        """Tüm görsel dosyalarını yükle ve ölçeklendir"""
        # Arka plan görseli
        self.background = pygame.image.load('assets/Forest.png')
        self.background = pygame.transform.scale(
            self.background, 
            (self.screen_width, self.screen_height)
        )
        
        # Karakter görseli
        original_char = pygame.image.load('assets/biyik_adam/biyik_adam_right.png')
        char_height = int(self.screen_height * 0.23)
        char_aspect = original_char.get_width() / original_char.get_height()
        self.character_image = pygame.transform.scale(
            original_char,
            (int(char_height * char_aspect), char_height)
        )
    
    def _calculate_layout(self):
        """Ekran boyutuna göre tüm elemanların konumlarını hesapla (Y ekseninde ortalı)"""
        # Buton boyutları
        self.button_width = min(500, int(self.screen_width * 0.35))
        self.button_height = min(90, int(self.screen_height * 0.08))
        self.button_x = (self.screen_width - self.button_width) // 2
        
        # Elemanlar arası boşluklar
        char_title_gap = 60
        title_instruction_gap = 50
        instruction_button_gap = 50
        button_spacing = 20
        
        # Toplam içerik yüksekliğini hesapla
        char_height = self.character_image.get_height()
        title_height = TITLE_FONT_SIZE
        instruction_height = INSTRUCTION_FONT_SIZE
        
        total_height = (
            char_height + 
            char_title_gap + 
            title_height + 
            title_instruction_gap + 
            instruction_height + 
            instruction_button_gap + 
            self.button_height +
            button_spacing + 
            self.button_height
        )
        
        # Her şeyi ortalamak için başlangıç Y konumu
        start_y = (self.screen_height - total_height) // 2
        
        # Her elemanın Y konumunu hesapla
        self.character_y = start_y
        self.title_y = self.character_y + char_height + char_title_gap + title_height // 2
        self.instruction_y = self.title_y + title_height // 2 + title_instruction_gap + instruction_height // 2
        self.start_button_y = self.instruction_y + instruction_height // 2 + instruction_button_gap
        self.quit_button_y = self.start_button_y + self.button_height + button_spacing
    
    def _create_buttons(self):
        """Menü butonlarını oluştur"""
        self.start_button = Button(
            self.button_x, 
            self.start_button_y, 
            self.button_width, 
            self.button_height, 
            "BAŞLA"
        )
        
        self.quit_button = Button(
            self.button_x, 
            self.quit_button_y, 
            self.button_width, 
            self.button_height, 
            "ÇIK"
        )
    
    def _create_pixel_overlay(self):
        """Retro efekt için piksel ızgara katmanını önceden oluştur"""
        self.pixel_overlay = pygame.Surface(
            (self.screen_width, self.screen_height), 
            pygame.SRCALPHA
        )
        for x in range(0, self.screen_width, 8):
            for y in range(0, self.screen_height, 8):
                if (x + y) % 16 == 0:
                    pygame.draw.rect(self.pixel_overlay, (255, 255, 255, 8), (x, y, 1, 1))
        
    def handle_events(self):
        """Menü olaylarını işle"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            # Tam ekrandan çıkış için ESC tuşu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            
            # Buton tıklamalarını işle
            if self.start_button.handle_event(event):
                return "start"
            
            if self.quit_button.handle_event(event):
                return "quit"
        
        return None
    
    def draw(self):
        """Menü ekranını retro oyun estetiğiyle çiz"""
        # Arka planı çiz
        self.screen.blit(self.background, (0, 0))
        
        # Karakter görselini ortala ve çiz
        char_x = (self.screen_width - self.character_image.get_width()) // 2
        self.screen.blit(self.character_image, (char_x, self.character_y))
        
        # Başlığı çiz
        draw_text_centered(
            self.screen,
            "Bıyık Bey'in Çilesi",
            TITLE_FONT_SIZE,
            YELLOW,
            self.title_y
        )
        
        # Talimatları çiz
        draw_text_centered(
            self.screen,
            "WSAD ile kaçın, çarpma ölür.",
            INSTRUCTION_FONT_SIZE,
            CYAN,
            self.instruction_y
        )
        
        # Butonları çiz
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
        # Piksel ızgara efektini uygula
        self.screen.blit(self.pixel_overlay, (0, 0))
        
        # Ekranı güncelle
        pygame.display.flip()
    
    def run(self):
        """
        Ana menü döngüsü
        
        Döndürür:
            Sonraki işlemi belirten string ("start" veya "quit")
        """
        clock = pygame.time.Clock()
        
        while self.running:
            action = self.handle_events()
            
            if action == "quit":
                return "quit"
            elif action == "start":
                return "start"
            
            self.draw()
            clock.tick(FPS)
        
        return "quit"
