"""
Bıyık Bey'in Çilesi - Oyuncu
WASD ile hareket eden ana karakter
"""

import pygame
from engine import Assets
from settings import (PLAYER_MAX_HEALTH, PLAYER_START_HEALTH, PLAYER_INVINCIBILITY_TIME,
                      BUFF_EFFECT_DURATION, SPEED_BUFF_MULTIPLIER, SPEED_DEBUFF_MULTIPLIER)


class Player(pygame.sprite.Sprite):
    """Ana oyuncu karakteri"""
    
    def __init__(self, x, y):
        super().__init__()
        
        self.base_speed = 10
        self.speed = self.base_speed
        self.direction = pygame.math.Vector2(0, 0)
        self.facing = 'down'
        self.is_moving = False
        
        # Can sistemi
        self.max_health = PLAYER_MAX_HEALTH
        self.health = PLAYER_START_HEALTH
        
        # Hasar sonrası dokunulmazlık
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = PLAYER_INVINCIBILITY_TIME
        self.blink_timer = 0
        self.visible = True
        
        # Buff/Debuff sistemi
        self.speed_buff_timer = 0
        self.speed_debuff_timer = 0
        self.buff_duration = BUFF_EFFECT_DURATION
        
        # Animasyon
        self.anim_speed = 0.15
        self.frame_index = 0
        
        self._load_animations()
        self.image = self.anims['idle']
        self.rect = self.image.get_rect(center=(x, y))
    
    def _load_animations(self):
        """Animasyonları yükle"""
        scale = 1.3
        self.anims = {
            'idle': Assets.load_scaled('assets/player/idle_stand.png', scale)
        }
        
        for dir in ['down', 'up', 'left', 'right']:
            self.anims[f'walk_{dir}'] = [
                Assets.load_scaled(f'assets/player/walk_{dir}_1.png', scale),
                Assets.load_scaled(f'assets/player/walk_{dir}_2.png', scale)
            ]
    
    def take_damage(self, amount=1):
        """Hasar al"""
        if self.invincible:
            return False
        
        self.health = max(0, self.health - amount)
        self.invincible = True
        self.invincible_timer = self.invincible_duration
        return True
    
    def heal(self, amount=1):
        """Can kazan"""
        if self.health < self.max_health:
            self.health = min(self.max_health, self.health + amount)
            return True
        return False
    
    def is_dead(self):
        """Öldü mü?"""
        return self.health <= 0
    
    def apply_speed_buff(self):
        """Hız artışı uygula"""
        self.speed_buff_timer = self.buff_duration
        self.speed_debuff_timer = 0  # Debuff'ı iptal et
        self.speed = self.base_speed * SPEED_BUFF_MULTIPLIER
    
    def apply_speed_debuff(self):
        """Hız azalması uygula"""
        self.speed_debuff_timer = self.buff_duration
        self.speed_buff_timer = 0  # Buff'ı iptal et
        self.speed = self.base_speed * SPEED_DEBUFF_MULTIPLIER
    
    def has_active_buff(self):
        """Aktif buff var mı?"""
        return self.speed_buff_timer > 0
    
    def has_active_debuff(self):
        """Aktif debuff var mı?"""
        return self.speed_debuff_timer > 0
    
    def get_buff_remaining_time(self):
        """Kalan buff/debuff süresi"""
        if self.speed_buff_timer > 0:
            return self.speed_buff_timer
        elif self.speed_debuff_timer > 0:
            return self.speed_debuff_timer
        return 0
    
    def update(self, screen_w, screen_h, dt=1/60):
        """Her frame güncelle"""
        self._handle_input()
        self._move(screen_w, screen_h)
        self._animate()
        self._update_invincibility(dt)
        self._update_buffs(dt)
    
    def _update_buffs(self, dt):
        """Buff/Debuff süresini güncelle"""
        if self.speed_buff_timer > 0:
            self.speed_buff_timer -= dt
            if self.speed_buff_timer <= 0:
                self.speed = self.base_speed
        
        if self.speed_debuff_timer > 0:
            self.speed_debuff_timer -= dt
            if self.speed_debuff_timer <= 0:
                self.speed = self.base_speed
    
    def _update_invincibility(self, dt):
        """Dokunulmazlık süresini güncelle"""
        if self.invincible:
            self.invincible_timer -= dt
            
            # Yanıp sönme efekti
            self.blink_timer += dt
            if self.blink_timer >= 0.1:
                self.blink_timer = 0
                self.visible = not self.visible
            
            if self.invincible_timer <= 0:
                self.invincible = False
                self.visible = True
    
    def _handle_input(self):
        """Klavye girişi"""
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0
        
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.direction.y = 1
            self.facing = 'down'
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing = 'right'
        
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            self.is_moving = True
        else:
            self.is_moving = False
    
    def _move(self, screen_w, screen_h):
        """Hareket ve sınır kontrolü"""
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(screen_w, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(screen_h, self.rect.bottom)
    
    def _animate(self):
        """Animasyon güncelle"""
        if self.is_moving:
            frames = self.anims[f'walk_{self.facing}']
            self.frame_index += self.anim_speed
            if self.frame_index >= len(frames):
                self.frame_index = 0
            self.image = frames[int(self.frame_index)]
        else:
            self.image = self.anims['idle']
            self.frame_index = 0
    
    def draw(self, screen):
        """Ekrana çiz"""
        if self.visible:
            screen.blit(self.image, self.rect)
    
    def get_collision_rect(self):
        """Çarpışma için daha küçük bir rect döndür"""
        # Karakterin ayak bölgesi için daha küçük rect
        shrink = 20
        return self.rect.inflate(-shrink, -shrink)
