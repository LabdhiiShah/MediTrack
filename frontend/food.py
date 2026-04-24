from tkinter import *
from scrollable import scrollablefunc
from config import BG, CARD, ACCENT, TEXT_DARK, TEXT_MED, F, FM
from frontend.sidebar import create_sidebar

from backend.db import getConnection
from frontend import session

# Dictionary mapping tags to food advice
DIET_GUIDE = {
    "antibiotic": {
        "eat": ["Probiotic yogurt", "Fermented foods (kimchi)", "High-fiber vegetables", "Garlic", "Ginger"],
        "avoid": ["Alcohol", "Grapefruit juice", "Calcium-fortified juice", "Excessive sugar"]
    },
    "analgesic": {
        "eat": ["Take with milk/meal", "Ginger tea", "Turmeric", "Stay hydrated"],
        "avoid": ["Alcohol (Dangerous)", "Excessive Caffeine", "Spicy foods", "Empty stomach"]
    },
    "antacid": {
        "eat": ["Oatmeal", "Bananas", "Melons", "Ginger", "Nonfat milk", "Alkaline vegetables"],
        "avoid": ["Spicy food", "Fried/Fatty foods", "Citrus fruits", "Chocolate", "Carbonated drinks"]
    },
    "antihistamine": {
        "eat": ["Water (for dry mouth)", "Onions", "Apples"],
        "avoid": ["Alcohol (Increases drowsiness)", "Fruit juices (Apple/Orange) near dose time"]
    },
    "antipyretic": {
        "eat": ["Clear soups", "Easily digestible fruits", "Coconut water"],
        "avoid": ["Heavy/Oily meals", "High-sugar desserts", "Spicy food"]
    },
    "anti_inflammatory": {
        "eat": ["Fatty fish (Salmon)", "Olive oil", "Walnuts", "Berries", "Leafy greens"],
        "avoid": ["Processed snacks", "Excessive Salt", "Refined sugar"]
    },
    "bronchodilator": {
        "eat": ["Magnesium-rich foods (spinach)", "Warm herbal teas"],
        "avoid": ["Sulfites (dried fruits)", "Gas-producing foods (beans, cabbage)", "Caffeine"]
    },
    "sedative": {
        "eat": ["Light snacks", "Chamomile tea"],
        "avoid": ["ALCOHOL (Fatal Interaction)", "Grapefruit juice", "Caffeine"]
    },
    "anticoagulant": {
        "eat": ["Consistent Vitamin K intake", "Plenty of water"],
        "avoid": ["Cranberry juice", "Alcohol", "Sudden changes in Spinach/Kale intake"]
    },
    "antiparasitic": {
        "eat": ["Fatty meals (improves absorption)", "Whole milk", "Eggs"],
        "avoid": ["Alcohol", "Raw/Undercooked meat", "Unwashed vegetables"]
    },
    "general": {
        "eat": ["Balanced diet", "Seasonal fruits", "Lean protein", "8 glasses of water"],
        "avoid": ["Highly processed junk food", "Excessive sugar", "Very salty snacks"]
    }
}

def foodpage(parent, controller):
    frame = Frame(parent, bg=BG)
    container = Frame(frame, bg=BG)
    container.pack(fill="both", expand=True)

    sidebar = create_sidebar(container, controller, "Food & Diet")
    frame.sidebar = sidebar

    main_content = Frame(container, bg=BG)
    main_content.pack(side="left", fill="both", expand=True)

    scroll_container = Frame(main_content, bg=BG)
    scroll_container.pack(fill="both", expand=True)
    
    Label(scroll_container, text="Food & Diet", bg=BG, font=F(20, "bold"),
          fg=TEXT_DARK, anchor="w").pack(fill="x", padx=20, pady=(20, 4))
    Label(scroll_container, text="Personalized nutrition based on your current prescriptions",
          bg=BG, font=F(12), fg=TEXT_MED, anchor="w").pack(fill="x", padx=20)
    
    # This is where the dynamic cards will go
    display_area = scrollablefunc(scroll_container, BG)

    def refresh():
        for widget in display_area.winfo_children():
            widget.destroy()

        try:
            conn = getConnection()
            cursor = conn.cursor(dictionary=True)

            # Step 1: Get current medicines
            cursor.execute("""
                SELECT medicine_name FROM medicines
                WHERE patient_id = %s AND status = 'current'
            """, (session.patientid,))
            meds = cursor.fetchall()

            if not meds:
                Label(display_area, text="No current medicines found.\nAdd medicines to see dietary advice.",
                    font=FM(11), bg=BG, fg=TEXT_MED, pady=40).pack()
                return

            shown = 0
            for med in meds:
                med_name = med['medicine_name'].strip()

                # Get primary_tag via medlookup → med_data
                
                cursor.execute("""
                    SELECT generic_name FROM medlookup
                    WHERE LOWER(input_name) = LOWER(%s)
                    LIMIT 1
                """, (med_name,))
                lookup = cursor.fetchone()

                tag = "general"
                if lookup:
                    generic = lookup['generic_name'].strip()
                    cursor.execute("""
                        SELECT primary_tag FROM med_data
                        WHERE LOWER(medicine_name) LIKE LOWER(%s)
                        OR LOWER(salt_composition) LIKE LOWER(%s)
                        LIMIT 1
                    """, (f"%{generic}%", f"%{generic}%"))
                    med_info = cursor.fetchone()
                    if med_info and med_info['primary_tag']:
                        tag = med_info['primary_tag'].lower().strip()

                advice = DIET_GUIDE.get(tag, DIET_GUIDE["general"])

                card = Frame(display_area, bg=CARD, padx=20, pady=15,
                            highlightthickness=1, highlightbackground="#EEE")
                card.pack(fill="x", padx=20, pady=10)

                Label(card, text=med_name, font=FM(12, "bold"),
                    bg=CARD, fg=ACCENT).pack(anchor="w")
                Label(card, text=f"Category: {tag}", font=FM(9),
                    bg=CARD, fg=TEXT_MED).pack(anchor="w")

                Label(card, text="✔ RECOMMENDED DIET", font=FM(9, "bold"),
                    fg="#27AE60", bg=CARD).pack(anchor="w", pady=(10, 2))
                Label(card, text=" • " + "\n • ".join(advice['eat']),
                    font=FM(10), fg=TEXT_DARK, bg=CARD, justify="left").pack(anchor="w")

                Label(card, text="✘ SUGGESTED TO AVOID", font=FM(9, "bold"),
                    fg="#E74C3C", bg=CARD).pack(anchor="w", pady=(10, 2))
                Label(card, text=" • " + "\n • ".join(advice['avoid']),
                    font=FM(10), fg=TEXT_DARK, bg=CARD, justify="left").pack(anchor="w")

                shown += 1

            if shown == 0:
                Label(display_area,
                    text="Medicines found but no dietary data available.",
                    font=FM(11), bg=BG, fg=TEXT_MED, pady=40).pack()

        except Exception as e:
            print(f"Food Page Error: {e}")
        finally:
            cursor.close()
            conn.close()

    frame.refresh = refresh
    return frame