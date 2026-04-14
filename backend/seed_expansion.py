#!/usr/bin/env python3
"""
Seed expansion script: triple the database content.
Adds new categories, destinations, vendors, and activities with all sub-entities.

Run against Docker DB:
    DATABASE_URL=postgresql://postgres:password@localhost:5432/findtravelmate python seed_expansion.py

Or from inside Docker:
    docker exec -e DATABASE_URL=postgresql://postgres:changeme123@postgres:5432/findtravelmate \
        findtravelmate_backend python seed_expansion.py
"""

import os
import sys
import random
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import Base
from app.models.user import User, Vendor, UserRole
from app.models.activity import (
    Category, Destination, Activity, ActivityImage, ActivityCategory,
    ActivityDestination, ActivityHighlight, ActivityInclude, ActivityFAQ,
    MeetingPoint, ActivityTimeline, ActivityPricingTier, ActivityAddOn,
)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/findtravelmate",
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# ── New categories (20 new → total 30) ────────────────────────────────────────

NEW_CATEGORIES = [
    ("Water Sports", "water-sports", "🏄"),
    ("Wellness & Spa", "wellness-spa", "🧘"),
    ("Photography Tours", "photography", "📷"),
    ("Nightlife & Entertainment", "nightlife", "🎭"),
    ("Cooking Classes", "cooking", "👨‍🍳"),
    ("Wine & Spirits", "wine-spirits", "🍷"),
    ("Cycling & Biking", "cycling", "🚴"),
    ("Art & Workshops", "art-workshops", "🎨"),
    ("Sailing & Cruises", "sailing-cruises", "⛵"),
    ("Winter Sports", "winter-sports", "⛷️"),
    ("Yoga & Meditation", "yoga-meditation", "🧘‍♀️"),
    ("Architecture Tours", "architecture", "🏗️"),
    ("Music & Concerts", "music-concerts", "🎵"),
    ("Helicopter & Aerial", "helicopter-aerial", "🚁"),
    ("Train Journeys", "train-journeys", "🚂"),
    ("Farm & Countryside", "farm-countryside", "🌾"),
    ("Scuba Diving", "scuba-diving", "🤿"),
    ("Street Art Tours", "street-art", "🖌️"),
    ("Sunset Experiences", "sunset", "🌅"),
    ("Underground & Caves", "underground-caves", "🕳️"),
]

# ── New destinations (18 new → total ~35) ─────────────────────────────────────

NEW_DESTINATIONS = [
    ("Barcelona", "barcelona", "Spain", "ES", 41.3874, 2.1686, True),
    ("London", "london", "United Kingdom", "GB", 51.5074, -0.1278, True),
    ("New York", "new-york", "United States", "US", 40.7128, -74.0060, True),
    ("Bangkok", "bangkok", "Thailand", "TH", 13.7563, 100.5018, True),
    ("Istanbul", "istanbul", "Turkey", "TR", 41.0082, 28.9784, True),
    ("Dubai", "dubai", "United Arab Emirates", "AE", 25.2048, 55.2708, True),
    ("Sydney", "sydney", "Australia", "AU", -33.8688, 151.2093, False),
    ("Lisbon", "lisbon", "Portugal", "PT", 38.7223, -9.1393, False),
    ("Amsterdam", "amsterdam", "Netherlands", "NL", 52.3676, 4.9041, True),
    ("Prague", "prague", "Czech Republic", "CZ", 50.0755, 14.4378, False),
    ("Marrakech", "marrakech", "Morocco", "MA", 31.6295, -7.9811, False),
    ("Bali", "bali", "Indonesia", "ID", -8.3405, 115.0920, True),
    ("Kyoto", "kyoto", "Japan", "JP", 35.0116, 135.7681, True),
    ("Cape Town", "cape-town", "South Africa", "ZA", -33.9249, 18.4241, False),
    ("Dubrovnik", "dubrovnik", "Croatia", "HR", 42.6507, 18.0944, False),
    ("Vienna", "vienna", "Austria", "AT", 48.2082, 16.3738, False),
    ("Havana", "havana", "Cuba", "CU", 23.1136, -82.3666, False),
    ("Queenstown", "queenstown", "New Zealand", "NZ", -45.0312, 168.6626, False),
]

# ── New vendors (5 new → total 12) ────────────────────────────────────────────

NEW_VENDORS = [
    ("Mediterranean Explorer Co.", "vendor6@example.com", "Expert tours across Mediterranean destinations"),
    ("Asia Pacific Adventures", "vendor7@example.com", "Premium experiences across Asia and Pacific"),
    ("Urban Discovery Tours", "vendor8@example.com", "City-focused walking tours and cultural experiences"),
    ("Wild Atlantic Expeditions", "vendor9@example.com", "Adventure and nature experiences worldwide"),
    ("Heritage & Craft Journeys", "vendor10@example.com", "Artisan workshops and cultural heritage tours"),
]

# ── 42 new activities ─────────────────────────────────────────────────────────

