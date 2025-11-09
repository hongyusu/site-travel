#!/usr/bin/env python3
"""Add discount data to activities for testing discount functionality."""

import os
import sys
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
from app.config import settings

def main():
    """Add discount data to selected activities."""
    engine = create_engine(settings.DATABASE_URL)
    
    # Activities to add discounts to with their discount percentages
    activities_with_discounts = [
        ("sichuan-culinary-masterclass-chengdu", 20),  # 20% discount
        ("shanghai-food-tour-street-food", 15),        # 15% discount
        ("copenhagen-design-academy-workshop", 25),    # 25% discount
        ("stockholm-university-study-tour", 10),       # 10% discount
    ]
    
    print("Adding discount data to activities...")
    
    with engine.connect() as conn:
        for slug, discount in activities_with_discounts:
            # First check if the activity exists
            result = conn.execute(
                text("SELECT id, title, price_adult, price_child FROM activities WHERE slug = :slug"),
                {"slug": slug}
            ).fetchone()
            
            if result:
                activity_id, title, price_adult, price_child = result
                
                # Calculate original prices (current price is discounted)
                original_adult = float(price_adult) / (1 - discount / 100)
                original_child = float(price_child) / (1 - discount / 100)
                
                # Update the activity with discount data
                conn.execute(
                    text("""
                        UPDATE activities 
                        SET 
                            discount_percentage = :discount,
                            original_price_adult = :original_adult,
                            original_price_child = :original_child
                        WHERE id = :activity_id
                    """),
                    {
                        "discount": discount,
                        "original_adult": round(original_adult, 2),
                        "original_child": round(original_child, 2), 
                        "activity_id": activity_id
                    }
                )
                
                print(f"✓ Added {discount}% discount to '{title}'")
                print(f"  Current price: €{price_adult} (Adult), €{price_child} (Child)")
                print(f"  Original price: €{original_adult:.2f} (Adult), €{original_child:.2f} (Child)")
                print()
            else:
                print(f"✗ Activity with slug '{slug}' not found")
        
        # Commit the changes
        conn.commit()
    
    print("Discount data added successfully!")

if __name__ == "__main__":
    main()