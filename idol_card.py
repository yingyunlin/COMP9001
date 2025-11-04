'''
IdolCard Class - Represents an individual idol card with complete profile
'''

from config import BASE_FANS, RARITY_SYMBOLS, FAN_INCREASE_PER_LEVEL
from idol_profiles import get_idol_profile


class IdolCard:
    '''
    Represents an idol card with gameplay stats and personality traits.
    
    Each idol has level and fans for progression, plus unique personality
    attributes loaded from the profile database.
    '''
    
    def __init__(self, name: str, rarity: str, level: int = 1, fans: int | None = None) -> None:
        '''
        Initialises an idol card with both gameplay and profile data.
        
        Parameters:
            name (str): The idol's name.
            rarity (str): Rarity tier (Common/Rare/Epic/Legendary).
            level (int): Starting level. Defaults to 1.
            fans (int | None): Starting fan count. Uses base fans from config if None.
        '''
        self.name = name
        self.rarity = rarity
        self.level = level
        
        if fans is None:
            self.fans = BASE_FANS.get(rarity, 100)
        else:
            self.fans = fans
        
        # Load personality profile
        profile = get_idol_profile(name)
        if profile:
            self.mood = profile.get("mood", "Unknown")
            self.color = profile.get("color", "Unknown")
            self.hobby = profile.get("hobby", "Unknown")
            self.description = profile.get("description", "A mysterious idol.")
        else:
            self.mood = "Unknown"
            self.color = "Unknown"
            self.hobby = "Unknown"
            self.description = "A mysterious idol with an unknown background."
    
    def level_up(self) -> None:
        '''
        Levels up the idol by increasing level and adding fans.
        
        Higher rarity idols gain more fans per level up.
        '''
        self.level += 1
        increase = FAN_INCREASE_PER_LEVEL.get(self.rarity, 100)
        self.fans += increase
    
    def __str__(self) -> str:
        '''Returns basic string representation for quick display.'''
        symbol = RARITY_SYMBOLS.get(self.rarity, "⭐")
        return f"{symbol} {self.rarity} - {self.name} | Lv.{self.level} | Fans: {self.fans:,}"
    
    def get_short_display(self) -> str:
        '''Returns shortened display format for collection view.'''
        return f"{self.name} (Lv.{self.level})"
    
    def get_full_profile(self) -> str:
        '''Returns complete profile with all personality and gameplay information.'''
        symbol = RARITY_SYMBOLS.get(self.rarity, "⭐")
        
        profile = f"\n"
        profile += f"{symbol} {self.rarity} - {self.name}\n"
        profile += f"\n"
        profile += f"Level: {self.level} | Fans: {self.fans:,}\n"
        profile += f"\n"
        profile += f"💫 Mood: {self.mood}\n"
        profile += f"🎨 Color: {self.color}\n"
        profile += f"🎯 Hobby: {self.hobby}\n"
        profile += f"\n📝 Profile:\n"
        profile += f'   "{self.description}"\n'
        
        return profile
    
    def get_compact_profile(self) -> str:
        '''Returns a compact single-line profile for list views.'''
        symbol = RARITY_SYMBOLS.get(self.rarity, "⭐")
        return f"{symbol} {self.name} (Lv.{self.level}) - {self.mood} | {self.color} | {self.hobby}"
