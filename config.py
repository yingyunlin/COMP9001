'''
Game configuration and balance settings
'''

# Idol Name Pools - 26 unique idols across 4 rarity tiers
IDOL_NAMES = {
    "Common": [
        "Amy", "Ella", "Emma", "Mira", "Coco", 
        "Nana", "Suki", "Kira", "Bella", "Mila"
    ],
    "Rare": [
        "Luna", "Mina", "Lena", "Rosa", "Ruby", 
        "Nora", "Sara", "Hana"
    ],
    "Epic": [
        "Stella", "Nova", "Aria", "Iris", "Elsa"
    ],
    "Legendary": [
        "Anna", "Belle", "Jasmine"
    ]
}

# Rarity Probability Distribution
RARITY_RATES = {
    "Common": 0.50,      # 50%
    "Rare": 0.35,        # 35%
    "Epic": 0.13,        # 13%
    "Legendary": 0.02    # 2%
}

# Base Fan Counts by Rarity
BASE_FANS = {
    "Common": 100,
    "Rare": 500,
    "Epic": 2000,
    "Legendary": 10000
}

# Fan Increase per Level Up by Rarity
FAN_INCREASE_PER_LEVEL = {
    "Common": 100,
    "Rare": 300,
    "Epic": 1000,
    "Legendary": 5000
}

# Tiered Duplicate Refund System
# Higher rarity duplicates return more coins to reduce frustration
DUPLICATE_REFUND_RATES = {
    "Common": 0.20,      # 20%
    "Rare": 0.40,        # 40%
    "Epic": 0.60,        # 60%
    "Legendary": 0.80    # 80%
}

# Game Balance Settings
STARTING_COINS = 1000        # Initial coins for new players
SINGLE_DRAW_COST = 10        # Cost per single draw
TEN_DRAW_COST = 100          # Cost per ten-draw (10% discount)
BANKRUPTCY_BONUS_SINGLE = 50 # Bonus coins for single draw bankruptcy
BANKRUPTCY_BONUS_TEN = 100   # Bonus coins for ten-draw bankruptcy

# Rarity Display Symbols
RARITY_SYMBOLS = {
    "Common": "⭐",
    "Rare": "⭐⭐",
    "Epic": "⭐⭐⭐",
    "Legendary": "⭐⭐⭐⭐"
}

# Save File Settings
SAVE_FILE_NAME = "player_data.txt"
