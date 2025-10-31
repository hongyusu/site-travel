"""Seed enhanced database with comprehensive demo data."""

import random
from datetime import datetime, timedelta
from decimal import Decimal
from slugify import slugify

from app.database import SessionLocal, engine, Base
from app.models import (
    User, Vendor, Category, Destination, Activity,
    ActivityImage, ActivityCategory, ActivityDestination,
    ActivityHighlight, ActivityInclude, MeetingPoint,
    ActivityTimeline, ActivityTimeSlot, ActivityPricingTier,
    ActivityAddOn, MeetingPointPhoto,
    Review, ReviewImage, ReviewCategory
)
from app.models.user import UserRole
from app.core.security import get_password_hash


def seed_enhanced_db():
    """Seed database with enhanced comprehensive demo data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already contains data. Skipping initialization.")
            return

        print("Creating enhanced demo data...")

        # ===== Create Base Users =====
        admin = User(
            email="admin@getyourguide.com",
            password_hash=get_password_hash("admin123"),
            full_name="Admin User",
            role=UserRole.ADMIN,
            email_verified=True
        )
        db.add(admin)

        customer = User(
            email="customer@example.com",
            password_hash=get_password_hash("customer123"),
            full_name="John Doe",
            role=UserRole.CUSTOMER,
            email_verified=True
        )
        db.add(customer)

        # Create additional customers for reviews
        customers = [customer]
        customer_names = [
            "Emily Johnson", "Michael Chen", "Sarah Williams", "David Martinez",
            "Jennifer Brown", "Robert Taylor", "Lisa Anderson", "James Wilson"
        ]
        for i, name in enumerate(customer_names, 2):
            user = User(
                email=f"customer{i}@example.com",
                password_hash=get_password_hash("customer123"),
                full_name=name,
                role=UserRole.CUSTOMER,
                email_verified=True
            )
            customers.append(user)
            db.add(user)

        # ===== Create Vendors =====
        vendor_users = []
        vendor_profiles = []

        vendor_data = [
            ("City Explorer Tours", "Premium city tours and experiences"),
            ("Local Flavors", "Authentic food and culinary experiences"),
            ("Adventure Seekers", "Outdoor and adventure activities"),
            ("Cultural Connections", "Museums, history, and cultural tours"),
            ("VIP Experiences", "Luxury and exclusive tours")
        ]

        for i, (company_name, description) in enumerate(vendor_data, 1):
            vendor_user = User(
                email=f"vendor{i}@example.com",
                password_hash=get_password_hash("vendor123"),
                full_name=f"{company_name} Manager",
                role=UserRole.VENDOR,
                email_verified=True
            )
            vendor_users.append(vendor_user)
            db.add(vendor_user)
            db.flush()

            vendor_profile = Vendor(
                user_id=vendor_user.id,
                company_name=company_name,
                description=description,
                is_verified=True,
                commission_rate=20.0
            )
            vendor_profiles.append(vendor_profile)
            db.add(vendor_profile)

        # ===== Create Categories =====
        categories = []
        category_data = [
            ("Tours & Sightseeing", "tours-sightseeing", "🏛️"),
            ("Museums & Attractions", "museums-attractions", "🎨"),
            ("Day Trips", "day-trips", "🚌"),
            ("Food & Drink", "food-drink", "🍽️"),
            ("Adventure & Nature", "adventure-nature", "🏔️"),
            ("Shows & Entertainment", "shows-entertainment", "🎭"),
            ("Transportation", "transportation", "🚗"),
            ("Water Sports", "water-sports", "🏄")
        ]

        for name, slug, icon in category_data:
            category = Category(name=name, slug=slug, icon=icon)
            categories.append(category)
            db.add(category)

        # ===== Create Destinations =====
        destinations = []
        destination_data = [
            ("Paris", "France", "FR", 48.8566, 2.3522),
            ("London", "United Kingdom", "GB", 51.5074, -0.1278),
            ("Rome", "Italy", "IT", 41.9028, 12.4964),
            ("Barcelona", "Spain", "ES", 41.3851, 2.1734),
            ("Amsterdam", "Netherlands", "NL", 52.3676, 4.9041),
            ("New York", "United States", "US", 40.7128, -74.0060),
            ("Tokyo", "Japan", "JP", 35.6762, 139.6503),
            ("Dubai", "United Arab Emirates", "AE", 25.2048, 55.2708),
            ("Prague", "Czech Republic", "CZ", 50.0755, 14.4378),
            ("Istanbul", "Turkey", "TR", 41.0082, 28.9784)
        ]

        for name, country, code, lat, lng in destination_data:
            destination = Destination(
                name=name,
                slug=slugify(name),
                country=country,
                country_code=code,
                latitude=lat,
                longitude=lng,
                is_featured=True,
                image_url=f"https://picsum.photos/seed/{slugify(name)}/800/600"
            )
            destinations.append(destination)
            db.add(destination)

        db.flush()

        # ===== Create Comprehensive Activities =====
        activities_data = [
            # ROME Activities
            {
                "title": "Skip-the-Line: Vatican Museums & Sistine Chapel Guided Tour",
                "vendor": 3,  # Cultural Connections
                "category": 1,  # Museums
                "destination": 2,  # Rome
                "short_description": "Skip the long lines and explore the Vatican Museums and Sistine Chapel with an expert guide",
                "description": "Discover the magnificent Vatican Museums and marvel at Michelangelo's Sistine Chapel ceiling on this skip-the-line guided tour. Your expert guide will lead you through the Gallery of Maps, Raphael's Rooms, and other highlights before reaching the breathtaking Sistine Chapel. Learn about the art, history, and significance of these masterpieces while avoiding the crowds.",
                "price_adult": Decimal("65.00"),
                "price_child": Decimal("55.00"),
                "original_price_adult": Decimal("75.00"),
                "discount_percentage": 13,
                "duration": 180,
                "max_group_size": 20,
                "languages": ["English", "Spanish", "Italian", "French"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "has_best_price_guarantee": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "is_stroller_accessible": False,
                "allows_service_animals": True,
                "has_infant_seats": False,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "All visitors must wear masks. Temperature checks at entrance. Enhanced cleaning protocols.",
                "is_giftable": True,
                "allows_reserve_now_pay_later": True,
                "what_to_bring": "Comfortable walking shoes, valid ID, modest clothing (no shorts, no bare shoulders)",
                "not_suitable_for": "People with mobility impairments, as there are many stairs",
                "has_multiple_tiers": True,
                "meeting_address": "Via Germanico, 16, 00192 Roma RM, Italy",
                "meeting_instructions": "Meet your guide in front of Caffe Vaticano. Look for the guide holding a yellow umbrella with 'Vatican Tours' logo.",
                "highlights": [
                    "Skip the ticket lines with priority access",
                    "Expert guide with in-depth knowledge of art history",
                    "Small group tour for a more personal experience",
                    "Marvel at Michelangelo's Sistine Chapel ceiling",
                    "Explore the Gallery of Maps and Raphael's Rooms"
                ],
                "includes": [
                    ("Skip-the-line entrance tickets", True),
                    ("Professional licensed guide", True),
                    ("Headsets for groups over 10 people", True),
                    ("Hotel pickup and drop-off", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Meeting Point", "Meet your guide at the designated meeting point near the Vatican Museums entrance. Your guide will provide an introduction and distribute skip-the-line tickets.", 15, None),
                    ("Vatican Museums Entry", "Enter the Vatican Museums through the priority access entrance, bypassing the regular ticket queues that can be hours long.", 10, None),
                    ("Gallery of Maps & Tapestries", "Walk through the stunning Gallery of Maps and Gallery of Tapestries while your guide explains the history and significance of these masterpieces.", 30, None),
                    ("Raphael's Rooms", "Explore the four Raphael Rooms, including the famous School of Athens fresco. Learn about Renaissance art and the rivalry between Raphael and Michelangelo.", 40, None),
                    ("Sistine Chapel", "Enter the Sistine Chapel and spend time admiring Michelangelo's iconic ceiling frescoes and The Last Judgment. Your guide will explain the stories depicted.", 50, None),
                    ("Tour Conclusion", "Exit through the museum and receive recommendations for nearby attractions and restaurants from your guide.", 15, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 20, Decimal("0.00")),
                    ("11:00", "Late Morning", 20, Decimal("0.00")),
                    ("14:00", "Afternoon", 20, Decimal("0.00")),
                    ("16:00", "Late Afternoon", 15, Decimal("5.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group tour with expert guide and skip-the-line access", Decimal("65.00"), Decimal("55.00"), 0),
                    ("Premium", "Smaller group (max 12 people) with extended tour including St. Peter's Basilica", Decimal("89.00"), Decimal("75.00"), 1),
                    ("VIP", "Private tour for your group only with art historian guide and exclusive after-hours access", Decimal("299.00"), Decimal("249.00"), 2)
                ],
                "add_ons": [
                    ("Audio guide in additional language", "Get an audio guide in Chinese, Japanese, German, or Portuguese", Decimal("8.00")),
                    ("St. Peter's Basilica add-on", "Extend your tour to include a guided visit to St. Peter's Basilica", Decimal("15.00")),
                    ("Professional photo service", "Professional photographer to capture your experience", Decimal("35.00")),
                    ("Vatican Gardens tour", "Add a guided tour of the beautiful Vatican Gardens", Decimal("25.00"))
                ]
            },
            # ROME - Colosseum
            {
                "title": "Colosseum Underground & Arena Floor Tour with Roman Forum",
                "vendor": 3,
                "category": 0,  # Tours
                "destination": 2,  # Rome
                "short_description": "Explore restricted areas of the Colosseum including the underground chambers and arena floor",
                "description": "Step onto the arena floor where gladiators once fought and descend into the underground chambers of the Colosseum on this exclusive tour. Your expert guide will bring ancient Rome to life as you explore these restricted areas, followed by a visit to the Roman Forum and Palatine Hill. This comprehensive tour offers unparalleled access to Rome's most iconic landmarks.",
                "price_adult": Decimal("89.00"),
                "price_child": Decimal("75.00"),
                "duration": 210,
                "max_group_size": 18,
                "languages": ["English", "Spanish", "Italian"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "has_best_price_guarantee": True,
                "is_verified_activity": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Reduced group sizes, mandatory masks, and temperature checks",
                "is_giftable": True,
                "what_to_bring": "Comfortable shoes, water bottle, sun protection",
                "not_suitable_for": "People with severe mobility issues (underground has stairs)",
                "has_multiple_tiers": True,
                "meeting_address": "Piazza del Colosseo, near the Colosseum Metro Station",
                "meeting_instructions": "Meet your guide at the newsstand near the Colosseum Metro exit. Look for the orange flag with 'Rome Tours' logo.",
                "highlights": [
                    "Exclusive access to Colosseum underground and arena floor",
                    "Walk where gladiators prepared for battle",
                    "Small group tour with expert archaeologist guide",
                    "Skip long entrance lines",
                    "Visit Roman Forum and Palatine Hill"
                ],
                "includes": [
                    ("Special access ticket to underground and arena floor", True),
                    ("Expert archaeologist guide", True),
                    ("Headsets for clear audio", True),
                    ("Roman Forum and Palatine Hill entrance", True),
                    ("Transportation", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Colosseum Exterior", "Meet your guide and receive an introduction to the Colosseum's history and architecture. Learn about the gladiatorial games and the engineering marvel of ancient Rome.", 20, None),
                    ("Arena Floor", "Step onto the arena floor where gladiators once fought. Your guide will explain the games, the crowd dynamics, and the social significance of the amphitheater.", 40, None),
                    ("Underground Chambers", "Descend into the hypogeum, the underground network where gladiators and animals waited before combat. See the elevator systems and trapdoors used for dramatic entrances.", 50, None),
                    ("Roman Forum", "Walk through the ancient Roman Forum, the center of political and social life in ancient Rome. See the ruins of temples, basilicas, and government buildings.", 45, None),
                    ("Palatine Hill", "Climb Palatine Hill, where Rome's emperors lived in luxury. Enjoy panoramic views of the city and explore the imperial palace ruins.", 35, None)
                ],
                "time_slots": [
                    ("08:30", "Early Morning", 18, Decimal("0.00")),
                    ("10:30", "Morning", 18, Decimal("0.00")),
                    ("13:30", "Afternoon", 18, Decimal("0.00")),
                    ("15:30", "Late Afternoon", 15, Decimal("5.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group tour with underground and arena floor access", Decimal("89.00"), Decimal("75.00"), 0),
                    ("Premium", "Smaller group (max 10) with extended tour and additional archaeological sites", Decimal("125.00"), Decimal("105.00"), 1)
                ],
                "add_ons": [
                    ("Video guide device", "Personal video guide with 3D reconstructions of ancient Rome", Decimal("12.00")),
                    ("Gladiator costume experience", "Dress as a gladiator for photos on the arena floor", Decimal("20.00")),
                    ("Ancient Rome lunch", "Traditional Roman lunch at nearby trattoria", Decimal("28.00"))
                ]
            },
            # PARIS - Eiffel Tower
            {
                "title": "Eiffel Tower: Summit Access with Skip-the-Line & Host",
                "vendor": 0,  # City Explorer Tours
                "category": 0,  # Tours
                "destination": 0,  # Paris
                "short_description": "Skip the lines and ascend to the summit of the Eiffel Tower with a knowledgeable host",
                "description": "Experience the magic of the Eiffel Tower with priority access tickets that let you bypass the long queues. A friendly host will accompany you, sharing fascinating stories about the tower's construction and Parisian history. Take the elevator to the second floor and then to the summit for breathtaking 360-degree views of Paris.",
                "price_adult": Decimal("79.00"),
                "price_child": Decimal("65.00"),
                "duration": 120,
                "max_group_size": 25,
                "languages": ["English", "French", "Spanish", "German"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "has_best_price_guarantee": True,
                "is_verified_activity": True,
                "weather_dependent": True,
                "has_covid_measures": True,
                "covid_measures": "Limited capacity, mask requirements indoors, hand sanitizer stations",
                "is_giftable": True,
                "allows_reserve_now_pay_later": True,
                "what_to_bring": "Camera, warm clothing (it can be windy at the top)",
                "not_suitable_for": "People with severe fear of heights",
                "has_multiple_tiers": True,
                "meeting_address": "Avenue Gustave Eiffel, 75007 Paris, France",
                "meeting_instructions": "Meet your host at the South Security Entrance (Pilier Sud) of the Eiffel Tower. Look for the red umbrella with 'Paris Tours' logo.",
                "highlights": [
                    "Skip-the-line priority access tickets",
                    "Summit access with panoramic views of Paris",
                    "Knowledgeable host sharing Eiffel Tower stories",
                    "See iconic landmarks from above: Arc de Triomphe, Louvre, Notre-Dame",
                    "Perfect photo opportunities"
                ],
                "includes": [
                    ("Skip-the-line summit access ticket", True),
                    ("Host to accompany you", True),
                    ("Elevator to summit", True),
                    ("Free time at the top", True),
                    ("Food and drinks", False),
                    ("Hotel pickup", False)
                ],
                "timelines": [
                    ("Security & Entry", "Meet your host at the South entrance. After a brief introduction, proceed through security and skip the regular ticket queues with your priority access.", 15, None),
                    ("First Observation Deck", "Take the elevator to the first observation deck. Your host will point out major Parisian landmarks and share interesting facts about the tower's construction.", 20, None),
                    ("Second Floor", "Ascend to the second floor for even more spectacular views. Learn about Gustave Eiffel and the tower's role in Parisian history.", 25, None),
                    ("Summit", "Continue to the summit, the highest accessible point of the Eiffel Tower. Enjoy 360-degree views of Paris and identify famous monuments. Your host will answer any questions.", 40, None),
                    ("Free Time & Descent", "Enjoy free time to take photos and soak in the views before descending at your own pace.", 20, None)
                ],
                "time_slots": [
                    ("09:30", "Morning", 25, Decimal("0.00")),
                    ("11:30", "Late Morning", 25, Decimal("0.00")),
                    ("14:00", "Afternoon", 25, Decimal("0.00")),
                    ("16:30", "Late Afternoon", 20, Decimal("0.00")),
                    ("19:00", "Evening", 20, Decimal("10.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Skip-the-line summit access with host", Decimal("79.00"), Decimal("65.00"), 0),
                    ("Premium", "Smaller group with extended commentary and champagne toast at summit", Decimal("120.00"), Decimal("100.00"), 1)
                ],
                "add_ons": [
                    ("Seine River cruise", "Add a 1-hour Seine River cruise after your tower visit", Decimal("18.00")),
                    ("Photo package", "Professional photos at the tower", Decimal("25.00")),
                    ("Macarons box", "Box of authentic French macarons from Ladurée", Decimal("15.00"))
                ]
            },
            # PARIS - Louvre
            {
                "title": "Louvre Museum: Skip-the-Line Guided Tour with Mona Lisa",
                "vendor": 3,
                "category": 1,  # Museums
                "destination": 0,  # Paris
                "short_description": "Discover the Louvre's masterpieces including the Mona Lisa with skip-the-line access",
                "description": "Explore the world's largest art museum with an expert guide who will navigate you through the vast Louvre collection. See iconic works including the Mona Lisa, Venus de Milo, and Winged Victory of Samothrace. Your guide will share captivating stories behind the art and help you make the most of your visit to this extraordinary museum.",
                "price_adult": Decimal("69.00"),
                "price_child": Decimal("59.00"),
                "duration": 180,
                "max_group_size": 20,
                "languages": ["English", "French", "Spanish", "Italian"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "is_stroller_accessible": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Timed entry tickets, reduced capacity, mandatory masks",
                "is_giftable": True,
                "what_to_bring": "Comfortable walking shoes, water bottle",
                "has_multiple_tiers": True,
                "meeting_address": "Place du Carrousel, 75001 Paris, France",
                "meeting_instructions": "Meet your guide at the Arc de Triomphe du Carrousel (between the Louvre and Tuileries Garden). Look for the guide with a blue flag.",
                "highlights": [
                    "Skip the long entrance queues",
                    "See the Mona Lisa, Venus de Milo, and other masterpieces",
                    "Expert art historian guide",
                    "Small group for personalized experience",
                    "Explore multiple wings of the museum"
                ],
                "includes": [
                    ("Skip-the-line entrance ticket", True),
                    ("Expert art historian guide", True),
                    ("Headsets for groups over 6", True),
                    ("Hotel pickup", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Museum Entry", "Meet your guide and enter the Louvre through the priority entrance, avoiding the long queues at the pyramid.", 10, None),
                    ("Venus de Milo & Ancient Greek Art", "Begin in the Greek antiquities section. Admire the Venus de Milo and learn about ancient Greek sculpture.", 30, None),
                    ("Mona Lisa", "Navigate to the Denon Wing to see Leonardo da Vinci's Mona Lisa. Your guide will share the painting's fascinating history and help you get a good view.", 35, None),
                    ("Italian Renaissance", "Explore more Italian masterpieces including works by Caravaggio, Raphael, and Titian.", 40, None),
                    ("French Paintings & Winged Victory", "Visit the French painting galleries and see the magnificent Winged Victory of Samothrace sculpture.", 35, None),
                    ("Tour Conclusion", "End the tour with free time recommendations and tips for exploring more of the Louvre on your own.", 10, None)
                ],
                "time_slots": [
                    ("09:00", "Early Morning", 20, Decimal("0.00")),
                    ("11:00", "Late Morning", 20, Decimal("0.00")),
                    ("14:00", "Afternoon", 20, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group guided tour with skip-the-line access", Decimal("69.00"), Decimal("59.00"), 0),
                    ("Premium", "Semi-private tour (max 8 people) with extended time and additional wings", Decimal("119.00"), Decimal("99.00"), 1),
                    ("VIP", "Private tour with art curator and access to museum's special collections", Decimal("450.00"), Decimal("400.00"), 2)
                ],
                "add_ons": [
                    ("Audio guide", "Multimedia audio guide for self-exploration after the tour", Decimal("6.00")),
                    ("Orsay Museum combo ticket", "Add skip-the-line ticket to Musée d'Orsay", Decimal("18.00")),
                    ("Louvre guidebook", "Comprehensive illustrated guidebook in your language", Decimal("15.00"))
                ]
            },
            # BARCELONA - Sagrada Familia
            {
                "title": "Sagrada Familia: Fast-Track Guided Tour with Tower Access",
                "vendor": 0,
                "category": 1,  # Museums
                "destination": 3,  # Barcelona
                "short_description": "Skip the lines and explore Gaudí's masterpiece with expert guide and tower access",
                "description": "Discover Antoni Gaudí's unfinished masterpiece with fast-track access and an expert guide. Marvel at the stunning stained glass windows, intricate facades, and unique architecture of this UNESCO World Heritage site. Climb one of the towers for spectacular views of Barcelona and learn about Gaudí's vision and the ongoing construction that continues to this day.",
                "price_adult": Decimal("55.00"),
                "price_child": Decimal("45.00"),
                "duration": 90,
                "max_group_size": 20,
                "languages": ["English", "Spanish", "Catalan", "French"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "has_best_price_guarantee": True,
                "is_verified_activity": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Mandatory timed entry, reduced capacity, mask requirements",
                "is_giftable": True,
                "what_to_bring": "Modest clothing (shoulders and knees covered), comfortable shoes",
                "not_suitable_for": "People with severe claustrophobia (tower stairs are narrow)",
                "has_multiple_tiers": False,
                "meeting_address": "Carrer de Mallorca, 401, 08013 Barcelona, Spain",
                "meeting_instructions": "Meet your guide at the Nativity Facade entrance. Look for the guide holding a green flag with 'Barcelona Tours' logo.",
                "highlights": [
                    "Fast-track entrance to skip the queues",
                    "Expert guide explains Gaudí's vision and symbolism",
                    "Tower access for panoramic city views",
                    "Marvel at stunning stained glass windows",
                    "Small group tour for better experience"
                ],
                "includes": [
                    ("Fast-track entrance ticket with tower access", True),
                    ("Expert guide", True),
                    ("Audio headsets", True),
                    ("Elevator to tower (one-way)", True),
                    ("Transportation", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Nativity Facade", "Meet your guide and admire the Nativity Facade. Learn about the symbolic elements and Gaudí's use of nature in his designs.", 20, None),
                    ("Interior & Stained Glass", "Enter the basilica and be amazed by the forest-like columns and breathtaking stained glass windows. Your guide explains the architectural innovations.", 30, None),
                    ("Passion Facade", "Explore the Passion Facade with its stark, angular sculptures depicting Christ's crucifixion.", 15, None),
                    ("Tower Ascent", "Take the elevator up one of the towers for spectacular views of Barcelona. Descend via spiral stairs.", 25, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 20, Decimal("0.00")),
                    ("10:30", "Late Morning", 20, Decimal("0.00")),
                    ("12:00", "Midday", 20, Decimal("0.00")),
                    ("14:30", "Afternoon", 20, Decimal("0.00")),
                    ("16:00", "Late Afternoon", 20, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Guided tour with tower access", Decimal("55.00"), Decimal("45.00"), 0)
                ],
                "add_ons": [
                    ("Park Güell combo ticket", "Add skip-the-line entry to Park Güell", Decimal("15.00")),
                    ("Casa Batlló combo", "Add fast-track ticket to Casa Batlló", Decimal("30.00")),
                    ("Audio guide in extra language", "Additional language audio guide", Decimal("5.00")),
                    ("Gaudí photo book", "Beautiful photo book of Gaudí's works in Barcelona", Decimal("20.00"))
                ]
            },
            # BARCELONA - Park Güell
            {
                "title": "Park Güell: Skip-the-Line Guided Tour",
                "vendor": 0,
                "category": 0,  # Tours
                "destination": 3,  # Barcelona
                "short_description": "Explore Gaudí's whimsical park with priority access and expert guide",
                "description": "Skip the line and discover the enchanting Park Güell, one of Antoni Gaudí's most colorful and imaginative creations. Your guide will lead you through the monumental zone, explaining the park's history, symbolism, and Gaudí's unique architectural style. See the famous mosaic dragon, the serpentine bench, and enjoy panoramic views of Barcelona from this UNESCO World Heritage site.",
                "price_adult": Decimal("32.00"),
                "price_child": Decimal("25.00"),
                "duration": 90,
                "max_group_size": 25,
                "languages": ["English", "Spanish", "Catalan"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": False,
                "weather_dependent": True,
                "has_covid_measures": True,
                "covid_measures": "Timed entry slots, outdoor activity with natural distancing",
                "is_giftable": True,
                "what_to_bring": "Comfortable walking shoes, sun protection, water",
                "not_suitable_for": "People with mobility issues (park has many stairs and slopes)",
                "has_multiple_tiers": False,
                "meeting_address": "Carrer d'Olot, s/n, 08024 Barcelona, Spain",
                "meeting_instructions": "Meet your guide at the main entrance of Park Güell on Carrer d'Olot. Look for the yellow flag.",
                "highlights": [
                    "Skip-the-line entrance to monumental zone",
                    "See Gaudí's famous mosaic dragon fountain",
                    "Admire the colorful serpentine bench",
                    "Panoramic views of Barcelona",
                    "Learn about Gaudí's architectural vision"
                ],
                "includes": [
                    ("Skip-the-line entrance ticket", True),
                    ("Expert guide", True),
                    ("Transportation", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Park Entrance & Dragon Stairway", "Enter the park and descend the famous dragon stairway. See the colorful mosaic dragon, one of Barcelona's most photographed symbols.", 20, None),
                    ("Hypostyle Room", "Explore the Hypostyle Room with its 86 stone columns. Your guide explains how Gaudí designed this space as a covered market.", 20, None),
                    ("Serpentine Bench & Terrace", "Visit the iconic serpentine bench covered in colorful broken tile mosaics. Enjoy panoramic views of Barcelona from the main terrace.", 30, None),
                    ("Park Exploration", "Walk through the park's gardens and discover hidden architectural details and natural beauty.", 20, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 25, Decimal("0.00")),
                    ("11:00", "Late Morning", 25, Decimal("0.00")),
                    ("13:00", "Afternoon", 25, Decimal("0.00")),
                    ("15:00", "Late Afternoon", 25, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Guided tour with skip-the-line access", Decimal("32.00"), Decimal("25.00"), 0)
                ],
                "add_ons": [
                    ("Casa Museu Gaudí", "Add entry to Gaudí's former residence in the park", Decimal("8.00")),
                    ("Barcelona photo book", "Souvenir photo book of Barcelona's landmarks", Decimal("18.00"))
                ]
            },
            # BARCELONA - Food Tour
            {
                "title": "Barcelona Tapas & Wine Tasting Walking Tour",
                "vendor": 1,  # Local Flavors
                "category": 3,  # Food & Drink
                "destination": 3,  # Barcelona
                "short_description": "Taste authentic tapas and wines while exploring Barcelona's historic neighborhoods",
                "description": "Embark on a culinary journey through Barcelona's historic Gothic Quarter and Born neighborhood. This food tour combines delicious tapas, local wines, and cultural insights. Visit hand-picked local bars and restaurants, taste traditional Catalan dishes, and learn about Barcelona's food culture from your foodie guide. Includes 8-10 tastings at 4-5 different venues.",
                "price_adult": Decimal("85.00"),
                "price_child": Decimal("65.00"),
                "duration": 210,
                "max_group_size": 12,
                "languages": ["English", "Spanish"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Small groups, outdoor seating when possible, partner venues follow health protocols",
                "is_giftable": True,
                "what_to_bring": "Appetite, comfortable walking shoes",
                "not_suitable_for": "People with severe food allergies (multiple venues make it difficult to accommodate)",
                "has_multiple_tiers": True,
                "meeting_address": "Plaça de Sant Jaume, Barcelona, Spain",
                "meeting_instructions": "Meet your guide in front of the Barcelona City Hall on Plaça de Sant Jaume. Look for the guide with a red apron.",
                "highlights": [
                    "8-10 food and drink tastings at local venues",
                    "Small group for intimate experience",
                    "Local foodie guide with insider knowledge",
                    "Explore Gothic Quarter and Born neighborhoods",
                    "Learn about Catalan food culture and history"
                ],
                "includes": [
                    ("8-10 food tastings including tapas, cheese, and charcuterie", True),
                    ("3-4 drinks (wine, cava, or vermouth)", True),
                    ("Expert local food guide", True),
                    ("All entrance fees to venues", True),
                    ("Additional drinks", False),
                    ("Transportation", False)
                ],
                "timelines": [
                    ("Gothic Quarter Introduction", "Meet your guide and begin your walking tour through the narrow streets of the Gothic Quarter. Learn about Barcelona's history and food culture.", 20, None),
                    ("First Tasting Stop", "Visit a traditional bodega and taste authentic Spanish jamón ibérico, manchego cheese, and vermouth. Your guide explains the origins and production methods.", 35, None),
                    ("Born Neighborhood", "Walk to the trendy Born neighborhood, stopping at a local tapas bar for patatas bravas, pan con tomate, and other classic tapas paired with Spanish wine.", 40, None),
                    ("Third Venue", "Continue to a seafood-focused bar for fresh anchoas, fried calamari, and Catalan-style bombes. Enjoy local cava.", 40, None),
                    ("Final Stop & Dessert", "End the tour at a traditional pastry shop for churros con chocolate or crema catalana, the Catalan version of crème brûlée.", 35, None)
                ],
                "time_slots": [
                    ("11:00", "Late Morning", 12, Decimal("0.00")),
                    ("18:00", "Evening", 12, Decimal("5.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group tapas and wine tour", Decimal("85.00"), Decimal("65.00"), 0),
                    ("Premium", "Private tour for your group with premium wine pairings", Decimal("160.00"), Decimal("130.00"), 1)
                ],
                "add_ons": [
                    ("Extra wine pairing", "Add premium wine pairing at each venue", Decimal("20.00")),
                    ("Cooking class", "Add a 2-hour paella cooking class after the tour", Decimal("45.00")),
                    ("Market tour add-on", "Start with a guided tour of La Boqueria market", Decimal("25.00"))
                ]
            },
            # LONDON - Tower of London
            {
                "title": "Tower of London: Crown Jewels & Yeoman Warder Tour",
                "vendor": 3,
                "category": 1,  # Museums
                "destination": 1,  # London
                "short_description": "Explore the historic Tower of London with a Yeoman Warder guide and see the Crown Jewels",
                "description": "Discover over 1,000 years of history at the Tower of London with an expert Yeoman Warder (Beefeater) guide. See the magnificent Crown Jewels, explore the medieval fortress, and hear tales of royal intrigue, execution, and imprisonment. This UNESCO World Heritage site offers a captivating glimpse into British history.",
                "price_adult": Decimal("48.00"),
                "price_child": Decimal("38.00"),
                "duration": 150,
                "max_group_size": 20,
                "languages": ["English"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Timed entry, enhanced cleaning, one-way routes in buildings",
                "is_giftable": True,
                "what_to_bring": "Camera, weather-appropriate clothing",
                "has_multiple_tiers": False,
                "meeting_address": "Tower Hill, London EC3N 4AB, United Kingdom",
                "meeting_instructions": "Meet your guide at the main entrance to the Tower of London. Look for the guide in Beefeater uniform.",
                "highlights": [
                    "Expert Yeoman Warder (Beefeater) guide",
                    "See the Crown Jewels including the Imperial State Crown",
                    "Explore the White Tower and Royal Armouries",
                    "Hear stories of famous prisoners like Anne Boleyn",
                    "See the famous Tower ravens"
                ],
                "includes": [
                    ("Tower of London entrance ticket", True),
                    ("Yeoman Warder guided tour", True),
                    ("Crown Jewels access", True),
                    ("White Tower access", True),
                    ("Transportation", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Tower Introduction", "Meet your Yeoman Warder guide who will introduce you to the Tower's 1,000-year history and share entertaining stories.", 15, None),
                    ("Guided Tour", "Follow your Beefeater guide through the fortress. See Traitors' Gate, Tower Green (execution site), and learn about famous prisoners.", 45, None),
                    ("Crown Jewels", "After the guided portion, visit the Crown Jewels exhibition to see the Imperial State Crown, coronation regalia, and royal diamonds.", 40, None),
                    ("White Tower & Armouries", "Explore the White Tower, the oldest part of the fortress, housing the Royal Armouries collection.", 30, None),
                    ("Ravens & Free Exploration", "Visit the Tower ravens and enjoy free time to explore battlements and other areas.", 20, None)
                ],
                "time_slots": [
                    ("09:30", "Morning", 20, Decimal("0.00")),
                    ("11:00", "Late Morning", 20, Decimal("0.00")),
                    ("13:00", "Afternoon", 20, Decimal("0.00")),
                    ("14:30", "Late Afternoon", 20, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Tower entry with Yeoman Warder tour", Decimal("48.00"), Decimal("38.00"), 0)
                ],
                "add_ons": [
                    ("Audio guide", "Multimedia audio guide with additional stories", Decimal("5.00")),
                    ("Thames River cruise", "Add a 30-minute Thames River cruise", Decimal("15.00")),
                    ("Medieval banquet", "Medieval-style dinner at a nearby historic venue", Decimal("55.00"))
                ]
            },
            # LONDON - Warner Bros Studio
            {
                "title": "Warner Bros. Studio Tour London: The Making of Harry Potter",
                "vendor": 4,  # VIP Experiences
                "category": 5,  # Shows & Entertainment
                "destination": 1,  # London
                "short_description": "Step into the magical world of Harry Potter at the official studio tour",
                "description": "Experience the magic behind the Harry Potter films at Warner Bros. Studio Tour London. Walk through authentic sets including the Great Hall, Diagon Alley, and Platform 9 3/4. See original costumes, props, and learn about the special effects and artistry that brought J.K. Rowling's wizarding world to life. Includes round-trip transportation from central London.",
                "price_adult": Decimal("110.00"),
                "price_child": Decimal("95.00"),
                "duration": 420,
                "max_group_size": 30,
                "languages": ["English"],
                "is_bestseller": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "has_best_price_guarantee": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "is_stroller_accessible": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Timed tickets, enhanced cleaning, hand sanitizer stations throughout",
                "is_giftable": True,
                "allows_reserve_now_pay_later": True,
                "what_to_bring": "Camera, Harry Potter enthusiasm",
                "has_multiple_tiers": True,
                "meeting_address": "Victoria Coach Station, 164 Buckingham Palace Rd, London SW1W 9TP",
                "meeting_instructions": "Meet at Victoria Coach Station bay 8. Look for the coach with 'Harry Potter Studio Tour' sign.",
                "highlights": [
                    "Round-trip luxury coach from central London",
                    "Explore authentic film sets and props",
                    "Walk through the Great Hall, Diagon Alley, and Forbidden Forest",
                    "See Hogwarts castle model",
                    "Ride a broomstick with green-screen experience",
                    "Taste Butterbeer"
                ],
                "includes": [
                    ("Round-trip luxury coach transportation", True),
                    ("Warner Bros. Studio Tour ticket", True),
                    ("Self-guided tour with digital guide", True),
                    ("Butterbeer sample", True),
                    ("Food and additional drinks", False),
                    ("Souvenir photos", False)
                ],
                "timelines": [
                    ("Coach Departure", "Board the luxury coach at Victoria Station for the scenic drive to the studio in Leavesden.", 60, None),
                    ("Studio Entrance & Introduction", "Arrive at the studio and enter through the iconic entrance. Watch a short film introduction before the Great Hall doors open.", 20, None),
                    ("Sets & Props Tour", "Explore at your own pace: Great Hall, Dumbledore's office, Gryffindor common room, potions classroom, and Hagrid's hut. See thousands of authentic props and costumes.", 120, None),
                    ("Outdoor Area & Butterbeer", "Visit the outdoor area with the Knight Bus, Privet Drive, and Hogwarts Bridge. Try Butterbeer at the café.", 40, None),
                    ("Diagon Alley & Hogwarts Model", "Walk through Diagon Alley's shops and end with the spectacular Hogwarts castle model.", 60, None),
                    ("Return Journey", "Board the coach for the return journey to central London.", 60, None)
                ],
                "time_slots": [
                    ("08:00", "Early Morning Departure", 30, Decimal("0.00")),
                    ("11:00", "Late Morning Departure", 30, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Coach transport and studio entry with digital guide", Decimal("110.00"), Decimal("95.00"), 0),
                    ("Premium", "Includes souvenir guidebook, exclusive photo ops, and reserved Great Hall seating", Decimal("145.00"), Decimal("125.00"), 1),
                    ("VIP", "Private transport, priority entry, personal guide, and premium gift package", Decimal("295.00"), Decimal("255.00"), 2)
                ],
                "add_ons": [
                    ("Souvenir guidebook", "Official guidebook with behind-the-scenes content", Decimal("12.00")),
                    ("Green screen photo package", "Professional photos of your broomstick flight experience", Decimal("18.00")),
                    ("Wand purchase voucher", "£10 voucher toward wand purchase in gift shop", Decimal("10.00")),
                    ("Lunch package", "Pre-ordered lunch at the studio café", Decimal("15.00"))
                ]
            },
            # AMSTERDAM - Canal Cruise
            {
                "title": "Amsterdam: Evening Canal Cruise with Wine & Cheese",
                "vendor": 4,
                "category": 0,  # Tours
                "destination": 4,  # Amsterdam
                "short_description": "Romantic evening canal cruise through Amsterdam with Dutch wine and cheese",
                "description": "Experience Amsterdam's iconic canals at sunset on this romantic evening cruise. Glide past historic merchant houses, charming bridges, and houseboats while enjoying Dutch wine and artisanal cheese. Your skipper will share fascinating stories about Amsterdam's Golden Age and point out notable landmarks. Perfect for couples and photography enthusiasts.",
                "price_adult": Decimal("42.00"),
                "price_child": Decimal("32.00"),
                "duration": 90,
                "max_group_size": 18,
                "languages": ["English", "Dutch", "German"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": True,
                "has_covid_measures": True,
                "covid_measures": "Small groups, open-air boat with good ventilation",
                "is_giftable": True,
                "what_to_bring": "Camera, warm clothing (can be cool on the water)",
                "has_multiple_tiers": True,
                "meeting_address": "Prins Hendrikkade 33A, 1012 TM Amsterdam, Netherlands",
                "meeting_instructions": "Meet at the dock near Amsterdam Central Station. Look for the classic canal boat with 'Amsterdam Cruises' sign.",
                "highlights": [
                    "Romantic evening cruise through UNESCO canal ring",
                    "Dutch wine and artisanal cheese included",
                    "See illuminated bridges and historic architecture",
                    "Small boat for intimate atmosphere",
                    "Live commentary from local skipper"
                ],
                "includes": [
                    ("90-minute canal cruise", True),
                    ("Dutch wine (2 glasses) or soft drinks", True),
                    ("Selection of Dutch cheeses and crackers", True),
                    ("Live commentary", True),
                    ("Additional drinks", False),
                    ("Hotel pickup", False)
                ],
                "timelines": [
                    ("Boarding & Welcome", "Board the classic canal boat and receive a welcome drink. Get settled and meet your skipper.", 10, None),
                    ("UNESCO Canal Ring", "Cruise through the famous canal ring, a UNESCO World Heritage site. See the Anne Frank House, Westerkerk, and iconic merchant houses.", 40, None),
                    ("Wine & Cheese Service", "Enjoy Dutch wine and artisanal cheese while cruising past the Seven Bridges and Amstel River.", 25, None),
                    ("Evening Lights", "As evening falls, see the bridges light up and houseboats glow. Perfect photo opportunities.", 15, None)
                ],
                "time_slots": [
                    ("18:30", "Early Evening", 18, Decimal("0.00")),
                    ("20:00", "Evening", 18, Decimal("5.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Evening cruise with wine and cheese", Decimal("42.00"), Decimal("32.00"), 0),
                    ("Premium", "Smaller group (max 10) with premium wines and extended cheese selection", Decimal("65.00"), Decimal("50.00"), 1),
                    ("VIP", "Private boat for your group with champagne and luxury catering", Decimal("350.00"), Decimal("300.00"), 2)
                ],
                "add_ons": [
                    ("Extra wine", "Additional glass of Dutch wine", Decimal("6.00")),
                    ("Flower bouquet", "Dutch tulip bouquet (seasonal)", Decimal("15.00")),
                    ("Photo package", "Professional photos during the cruise", Decimal("20.00"))
                ]
            },
            # AMSTERDAM - Bike Tour
            {
                "title": "Amsterdam: Guided Bike Tour with Local Guide",
                "vendor": 2,  # Adventure Seekers
                "category": 0,  # Tours
                "destination": 4,  # Amsterdam
                "short_description": "Explore Amsterdam like a local on a bicycle tour through the city and countryside",
                "description": "Discover Amsterdam the authentic way - by bike! Join a small-group cycling tour led by a local guide who will show you hidden gems beyond the tourist areas. Pedal through charming neighborhoods, along peaceful canals, and into the countryside to see windmills and traditional Dutch landscapes. Includes bike rental and rain gear.",
                "price_adult": Decimal("38.00"),
                "price_child": Decimal("28.00"),
                "duration": 180,
                "max_group_size": 15,
                "languages": ["English", "Dutch"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": True,
                "has_covid_measures": True,
                "covid_measures": "Bikes sanitized between uses, outdoor activity with natural distancing",
                "is_giftable": True,
                "what_to_bring": "Comfortable clothes, sunscreen",
                "not_suitable_for": "People who cannot ride a bicycle, children under 8",
                "has_multiple_tiers": False,
                "meeting_address": "Weteringschans 24, 1017 SG Amsterdam, Netherlands",
                "meeting_instructions": "Meet at the bike rental shop near Rijksmuseum. Look for the red awning with 'Amsterdam Bike Tours' sign.",
                "highlights": [
                    "Bike through Amsterdam like a local",
                    "See hidden neighborhoods and local favorites",
                    "Ride to Dutch countryside and windmills",
                    "Small group for personalized experience",
                    "Expert local guide"
                ],
                "includes": [
                    ("Bike rental and helmet", True),
                    ("Rain gear if needed", True),
                    ("Local guide", True),
                    ("Snack and water break", True),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Bike Fitting & Safety", "Get fitted with your bike, receive safety instructions and route overview from your guide.", 15, None),
                    ("Jordaan & Canals", "Cycle through the charming Jordaan neighborhood and along scenic canals. Stop for photos at picturesque bridges.", 45, None),
                    ("Vondelpark", "Ride through Amsterdam's largest park, popular with locals for picnics and recreation.", 30, None),
                    ("Countryside & Windmills", "Head out of the city center to see authentic windmills and rural Dutch landscapes. Snack break at a local spot.", 60, None),
                    ("Return to City", "Cycle back through different neighborhoods, seeing hidden courtyards and local hangouts.", 30, None)
                ],
                "time_slots": [
                    ("09:30", "Morning", 15, Decimal("0.00")),
                    ("13:30", "Afternoon", 15, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group bike tour with local guide", Decimal("38.00"), Decimal("28.00"), 0)
                ],
                "add_ons": [
                    ("E-bike upgrade", "Upgrade to an electric bike for easier riding", Decimal("10.00")),
                    ("Lunch stop", "Add a traditional Dutch lunch stop at a local café", Decimal("15.00")),
                    ("Photo package", "Professional photos during the tour", Decimal("18.00"))
                ]
            },
            # AMSTERDAM - Anne Frank House
            {
                "title": "Anne Frank House: Timed Entry Ticket",
                "vendor": 3,
                "category": 1,  # Museums
                "destination": 4,  # Amsterdam
                "short_description": "Visit the Anne Frank House with timed entry ticket to avoid queues",
                "description": "Visit the Anne Frank House, one of Amsterdam's most important historical sites. This timed entry ticket allows you to skip the often long queues and explore the Secret Annex where Anne Frank hid during World War II. Walk through the rooms described in her famous diary and learn about her life, the Holocaust, and the importance of tolerance. This is a self-guided visit using multimedia guides.",
                "price_adult": Decimal("16.00"),
                "price_child": Decimal("7.00"),
                "duration": 90,
                "max_group_size": 50,
                "languages": ["English", "Dutch", "German", "French", "Spanish"],
                "is_bestseller": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": False,
                "is_stroller_accessible": False,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Mandatory timed entry to manage capacity, enhanced ventilation and cleaning",
                "is_giftable": True,
                "what_to_bring": "Valid ID, respectful attitude",
                "not_suitable_for": "People with mobility issues (many steep stairs, no elevator)",
                "has_multiple_tiers": False,
                "meeting_address": "Westermarkt 20, 1016 GV Amsterdam, Netherlands",
                "meeting_instructions": "Present your timed entry ticket at the entrance of the Anne Frank House at your designated time slot.",
                "highlights": [
                    "Visit the authentic Secret Annex",
                    "See where Anne Frank wrote her famous diary",
                    "Timed entry to skip long queues",
                    "Multimedia guide in multiple languages",
                    "Learn about World War II and the Holocaust"
                ],
                "includes": [
                    ("Timed entry ticket", True),
                    ("Multimedia guide", True),
                    ("Access to all exhibitions", True),
                    ("Guided tour", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Introduction Exhibition", "Begin with the introductory exhibition explaining the historical context of World War II and the Nazi occupation of the Netherlands.", 15, None),
                    ("The Secret Annex", "Enter the Secret Annex through the famous bookcase door. Walk through the small rooms where the Frank family and four others hid for two years.", 40, None),
                    ("Anne's Room", "See Anne Frank's room where she wrote her diary, including the photos of movie stars she pasted on the wall.", 15, None),
                    ("Permanent Exhibition", "Visit the permanent exhibition about Anne's life, her diary's publication, and its worldwide impact. Reflect on themes of discrimination and human rights.", 20, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 50, Decimal("0.00")),
                    ("10:30", "Late Morning", 50, Decimal("0.00")),
                    ("12:00", "Midday", 50, Decimal("0.00")),
                    ("13:30", "Afternoon", 50, Decimal("0.00")),
                    ("15:00", "Late Afternoon", 50, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Timed entry ticket with multimedia guide", Decimal("16.00"), Decimal("7.00"), 0)
                ],
                "add_ons": [
                    ("Anne Frank diary book", "Purchase the diary of Anne Frank in your language", Decimal("12.00")),
                    ("Audio guide upgrade", "Enhanced audio guide with additional survivor testimonies", Decimal("5.00"))
                ]
            },
            # LONDON - British Museum
            {
                "title": "British Museum: Guided Highlights Tour",
                "vendor": 3,
                "category": 1,  # Museums
                "destination": 1,  # London
                "short_description": "Discover the British Museum's greatest treasures with an expert guide",
                "description": "Explore one of the world's greatest museums with an expert guide who will navigate you through the vast collection. See the Rosetta Stone, Egyptian mummies, the Parthenon Marbles, and other iconic artifacts spanning human history. This guided tour ensures you don't miss the highlights while learning fascinating stories behind the objects. Free museum entry, you only pay for the guide.",
                "price_adult": Decimal("35.00"),
                "price_child": Decimal("25.00"),
                "duration": 150,
                "max_group_size": 20,
                "languages": ["English", "Spanish", "French"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "is_stroller_accessible": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Museum follows current health guidelines, enhanced ventilation",
                "is_giftable": True,
                "what_to_bring": "Comfortable walking shoes",
                "has_multiple_tiers": True,
                "meeting_address": "Great Russell St, London WC1B 3DG, United Kingdom",
                "meeting_instructions": "Meet your guide at the main entrance steps of the British Museum. Look for the guide with a purple flag.",
                "highlights": [
                    "Expert guide to navigate the vast museum",
                    "See the Rosetta Stone, Egyptian mummies, and Parthenon Marbles",
                    "Learn about artifacts from ancient civilizations",
                    "Small group for better interaction",
                    "Free museum entry (you pay only for guide)"
                ],
                "includes": [
                    ("Expert guide", True),
                    ("Headsets for larger groups", True),
                    ("Museum entry (free)", True),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Museum Introduction", "Meet your guide and enter the museum. Brief overview of the collection and the day's route.", 10, None),
                    ("Ancient Egypt", "Explore the Egyptian galleries to see the Rosetta Stone, mummies, and ancient artifacts. Learn about Egyptian civilization and burial practices.", 40, None),
                    ("Ancient Greece", "Visit the Parthenon Marbles and other Greek sculptures. Your guide explains the controversy and significance of these classical masterpieces.", 35, None),
                    ("Middle East & Assyrian Reliefs", "See massive Assyrian stone reliefs and artifacts from ancient Mesopotamia. Learn about the earliest civilizations.", 30, None),
                    ("Additional Highlights", "Visit other key galleries based on group interest - options include Roman Britain, Medieval Europe, or Asian art.", 25, None),
                    ("Tour Conclusion", "Receive recommendations for further exploration and nearby attractions.", 10, None)
                ],
                "time_slots": [
                    ("10:00", "Morning", 20, Decimal("0.00")),
                    ("13:00", "Afternoon", 20, Decimal("0.00")),
                    ("15:00", "Late Afternoon", 20, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group tour with expert guide", Decimal("35.00"), Decimal("25.00"), 0),
                    ("Premium", "Semi-private tour (max 8) with extended time and curator insights", Decimal("75.00"), Decimal("60.00"), 1)
                ],
                "add_ons": [
                    ("Museum guidebook", "Comprehensive illustrated guidebook", Decimal("10.00")),
                    ("Audio guide", "Self-guided audio tour for further exploration after the tour", Decimal("7.00"))
                ]
            },
            # NEW YORK - Statue of Liberty
            {
                "title": "Statue of Liberty & Ellis Island: Ferry Tour with Pedestal Access",
                "vendor": 0,
                "category": 0,  # Tours
                "destination": 5,  # New York
                "short_description": "Visit the Statue of Liberty and Ellis Island with pedestal access and ferry ride",
                "description": "Experience two of America's most iconic landmarks on this comprehensive tour. Take the ferry to Liberty Island and ascend to the pedestal of the Statue of Liberty for spectacular views of New York Harbor. Continue to Ellis Island to explore the Immigration Museum and trace the journey of millions who arrived in America. Audio guide included in 15 languages.",
                "price_adult": Decimal("45.00"),
                "price_child": Decimal("35.00"),
                "duration": 300,
                "max_group_size": 40,
                "languages": ["English", "Spanish", "French", "German", "Italian", "Japanese", "Chinese"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "has_covid_measures": True,
                "covid_measures": "Ferry operates at reduced capacity, enhanced cleaning protocols",
                "is_giftable": True,
                "what_to_bring": "Valid photo ID (required for security), camera, weather-appropriate clothing",
                "has_multiple_tiers": True,
                "meeting_address": "Battery Park, New York, NY 10004, United States",
                "meeting_instructions": "Arrive at Battery Park and present your ticket at the Statue Cruises ticket office. Go through security before boarding.",
                "highlights": [
                    "Ferry ride with NYC skyline views",
                    "Pedestal access to Statue of Liberty",
                    "Explore Ellis Island Immigration Museum",
                    "Audio guide in 15 languages",
                    "Learn about immigration history"
                ],
                "includes": [
                    ("Round-trip ferry to Liberty Island and Ellis Island", True),
                    ("Pedestal access to Statue of Liberty", True),
                    ("Ellis Island Immigration Museum entry", True),
                    ("Audio guide in multiple languages", True),
                    ("Food and drinks", False),
                    ("Crown access", False)
                ],
                "timelines": [
                    ("Ferry Departure", "Board the ferry at Battery Park. Enjoy views of Lower Manhattan and the Brooklyn Bridge during the 15-minute ride.", 30, None),
                    ("Liberty Island", "Disembark at Liberty Island. Enter the Statue of Liberty pedestal for close-up views and harbor panoramas. Visit the museum about the statue's history and construction.", 90, None),
                    ("Ferry to Ellis Island", "Take the short ferry ride to Ellis Island.", 15, None),
                    ("Ellis Island Museum", "Explore the Immigration Museum where millions of immigrants were processed. Use your audio guide to learn personal stories and see historical exhibits.", 120, None),
                    ("Return to Manhattan", "Board the ferry back to Battery Park.", 25, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 40, Decimal("0.00")),
                    ("10:30", "Late Morning", 40, Decimal("0.00")),
                    ("12:00", "Midday", 40, Decimal("0.00")),
                    ("14:00", "Afternoon", 40, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Pedestal Access", "Ferry with pedestal access and Ellis Island", Decimal("45.00"), Decimal("35.00"), 0),
                    ("Crown Access", "Includes climb to Statue of Liberty crown (reserve early!)", Decimal("65.00"), Decimal("55.00"), 1)
                ],
                "add_ons": [
                    ("Crown reserve ticket", "Upgrade to crown access (subject to availability)", Decimal("20.00")),
                    ("Souvenir guidebook", "Illustrated guidebook about the statue and Ellis Island", Decimal("12.00"))
                ]
            },
            # NEW YORK - Empire State Building
            {
                "title": "Empire State Building: Skip-the-Line Tickets to 86th & 102nd Floor",
                "vendor": 0,
                "category": 1,  # Museums & Attractions
                "destination": 5,  # New York
                "short_description": "Skip the lines and visit both the 86th and 102nd floor observatories",
                "description": "Ascend to the top of New York City's most iconic skyscraper with skip-the-line access. Visit both the open-air 86th floor observatory and the 102nd floor top deck for unparalleled 360-degree views of Manhattan and beyond. On clear days, see up to 80 miles. Includes interactive exhibits about the building's construction and history.",
                "price_adult": Decimal("75.00"),
                "price_child": Decimal("65.00"),
                "original_price_adult": Decimal("85.00"),
                "discount_percentage": 12,
                "duration": 120,
                "max_group_size": 50,
                "languages": ["English", "Spanish", "French", "German", "Italian", "Portuguese"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "has_best_price_guarantee": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Limited capacity, enhanced cleaning, touchless payment",
                "is_giftable": True,
                "what_to_bring": "Camera, jacket (it can be windy at the top)",
                "has_multiple_tiers": True,
                "meeting_address": "20 W 34th St, New York, NY 10001, United States",
                "meeting_instructions": "Enter the Empire State Building at the main entrance on 34th Street. Present your mobile ticket at the dedicated skip-the-line entrance.",
                "highlights": [
                    "Skip the regular queues",
                    "Visit both 86th and 102nd floor observatories",
                    "360-degree views of NYC",
                    "Open-air viewing deck on 86th floor",
                    "Interactive exhibits about building history"
                ],
                "includes": [
                    ("Skip-the-line access", True),
                    ("86th floor observatory access", True),
                    ("102nd floor top deck access", True),
                    ("Multimedia exhibits", True),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Express Entry & Exhibits", "Enter through the skip-the-line entrance. Visit the interactive exhibits about the Empire State Building's construction, history, and cultural significance.", 30, None),
                    ("86th Floor Observatory", "Take the high-speed elevator to the famous 86th floor open-air observatory. Walk around the entire deck for 360-degree views. Identify landmarks with telescopes.", 50, None),
                    ("102nd Floor Top Deck", "Ascend to the 102nd floor, the highest observatory in the building. Floor-to-ceiling windows provide stunning views without wind. Perfect for photos.", 40, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 50, Decimal("0.00")),
                    ("11:00", "Late Morning", 50, Decimal("0.00")),
                    ("13:00", "Afternoon", 50, Decimal("0.00")),
                    ("15:00", "Late Afternoon", 50, Decimal("0.00")),
                    ("17:00", "Evening", 50, Decimal("5.00")),
                    ("19:00", "Night", 50, Decimal("10.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Skip-the-line access to 86th and 102nd floors", Decimal("75.00"), Decimal("65.00"), 0),
                    ("VIP", "Private elevator, expedited entry, and complimentary beverage", Decimal("150.00"), Decimal("130.00"), 1)
                ],
                "add_ons": [
                    ("Photo package", "Professional photo with green screen NYC background", Decimal("20.00")),
                    ("Audio guide", "Enhanced audio guide with celebrity narration", Decimal("10.00")),
                    ("Souvenir guidebook", "Hardcover book about the Empire State Building", Decimal("18.00"))
                ]
            },
            # NEW YORK - Broadway Show
            {
                "title": "Broadway Show: The Lion King - Orchestra or Mezzanine Seats",
                "vendor": 4,
                "category": 5,  # Shows & Entertainment
                "destination": 5,  # New York
                "short_description": "Experience Disney's award-winning Broadway musical with premium seating",
                "description": "See Disney's spectacular Broadway adaptation of The Lion King at the Minskoff Theatre. This Tony Award-winning musical features stunning costumes, innovative puppetry, and unforgettable music by Elton John and Tim Rice. Watch as Pride Rock comes to life in one of Broadway's longest-running and most beloved shows. Choose from Orchestra or Mezzanine seating.",
                "price_adult": Decimal("145.00"),
                "price_child": Decimal("145.00"),
                "duration": 165,
                "max_group_size": 8,
                "languages": ["English"],
                "is_bestseller": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Follow current Broadway League health protocols",
                "is_giftable": True,
                "dress_code": "Smart casual recommended (no shorts or flip-flops)",
                "what_to_bring": "Mobile ticket, valid ID",
                "has_multiple_tiers": True,
                "meeting_address": "Minskoff Theatre, 200 W 45th St, New York, NY 10036",
                "meeting_instructions": "Arrive at the Minskoff Theatre at least 30 minutes before showtime. Present your mobile ticket at the entrance.",
                "highlights": [
                    "See Disney's award-winning The Lion King on Broadway",
                    "Orchestra or Mezzanine premium seating",
                    "Stunning costumes and innovative puppetry",
                    "Iconic songs: Circle of Life, Can You Feel the Love Tonight",
                    "Perfect for families and theater lovers"
                ],
                "includes": [
                    ("Premium orchestra or mezzanine seat ticket", True),
                    ("Playbill souvenir program", True),
                    ("Merchandise", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Theater Arrival", "Arrive at the Minskoff Theatre, collect your ticket, and find your seat. Enjoy the elegant Broadway theater atmosphere.", 30, None),
                    ("Act One", "The show begins with the iconic 'Circle of Life' opening. Follow young Simba's journey in the Pride Lands. Act One is approximately 75 minutes.", 75, None),
                    ("Intermission", "15-minute intermission. Visit the restrooms or concession stands.", 15, None),
                    ("Act Two", "Simba's journey continues as he grows up and must face his destiny. Conclude with powerful finale. Act Two is approximately 45 minutes.", 45, None)
                ],
                "time_slots": [
                    ("14:00", "Matinee", 8, Decimal("0.00")),
                    ("19:00", "Evening Show", 8, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Mezzanine", "Premium mezzanine seating with excellent views", Decimal("145.00"), Decimal("145.00"), 0),
                    ("Orchestra", "Premium orchestra level seating for best experience", Decimal("195.00"), Decimal("195.00"), 1),
                    ("VIP Package", "Best orchestra seats with souvenir merchandise and backstage tour", Decimal("395.00"), Decimal("395.00"), 2)
                ],
                "add_ons": [
                    ("Backstage tour", "Behind-the-scenes tour after the show", Decimal("45.00")),
                    ("Souvenir program", "Deluxe program with cast signatures", Decimal("25.00")),
                    ("Pre-theater dinner", "3-course dinner at nearby restaurant", Decimal("55.00"))
                ]
            },
            # TOKYO - Mt Fuji Day Trip
            {
                "title": "Mt. Fuji Day Trip: 5th Station, Lake Kawaguchi & Oshino Hakkai",
                "vendor": 2,
                "category": 2,  # Day Trips
                "destination": 6,  # Tokyo
                "short_description": "Full-day guided tour to Mt. Fuji with stops at scenic viewpoints and traditional villages",
                "description": "Escape Tokyo for a day and discover the majestic Mt. Fuji, Japan's most iconic landmark. This comprehensive tour takes you to the Mt. Fuji 5th Station for breathtaking views, the scenic Lake Kawaguchi area, and the traditional Oshino Hakkai village with its crystal-clear springs. Includes lunch and round-trip transportation from central Tokyo in a comfortable coach.",
                "price_adult": Decimal("95.00"),
                "price_child": Decimal("75.00"),
                "duration": 660,
                "max_group_size": 40,
                "languages": ["English", "Japanese"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": True,
                "has_covid_measures": True,
                "covid_measures": "Coach sanitized between tours, masks required on bus",
                "is_giftable": True,
                "what_to_bring": "Camera, warm jacket (cooler at Mt. Fuji), comfortable walking shoes",
                "not_suitable_for": "People with severe mobility issues",
                "has_multiple_tiers": False,
                "meeting_address": "Shinjuku Center Building, 1 Chome-25-1 Nishishinjuku, Tokyo",
                "meeting_instructions": "Meet at the Shinjuku Center Building main entrance. Look for the coach with 'Mt. Fuji Tours' sign.",
                "highlights": [
                    "Visit Mt. Fuji 5th Station at 2,300 meters altitude",
                    "Scenic views at Lake Kawaguchi",
                    "Explore traditional Oshino Hakkai village",
                    "Lunch included",
                    "Round-trip coach from Tokyo"
                ],
                "includes": [
                    ("Round-trip coach transportation", True),
                    ("English-speaking guide", True),
                    ("Mt. Fuji 5th Station visit", True),
                    ("Lake Kawaguchi scenic area", True),
                    ("Oshino Hakkai village visit", True),
                    ("Lunch", True),
                    ("Personal expenses", False)
                ],
                "timelines": [
                    ("Departure from Tokyo", "Board the comfortable coach at Shinjuku and depart for Mt. Fuji. Your guide provides commentary during the scenic drive.", 120, None),
                    ("Mt. Fuji 5th Station", "Arrive at the Mt. Fuji 5th Station at 2,300 meters elevation. Enjoy panoramic views of the surrounding landscape and visit the shrine and souvenir shops.", 60, None),
                    ("Lunch", "Enjoy a traditional Japanese lunch at a local restaurant with views of Mt. Fuji.", 60, None),
                    ("Lake Kawaguchi", "Visit the scenic Lake Kawaguchi area, one of the Fuji Five Lakes. Take photos of Mt. Fuji reflected in the lake waters (weather permitting).", 45, None),
                    ("Oshino Hakkai", "Explore the traditional village of Oshino Hakkai, famous for its eight crystal-clear spring water ponds fed by Mt. Fuji's snowmelt. See traditional thatched-roof houses.", 60, None),
                    ("Return to Tokyo", "Relax on the coach ride back to Tokyo, arriving in early evening.", 135, None)
                ],
                "time_slots": [
                    ("07:30", "Morning Departure", 40, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Full-day tour with lunch and transportation", Decimal("95.00"), Decimal("75.00"), 0)
                ],
                "add_ons": [
                    ("Mt. Fuji Photo Book", "Professional photo book of Mt. Fuji", Decimal("18.00")),
                    ("Sake tasting", "Add sake tasting at a local brewery", Decimal("25.00"))
                ]
            },
            # TOKYO - Tsukiji Fish Market
            {
                "title": "Tokyo: Tsukiji Outer Market Food Tour with Local Guide",
                "vendor": 1,
                "category": 3,  # Food & Drink
                "destination": 6,  # Tokyo
                "short_description": "Explore Tsukiji Outer Market and taste fresh sushi, street food, and Japanese delicacies",
                "description": "Experience Tokyo's legendary food scene with a local guide at the Tsukiji Outer Market. Although the inner wholesale market has moved, the outer market still thrives with hundreds of vendors, restaurants, and shops. Sample fresh sushi, tamagoyaki (Japanese omelette), grilled seafood, and other Japanese street food while learning about Japanese culinary culture. Includes 7-8 food tastings.",
                "price_adult": Decimal("85.00"),
                "price_child": Decimal("65.00"),
                "duration": 180,
                "max_group_size": 10,
                "languages": ["English", "Japanese"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Small groups, outdoor market environment, vendor health protocols",
                "is_giftable": True,
                "what_to_bring": "Appetite, camera, cash for personal purchases",
                "not_suitable_for": "Vegetarians (tour is heavily seafood-focused), people with severe seafood allergies",
                "has_multiple_tiers": False,
                "meeting_address": "Tsukiji Station, Exit 1, Tokyo Metro Hibiya Line",
                "meeting_instructions": "Meet your guide at Tsukiji Station Exit 1. Look for the guide holding a red fish-shaped sign.",
                "highlights": [
                    "Explore the historic Tsukiji Outer Market",
                    "7-8 food tastings including fresh sushi",
                    "Local guide with insider knowledge",
                    "Small group for personalized experience",
                    "Learn about Japanese food culture and ingredients"
                ],
                "includes": [
                    ("Local guide", True),
                    ("7-8 food tastings", True),
                    ("Green tea", True),
                    ("Additional purchases", False),
                    ("Transportation", False)
                ],
                "timelines": [
                    ("Market Introduction", "Meet your guide and receive an introduction to Tsukiji's history and the difference between the inner and outer markets.", 15, None),
                    ("First Tastings", "Begin tasting at a famous tamagoyaki (Japanese omelette) shop and fresh sashimi stand. Learn about fish varieties and selection.", 40, None),
                    ("Street Food Vendors", "Sample grilled seafood, fish cakes, and other Japanese street food favorites. Your guide explains preparation methods and ingredients.", 50, None),
                    ("Sushi Restaurant", "Sit down at a traditional sushi counter for nigiri sushi made from the day's freshest catch. Watch the chef's knife skills.", 45, None),
                    ("Final Tastings & Shop Browsing", "Taste Japanese sweets or matcha desserts. Browse the market shops for souvenirs like tea, knives, and ceramics.", 30, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 10, Decimal("0.00")),
                    ("11:00", "Late Morning", 10, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group food tour with local guide", Decimal("85.00"), Decimal("65.00"), 0)
                ],
                "add_ons": [
                    ("Sake tasting", "Add sake tasting at a local shop with pairing explanation", Decimal("20.00")),
                    ("Japanese knife shop visit", "Visit a famous knife shop with explanation of Japanese knife-making", Decimal("15.00"))
                ]
            },
            # DUBAI - Burj Khalifa
            {
                "title": "Burj Khalifa: At the Top SKY Ticket (148th Floor)",
                "vendor": 4,
                "category": 1,  # Museums & Attractions
                "destination": 7,  # Dubai
                "short_description": "Visit the world's highest observation deck on the 148th floor of Burj Khalifa",
                "description": "Experience the ultimate Dubai attraction with exclusive access to the world's highest observation deck on the 148th floor of Burj Khalifa, the world's tallest building. At 555 meters high, enjoy unparalleled 360-degree views of Dubai's skyline, desert, and ocean. Includes access to levels 148, 125, and 124. Reception with refreshments on 148th floor. Fast-track entry.",
                "price_adult": Decimal("120.00"),
                "price_child": Decimal("95.00"),
                "duration": 90,
                "max_group_size": 30,
                "languages": ["English", "Arabic", "French", "German", "Chinese"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "is_likely_to_sell_out": True,
                "has_mobile_ticket": True,
                "has_best_price_guarantee": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Limited capacity, enhanced cleaning, touchless entry systems",
                "is_giftable": True,
                "what_to_bring": "Camera, modest clothing (shoulders and knees covered)",
                "has_multiple_tiers": True,
                "meeting_address": "The Dubai Mall, Lower Ground Level, Dubai, UAE",
                "meeting_instructions": "Enter the Dubai Mall and head to the Burj Khalifa entrance on the Lower Ground floor near the Fashion Avenue. Present your mobile ticket.",
                "highlights": [
                    "Visit the world's highest observation deck (148th floor)",
                    "Fast-track entry to skip queues",
                    "360-degree views from 555 meters high",
                    "Access to levels 148, 125, and 124",
                    "Refreshments on 148th floor",
                    "Multimedia presentations about Dubai and the tower"
                ],
                "includes": [
                    ("Fast-track entry", True),
                    ("Access to 148th, 125th, and 124th floor observatories", True),
                    ("Refreshments on 148th floor", True),
                    ("Interactive displays", True),
                    ("Food and additional drinks", False),
                    ("Transportation", False)
                ],
                "timelines": [
                    ("Fast-Track Entry", "Enter through the dedicated fast-track entrance, bypassing regular queues. Take the high-speed elevator to the 125th floor.", 15, None),
                    ("125th & 124th Floors", "Begin at the 125th floor outdoor terrace and 124th floor observatory. Enjoy panoramic views and interactive displays about Dubai.", 30, None),
                    ("148th Floor SKY", "Take another elevator to the exclusive 148th floor, the world's highest observation deck at 555 meters. Enjoy a beverage while taking in extraordinary views.", 35, None),
                    ("Descent & Dubai Mall", "Return to ground level via high-speed elevator. Optional time to explore The Dubai Mall.", 10, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 30, Decimal("0.00")),
                    ("11:30", "Late Morning", 30, Decimal("0.00")),
                    ("14:00", "Afternoon", 30, Decimal("0.00")),
                    ("16:30", "Late Afternoon", 30, Decimal("10.00")),
                    ("18:00", "Sunset", 30, Decimal("20.00")),
                    ("19:30", "Evening", 30, Decimal("15.00"))
                ],
                "pricing_tiers": [
                    ("At the Top", "Standard ticket to 124th and 125th floors only", Decimal("55.00"), Decimal("45.00"), 0),
                    ("At the Top SKY", "Premium ticket to 148th, 125th, and 124th floors with refreshments", Decimal("120.00"), Decimal("95.00"), 1),
                    ("VIP", "Private elevator, personalized tour, premium lounge access", Decimal("350.00"), Decimal("300.00"), 2)
                ],
                "add_ons": [
                    ("Photo package", "Professional photos with city backdrop", Decimal("30.00")),
                    ("Dubai Fountain show viewing", "Reserved seating for Dubai Fountain show", Decimal("20.00")),
                    ("Souvenir book", "Hardcover book about Burj Khalifa construction", Decimal("25.00"))
                ]
            },
            # DUBAI - Desert Safari
            {
                "title": "Dubai: Desert Safari with BBQ Dinner and Bedouin Camp Experience",
                "vendor": 2,
                "category": 4,  # Adventure & Nature
                "destination": 7,  # Dubai
                "short_description": "Thrilling desert safari with dune bashing, camel ride, BBQ dinner, and live entertainment",
                "description": "Experience the Arabian desert on this action-packed evening safari. Enjoy exhilarating dune bashing in a 4x4 vehicle, ride a camel, try sandboarding, and watch the sunset over the desert. Arrive at a traditional Bedouin camp for a delicious BBQ dinner, shisha smoking, henna painting, and live entertainment including belly dancing and Tanoura shows. Hotel pickup and drop-off included.",
                "price_adult": Decimal("75.00"),
                "price_child": Decimal("60.00"),
                "duration": 360,
                "max_group_size": 6,
                "languages": ["English", "Arabic"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": True,
                "has_covid_measures": True,
                "covid_measures": "Sanitized vehicles, smaller groups, outdoor activities",
                "is_giftable": True,
                "what_to_bring": "Sunglasses, sunscreen, light jacket for evening, camera",
                "not_suitable_for": "Pregnant women, people with back problems, children under 3",
                "has_multiple_tiers": True,
                "meeting_address": "Hotel pickup from Dubai city hotels",
                "meeting_instructions": "Driver will pick you up from your hotel lobby. Pickup time will be confirmed 24 hours before the tour (typically 15:00-15:30).",
                "highlights": [
                    "Hotel pickup and drop-off in 4x4 vehicle",
                    "Thrilling dune bashing experience",
                    "Camel riding and sandboarding",
                    "Sunset views in the desert",
                    "BBQ dinner at Bedouin camp",
                    "Live entertainment: belly dancing, Tanoura show",
                    "Henna painting and shisha smoking"
                ],
                "includes": [
                    ("Hotel pickup and drop-off", True),
                    ("Dune bashing in 4x4 vehicle", True),
                    ("Camel riding", True),
                    ("Sandboarding", True),
                    ("BBQ dinner with unlimited soft drinks", True),
                    ("Live entertainment shows", True),
                    ("Henna painting", True),
                    ("Shisha smoking", True),
                    ("Alcoholic beverages", False),
                    ("Quad biking (available as add-on)", False)
                ],
                "timelines": [
                    ("Hotel Pickup", "Your driver picks you up from your hotel in a comfortable 4x4 vehicle. Drive to the desert (approximately 45 minutes).", 60, None),
                    ("Dune Bashing", "Experience thrilling dune bashing as your expert driver navigates the desert dunes in the 4x4.", 30, None),
                    ("Desert Activities", "Try sandboarding down the dunes, ride a camel, and take photos in traditional Arabic costumes. Watch the spectacular desert sunset.", 60, None),
                    ("Bedouin Camp Arrival", "Arrive at the traditional Bedouin camp. Enjoy Arabic coffee and dates, get henna painting, and explore the camp.", 30, None),
                    ("BBQ Dinner & Shows", "Enjoy a delicious BBQ buffet dinner with Arabic and international dishes. Watch live entertainment including belly dancing, Tanoura shows, and fire shows.", 120, None),
                    ("Return to Hotel", "Relax during the drive back to your hotel.", 60, None)
                ],
                "time_slots": [
                    ("15:00", "Afternoon Pickup", 6, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Shared 4x4 vehicle (max 6 passengers)", Decimal("75.00"), Decimal("60.00"), 0),
                    ("Premium", "Private 4x4 for your group with quad biking included", Decimal("180.00"), Decimal("150.00"), 1),
                    ("VIP", "Private vehicle, VIP camp seating, falcon photo session, premium dinner", Decimal("280.00"), Decimal("240.00"), 2)
                ],
                "add_ons": [
                    ("Quad biking", "30-minute quad bike ride in the desert", Decimal("45.00")),
                    ("Falcon photo session", "Professional photo with falcon on your arm", Decimal("25.00")),
                    ("Private seating at camp", "Private table and seating area at the Bedouin camp", Decimal("35.00"))
                ]
            },
            # PRAGUE - Castle Tour
            {
                "title": "Prague Castle: Skip-the-Line Guided Tour with St. Vitus Cathedral",
                "vendor": 3,
                "category": 1,  # Museums
                "destination": 8,  # Prague
                "short_description": "Explore Prague Castle complex with skip-the-line access and expert guide",
                "description": "Discover the largest ancient castle complex in the world with an expert guide. Skip the ticket lines and explore Prague Castle's highlights including St. Vitus Cathedral, Old Royal Palace, Golden Lane, and St. George's Basilica. Learn about Czech history, kings, and emperors while admiring Gothic architecture and stunning city views.",
                "price_adult": Decimal("45.00"),
                "price_child": Decimal("35.00"),
                "duration": 180,
                "max_group_size": 20,
                "languages": ["English", "German", "Czech"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": False,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Limited group sizes, timed entry to buildings",
                "is_giftable": True,
                "what_to_bring": "Comfortable walking shoes, modest clothing for cathedral",
                "not_suitable_for": "People with severe mobility issues (many stairs and hills)",
                "has_multiple_tiers": False,
                "meeting_address": "Malostranská Metro Station, Prague 1",
                "meeting_instructions": "Meet your guide at the exit of Malostranská Metro Station (green line). Look for the guide with a yellow castle flag.",
                "highlights": [
                    "Skip the ticket lines at Prague Castle",
                    "Explore St. Vitus Cathedral's Gothic interior",
                    "Visit the Old Royal Palace",
                    "See the colorful houses of Golden Lane",
                    "Panoramic views of Prague"
                ],
                "includes": [
                    ("Skip-the-line entrance tickets", True),
                    ("Expert guide", True),
                    ("Headsets for larger groups", True),
                    ("Transportation", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Castle Approach", "Meet your guide and walk up to Prague Castle through historic streets. Learn about the castle's 1,000-year history.", 20, None),
                    ("Castle Courtyards", "Enter the castle grounds and walk through the courtyards. See the changing of the guard ceremony (if timed right).", 20, None),
                    ("St. Vitus Cathedral", "Enter the magnificent Gothic cathedral. Admire the stained glass windows, royal tombs, and St. Wenceslas Chapel.", 45, None),
                    ("Old Royal Palace", "Visit the Old Royal Palace including the stunning Vladislav Hall with its Gothic vaulted ceiling.", 30, None),
                    ("Golden Lane", "Explore the charming Golden Lane with its tiny colorful houses where castle craftsmen once lived. Visit Franz Kafka's former residence.", 35, None),
                    ("St. George's Basilica", "Tour the oldest surviving church building within Prague Castle, dating from 920 AD.", 10, None)
                ],
                "time_slots": [
                    ("09:30", "Morning", 20, Decimal("0.00")),
                    ("11:30", "Late Morning", 20, Decimal("0.00")),
                    ("14:00", "Afternoon", 20, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group tour with skip-the-line access", Decimal("45.00"), Decimal("35.00"), 0)
                ],
                "add_ons": [
                    ("Castle gardens", "Add access to beautiful Prague Castle gardens", Decimal("8.00")),
                    ("Lobkowicz Palace", "Add entry to Lobkowicz Palace museum", Decimal("15.00")),
                    ("Audio guide", "Take-home audio guide for further castle exploration", Decimal("6.00"))
                ]
            },
            # PRAGUE - Beer Tour
            {
                "title": "Prague: Czech Beer Tasting Tour with Local Guide",
                "vendor": 1,
                "category": 3,  # Food & Drink
                "destination": 8,  # Prague
                "short_description": "Taste authentic Czech beers at local breweries and traditional pubs",
                "description": "Discover why the Czech Republic has the highest beer consumption per capita in the world! Join a local beer expert for a tour of Prague's best traditional pubs and microbreweries. Sample 5-6 different Czech beers including pilsner, lager, and dark beer while learning about Czech brewing traditions. Includes beer snacks and a fun, social atmosphere.",
                "price_adult": Decimal("55.00"),
                "price_child": Decimal("35.00"),
                "duration": 210,
                "max_group_size": 15,
                "languages": ["English", "German"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Small groups, venues follow health protocols",
                "is_giftable": True,
                "what_to_bring": "Appetite for beer and Czech culture",
                "not_suitable_for": "People under 18, non-drinkers (limited non-alcoholic options)",
                "has_multiple_tiers": False,
                "meeting_address": "Old Town Square, Prague 1, near the Astronomical Clock",
                "meeting_instructions": "Meet your guide in Old Town Square near the Jan Hus statue. Look for the guide with a beer mug sign.",
                "highlights": [
                    "Visit 3-4 traditional Czech pubs and breweries",
                    "Taste 5-6 authentic Czech beers",
                    "Learn about Czech brewing history and traditions",
                    "Local beer expert guide",
                    "Beer snacks included",
                    "Small group for social atmosphere"
                ],
                "includes": [
                    ("Local beer expert guide", True),
                    ("5-6 beer tastings (0.3L each)", True),
                    ("Beer snacks (cheese, sausage, bread)", True),
                    ("Visit to 3-4 venues", True),
                    ("Additional drinks", False),
                    ("Dinner", False)
                ],
                "timelines": [
                    ("First Pub - Introduction", "Meet your guide and walk to the first traditional Czech pub. Learn about Czech beer culture and taste your first pilsner.", 45, None),
                    ("Microbrewery Visit", "Visit a local microbrewery and taste craft beers. Learn about the brewing process and try unique flavors.", 50, None),
                    ("Historic Beer Hall", "Experience a historic Prague beer hall. Taste dark Czech beer and lager while enjoying the authentic atmosphere.", 45, None),
                    ("Final Stop & Snacks", "End at a local favorite pub for one more beer and traditional Czech beer snacks. Your guide shares final recommendations for Prague nightlife.", 40, None)
                ],
                "time_slots": [
                    ("17:00", "Evening", 15, Decimal("0.00")),
                    ("19:00", "Late Evening", 15, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Beer tasting tour with snacks", Decimal("55.00"), Decimal("35.00"), 0)
                ],
                "add_ons": [
                    ("Extra beer", "Additional beer at each venue", Decimal("10.00")),
                    ("Czech dinner", "Add traditional Czech dinner at final venue", Decimal("20.00")),
                    ("Brewery gift pack", "Take-home selection of Czech beers", Decimal("18.00"))
                ]
            },
            # ISTANBUL - Bosphorus Cruise
            {
                "title": "Istanbul: Bosphorus Sunset Cruise with Dinner and Turkish Entertainment",
                "vendor": 4,
                "category": 0,  # Tours
                "destination": 9,  # Istanbul
                "short_description": "Romantic Bosphorus cruise with dinner, drinks, and traditional Turkish shows",
                "description": "Experience Istanbul's beauty from the water on this magical sunset cruise along the Bosphorus Strait. Enjoy a delicious Turkish dinner buffet while sailing past iconic landmarks including Dolmabahçe Palace, Maiden's Tower, and the Bosphorus bridges. Be entertained by live Turkish music, belly dancing, and whirling dervish performances. Includes hotel pickup and drop-off.",
                "price_adult": Decimal("85.00"),
                "price_child": Decimal("65.00"),
                "duration": 240,
                "max_group_size": 100,
                "languages": ["English", "Turkish"],
                "is_bestseller": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "weather_dependent": True,
                "has_covid_measures": True,
                "covid_measures": "Outdoor deck seating available, enhanced ventilation",
                "is_giftable": True,
                "dress_code": "Smart casual (no shorts or flip-flops)",
                "what_to_bring": "Camera, jacket for evening breeze",
                "has_multiple_tiers": True,
                "meeting_address": "Hotel pickup from European and Asian side hotels",
                "meeting_instructions": "Driver will pick you up from your hotel lobby. Pickup time will be confirmed 24 hours before the cruise.",
                "highlights": [
                    "Sunset cruise along the Bosphorus Strait",
                    "See Dolmabahçe Palace, Maiden's Tower, and Bosphorus bridges",
                    "Turkish dinner buffet with unlimited soft drinks",
                    "Live entertainment: belly dancing, whirling dervish, Turkish music",
                    "Hotel pickup and drop-off included"
                ],
                "includes": [
                    ("Round-trip hotel pickup and drop-off", True),
                    ("4-hour Bosphorus cruise", True),
                    ("Turkish dinner buffet", True),
                    ("Unlimited soft drinks", True),
                    ("Live entertainment shows", True),
                    ("Alcoholic beverages", False)
                ],
                "timelines": [
                    ("Hotel Pickup & Boarding", "Pick up from your hotel and transfer to the cruise pier. Board the boat and find your table.", 45, None),
                    ("Cruise Begins - Sunset", "Cruise departs and sails along the Bosphorus at sunset. See landmarks lit up as evening falls. Enjoy welcome drinks.", 45, None),
                    ("Dinner Service", "Enjoy a Turkish buffet dinner with hot and cold meze, grilled meats, fish, and traditional desserts.", 60, None),
                    ("Live Entertainment", "Watch live Turkish entertainment including belly dancing, whirling dervish performance, DJ music, and traditional Turkish folk dancers.", 75, None),
                    ("Return to Pier & Hotel Drop-off", "Boat returns to pier. Transfer back to your hotel.", 35, None)
                ],
                "time_slots": [
                    ("18:00", "Evening Pickup", 100, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Standard seating with buffet dinner", Decimal("85.00"), Decimal("65.00"), 0),
                    ("VIP", "Window-side table, premium seating, and welcome drink", Decimal("120.00"), Decimal("95.00"), 1)
                ],
                "add_ons": [
                    ("Unlimited alcoholic drinks", "Add unlimited beer, wine, and raki", Decimal("25.00")),
                    ("Premium photo package", "Professional photos throughout the cruise", Decimal("20.00")),
                    ("VIP transfer", "Private car pickup instead of shared van", Decimal("30.00"))
                ]
            },
            # ISTANBUL - Hagia Sophia & Blue Mosque
            {
                "title": "Istanbul: Hagia Sophia, Blue Mosque & Topkapi Palace Guided Tour",
                "vendor": 3,
                "category": 0,  # Tours
                "destination": 9,  # Istanbul
                "short_description": "Explore Istanbul's most iconic landmarks with skip-the-line access and expert guide",
                "description": "Discover Istanbul's rich Byzantine and Ottoman heritage on this comprehensive guided tour. Visit the magnificent Hagia Sophia, the stunning Blue Mosque, and the opulent Topkapi Palace. Your expert guide will bring these UNESCO World Heritage sites to life with fascinating stories of sultans, emperors, and empires. Includes skip-the-line access to Topkapi Palace.",
                "price_adult": Decimal("75.00"),
                "price_child": Decimal("60.00"),
                "duration": 300,
                "max_group_size": 15,
                "languages": ["English", "Turkish", "Spanish"],
                "is_bestseller": True,
                "is_skip_the_line": True,
                "has_mobile_ticket": True,
                "is_verified_activity": True,
                "is_wheelchair_accessible": False,
                "weather_dependent": False,
                "has_covid_measures": True,
                "covid_measures": "Small groups, timed entry to monuments",
                "is_giftable": True,
                "what_to_bring": "Modest clothing, comfortable shoes, headscarf for women (for Blue Mosque)",
                "not_suitable_for": "People unable to walk for extended periods",
                "has_multiple_tiers": False,
                "meeting_address": "Sultanahmet Square, near the German Fountain",
                "meeting_instructions": "Meet your guide at Sultanahmet Square in front of the German Fountain. Look for the guide with a red Turkish flag.",
                "highlights": [
                    "Visit three UNESCO World Heritage sites",
                    "Skip the lines at Topkapi Palace",
                    "Expert guide bringing history to life",
                    "See Hagia Sophia's Byzantine mosaics and architecture",
                    "Marvel at Blue Mosque's Iznik tiles",
                    "Explore Topkapi Palace including Harem"
                ],
                "includes": [
                    ("Expert guide", True),
                    ("Hagia Sophia entrance", True),
                    ("Blue Mosque guided tour", True),
                    ("Skip-the-line Topkapi Palace ticket including Harem", True),
                    ("Headsets for larger groups", True),
                    ("Transportation", False),
                    ("Food and drinks", False)
                ],
                "timelines": [
                    ("Hagia Sophia", "Begin at the magnificent Hagia Sophia. Explore this architectural marvel that served as a church, mosque, museum, and mosque again. See Byzantine mosaics and massive dome.", 75, None),
                    ("Blue Mosque", "Walk to the Blue Mosque (Sultan Ahmed Mosque). Admire the six minarets and interior decorated with over 20,000 handmade Iznik tiles. Learn about Islamic architecture.", 60, None),
                    ("Lunch Break", "Free time for lunch at your own expense in the Sultanahmet area. Your guide provides recommendations.", 45, None),
                    ("Topkapi Palace", "Skip the lines at Topkapi Palace, former residence of Ottoman sultans. Explore the palace courtyards, treasury with priceless artifacts, and the Harem quarters.", 90, None),
                    ("Tour Conclusion", "End the tour with views of the Bosphorus from the palace gardens. Receive recommendations for further exploration.", 10, None)
                ],
                "time_slots": [
                    ("09:00", "Morning", 15, Decimal("0.00")),
                    ("13:00", "Afternoon", 15, Decimal("0.00"))
                ],
                "pricing_tiers": [
                    ("Standard", "Small group tour with skip-the-line palace access", Decimal("75.00"), Decimal("60.00"), 0)
                ],
                "add_ons": [
                    ("Basilica Cistern", "Add entry to the ancient underground Basilica Cistern", Decimal("12.00")),
                    ("Turkish lunch", "Add traditional Turkish lunch at a local restaurant", Decimal("18.00")),
                    ("Grand Bazaar extension", "Extend your tour with a guided visit to the Grand Bazaar", Decimal("25.00"))
                ]
            }
        ]

        print(f"\nCreating {len(activities_data)} comprehensive activities...")

        # Create activities with all enhanced fields
        for idx, data in enumerate(activities_data, 1):
            vendor = vendor_profiles[data["vendor"]]
            category = categories[data["category"]]
            destination = destinations[data["destination"]]

            # Create activity
            activity = Activity(
                vendor_id=vendor.id,
                title=data["title"],
                slug=slugify(data["title"]),
                description=data["description"],
                short_description=data["short_description"],
                price_adult=data["price_adult"],
                price_child=data["price_child"],
                original_price_adult=data.get("original_price_adult"),
                discount_percentage=data.get("discount_percentage"),
                duration_minutes=data["duration"],
                max_group_size=data["max_group_size"],
                instant_confirmation=True,
                free_cancellation_hours=24,
                languages=data["languages"],
                is_bestseller=data.get("is_bestseller", False),
                is_skip_the_line=data.get("is_skip_the_line", False),
                is_likely_to_sell_out=data.get("is_likely_to_sell_out", False),
                has_mobile_ticket=data.get("has_mobile_ticket", True),
                has_best_price_guarantee=data.get("has_best_price_guarantee", False),
                is_verified_activity=data.get("is_verified_activity", True),
                is_wheelchair_accessible=data.get("is_wheelchair_accessible", False),
                is_stroller_accessible=data.get("is_stroller_accessible", False),
                allows_service_animals=data.get("allows_service_animals", False),
                has_infant_seats=data.get("has_infant_seats", False),
                video_url=data.get("video_url"),
                dress_code=data.get("dress_code"),
                weather_dependent=data.get("weather_dependent", False),
                not_suitable_for=data.get("not_suitable_for"),
                what_to_bring=data.get("what_to_bring"),
                has_covid_measures=data.get("has_covid_measures", False),
                covid_measures=data.get("covid_measures"),
                is_giftable=data.get("is_giftable", True),
                allows_reserve_now_pay_later=data.get("allows_reserve_now_pay_later", False),
                has_multiple_tiers=data.get("has_multiple_tiers", False),
                average_rating=round(random.uniform(4.5, 5.0), 1),
                total_reviews=random.randint(50, 800),
                total_bookings=random.randint(200, 2000)
            )
            db.add(activity)
            db.flush()

            # Add images
            for i in range(5):
                image = ActivityImage(
                    activity_id=activity.id,
                    url=f"https://picsum.photos/seed/{activity.slug}-{i}/800/600",
                    is_primary=(i == 0),
                    is_hero=(i == 0),
                    order_index=i
                )
                db.add(image)

            # Add category
            activity_category = ActivityCategory(
                activity_id=activity.id,
                category_id=category.id
            )
            db.add(activity_category)

            # Add destination
            activity_destination = ActivityDestination(
                activity_id=activity.id,
                destination_id=destination.id
            )
            db.add(activity_destination)

            # Add highlights
            for i, highlight_text in enumerate(data["highlights"]):
                highlight = ActivityHighlight(
                    activity_id=activity.id,
                    text=highlight_text,
                    order_index=i
                )
                db.add(highlight)

            # Add includes
            for i, (item, is_included) in enumerate(data["includes"]):
                include = ActivityInclude(
                    activity_id=activity.id,
                    item=item,
                    is_included=is_included,
                    order_index=i
                )
                db.add(include)

            # Add meeting point
            meeting_point = MeetingPoint(
                activity_id=activity.id,
                address=data["meeting_address"],
                instructions=data["meeting_instructions"],
                latitude=destination.latitude + random.uniform(-0.01, 0.01),
                longitude=destination.longitude + random.uniform(-0.01, 0.01)
            )
            db.add(meeting_point)
            db.flush()

            # Add meeting point photos
            for i in range(3):
                photo = MeetingPointPhoto(
                    meeting_point_id=meeting_point.id,
                    url=f"https://picsum.photos/seed/{activity.slug}-meeting-{i}/400/300",
                    caption=f"Meeting point view {i+1}",
                    order_index=i
                )
                db.add(photo)

            # Add timelines
            for i, (title, description, duration, image) in enumerate(data["timelines"]):
                timeline = ActivityTimeline(
                    activity_id=activity.id,
                    step_number=i + 1,
                    title=title,
                    description=description,
                    duration_minutes=duration,
                    image_url=image,
                    order_index=i
                )
                db.add(timeline)

            # Add time slots
            for i, (slot_time, label, capacity, price_adj) in enumerate(data["time_slots"]):
                time_slot = ActivityTimeSlot(
                    activity_id=activity.id,
                    slot_time=slot_time,
                    slot_label=label,
                    max_capacity=capacity,
                    is_available=True,
                    price_adjustment=price_adj
                )
                db.add(time_slot)

            # Add pricing tiers
            if "pricing_tiers" in data:
                for tier_name, tier_desc, price_adult, price_child, order in data["pricing_tiers"]:
                    tier = ActivityPricingTier(
                        activity_id=activity.id,
                        tier_name=tier_name,
                        tier_description=tier_desc,
                        price_adult=price_adult,
                        price_child=price_child,
                        order_index=order,
                        is_active=True
                    )
                    db.add(tier)

            # Add add-ons
            if "add_ons" in data:
                for j, addon_data in enumerate(data["add_ons"]):
                    addon = ActivityAddOn(
                        activity_id=activity.id,
                        name=addon_data[0],
                        description=addon_data[1],
                        price=addon_data[2],
                        is_optional=True,
                        order_index=j
                    )
                    db.add(addon)

            # Add reviews
            num_reviews = random.randint(7, 12)
            for _ in range(num_reviews):
                reviewer = random.choice(customers)
                rating = random.choice([4, 4, 5, 5, 5])  # Mostly 4-5 stars

                review_titles = [
                    "Amazing experience!",
                    "Highly recommended",
                    "Great tour",
                    "Fantastic guide",
                    "Wonderful day",
                    "Exceeded expectations",
                    "Must do activity",
                    "Unforgettable",
                    "Well organized",
                    "Perfect experience"
                ]

                review_comments = [
                    "This was one of the highlights of our trip. The guide was knowledgeable and friendly. Everything was well-organized and we learned so much. Would definitely recommend to anyone visiting!",
                    "Excellent tour! Our guide was amazing and really brought the history to life. The skip-the-line access was worth it - we saved so much time. Great value for money.",
                    "Really enjoyed this experience. The group size was perfect and the guide took time to answer all our questions. The locations were stunning and we got some great photos.",
                    "We had a wonderful time on this tour. Very well planned and executed. The guide was professional and entertaining. Highly recommend booking this in advance!",
                    "Great experience overall. The timing was perfect and we never felt rushed. Our guide was passionate about sharing the history and culture. Worth every penny!",
                    "This tour exceeded our expectations. The guide was incredibly knowledgeable and the small group size made it feel personalized. Definitely a must-do!",
                    "Fantastic day out! Everything ran smoothly from start to finish. The guide was engaging and informative. We learned so much and had a great time.",
                    "Absolutely loved this tour. The skip-the-line feature was a huge plus. Our guide was friendly and accommodating. Would do it again in a heartbeat!",
                    "One of the best tours we've taken. The itinerary was well-paced and covered all the highlights. Our guide was excellent and made the experience memorable.",
                    "Highly recommended! The tour was informative, fun, and well worth the price. Our guide was professional and clearly loved what they do."
                ]

                review = Review(
                    user_id=reviewer.id,
                    activity_id=activity.id,
                    vendor_id=vendor.id,
                    rating=rating,
                    title=random.choice(review_titles),
                    comment=random.choice(review_comments),
                    is_verified_booking=True,
                    helpful_count=random.randint(0, 50),
                    created_at=datetime.now() - timedelta(days=random.randint(1, 365))
                )
                db.add(review)
                db.flush()

                # Add review category ratings
                categories_to_rate = [
                    "Value for money",
                    "Guide quality",
                    "Service",
                    "Organization"
                ]

                for cat_name in categories_to_rate:
                    cat_rating = rating + random.choice([-1, 0, 0, 0, 1])  # Slight variation
                    cat_rating = max(1, min(5, cat_rating))  # Clamp between 1-5

                    review_category = ReviewCategory(
                        review_id=review.id,
                        category_name=cat_name,
                        rating=cat_rating
                    )
                    db.add(review_category)

                # Occasionally add review images
                if random.random() < 0.3:  # 30% chance
                    for img_idx in range(random.randint(1, 3)):
                        review_image = ReviewImage(
                            review_id=review.id,
                            url=f"https://picsum.photos/seed/{activity.slug}-review-{review.id}-{img_idx}/400/300",
                            caption=f"Photo from {reviewer.full_name}"
                        )
                        db.add(review_image)

            print(f"Created activity {idx}/{len(activities_data)}: {data['title']}")

        db.commit()
        print("\n" + "="*80)
        print("Enhanced demo data created successfully!")
        print("="*80)
        print(f"- 1 Admin user (admin@getyourguide.com / admin123)")
        print(f"- {len(customers)} Customers (customer@example.com and customer2-9@example.com / customer123)")
        print(f"- {len(vendor_profiles)} Vendors (vendor1-5@example.com / vendor123)")
        print(f"- {len(categories)} Categories")
        print(f"- {len(destinations)} Destinations")
        print(f"- {len(activities_data)} Enhanced Activities with:")
        print(f"  - Activity timelines (4-6 steps each)")
        print(f"  - Time slots (3-5 per activity)")
        print(f"  - Pricing tiers (2-3 per activity)")
        print(f"  - Add-ons (3-5 per activity)")
        print(f"  - Meeting point photos (3 per activity)")
        print(f"  - Reviews with category ratings (7-12 per activity)")
        print("="*80)

    except Exception as e:
        print(f"Error creating demo data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_enhanced_db()
