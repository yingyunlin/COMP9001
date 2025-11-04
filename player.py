'''
Player Class - Manages player data, collection, and game operations
'''

from gacha_system import GachaSystem
from idol_card import IdolCard
from config import (
    STARTING_COINS, SINGLE_DRAW_COST, TEN_DRAW_COST,
    DUPLICATE_REFUND_RATES, SAVE_FILE_NAME, 
    BANKRUPTCY_BONUS_SINGLE, BANKRUPTCY_BONUS_TEN
)


class Player:
    '''
    Represents the player (producer) with coins, idol collection, and game statistics.

    Each player has a coin balance, collection of idols, and draw statistics.
    '''
    
    def __init__(self) -> None:
        '''
        Initialises a new player with default starting values.
        
        Sets starting coins, empty collection, zero draws, and gacha system.
        '''
        self.coins = STARTING_COINS
        self.collection = {}
        self.total_draws = 0
        self.gacha = GachaSystem()
    
    def has_idol(self, name: str) -> IdolCard | None:
        '''
        Checks if player already owns an idol by name.
        
        Parameters:
            name (str): The name of the idol to search for.
        
        Returns:
            IdolCard | None: The idol if found in collection, None otherwise.
        '''
        return self.collection.get(name)
    
    def add_idol(self, idol: IdolCard) -> None:
        '''
        Adds a new idol to the collection.
        
        Parameters:
            idol (IdolCard): The idol card to add to the player's collection.
        '''
        self.collection[idol.name] = idol
    
    def calculate_refund(self, idol: IdolCard) -> int:
        '''
        Calculates refund amount for duplicate idol based on rarity.
        
        Uses tiered refund system from config.
        
        Parameters:
            idol (IdolCard): The duplicate idol card.
        
        Returns:
            int: Refund amount in coins.
        '''
        refund_rate = DUPLICATE_REFUND_RATES[idol.rarity]
        return int(SINGLE_DRAW_COST * refund_rate)
    
    def single_draw(self) -> tuple[IdolCard, bool, int, bool]:
        '''
        Performs a single card draw.
        
        Deducts cost, generates a card, and handles duplicates with refunds.
        Includes bankruptcy protection to ensure players can always continue.
        
        Returns:
            tuple[IdolCard, bool, int, bool]: A tuple containing:
                - The drawn idol card
                - Whether it's a duplicate (True/False)
                - Refund amount in coins (0 if not duplicate)
                - Whether bankruptcy protection was triggered (True/False)
        '''
        # Bankruptcy protection: give 50 bonus coins if player cannot afford a single draw
        bankruptcy_triggered = False
        if self.coins < SINGLE_DRAW_COST:
            self.coins += BANKRUPTCY_BONUS_SINGLE  # Add 50 coins (enough for 5 draws)
            bankruptcy_triggered = True
        
        self.coins -= SINGLE_DRAW_COST
        self.total_draws += 1
        
        idol = self.gacha.generate_card()
        
        existing_idol = self.has_idol(idol.name)
        
        if existing_idol:
            existing_idol.level_up()
            refund = self.calculate_refund(existing_idol)
            self.coins += refund
            return (existing_idol, True, refund, bankruptcy_triggered)
        else:
            self.add_idol(idol)
            return (idol, False, 0, bankruptcy_triggered)
    
    def ten_draw(self) -> tuple[list[tuple[IdolCard, bool, int]], bool]:
        '''
        Performs a ten-card draw with guaranteed Rare+ mechanic.
        
        Draws 9 cards normally, then guarantees Rare+ (Rare, Epic, or Legendary) on the 10th card
        if no Rare or better was drawn in the first 9. Includes bankruptcy protection.
        
        Returns:
            tuple[list[tuple[IdolCard, bool, int]], bool]: A tuple containing:
                - List of 10 tuples, each containing (idol, is_duplicate, refund)
                - Whether bankruptcy protection was triggered (True/False)
        '''
        # Bankruptcy protection: give 100 bonus coins if player cannot afford a ten-draw
        bankruptcy_triggered = False
        if self.coins < TEN_DRAW_COST:
            self.coins += BANKRUPTCY_BONUS_TEN  # Add 100 coins (enough for 1 ten-draw)
            bankruptcy_triggered = True
        
        self.coins -= TEN_DRAW_COST
        self.total_draws += 10
        
        results = []
        has_rare_or_better = False
        
        # Draw first 9 cards
        for i in range(9):
            idol = self.gacha.generate_card()
            
            # Check if player got Rare or better (Rare, Epic, or Legendary)
            if idol.rarity in ["Rare", "Epic", "Legendary"]:
                has_rare_or_better = True
            
            existing_idol = self.has_idol(idol.name)
            
            if existing_idol:
                existing_idol.level_up()
                refund = self.calculate_refund(existing_idol)
                self.coins += refund
                results.append((existing_idol, True, refund))
            else:
                self.add_idol(idol)
                results.append((idol, False, 0))
        
        # 10th card: guarantee Rare+ if first 9 cards were all Common
        if not has_rare_or_better:
            idol = self.gacha.generate_card(guarantee_rare=True)
        else:
            idol = self.gacha.generate_card()
        
        existing_idol = self.has_idol(idol.name)
        
        if existing_idol:
            existing_idol.level_up()
            refund = self.calculate_refund(existing_idol)
            self.coins += refund
            results.append((existing_idol, True, refund))
        else:
            self.add_idol(idol)
            results.append((idol, False, 0))
        
        return (results, bankruptcy_triggered)
    
    def get_collection_list(self, sort_by: str = "rarity") -> list[IdolCard]:
        '''
        Returns a sorted list of idols in the collection.
        
        Parameters:
            sort_by (str): Sort method - "rarity", "name", or "level". Defaults to "rarity".
        
        Returns:
            list[IdolCard]: Sorted list of IdolCard objects.
        '''
        idols = list(self.collection.values())
        
        if sort_by == "rarity":
            rarity_order = {"Legendary": 0, "Epic": 1, "Rare": 2, "Common": 3}
            idols.sort(key=lambda x: (rarity_order.get(x.rarity, 4), x.name))  # Sort by rarity tier, then name
        elif sort_by == "name":
            idols.sort(key=lambda x: x.name)  # Sort alphabetically by name
        elif sort_by == "level":
            idols.sort(key=lambda x: (-x.level, x.name))  # Sort by level (highest first), then name
        
        return idols
    
    def get_total_fans(self) -> int:
        '''Returns the total fan count across all idols in the collection.'''
        return sum(idol.fans for idol in self.collection.values())
    
    def save_to_file(self, filename: str | None = None, silent: bool = True) -> None:
        '''
        Saves player data to a text file.
        
        Writes coin balance, total draws, and all idol data to persistent storage.
        
        Parameters:
            filename (str | None): Name of the save file. Uses default from config if None.
            silent (bool): If True, suppress success message. Defaults to True.
        '''
        if filename is None:
            filename = SAVE_FILE_NAME
        
        try:
            with open(filename, 'w') as f:
                # Write player information
                f.write(f"COINS:{self.coins}\n")
                f.write(f"DRAWS:{self.total_draws}\n")
                
                # Write idol data (one idol per line: name,rarity,level,fans)
                for idol in self.collection.values():
                    f.write(f"{idol.name},{idol.rarity},{idol.level},{idol.fans}\n")
            
            if not silent:
                print(f"✅ Game saved successfully!")
            
        except IOError as e:
            print(f"❌ Error saving game: {e}")
    
    def load_from_file(self, filename: str | None = None) -> bool:
        '''
        Loads player data from a text file.
        
        Reads saved coin balance, total draws, and idol collection from file.
        Handles missing or corrupted save files gracefully.
        
        Parameters:
            filename (str | None): Name of the save file. Uses default from config if None.
        
        Returns:
            bool: True if load successful, False otherwise.
        '''
        if filename is None:
            filename = SAVE_FILE_NAME
        
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            
            if len(lines) < 2:
                raise ValueError("Save file corrupted: insufficient data")
            
            coins_line = lines[0].strip()
            if not coins_line.startswith("COINS:"):
                raise ValueError("Save file corrupted: invalid format")
            self.coins = int(coins_line.split(':')[1])
            
            draws_line = lines[1].strip()
            if not draws_line.startswith("DRAWS:"):
                raise ValueError("Save file corrupted: invalid format")
            self.total_draws = int(draws_line.split(':')[1])
            
            self.collection = {}  # Clear existing collection before loading
            for line in lines[2:]:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                
                parts = line.split(',')
                if len(parts) != 4:  # Skip lines with invalid format
                    continue
                
                name, rarity, level, fans = parts
                idol = IdolCard(name, rarity, int(level), int(fans))
                self.collection[name] = idol
                self.gacha.used_names.add(name)
            
            print(f"✅ Welcome back, Producer! Game loaded successfully!")
            return True
            
        except FileNotFoundError:
            print("No save file found. Starting a new game!")
            return False
        except (ValueError, IndexError) as e:
            print(f"❌ Save file corrupted: {e}")
            print("Starting a new game with default values.")
            return False
