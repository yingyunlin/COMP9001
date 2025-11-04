'''
GachaSystem Class - Manages idol card draws and randomised card creation
'''

import random
from idol_card import IdolCard
from config import IDOL_NAMES, RARITY_RATES


class GachaSystem:
    '''
    Manages the gacha draw system with rarity rates and idol generation.
    
    Creates idol cards using probability rates and tracks drawn idols
    to avoid duplicate names in the collection.
    '''
    
    def __init__(self) -> None:
        '''
        Initialises the gacha system with idol names and rarity rates.
        
        Sets up the idol name pool, rarity probability rates, and used names tracker.
        '''
        self.idol_names = IDOL_NAMES
        self.rarity_rates = RARITY_RATES
        self.used_names = set()
    
    def generate_card(self, guarantee_rare: bool = False) -> IdolCard:
        '''
        Generates a random idol card with probability-based rarity.
        
        Parameters:
            guarantee_rare (bool): If True, guarantees at least Rare rarity (used for ten-draw). Defaults to False.
        
        Returns:
            IdolCard: A newly generated idol card with randomised name and rarity.
        '''
        # Determine rarity based on guarantee flag
        if guarantee_rare:
            # Guarantee mechanic: exclude Common to ensure at least Rare rarity
            rarities = ["Rare", "Epic", "Legendary"]
            weights = [
                self.rarity_rates["Rare"], 
                self.rarity_rates["Epic"], 
                self.rarity_rates["Legendary"]
            ]
            # Normalise weights to sum to 1.0
            total = sum(weights)
            weights = [w/total for w in weights]
            rarity = random.choices(rarities, weights=weights)[0]
        else:
            # Normal draw with all rarities included
            rarities = list(self.rarity_rates.keys())
            weights = list(self.rarity_rates.values())
            rarity = random.choices(rarities, weights=weights)[0]
        
        # Select a random name from the rarity pool
        available_names = [
            name for name in self.idol_names[rarity] 
            if name not in self.used_names  # Filter out already used names
        ]
        
        # If all names used, allow repeats
        if not available_names:
            available_names = self.idol_names[rarity]
        
        name = random.choice(available_names)
        self.used_names.add(name)
        
        return IdolCard(name, rarity)
    
    def reset_used_names(self) -> None:
        '''
        Resets the used names tracker.
        
        Clears the set of used idol names. Useful for starting a new game session.
        '''
        self.used_names.clear()
