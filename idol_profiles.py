'''
Complete database of all 26 idols with detailed personality profiles
'''

IDOL_PROFILES = {
    # Common Tier
    "Amy": {
        "rarity": "Common",
        "mood": "Bubbly",
        "color": "Pastel Peach",
        "hobby": "Baking cupcakes",
        "description": "A sweet girl who loves sharing homemade treats with everyone."
    },
    
    "Ella": {
        "rarity": "Common",
        "mood": "Lively",
        "color": "Sunny Yellow",
        "hobby": "Playing guitar",
        "description": "An upbeat performer who brings sunshine wherever she goes."
    },
    
    "Emma": {
        "rarity": "Common",
        "mood": "Gentle",
        "color": "Lavender",
        "hobby": "Reading novels",
        "description": "A quiet bookworm who expresses herself through music."
    },
    
    "Mira": {
        "rarity": "Common",
        "mood": "Dreamy",
        "color": "Sky Blue",
        "hobby": "Cloud watching",
        "description": "A thoughtful girl who finds inspiration in the sky above."
    },
    
    "Coco": {
        "rarity": "Common",
        "mood": "Warm",
        "color": "Chocolate Brown",
        "hobby": "Making desserts",
        "description": "A dessert enthusiast who believes sweetness makes the world better."
    },
    
    "Nana": {
        "rarity": "Common",
        "mood": "Playful",
        "color": "Peach Orange",
        "hobby": "Dancing freestyle",
        "description": "A fun-loving dancer who never takes life too seriously."
    },
    
    "Suki": {
        "rarity": "Common",
        "mood": "Sweet",
        "color": "Soft Pink",
        "hobby": "Drinking bubble tea",
        "description": "A gentle girl with long pink hair who's always seen with her favorite bubble tea."
    },
    
    "Kira": {
        "rarity": "Common",
        "mood": "Bright",
        "color": "Pearl White",
        "hobby": "Photography",
        "description": "A creative soul who captures beautiful moments through her lens."
    },
    
    "Bella": {
        "rarity": "Common",
        "mood": "Confident",
        "color": "Rose Red",
        "hobby": "Fashion design",
        "description": "A style icon who loves experimenting with bold outfits."
    },
    
    "Mila": {
        "rarity": "Common",
        "mood": "Poetic",
        "color": "Deep Purple",
        "hobby": "Writing poetry",
        "description": "A poetic soul who expresses her feelings through verses."
    },
    
    # Rare Tier
    "Luna": {
        "rarity": "Rare",
        "mood": "Elegant",
        "color": "Moonlight Silver",
        "hobby": "Playing harp",
        "description": "A graceful musician who enchants audiences with ethereal harp melodies under the moonlight."
    },

    "Mina": {
        "rarity": "Rare",
        "mood": "Cute",
        "color": "Bubblegum Pink",
        "hobby": "Playing with cats",
        "description": "An adorable idol who can't resist cute animals and fluffy things."
    },

    "Lena": {
        "rarity": "Rare",
        "mood": "Sophisticated",
        "color": "Royal Gold",
        "hobby": "Classical piano",
        "description": "A refined musician with a passion for timeless elegance."
    },

    "Rosa": {
        "rarity": "Rare",
        "mood": "Cheerful",
        "color": "Lavender Purple",
        "hobby": "Singing on stage",
        "description": "An adorable idol with cat ears and purple hair who brings joy to every performance."
    },

    "Ruby": {
        "rarity": "Rare",
        "mood": "Passionate",
        "color": "Ruby Red",
        "hobby": "Jewelry making",
        "description": "A fiery performer who shines bright like a precious gem."
    },

    "Nora": {
        "rarity": "Rare",
        "mood": "Mysterious",
        "color": "Starlight Blonde",
        "hobby": "Stargazing",
        "description": "A celestial dreamer with golden hair who maps the constellations and finds wonder in the night sky."
    },

    "Sara": {
        "rarity": "Rare",
        "mood": "Free-spirited",
        "color": "Ocean Teal",
        "hobby": "Surfing",
        "description": "A free spirit who loves riding the waves and chasing thrills."
    },

    "Hana": {
        "rarity": "Rare",
        "mood": "Traditional",
        "color": "Cherry Blossom",
        "hobby": "Tea ceremony",
        "description": "A graceful idol who honors tradition while embracing modern music."
    },

    # Epic Tier
    "Stella": {
        "rarity": "Epic",
        "mood": "Focused",
        "color": "Starlight Gold",
        "hobby": "Astronomy",
        "description": "A brilliant performer who channels cosmic energy through her music."
    },

    "Nova": {
        "rarity": "Epic",
        "mood": "Explosive",
        "color": "Galaxy Purple",
        "hobby": "DJ mixing",
        "description": "A high-energy idol who creates explosive beats from another dimension."
    },

    "Aria": {
        "rarity": "Epic",
        "mood": "Artistic",
        "color": "Rainbow Prism",
        "hobby": "Opera singing",
        "description": "A virtuoso vocalist whose voice can move hearts and shake stages."
    },

    "Iris": {
        "rarity": "Epic",
        "mood": "Magical",
        "color": "Blonde Gold",
        "hobby": "Collecting crystals",
        "description": "A magical girl with blonde hair who loves collecting purple crystals."
    },

    "Elsa": {
        "rarity": "Epic",
        "mood": "Cool",
        "color": "Ice Blue",
        "hobby": "Ice skating",
        "description": "A graceful ice queen who performs with elegant precision and cool confidence."
    },

    # Legendary Tier
    "Anna": {
        "rarity": "Legendary",
        "mood": "Energetic",
        "color": "Bright Orange",
        "hobby": "Performing on stage",
        "description": "The top idol everyone adores, with bright orange twin-tails and unstoppable energy on stage."
    },

    "Belle": {
        "rarity": "Legendary",
        "mood": "Enchanting",
        "color": "Golden Rose",
        "hobby": "Reading magical books",
        "description": "A beauty with brains who believes true magic lies in kindness and knowledge."
    },

    "Jasmine": {
        "rarity": "Legendary",
        "mood": "Adventurous",
        "color": "Desert Gold",
        "hobby": "Exploring new worlds",
        "description": "A fearless adventurer who brings exotic charm and unlimited courage to the stage."
    }
}


def get_idol_profile(name: str) -> dict | None:
    '''Returns the complete profile for an idol by name.'''
    return IDOL_PROFILES.get(name)


def get_idol_description(name: str) -> str:
    '''Returns just the description for an idol.'''
    profile = IDOL_PROFILES.get(name)
    if profile:
        return profile["description"]
    return "A mysterious idol with an unknown background."


def get_all_profiles_by_rarity(rarity: str) -> dict:
    '''Returns all idol profiles of a specific rarity tier.'''
    return {
        name: profile
        for name, profile in IDOL_PROFILES.items()
        if profile["rarity"] == rarity
    }