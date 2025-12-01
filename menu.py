"""
Bıyık Bey'in Çilesi - Ana Menü
Başlık, talimatlar ve butonlar içeren ana menü ekranı
"""

import pygame
from settings import *
from ui import ImageButton, VolumeControl


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
        self._setup_music()
        self._calculate_layout()
        self._create_buttons()
        self._create_volume_control()
    
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
        
        # Başlık görseli
        original_title = pygame.image.load('assets/title.png')
        title_width = int(self.screen_width * 0.5)
        title_aspect = original_title.get_width() / original_title.get_height()
        title_height = int(title_width / title_aspect)
        self.title_image = pygame.transform.scale(original_title, (title_width, title_height))
        
        # Talimat görseli
        original_instruction = pygame.image.load('assets/instruction.png')
        instruction_width = int(self.screen_width * 0.35)
        instruction_aspect = original_instruction.get_width() / original_instruction.get_height()
        instruction_height = int(instruction_width / instruction_aspect)
        self.instruction_image = pygame.transform.scale(original_instruction, (instruction_width, instruction_height))
    
    def _setup_music(self):
        """Arka plan müziğini yükle ve başlat (intro + loop)"""
        pygame.mixer.init()
        
        # Müzik durumu: 'intro' veya 'loop'
        self.music_state = 'intro'
        
        # Önce intro müziğini çal (1 kez)
        pygame.mixer.music.load('assets/music/menu_music_intro.mp3')
        pygame.mixer.music.set_volume(VOLUME_LEVELS[DEFAULT_VOLUME_INDEX])
        pygame.mixer.music.play()
        
        # Müzik bittiğinde event gönder
        self.MUSIC_END_EVENT = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END_EVENT)
    
    def _create_volume_control(self):
        """Ses kontrol butonunu oluştur"""
        self.volume_control = VolumeControl(self.screen_width, self.screen_height)
    
    def _calculate_layout(self):
        """Ekran boyutuna göre tüm elemanların konumlarını hesapla (Y ekseninde ortalı)"""
        # Elemanlar arası boşluklar
        char_title_gap = 40
        title_instruction_gap = 30
        instruction_button_gap = 40
        button_spacing = 20
        
        # Buton boyutları (görsellerden alınacak, şimdilik tahmini)
        self.button_height = int(self.screen_height * 0.08)
        
        # Toplam içerik yüksekliğini hesapla
        char_height = self.character_image.get_height()
        title_height = self.title_image.get_height()
        instruction_height = self.instruction_image.get_height()
        
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
        self.title_y = self.character_y + char_height + char_title_gap
        self.instruction_y = self.title_y + title_height + title_instruction_gap
        self.start_button_y = self.instruction_y + instruction_height + instruction_button_gap
        self.quit_button_y = self.start_button_y + self.button_height + button_spacing
    
    def _create_buttons(self):
        """Menü butonlarını oluştur (görsel tabanlı)"""
        # Buton boyutları
        button_width = int(self.screen_width * 0.25)
        button_height = self.button_height
        button_x = (self.screen_width - button_width) // 2
        
        self.start_button = ImageButton(
            button_x, 
            self.start_button_y, 
            button_width, 
            button_height,
            'assets/button_start.png',
            'assets/button_start_h.png'
        )
        
        self.quit_button = ImageButton(
            button_x, 
            self.quit_button_y, 
            button_width, 
            button_height,
            'assets/button_quit.png',
            'assets/button_quit_h.png'
        )
        
    def handle_events(self):
        """Menü olaylarını işle"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            # Müzik bittiğinde: intro ise loop'a geç, loop ise tekrar başlat
            if event.type == self.MUSIC_END_EVENT:
                if self.music_state == 'intro':
                    # Intro bitti, loop müziğine geç
                    self.music_state = 'loop'
                    pygame.mixer.music.load('assets/music/menu_music_loop.mp3')
                    pygame.mixer.music.set_volume(self.volume_control.get_volume())
                    pygame.mixer.music.play(-1)  # Sonsuz döngü
            
            # Tam ekrandan çıkış için ESC tuşu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
            
            # Buton tıklamalarını işle
            if self.start_button.handle_event(event):
                return "start"
            
            if self.quit_button.handle_event(event):
                return "quit"
            
            # Ses kontrolü tıklamalarını işle
            new_volume = self.volume_control.handle_event(event)
            if new_volume is not None:
                pygame.mixer.music.set_volume(new_volume)
        
        return None
    
    def draw(self):
        """Menü ekranını çiz"""
        # Arka planı çiz
        self.screen.blit(self.background, (0, 0))
        
        # Karakter görselini ortala ve çiz
        char_x = (self.screen_width - self.character_image.get_width()) // 2
        self.screen.blit(self.character_image, (char_x, self.character_y))
        
        # Başlık görselini ortala ve çiz
        title_x = (self.screen_width - self.title_image.get_width()) // 2
        self.screen.blit(self.title_image, (title_x, self.title_y))
        
        # Talimat görselini ortala ve çiz
        instruction_x = (self.screen_width - self.instruction_image.get_width()) // 2
        self.screen.blit(self.instruction_image, (instruction_x, self.instruction_y))
        
        # Butonları çiz
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
        # Ses kontrolünü çiz
        self.volume_control.draw(self.screen)
        
        # Ekranı güncelle
        pygame.display.flip()
    
    def run(self):
        """
        Ana menü döngüsü
        
        Döndürür:
            Sonraki işlemi belirten string ("start" veya "quit")
        """
        clock = pygame.time.Clock()
        
        while True:
            action = self.handle_events()
            
            if action == "quit":
                return "quit"
            elif action == "start":
                return "start"
            
            self.draw()
            clock.tick(FPS)
