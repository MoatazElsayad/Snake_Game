import pygame
from config import *

class UIElement:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)

class Button(UIElement):
    def __init__(self, x, y, w, h, text, action=None, param=None):
        super().__init__(x, y, w, h)
        self.text = text
        self.action = action
        self.param = param
        self.hovered = False

    def draw(self, surface, font, theme):
        color = theme["ui_bg"]
        if self.hovered:
            # Make it slightly lighter or different on hover
            r = min(255, color[0] + 30)
            g = min(255, color[1] + 30)
            b = min(255, color[2] + 30)
            color = (r, g, b)
        
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, theme["ui_border"], self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.text, True, theme["text"])
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                if self.param is not None:
                    return self.action(self.param)
                return self.action()
        return None

class InputBox(UIElement):
    def __init__(self, x, y, w, h, text=''):
        super().__init__(x, y, w, h)
        self.text = text
        self.active = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 15: # Limit length
                        self.text += event.unicode
        return None

    def draw(self, surface, font, theme):
        color = theme["input_bg"]
        border_color = theme["ui_border"] if not self.active else theme["text"]
        
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, border_color, self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.text, True, theme["input_text"])
        surface.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
        self.rect.w = max(200, text_surf.get_width() + 10)

class ColorPicker:
    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.selected_color_name = "Green"
        self.buttons = []
        
        # Create buttons for each color
        btn_size = 40
        gap = 10
        start_x = x
        
        for name, color in SNAKE_COLORS.items():
            rect = pygame.Rect(start_x, y, btn_size, btn_size)
            self.buttons.append({"name": name, "color": color, "rect": rect})
            start_x += btn_size + gap

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn["rect"].collidepoint(event.pos):
                    self.selected_color_name = btn["name"]
                    return btn["color"]
        return None

    def draw(self, surface, theme):
        # Draw Label
        # Assuming font is handled externally or passed, but for simplicity let's rely on visual feedback
        for btn in self.buttons:
            # Draw color box
            pygame.draw.rect(surface, btn["color"], btn["rect"], border_radius=5)
            # Draw selection border
            if btn["name"] == self.selected_color_name:
                pygame.draw.rect(surface, theme["text"], btn["rect"], 3, border_radius=5)
            else:
                pygame.draw.rect(surface, theme["ui_border"], btn["rect"], 1, border_radius=5)

class ThemeToggle(Button):
    def __init__(self, x, y, w, h, current_theme_name):
        super().__init__(x, y, w, h, f"Theme: {current_theme_name}")
        self.current_theme_name = current_theme_name

    def toggle(self):
        if self.current_theme_name == "DARK":
            self.current_theme_name = "LIGHT"
        else:
            self.current_theme_name = "DARK"
        self.text = f"Theme: {self.current_theme_name}"
        return self.current_theme_name
