# Rule 205.4a
SUPERTYPES = {"Basic", "Legendary", "Snow", "World", "Host"}

# Rule 205.2a
TYPES = {"Land", "Creature", "Artifact", "Enchantment", "Planeswalker", "Instant", "Sorcery", "Tribal", "Battle"}

# Rule 205.3i
LAND_SUBTYPES = {
    "Plains", "Island", "Swamp", "Mountain", "Forest",
    "Cave", "Desert", "Gate", "Lair", "Locus",
    "Sphere", "Urza's", "Mine", "Power-Plant", "Tower"
}

# Rule 205.3m
CREATURE_SUBTYPES = {
     "Advisor", "Aetherborn", "Ally", "Angel", "Antelope", "Ape", "Archer", "Archon", "Army",
     "Artificer", "Assassin", "Assembly-Worker", "Atog", "Aurochs", "Avatar", "Azra", "Badger",
     "Barbarian", "Bard", "Basilisk", "Bat", "Bear", "Beast", "Beeble", "Beholder", "Berserker",
     "Bird", "Blinkmoth", "Boar", "Bringer", "Brushwagg", "Camarid", "Camel", "Capybara", "Caribou", "Carrier",
     "Cat", "Centaur", "Cephalid", "Chimera", "Citizen", "Cleric", "Cockatrice", "Construct", "Coward",
     "Crab", "Crocodile", "Cyclops", "Dauthi", "Demigod", "Demon", "Deserter", "Detective", "Devil", "Dinosaur",
     "Djinn", "Dog", "Dragon", "Drake", "Dreadnought", "Drone", "Druid", "Dryad", "Dwarf", "Efreet",
     "Egg", "Elder", "Eldrazi", "Elemental", "Elephant", "Elf", "Elk", "Eye", "Faerie", "Ferret",
     "Fish", "Flagbearer", "Fox", "Fractal", "Frog", "Fungus", "Gargoyle", "Germ", "Giant", "Gith", "Gnoll",
     "Gnome", "Goat", "Goblin", "God", "Golem", "Gorgon", "Graveborn", "Gremlin", "Griffin", "Hag",
     "Halfling", "Hamster", "Harpy", "Hellion", "Hippo", "Hippogriff", "Homarid", "Homunculus",
     "Horror", "Horse", "Human", "Hydra", "Hyena", "Illusion", "Imp", "Incarnation", "Inkling",
     "Insect", "Jackal", "Jellyfish", "Juggernaut", "Kavu", "Kirin", "Kithkin", "Knight", "Kobold",
     "Kor", "Kraken", "Lamia", "Lammasu", "Leech", "Leviathan", "Lhurgoyf", "Licid", "Lizard",
     "Manticore", "Masticore", "Mercenary", "Merfolk", "Metathran", "Minion", "Minotaur", "Mite", "Mole",
     "Monger", "Mongoose", "Monk", "Monkey", "Moonfolk", "Mouse", "Mutant", "Myr", "Mystic", "Naga",
     "Nautilus", "Nephilim", "Nightmare", "Nightstalker", "Ninja", "Noble", "Noggle", "Nomad", "Nymph",
     "Octopus", "Ogre", "Ooze", "Orb", "Orc", "Orgg", "Otter", "Ouphe", "Ox", "Oyster", "Pangolin",
     "Peasant", "Pegasus", "Pentavite", "Pest", "Phelddagrif", "Phoenix", "Phyrexian", "Pilot",
     "Pincher", "Pirate", "Plant", "Praetor", "Prism", "Processor", "Rabbit", "Raccoon", "Ranger",
     "Rat", "Rebel", "Reflection", "Rhino", "Rigger", "Rogue", "Sable", "Salamander", "Samurai",
     "Sand", "Saproling", "Satyr", "Scarecrow", "Scion", "Scorpion", "Scout", "Sculpture", "Serf",
     "Serpent", "Servo", "Shade", "Shaman", "Shapeshifter", "Shark", "Sheep", "Siren", "Skeleton",
     "Slith", "Sliver", "Slug", "Snail", "Snake", "Soldier", "Soltari", "Spawn", "Specter", "Spellshaper",
     "Sphinx", "Spider", "Spike", "Spirit", "Splinter", "Sponge", "Squid", "Squirrel", "Starfish",
     "Surrakar", "Survivor", "Tentacle", "Tetravite", "Thalakos", "Thopter", "Thrull", "Tiefling",
     "Treefolk", "Trilobite", "Triskelavite", "Troll", "Turtle", "Unicorn", "Vampire", "Vedalken",
     "Viashino", "Volver", "Wall", "Walrus", "Warlock", "Warrior", "Weird", "Werewolf", "Whale",
     "Wizard", "Wolf", "Wolverine", "Wombat", "Worm", "Wraith", "Wurm", "Yeti", "Zombie", "Zubera"
}

# Rule 205.3g
ARTIFACT_SUBTYPES = {
    "Blood", "Clue", "Contraption", "Equipment", "Food",
    "Gold", "Fortification", "Powerstone", "Treasure", "Vehicle"
}

# Rule 205.3h
ENCHANTMENT_SUBTYPES = {
    "Aura", "Cartouche", "Case", "Curse", "Rune", "Background", "Class", "Saga", "Shard", "Shrine"
}

# Rule 205.3j
PLANESWALKER_SUBTYPES = {
    "Ajani", "Aminatou", "Angrath", "Arlinn", "Ashiok", "Bahamut", "Basri", "Bolas", "Calix",
    "Chandra", "Dack", "Dakkon", "Daretti", "Davriel", "Dihada", "Domri", "Dovin", "Ellywick",
    "Elspeth", "Estrid", "Freyalise", "Garruk", "Gideon", "Grist", "Huatli", "Jace", "Jaya",
    "Jeska", "Kaito", "Karn", "Kasmina", "Kaya", "Kiora", "Koth", "Liliana", "Lolth", "Lukka",
    "Minsc", "Mordenkainen", "Nahiri", "Narset", "Niko", "Nissa", "Nixilis",  "Quintorius", "Oko", "Ral", "Rowan",
    "Saheeli", "Samut", "Sarkhan", "Serra", "Sorin", "Szat", "Tamiyo", "Tasha", "Teferi", "Teyo",
    "Tezzeret", "Tibalt", "Tyvar", "Ugin", "Urza", "Venser", "Vivien", "Vraska", "Will", "Windgrace",
    "Wrenn", "Xenagos", "Yanggu", "Yanling", "Zariel"
}

# Rule 205.3k
INSTANT_SUBTYPES = {"Adventure", "Arcane", "Chorus", "Trap"}

# Rule 205.3k
SORCERY_SUBTYPES = {"Adventure", "Arcane", "Lesson"}

# Rule ???
BATTLE_SUBTYPES = {"Siege"}

SUBTYPES = (LAND_SUBTYPES | CREATURE_SUBTYPES | ARTIFACT_SUBTYPES | ENCHANTMENT_SUBTYPES |
            PLANESWALKER_SUBTYPES | INSTANT_SUBTYPES | SORCERY_SUBTYPES | BATTLE_SUBTYPES)