NEW_ACTIVITIES = [
    # Barcelona (4 activities)
    {
        "title": "Barcelona Gothic Quarter Walking Tour & Tapas Tasting",
        "slug": "barcelona-gothic-quarter-walking-tapas",
        "dest": "barcelona",
        "cats": ["tours", "food-drink"],
        "price": 55, "duration": 210, "group": 15,
        "desc": "Wander through the labyrinthine streets of Barcelona's Gothic Quarter, where Roman ruins meet medieval architecture. Your knowledgeable guide reveals hidden courtyards, ancient temples, and stories spanning 2,000 years. The tour culminates with a tapas tasting at a local bodega, sampling traditional Catalan dishes paired with regional wines.",
        "short": "Discover Barcelona's medieval heart with hidden gems and authentic tapas tasting",
        "langs": ["english", "spanish"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Comfortable walking shoes, camera, light jacket",
    },
    {
        "title": "Sagrada Familia Skip-the-Line Tour with Tower Access",
        "slug": "sagrada-familia-skip-line-tower-access",
        "dest": "barcelona",
        "cats": ["tours", "architecture"],
        "price": 85, "duration": 150, "group": 12,
        "desc": "Skip the notoriously long queues and step inside Gaudi's masterpiece with an expert art historian. Marvel at the forest-like interior columns, the kaleidoscopic stained glass windows, and ascend one of the iconic towers for panoramic city views. Learn about the 140-year construction saga and the innovative techniques Gaudi pioneered.",
        "short": "Priority access to Gaudi's masterpiece with tower ascent and expert guide",
        "langs": ["english", "spanish", "french"], "bestseller": True, "skip_line": True,
        "what_to_bring": "Covered shoulders and knees required, camera",
    },
    {
        "title": "Barcelona Sunset Sailing with Cava & Snacks",
        "slug": "barcelona-sunset-sailing-cava",
        "dest": "barcelona",
        "cats": ["sailing-cruises", "sunset"],
        "price": 75, "duration": 120, "group": 10,
        "desc": "Set sail from Port Olympic aboard a sleek catamaran as the sun paints Barcelona's skyline in gold. Sip chilled cava and enjoy Mediterranean snacks while gliding past the W Hotel, Barceloneta Beach, and the port. Perfect for couples, friends, or anyone wanting a magical evening on the water.",
        "short": "Sail Barcelona's coast at golden hour with sparkling cava and views",
        "langs": ["english", "spanish"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Sunscreen, light jacket, swimwear if you wish",
    },
    {
        "title": "Catalan Cooking Masterclass in a Chef's Home Kitchen",
        "slug": "catalan-cooking-masterclass-barcelona",
        "dest": "barcelona",
        "cats": ["cooking", "food-drink"],
        "price": 95, "duration": 240, "group": 8,
        "desc": "Join a local chef in their private kitchen for an intimate cooking session. Visit La Boqueria market together to select the freshest seasonal ingredients, then return to prepare a full Catalan meal: pa amb tomaquet, seafood paella, and crema catalana. Enjoy your creations with wine and take home the recipes.",
        "short": "Market visit and hands-on Catalan cooking with a local chef",
        "langs": ["english", "spanish"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Appetite, comfortable clothing",
    },
    # London (4 activities)
    {
        "title": "Tower of London & Crown Jewels Early Access Tour",
        "slug": "tower-of-london-crown-jewels-early-access",
        "dest": "london",
        "cats": ["tours", "historical"],
        "price": 95, "duration": 180, "group": 15,
        "desc": "Enter the Tower of London before the general public and see the Crown Jewels without the crowds. Your expert Yeoman Warder-style guide brings 1,000 years of royal intrigue to life — from the imprisonment of Anne Boleyn to the mysterious disappearance of the Princes in the Tower. Includes the White Tower, Traitors' Gate, and the iconic ravens.",
        "short": "Beat the crowds at the Tower of London with priority Crown Jewels viewing",
        "langs": ["english"], "bestseller": True, "skip_line": True,
        "what_to_bring": "Comfortable shoes, umbrella, camera",
    },
    {
        "title": "London Street Art & East End Culture Walk",
        "slug": "london-street-art-east-end-walk",
        "dest": "london",
        "cats": ["street-art", "tours"],
        "price": 40, "duration": 150, "group": 18,
        "desc": "Explore Shoreditch and Brick Lane through the lens of street art. Spot works by Banksy, Stik, and ROA while learning how this once-industrial neighborhood became London's creative epicenter. Visit hidden courtyards, independent galleries, and hear stories of the artists who transformed these streets into open-air museums.",
        "short": "Discover Banksy, Stik, and London's vibrant street art scene",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Camera, comfortable walking shoes",
    },
    {
        "title": "Thames River Evening Cruise with Dinner & Live Jazz",
        "slug": "thames-evening-cruise-dinner-jazz",
        "dest": "london",
        "cats": ["sailing-cruises", "nightlife"],
        "price": 120, "duration": 180, "group": 40,
        "desc": "Glide past London's illuminated landmarks — the Houses of Parliament, the London Eye, Tower Bridge, and the Shard — while enjoying a three-course dinner with live jazz accompaniment. A sophisticated evening combining world-class cuisine, smooth music, and one of the most scenic river journeys in the world.",
        "short": "Three-course dinner cruise past London's illuminated skyline with live jazz",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Smart casual attire, camera",
    },
    {
        "title": "Harry Potter Film Locations Walking Tour",
        "slug": "london-harry-potter-film-locations-tour",
        "dest": "london",
        "cats": ["tours", "family"],
        "price": 35, "duration": 150, "group": 20,
        "desc": "Step into the wizarding world with this magical walking tour through central London. Visit the real-life locations that inspired J.K. Rowling and were featured in the films: Leadenhall Market (Diagon Alley), the Millennium Bridge, King's Cross Platform 9¾, and more. Your guide shares behind-the-scenes film trivia throughout.",
        "short": "Visit real Harry Potter film locations across central London",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Wand optional, comfortable shoes essential",
    },
    # New York (3 activities)
    {
        "title": "New York Helicopter Tour over Manhattan",
        "slug": "new-york-helicopter-tour-manhattan",
        "dest": "new-york",
        "cats": ["helicopter-aerial", "tours"],
        "price": 250, "duration": 30, "group": 6,
        "desc": "Soar above the Manhattan skyline for breathtaking aerial views of the Statue of Liberty, Central Park, the Empire State Building, and the Brooklyn Bridge. This thrilling 30-minute helicopter flight offers unparalleled photo opportunities and a perspective of New York City that few ever experience.",
        "short": "Iconic aerial views of Manhattan, Statue of Liberty, and Central Park",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Camera, dark clothing reduces window reflections",
    },
    {
        "title": "Brooklyn Food & Culture Walking Tour",
        "slug": "brooklyn-food-culture-walking-tour",
        "dest": "new-york",
        "cats": ["food-drink", "tours"],
        "price": 80, "duration": 210, "group": 12,
        "desc": "Cross the iconic Brooklyn Bridge on foot and dive into DUMBO, Williamsburg, and Bushwick's thriving food scene. Sample artisanal pizza, craft chocolate, authentic dumplings, and small-batch coffee while learning about the immigrant communities that shaped Brooklyn's culinary identity. Includes 6+ tastings — come hungry!",
        "short": "Cross the Brooklyn Bridge and taste your way through Brooklyn's best bites",
        "langs": ["english", "spanish"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Empty stomach, comfortable walking shoes",
    },
    {
        "title": "Central Park Sunrise Yoga & Meditation Session",
        "slug": "central-park-sunrise-yoga-meditation",
        "dest": "new-york",
        "cats": ["yoga-meditation", "wellness-spa"],
        "price": 35, "duration": 75, "group": 20,
        "desc": "Start your morning with a revitalizing yoga flow in the heart of Central Park. As the city wakes up around you, find your center with guided meditation on the Great Lawn. Suitable for all levels, mats and props provided. Ends with herbal tea and a moment of gratitude amid nature.",
        "short": "Morning yoga and meditation in Central Park with all equipment provided",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Comfortable clothing, water bottle",
    },
    # Bangkok (3 activities)
    {
        "title": "Bangkok Floating Market & Temple Tour by Longtail Boat",
        "slug": "bangkok-floating-market-temple-longtail-boat",
        "dest": "bangkok",
        "cats": ["tours", "food-drink"],
        "price": 60, "duration": 360, "group": 10,
        "desc": "Cruise through Bangkok's iconic canals aboard a traditional longtail boat to the Damnoen Saduak Floating Market. Bargain for tropical fruits, taste pad thai cooked on a boat, and visit the stunning Wat Arun and Wat Pho temples. Experience the 'Venice of the East' as locals have for centuries.",
        "short": "Longtail boat through floating markets and Bangkok's grandest temples",
        "langs": ["english", "chinese"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Sunscreen, hat, modest clothing for temples, cash for market",
    },
    {
        "title": "Thai Boxing (Muay Thai) Training Experience",
        "slug": "bangkok-muay-thai-training-experience",
        "dest": "bangkok",
        "cats": ["adventure", "wellness-spa"],
        "price": 45, "duration": 120, "group": 12,
        "desc": "Train with a professional Muay Thai champion at an authentic Bangkok gym. Learn basic stances, punches, kicks, and combinations in a supportive environment. Suitable for complete beginners to intermediate level. Cool down with a coconut water and hear about the cultural significance of Thailand's national sport.",
        "short": "Train with a Muay Thai champion at an authentic Bangkok gym",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Athletic wear, towel, water bottle, change of clothes",
    },
    {
        "title": "Bangkok Night Food Tour by Tuk-Tuk",
        "slug": "bangkok-night-food-tour-tuktuk",
        "dest": "bangkok",
        "cats": ["food-drink", "nightlife"],
        "price": 70, "duration": 240, "group": 8,
        "desc": "Hop aboard a tuk-tuk and zoom through Bangkok's neon-lit streets to discover the city's legendary street food scene. Visit Chinatown's Yaowarat Road, hidden night markets, and roadside stalls that have served locals for generations. Taste 10+ dishes including mango sticky rice, boat noodles, and grilled satay.",
        "short": "Tuk-tuk adventure through Bangkok's best street food spots after dark",
        "langs": ["english", "chinese"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Cash, camera, stretchy pants",
    },
    # Istanbul (3 activities)
    {
        "title": "Istanbul Grand Bazaar & Spice Market Guided Tour",
        "slug": "istanbul-grand-bazaar-spice-market-tour",
        "dest": "istanbul",
        "cats": ["tours", "food-drink"],
        "price": 50, "duration": 180, "group": 12,
        "desc": "Navigate the legendary Grand Bazaar's 4,000+ shops with a local guide who knows its secrets. Learn the art of Turkish bargaining, discover hidden caravanserais, and sample Turkish delight and apple tea. Continue to the Spice Market for an aromatic exploration of saffron, sumac, and exotic blends.",
        "short": "Expert-guided journey through Istanbul's legendary markets and flavors",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Cash for shopping, comfortable shoes, camera",
    },
    {
        "title": "Bosphorus Sunset Cruise with Turkish Dinner",
        "slug": "istanbul-bosphorus-sunset-cruise-dinner",
        "dest": "istanbul",
        "cats": ["sailing-cruises", "sunset"],
        "price": 85, "duration": 180, "group": 30,
        "desc": "Sail the strait that divides Europe and Asia as the sun sets over Istanbul's minarets and palaces. Pass Dolmabahce Palace, the Maiden's Tower, and the Rumeli Fortress while enjoying a traditional Turkish dinner of mezze, kebabs, and baklava with live music and folk dancing onboard.",
        "short": "Sunset sail between two continents with Turkish feast and live music",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Light jacket, camera",
    },
    {
        "title": "Turkish Hammam & Spa Ritual Experience",
        "slug": "istanbul-turkish-hammam-spa-ritual",
        "dest": "istanbul",
        "cats": ["wellness-spa"],
        "price": 65, "duration": 90, "group": 1,
        "desc": "Experience an authentic Turkish bath in a beautifully restored 16th-century hammam. The traditional ritual includes a steam room session, full-body scrub with a kese mitt, foam massage, and relaxation with Turkish tea. A centuries-old wellness tradition that leaves you deeply rejuvenated.",
        "short": "Traditional Turkish bath ritual in a historic 16th-century hammam",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Swimwear, the rest is provided",
    },
    # Amsterdam (3 activities)
    {
        "title": "Amsterdam Canal Cruise & Rijksmuseum Combo Tour",
        "slug": "amsterdam-canal-cruise-rijksmuseum-combo",
        "dest": "amsterdam",
        "cats": ["sailing-cruises", "museums"],
        "price": 75, "duration": 240, "group": 20,
        "desc": "Start with a scenic cruise through Amsterdam's UNESCO-listed canal ring, learning about the Golden Age mansions and hidden churches. Then skip the line at the Rijksmuseum for a guided tour of Rembrandt's Night Watch, Vermeer's Milkmaid, and the museum's greatest treasures.",
        "short": "Canal cruise through UNESCO waterways plus skip-the-line Rijksmuseum",
        "langs": ["english", "french"], "bestseller": True, "skip_line": True,
        "what_to_bring": "Rain jacket, camera",
    },
    {
        "title": "Amsterdam Craft Beer & Brewery Cycling Tour",
        "slug": "amsterdam-craft-beer-brewery-cycling-tour",
        "dest": "amsterdam",
        "cats": ["cycling", "wine-spirits"],
        "price": 65, "duration": 210, "group": 12,
        "desc": "Cycle like a local through Amsterdam's charming neighborhoods while visiting three independent craft breweries. Sample 10+ Dutch craft beers, learn about the brewing process from passionate brewmasters, and discover why the Netherlands has become Europe's craft beer capital. Bike and tastings included.",
        "short": "Cycle to Amsterdam's best craft breweries with guided tastings",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Valid ID (18+), comfortable clothes, rain jacket",
    },
    {
        "title": "Anne Frank & Jewish Heritage Quarter Walking Tour",
        "slug": "amsterdam-anne-frank-jewish-heritage-tour",
        "dest": "amsterdam",
        "cats": ["historical", "tours"],
        "price": 45, "duration": 150, "group": 15,
        "desc": "Walk in the footsteps of Anne Frank through Amsterdam's Jewish Heritage Quarter. Visit the Portuguese Synagogue, the Jewish Historical Museum, and Westerkerk. Your guide shares deeply personal stories of resistance, survival, and the vibrant Jewish community that shaped Amsterdam's identity.",
        "short": "Moving walk through Amsterdam's Jewish Heritage Quarter and Anne Frank's world",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Comfortable shoes, umbrella",
    },
    # Bali (3 activities)
    {
        "title": "Bali Rice Terrace Trek & Waterfall Swimming Adventure",
        "slug": "bali-rice-terrace-waterfall-trek",
        "dest": "bali",
        "cats": ["outdoor", "nature"],
        "price": 55, "duration": 480, "group": 10,
        "desc": "Trek through the iconic Tegallalang rice terraces, learning about the ancient subak irrigation system. Continue through lush jungle trails to a hidden waterfall for a refreshing swim. Enjoy a traditional Balinese lunch overlooking the terraces. An unforgettable immersion in Bali's natural beauty.",
        "short": "Trek emerald rice terraces and swim at a secret jungle waterfall",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Swimwear, hiking shoes, sunscreen, insect repellent",
    },
    {
        "title": "Bali Sunrise at Mount Batur with Hot Springs",
        "slug": "bali-mount-batur-sunrise-hot-springs",
        "dest": "bali",
        "cats": ["adventure", "outdoor"],
        "price": 65, "duration": 600, "group": 12,
        "desc": "Begin the pre-dawn trek up Mount Batur, an active volcano, arriving at the summit for a spectacular sunrise above the clouds. Watch the sky transform as Lake Batur and Mount Agung emerge in the golden light. Descend to natural volcanic hot springs for a soothing soak. Breakfast included at the summit.",
        "short": "Volcanic summit sunrise with breakfast and natural hot springs recovery",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Warm layers, flashlight, hiking shoes, camera",
    },
    {
        "title": "Balinese Cooking Class in a Traditional Village",
        "slug": "bali-cooking-class-traditional-village",
        "dest": "bali",
        "cats": ["cooking", "food-drink"],
        "price": 45, "duration": 300, "group": 10,
        "desc": "Visit a local market to shop for exotic ingredients, then travel to a family compound in a traditional village. Learn to prepare 7 Balinese dishes from scratch using a wood-fired kitchen: satay lilit, lawar, nasi goreng, and more. Eat your creations in a tropical garden setting.",
        "short": "Market-to-table Balinese cooking in a family village compound",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Comfortable clothes, appetite",
    },
    # Kyoto (3 activities)
    {
        "title": "Kyoto Traditional Tea Ceremony & Zen Garden Tour",
        "slug": "kyoto-tea-ceremony-zen-garden-tour",
        "dest": "kyoto",
        "cats": ["museums", "wellness-spa"],
        "price": 70, "duration": 180, "group": 8,
        "desc": "Experience the art of Japanese tea ceremony (chado) in a 200-year-old machiya townhouse. A tea master guides you through each graceful movement while explaining the Zen philosophy behind this ancient ritual. Then visit Ryoanji's famous rock garden and the golden pavilion of Kinkaku-ji.",
        "short": "Authentic tea ceremony in a historic townhouse plus Zen garden visits",
        "langs": ["english", "chinese"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Socks required (no shoes indoors), camera",
    },
    {
        "title": "Arashiyama Bamboo Grove & Monkey Park Cycling Tour",
        "slug": "kyoto-arashiyama-bamboo-cycling-tour",
        "dest": "kyoto",
        "cats": ["cycling", "nature"],
        "price": 55, "duration": 240, "group": 10,
        "desc": "Cycle through Kyoto's scenic western district to the ethereal Arashiyama Bamboo Grove. Continue to Iwatayama Monkey Park where wild macaques roam freely with panoramic city views. Cross the iconic Togetsukyo Bridge and visit the serene Tenryu-ji Temple. Lunch at a riverside noodle shop.",
        "short": "Cycle to the magical Bamboo Grove, monkey park, and riverside temples",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Comfortable clothes, sunscreen, camera",
    },
    {
        "title": "Kyoto Geisha District Night Walk & Sake Tasting",
        "slug": "kyoto-geisha-district-night-walk-sake",
        "dest": "kyoto",
        "cats": ["nightlife", "wine-spirits"],
        "price": 80, "duration": 180, "group": 10,
        "desc": "Stroll through Gion, Kyoto's atmospheric geisha district, as lanterns illuminate the wooden machiya houses. Your guide explains the secretive world of geisha and maiko while you explore hidden alleyways. End at a traditional sake bar for a curated tasting of five premium sakes paired with small plates.",
        "short": "Lantern-lit walk through Gion's geisha district with premium sake tasting",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Valid ID (20+ for sake), camera, comfortable shoes",
    },
    # Dubai (3 activities)
    {
        "title": "Desert Safari with Dune Bashing, Camel Ride & BBQ Dinner",
        "slug": "dubai-desert-safari-dune-bashing-bbq",
        "dest": "dubai",
        "cats": ["adventure", "tours"],
        "price": 85, "duration": 420, "group": 20,
        "desc": "Experience the thrill of dune bashing in a 4x4 across the Arabian desert, then slow down with a camel ride at sunset. At a Bedouin-style camp, try sandboarding, get henna art, and watch belly dancing under the stars. Feast on a lavish BBQ dinner with grilled meats, Arabic mezze, and shisha.",
        "short": "Ultimate desert adventure with dune bashing, sunset camels, and starlit BBQ",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Sunglasses, sunscreen, camera, light clothing",
    },
    {
        "title": "Burj Khalifa At the Top & Dubai Fountain Show",
        "slug": "dubai-burj-khalifa-top-fountain-show",
        "dest": "dubai",
        "cats": ["tours", "architecture"],
        "price": 65, "duration": 120, "group": 15,
        "desc": "Ascend the world's tallest building to the 124th and 125th floor observation decks for jaw-dropping 360-degree views of Dubai's skyline, coastline, and desert beyond. Time your visit for sunset and descend to watch the spectacular Dubai Fountain show choreographed to music on Burj Khalifa Lake.",
        "short": "Sunset at the top of the world's tallest building plus fountain show",
        "langs": ["english"], "bestseller": True, "skip_line": True,
        "what_to_bring": "Camera, valid ID",
    },
    {
        "title": "Dubai Marina Luxury Yacht Cruise with Brunch",
        "slug": "dubai-marina-luxury-yacht-brunch",
        "dest": "dubai",
        "cats": ["sailing-cruises", "luxury"],
        "price": 150, "duration": 180, "group": 12,
        "desc": "Cruise Dubai Marina and Palm Jumeirah aboard a private luxury yacht. Sip champagne and enjoy a gourmet brunch spread while passing Atlantis The Palm, Bluewaters Island, and the marina's iconic skyscrapers. Swim stops included at secluded spots along the coast.",
        "short": "Private yacht brunch cruising past Palm Jumeirah and Dubai Marina",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Swimwear, sunscreen, sunglasses",
    },
    # Lisbon (3 activities)
    {
        "title": "Lisbon Tram 28 Route & Alfama District Walking Tour",
        "slug": "lisbon-tram-28-alfama-walking-tour",
        "dest": "lisbon",
        "cats": ["tours", "historical"],
        "price": 40, "duration": 180, "group": 15,
        "desc": "Ride the iconic yellow Tram 28 through Lisbon's steepest hills, then explore the Alfama district on foot. Discover Fado music venues, ancient Moorish architecture, and viewpoints offering sweeping views over the Tagus River. Your guide shares tales of explorers, earthquakes, and the revolution of 1974.",
        "short": "Iconic tram ride and walk through Lisbon's oldest and most charming district",
        "langs": ["english", "spanish"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Comfortable walking shoes (steep hills!), camera",
    },
    {
        "title": "Sintra Palaces & Cabo da Roca Day Trip from Lisbon",
        "slug": "lisbon-sintra-palaces-cabo-da-roca-daytrip",
        "dest": "lisbon",
        "cats": ["tours", "historical"],
        "price": 75, "duration": 480, "group": 12,
        "desc": "Escape to the fairytale world of Sintra's UNESCO palaces. Visit the colorful Pena Palace perched on a hilltop, explore the mysterious Quinta da Regaleira with its initiatic well, and drive to Cabo da Roca — the westernmost point of mainland Europe. Includes local pastry tasting.",
        "short": "Fairytale palaces, mysterious wells, and Europe's western edge",
        "langs": ["english", "spanish"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Comfortable shoes, layers (Sintra is cooler), camera",
    },
    {
        "title": "Lisbon Pastéis de Nata Baking Workshop",
        "slug": "lisbon-pasteis-de-nata-baking-workshop",
        "dest": "lisbon",
        "cats": ["cooking", "food-drink"],
        "price": 55, "duration": 150, "group": 10,
        "desc": "Master Portugal's most beloved pastry in this hands-on workshop. A local pastry chef teaches you the secrets of crispy puff pastry and silky custard filling. Bake your own batch of pastéis de nata and learn why the original recipe from Belém remains a closely guarded secret since 1837.",
        "short": "Learn to bake Portugal's iconic custard tarts from a master pastry chef",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Appetite, comfortable clothing",
    },
    # Prague (2 activities)
    {
        "title": "Prague Castle & Old Town Astronomical Clock Tour",
        "slug": "prague-castle-old-town-astronomical-clock",
        "dest": "prague",
        "cats": ["historical", "tours"],
        "price": 50, "duration": 210, "group": 15,
        "desc": "Explore the world's largest ancient castle complex with its Gothic cathedral, royal palace, and Golden Lane. Cross the Charles Bridge adorned with baroque statues and reach Old Town Square to witness the 600-year-old Astronomical Clock in action. A comprehensive journey through Bohemian history.",
        "short": "Full Prague experience: castle complex, Charles Bridge, and medieval Old Town",
        "langs": ["english"], "bestseller": True, "skip_line": True,
        "what_to_bring": "Comfortable walking shoes, camera",
    },
    {
        "title": "Prague Underground: Medieval Cellars & Beer Tasting",
        "slug": "prague-underground-medieval-cellars-beer",
        "dest": "prague",
        "cats": ["underground-caves", "wine-spirits"],
        "price": 55, "duration": 150, "group": 12,
        "desc": "Descend beneath Prague's streets into a network of medieval cellars and tunnels most tourists never see. Learn about the hidden history below the city while visiting three underground venues. Finish with a Czech beer tasting in a 14th-century cellar bar, sampling pilsners, dark lagers, and local craft brews.",
        "short": "Explore secret medieval tunnels beneath Prague with Czech beer tasting",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Warm layer (cellars are cool), comfortable shoes, valid ID",
    },
    # Cape Town (2 activities)
    {
        "title": "Table Mountain Hike & Cape Peninsula Scenic Drive",
        "slug": "cape-town-table-mountain-cape-peninsula",
        "dest": "cape-town",
        "cats": ["outdoor", "nature"],
        "price": 90, "duration": 540, "group": 10,
        "desc": "Hike the Platteklip Gorge route up Table Mountain for panoramic views from the flat summit. After descending by cable car, drive the spectacular Cape Peninsula past Chapman's Peak, visit the penguin colony at Boulders Beach, and reach the Cape of Good Hope — where two oceans meet.",
        "short": "Summit Table Mountain and drive to the Cape of Good Hope with penguins",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Hiking shoes, sunscreen, water, windbreaker, camera",
    },
    {
        "title": "Cape Winelands Full-Day Tour with Tastings & Lunch",
        "slug": "cape-town-winelands-tastings-lunch",
        "dest": "cape-town",
        "cats": ["wine-spirits", "food-drink"],
        "price": 95, "duration": 480, "group": 12,
        "desc": "Visit three award-winning wine estates in Stellenbosch and Franschhoek, South Africa's premier wine regions. Sample Pinotage, Chenin Blanc, and blends unique to the Cape while learning about the 350-year winemaking tradition. Includes a gourmet lunch at a vineyard restaurant with mountain views.",
        "short": "Three estate tastings in Stellenbosch and Franschhoek with vineyard lunch",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Sunscreen, camera, jacket for wine cellars",
    },
    # Dubrovnik (2 activities)
    {
        "title": "Dubrovnik City Walls Walk & Game of Thrones Tour",
        "slug": "dubrovnik-city-walls-game-of-thrones",
        "dest": "dubrovnik",
        "cats": ["historical", "tours"],
        "price": 55, "duration": 180, "group": 15,
        "desc": "Walk the complete circuit of Dubrovnik's medieval city walls — a 2km path offering stunning Adriatic views. Then explore the filming locations of Game of Thrones with a guide who brings King's Landing to life: the Walk of Shame steps, the Red Keep, and Blackwater Bay.",
        "short": "Medieval walls circuit and Game of Thrones filming locations tour",
        "langs": ["english"], "bestseller": True, "skip_line": True,
        "what_to_bring": "Sunscreen, hat, water, comfortable shoes",
    },
    {
        "title": "Dubrovnik Sea Kayaking & Lokrum Island Snorkeling",
        "slug": "dubrovnik-sea-kayaking-lokrum-snorkeling",
        "dest": "dubrovnik",
        "cats": ["water-sports", "adventure"],
        "price": 50, "duration": 180, "group": 10,
        "desc": "Paddle along Dubrovnik's dramatic city walls from the sea, exploring hidden caves and pristine beaches inaccessible by land. Cross to Lokrum Island for snorkeling in crystal-clear Adriatic waters and explore the island's botanical garden and medieval monastery ruins.",
        "short": "Kayak along the medieval walls and snorkel at pristine Lokrum Island",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Swimwear, sunscreen, waterproof camera, water shoes",
    },
    # Vienna (2 activities)
    {
        "title": "Vienna Classical Concert at Schönbrunn Palace Orangery",
        "slug": "vienna-classical-concert-schonbrunn-orangery",
        "dest": "vienna",
        "cats": ["music-concerts", "luxury"],
        "price": 85, "duration": 120, "group": 50,
        "desc": "Attend an evening of Mozart and Strauss performed by the Schönbrunn Palace Orchestra in the stunning Orangery, where Mozart himself once performed. The intimate Baroque hall provides extraordinary acoustics. Optional upgrade includes a pre-concert dinner in a palace-adjacent restaurant.",
        "short": "Mozart and Strauss in the palace where Mozart once performed",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Smart casual attire, camera (no flash during performance)",
    },
    {
        "title": "Viennese Coffee House Culture & Pastry Walking Tour",
        "slug": "vienna-coffee-house-pastry-walking-tour",
        "dest": "vienna",
        "cats": ["food-drink", "tours"],
        "price": 55, "duration": 180, "group": 12,
        "desc": "Discover why Vienna's coffee house culture is UNESCO-listed on this delicious walking tour. Visit three legendary cafés, each with distinct character and history. Sample Sachertorte, Apfelstrudel, and Melange coffee while your guide shares stories of the writers, artists, and revolutionaries who shaped their culture here.",
        "short": "UNESCO coffee culture tour with Sachertorte, strudel, and stories",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Appetite for pastry, camera",
    },
    # Marrakech (2 activities)
    {
        "title": "Marrakech Medina & Souks Guided Discovery Tour",
        "slug": "marrakech-medina-souks-guided-discovery",
        "dest": "marrakech",
        "cats": ["tours", "art-workshops"],
        "price": 40, "duration": 240, "group": 12,
        "desc": "Navigate the mesmerizing labyrinth of Marrakech's medina with a born-and-raised local guide. Explore the vibrant souks of spices, leather, and metalwork, visit the serene Bahia Palace, and discover the hidden Ben Youssef Madrasa. Learn to negotiate like a local and taste freshly squeezed orange juice in Jemaa el-Fna.",
        "short": "Local-guided exploration of Marrakech's souks, palaces, and hidden gems",
        "langs": ["english", "french"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Comfortable shoes, cash for souks, hat, sunscreen",
    },
    {
        "title": "Atlas Mountains Day Trek & Berber Village Lunch",
        "slug": "marrakech-atlas-mountains-berber-village-trek",
        "dest": "marrakech",
        "cats": ["outdoor", "adventure"],
        "price": 65, "duration": 540, "group": 10,
        "desc": "Escape the city heat with a day trek in the Atlas Mountains. Hike through walnut groves and terraced fields to a traditional Berber village, where a local family welcomes you for a home-cooked tagine lunch with mint tea. Stunning mountain scenery and authentic cultural exchange.",
        "short": "Mountain trek to a Berber village with traditional tagine lunch",
        "langs": ["english", "french"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Hiking shoes, sunscreen, layers, water bottle",
    },
    # Sydney (2 activities)
    {
        "title": "Sydney Harbour Bridge Climb at Twilight",
        "slug": "sydney-harbour-bridge-climb-twilight",
        "dest": "sydney",
        "cats": ["adventure", "sunset"],
        "price": 180, "duration": 210, "group": 14,
        "desc": "Climb to the summit of the Sydney Harbour Bridge at twilight for the ultimate panoramic view as the city transforms from day to night. Watch the sunset paint the Opera House and harbour gold, then see the city lights switch on below you. An adrenaline-pumping bucket-list experience.",
        "short": "Climb the Harbour Bridge at sunset for 360-degree city panoramas",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Closed-toe shoes, no loose items (lockers provided)",
    },
    {
        "title": "Sydney Coastal Walk: Bondi to Coogee with Brunch",
        "slug": "sydney-bondi-to-coogee-coastal-walk-brunch",
        "dest": "sydney",
        "cats": ["outdoor", "nature"],
        "price": 45, "duration": 240, "group": 12,
        "desc": "Walk the famous 6km Bondi to Coogee coastal trail, one of the world's most scenic urban walks. Pass dramatic sandstone cliffs, ocean pools, Aboriginal rock carvings, and pristine beaches. Start with brunch at a Bondi café and learn about the coastal ecology and local surf culture.",
        "short": "Iconic coastal walk past cliffs, ocean pools, and beaches with beachside brunch",
        "langs": ["english"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Sunscreen, hat, swimwear, comfortable shoes, water",
    },
    # Queenstown (1 activity)
    {
        "title": "Queenstown Bungee Jump at Kawarau Bridge",
        "slug": "queenstown-bungee-jump-kawarau-bridge",
        "dest": "queenstown",
        "cats": ["adventure"],
        "price": 175, "duration": 120, "group": 20,
        "desc": "Take the plunge at the world's original commercial bungee jump site — the iconic Kawarau Bridge, 43 meters above the turquoise Kawarau River. Professional jump masters guide you through every step. Optional water touch and tandem jumps available. Free photo and video package included.",
        "short": "Leap from the world's first bungee site above a turquoise gorge",
        "langs": ["english"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Comfortable clothing, courage",
    },
    # Havana (1 activity)
    {
        "title": "Havana Classic Car Tour & Salsa Dancing Lesson",
        "slug": "havana-classic-car-tour-salsa-lesson",
        "dest": "havana",
        "cats": ["tours", "music-concerts"],
        "price": 70, "duration": 300, "group": 4,
        "desc": "Cruise through Havana in a meticulously restored 1950s American convertible. Visit the Malecón, Capitolio, Plaza de la Revolución, and colorful Old Havana. Then step into a local dance studio for a private salsa lesson with a professional Cuban dancer. Mojitos included.",
        "short": "1950s convertible cruise through Havana with private salsa lesson",
        "langs": ["english", "spanish"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Comfortable shoes for dancing, sunscreen, camera",
    },
    # Paris (existing destination, new activities)
    {
        "title": "Paris Photography Tour: Iconic Spots & Hidden Gems",
        "slug": "paris-photography-tour-iconic-hidden-gems",
        "dest": "paris",
        "cats": ["photography", "tours"],
        "price": 85, "duration": 210, "group": 8,
        "desc": "Capture Paris through the lens with a professional photographer as your guide. Visit both iconic landmarks and secret spots only photographers know — hidden courtyards, cobblestone passages, and rooftop viewpoints. Get personalized tips on composition, lighting, and editing. All camera types welcome.",
        "short": "Professional photographer-led tour of Paris's most photogenic spots",
        "langs": ["english", "french"], "bestseller": False, "skip_line": False,
        "what_to_bring": "Camera or smartphone, comfortable shoes, memory card",
    },
    # Rome (existing destination, new activity)
    {
        "title": "Rome Underground: Catacombs & Ancient Aqueducts Tour",
        "slug": "rome-underground-catacombs-aqueducts-tour",
        "dest": "rome",
        "cats": ["underground-caves", "historical"],
        "price": 70, "duration": 180, "group": 12,
        "desc": "Descend beneath Rome to explore the mysterious catacombs of San Callisto, where early Christians buried their dead in miles of underground tunnels. Continue to a section of ancient Roman aqueduct normally closed to the public. A haunting, fascinating journey through Rome's hidden layers.",
        "short": "Explore ancient catacombs and secret aqueducts beneath the Eternal City",
        "langs": ["english"], "bestseller": True, "skip_line": True,
        "what_to_bring": "Warm layer, comfortable shoes, camera (no flash in catacombs)",
    },
    # Tokyo (existing destination, new activity)
    {
        "title": "Tokyo Tsukiji Outer Market Food Tour & Sushi Making",
        "slug": "tokyo-tsukiji-market-food-tour-sushi-making",
        "dest": "tokyo",
        "cats": ["food-drink", "cooking"],
        "price": 90, "duration": 240, "group": 10,
        "desc": "Explore Tokyo's legendary Tsukiji Outer Market with a local foodie guide. Sample tamagoyaki, fresh sashimi, wagyu skewers, and Japanese street snacks. Then head to a nearby kitchen for a hands-on sushi-making class where you learn to prepare nigiri and maki rolls like a Tokyo sushi chef.",
        "short": "Tsukiji market grazing plus hands-on sushi-making with a local chef",
        "langs": ["english", "chinese"], "bestseller": True, "skip_line": False,
        "what_to_bring": "Empty stomach, camera, cash for extra market purchases",
    },
]

# ── Timeline templates ─────────────────────────────────────────────────────────

TIMELINE_TEMPLATES = {
    "short": [  # < 150 min
        ("Welcome & Introduction", "Meet your guide, get oriented, and receive safety briefing", 15),
        ("Main Experience", "Dive into the core activity with expert guidance", 60),
        ("Exploration & Discovery", "Free time to explore and capture photos", 30),
        ("Wrap-up & Farewell", "Final Q&A, recommendations, and group photo", 15),
    ],
    "medium": [  # 150-300 min
        ("Welcome & Orientation", "Meet your guide at the meeting point and overview of the day", 20),
        ("First Stop", "Begin with the highlight attraction of the experience", 50),
        ("Second Stop", "Continue to the next key location with guided commentary", 45),
        ("Break & Refreshments", "Rest stop with local refreshments included", 30),
        ("Final Experience", "Conclude with the culminating activity or visit", 40),
        ("Farewell", "Return to starting point with final thoughts and tips", 15),
    ],
    "long": [  # > 300 min
        ("Meet & Greet", "Arrive at meeting point, introductions and day overview", 20),
        ("Journey to First Location", "Travel to the first destination with background context", 45),
        ("Morning Activity", "Main morning experience with hands-on participation", 90),
        ("Lunch Break", "Enjoy a traditional local meal at a carefully selected venue", 60),
        ("Afternoon Exploration", "Continue with afternoon activities and deeper immersion", 90),
        ("Cultural Highlight", "Special cultural experience unique to this tour", 45),
        ("Return Journey", "Head back to the starting point with time for questions", 30),
    ],
}

# ── Helper functions ───────────────────────────────────────────────────────────

# bcrypt hash for "vendor123"
VENDOR_PASSWORD_HASH = "$2b$12$lH7lGrwYzw59i.iWbDHTvuOI3LWRkddc6Vcnul./qr4PheYet67MS"


def get_timeline_template(duration_minutes):
    if duration_minutes <= 150:
        return TIMELINE_TEMPLATES["short"]
    elif duration_minutes <= 300:
        return TIMELINE_TEMPLATES["medium"]
    else:
        return TIMELINE_TEMPLATES["long"]


def make_slug_seed(slug, suffix):
    return f"{slug}-{suffix}"


def run():
    session = Session()

    try:
        # ── 0. Fix sequences (out of sync after backup restore) ────────────
        print("Fixing sequences...")
        seq_fixes = [
            ("categories", "id"),
            ("destinations", "id"),
            ("users", "id"),
            ("vendors", "id"),
            ("activities", "id"),
            ("activity_images", "id"),
            ("activity_highlights", "id"),
            ("activity_includes", "id"),
            ("activity_faqs", "id"),
            ("activity_timelines", "id"),
            ("activity_time_slots", "id"),
            ("activity_pricing_tiers", "id"),
            ("activity_add_ons", "id"),
            ("meeting_points", "id"),
        ]
        from sqlalchemy import text
        for table, col in seq_fixes:
            session.execute(text(
                f"SELECT setval(pg_get_serial_sequence('{table}', '{col}'), "
                f"COALESCE((SELECT MAX({col}) FROM {table}), 0) + 1, false)"
            ))
        session.commit()
        print("  Sequences fixed.")

        # ── 1. Add categories ──────────────────────────────────────────────
        print("Adding new categories...")
        cat_map = {}
        # Load existing categories
        for cat in session.query(Category).all():
            cat_map[cat.slug] = cat

        for name, slug, icon in NEW_CATEGORIES:
            if slug not in cat_map:
                cat = Category(name=name, slug=slug, icon=icon, order_index=len(cat_map))
                session.add(cat)
                session.flush()
                cat_map[slug] = cat
                print(f"  + Category: {name}")
            else:
                print(f"  = Category exists: {name}")

        # ── 2. Add destinations ────────────────────────────────────────────
        print("Adding new destinations...")
        dest_map = {}
        for dest in session.query(Destination).all():
            dest_map[dest.slug] = dest

        for name, slug, country, code, lat, lng, featured in NEW_DESTINATIONS:
            if slug not in dest_map:
                dest = Destination(
                    name=name, slug=slug, country=country, country_code=code,
                    image_url=f"https://picsum.photos/seed/{slug}-dest/800/600",
                    latitude=lat, longitude=lng, is_featured=featured,
                )
                session.add(dest)
                session.flush()
                dest_map[slug] = dest
                print(f"  + Destination: {name}")
            else:
                print(f"  = Destination exists: {name}")

        # ── 3. Add vendors ─────────────────────────────────────────────────
        print("Adding new vendors...")
        vendor_ids = [v.id for v in session.query(Vendor).all()]

        for company, email, desc in NEW_VENDORS:
            existing = session.query(User).filter_by(email=email).first()
            if existing:
                print(f"  = Vendor exists: {company}")
                if existing.vendor_profile:
                    vendor_ids.append(existing.vendor_profile.id)
                continue
            user = User(
                email=email,
                password_hash=VENDOR_PASSWORD_HASH,
                full_name=f"{company} Manager",
                role=UserRole.VENDOR,
                is_active=True,
                email_verified=True,
            )
            session.add(user)
            session.flush()
            vendor = Vendor(
                user_id=user.id,
                company_name=company,
                description=desc,
                is_verified=True,
            )
            session.add(vendor)
            session.flush()
            vendor_ids.append(vendor.id)
            print(f"  + Vendor: {company}")

        # ── 4. Add activities with all sub-entities ────────────────────────
        print("Adding new activities...")
        activity_count = 0

        for act_data in NEW_ACTIVITIES:
            # Check if slug already exists
            existing = session.query(Activity).filter_by(slug=act_data["slug"]).first()
            if existing:
                print(f"  = Activity exists: {act_data['title']}")
                continue

            price = Decimal(str(act_data["price"]))
            child_price = (price * Decimal("0.7")).quantize(Decimal("0.01"))

            # Pick a vendor (round-robin from all available)
            vid = vendor_ids[activity_count % len(vendor_ids)]

            # Randomize some flags
            has_discount = random.random() < 0.35
            discount_pct = random.choice([10, 15, 20, 25]) if has_discount else None
            orig_price = (price / (1 - Decimal(str(discount_pct)) / 100)).quantize(Decimal("0.01")) if has_discount else None
            orig_child = (child_price / (1 - Decimal(str(discount_pct)) / 100)).quantize(Decimal("0.01")) if has_discount else None

            activity = Activity(
                vendor_id=vid,
                title=act_data["title"],
                slug=act_data["slug"],
                description=act_data["desc"],
                short_description=act_data["short"],
                price_adult=price,
                price_child=child_price,
                price_currency="EUR",
                duration_minutes=act_data["duration"],
                max_group_size=act_data["group"],
                instant_confirmation=True,
                free_cancellation_hours=24,
                languages=act_data["langs"],
                is_bestseller=act_data["bestseller"],
                is_skip_the_line=act_data["skip_line"],
                is_active=True,
                has_multiple_tiers=True,
                discount_percentage=discount_pct,
                original_price_adult=orig_price,
                original_price_child=orig_child,
                is_likely_to_sell_out=act_data["bestseller"],
                has_mobile_ticket=True,
                has_best_price_guarantee=True,
                is_verified_activity=True,
                response_time_hours=24,
                is_wheelchair_accessible=random.random() < 0.4,
                is_stroller_accessible=random.random() < 0.3,
                allows_service_animals=True,
                has_infant_seats=False,
                weather_dependent=act_data["duration"] > 180,
                what_to_bring=act_data["what_to_bring"],
                has_covid_measures=True,
                covid_measures="Hand sanitizer provided, reduced group sizes",
                is_giftable=True,
                allows_reserve_now_pay_later=True,
                reserve_payment_deadline_hours=24,
                average_rating=Decimal(str(round(random.uniform(3.8, 4.9), 1))),
                total_reviews=random.randint(5, 120),
                total_bookings=random.randint(10, 300),
            )
            session.add(activity)
            session.flush()
            aid = activity.id
            slug = act_data["slug"]

            # ── Images (6 per activity) ────────────────────────────────────
            for i in range(6):
                session.add(ActivityImage(
                    activity_id=aid,
                    url=f"https://picsum.photos/seed/{make_slug_seed(slug, f'image-{i}')}/800/600",
                    alt_text=f"{act_data['title']} - Image {i+1}",
                    is_primary=(i == 0),
                    is_hero=(i == 0),
                    order_index=i,
                ))

            # ── Category links ─────────────────────────────────────────────
            for cat_slug in act_data["cats"]:
                if cat_slug in cat_map:
                    session.add(ActivityCategory(
                        activity_id=aid,
                        category_id=cat_map[cat_slug].id,
                    ))

            # ── Destination link ───────────────────────────────────────────
            dest_slug = act_data["dest"]
            if dest_slug in dest_map:
                session.add(ActivityDestination(
                    activity_id=aid,
                    destination_id=dest_map[dest_slug].id,
                ))

            # ── Highlights (6 per activity) ────────────────────────────────
            highlights = [
                f"Expert local guide with deep knowledge",
                f"Small group experience (max {act_data['group']} people)",
                f"Unique access to hidden or exclusive locations",
                f"All entrance fees and tastings included",
                f"Photo opportunities at iconic viewpoints",
                f"Free cancellation up to 24 hours before",
            ]
            for i, text in enumerate(highlights):
                session.add(ActivityHighlight(
                    activity_id=aid, text=text, order_index=i,
                ))

            # ── Includes (8 per activity: 6 included, 2 excluded) ─────────
            includes = [
                ("Professional English-speaking guide", True),
                ("All entrance fees and tickets", True),
                ("Tastings or refreshments as described", True),
                ("Small group size guarantee", True),
                ("Hotel pickup (selected areas)", True),
                ("Gratuities (optional)", False),
                ("Personal expenses and souvenirs", False),
                ("Travel insurance", False),
            ]
            for i, (item, is_inc) in enumerate(includes):
                session.add(ActivityInclude(
                    activity_id=aid, item=item, is_included=is_inc, order_index=i,
                ))

            # ── FAQs (3 per activity) ──────────────────────────────────────
            faqs = [
                ("What is the cancellation policy?",
                 "Free cancellation up to 24 hours before the start time for a full refund."),
                ("Is this activity suitable for children?",
                 f"Yes, children are welcome. Child pricing applies for ages 4-12. Under 4 is free."),
                ("What happens if it rains?",
                 "The activity runs in light rain. In case of severe weather, we offer a full reschedule or refund."),
            ]
            for i, (q, a) in enumerate(faqs):
                session.add(ActivityFAQ(
                    activity_id=aid, question=q, answer=a, order_index=i,
                ))

            # ── Timeline ───────────────────────────────────────────────────
            template = get_timeline_template(act_data["duration"])
            for i, (title, desc, dur) in enumerate(template):
                session.add(ActivityTimeline(
                    activity_id=aid,
                    step_number=i + 1,
                    title=title,
                    description=desc,
                    duration_minutes=dur,
                    image_url=f"https://picsum.photos/seed/{make_slug_seed(slug, f'timeline-{i+1}')}/600/400",
                    order_index=i,
                ))

            # ── Pricing tiers (3 per activity) ────────────────────────────
            tiers = [
                ("Standard", "Basic experience with all core activities",
                 price, child_price),
                ("Premium", "Enhanced experience with priority access and extras",
                 (price * Decimal("1.4")).quantize(Decimal("0.01")),
                 (child_price * Decimal("1.4")).quantize(Decimal("0.01"))),
                ("VIP", "Luxury experience with exclusive access and perks",
                 (price * Decimal("1.8")).quantize(Decimal("0.01")),
                 (child_price * Decimal("1.8")).quantize(Decimal("0.01"))),
            ]
            for i, (name, desc, pa, pc) in enumerate(tiers):
                session.add(ActivityPricingTier(
                    activity_id=aid,
                    tier_name=name, tier_description=desc,
                    price_adult=pa, price_child=pc,
                    order_index=i, is_active=True,
                ))

            # ── Add-ons (3 per activity) ───────────────────────────────────
            addons = [
                ("Professional Photography Package",
                 "Professional photos of your experience delivered digitally within 24 hours",
                 Decimal("25.00")),
                ("Private Upgrade",
                 "Upgrade to a private experience for your group only",
                 Decimal("40.00")),
                ("Extended Experience",
                 "Add extra time with additional stops or activities",
                 Decimal("20.00")),
            ]
            for i, (name, desc, addon_price) in enumerate(addons):
                session.add(ActivityAddOn(
                    activity_id=aid,
                    name=name, description=desc, price=addon_price,
                    is_optional=True, order_index=i,
                ))

            # ── Meeting point ──────────────────────────────────────────────
            dest_obj = dest_map.get(dest_slug)
            lat = dest_obj.latitude + random.uniform(-0.01, 0.01) if dest_obj else 0
            lng = dest_obj.longitude + random.uniform(-0.01, 0.01) if dest_obj else 0
            dest_name = dest_obj.name if dest_obj else act_data["dest"].title()

            session.add(MeetingPoint(
                activity_id=aid,
                address=f"Central Meeting Point, {dest_name}",
                instructions="Look for guide with company banner. Arrive 15 minutes early.",
                latitude=lat,
                longitude=lng,
                parking_info="Street parking available nearby",
                public_transport_info="Accessible by metro and bus",
                nearby_landmarks=f"Near main tourist area in {dest_name}",
            ))

            activity_count += 1
            print(f"  + Activity: {act_data['title']}")

        session.commit()
        print(f"\nDone! Added {activity_count} new activities.")
        print("Verifying totals...")

        total_cats = session.query(Category).count()
        total_dests = session.query(Destination).count()
        total_acts = session.query(Activity).count()
        total_vendors = session.query(Vendor).count()
        print(f"  Categories:   {total_cats}")
        print(f"  Destinations: {total_dests}")
        print(f"  Activities:   {total_acts}")
        print(f"  Vendors:      {total_vendors}")

    except Exception as e:
        session.rollback()
        print(f"ERROR: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    run()
