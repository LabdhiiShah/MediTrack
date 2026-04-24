from backend.db import getConnection
from backend.engine import score_all


def analyze_interactions(patient_id):
    if not patient_id:
        return {"interactions": [], "total_medicines": 0, "patient": {}}

    conn = getConnection()
    cursor = conn.cursor(dictionary=True)

    try:
        # get patient name
        cursor.execute(
            "SELECT username FROM patientinfo WHERE id = %s", (patient_id,)
        )
        name = cursor.fetchone()
        patient_name = name['username'] if name else "Patient"

        # Get current medicines for this patient
        cursor.execute("""
            SELECT medicine_name
            FROM   medicines
            WHERE  patient_id = %s AND status = 'current'
        """, (patient_id,))
        db_meds = cursor.fetchall()
        # print(f"DEBUG: Found {len(db_meds)} medicines for patient")

        # clean medicine names for gui
        enriched_list = []

        for m in db_meds:
            med_name = m['medicine_name'].strip()
            # print(f"\nDEBUG: Processing '{med_name}'")

            # in med lookup table find medicine
            # converts brand name to generic
            cursor.execute("""
                SELECT input_name, generic_name
                FROM   medlookup
                WHERE  LOWER(input_name) = LOWER(%s)
                LIMIT  1
            """, (med_name,))
            lookup = cursor.fetchone()

            if not lookup:
                cursor.execute("""
                    SELECT input_name, generic_name
                    FROM   medlookup
                    WHERE  LOWER(input_name) LIKE LOWER(%s)
                       OR  LOWER(%s) LIKE LOWER(CONCAT('%', input_name, '%'))
                    LIMIT  1
                """, (f"%{med_name}%", med_name))
                lookup = cursor.fetchone()

            generic = lookup['generic_name'].strip() if lookup else None
            # print(f"DEBUG: medlookup → generic='{generic}'")

            # get medicine data factors (salt and tags)
            salt = ""
            tags = ""

            if generic:
                # try matching generic_name inside salt_composition or medicine_name
                cursor.execute("""
                    SELECT salt_composition, tags
                    FROM   med_data
                    WHERE  LOWER(medicine_name) LIKE LOWER(%s)
                       OR  LOWER(salt_composition) LIKE LOWER(%s)
                    LIMIT  1
                """, (f"%{generic}%", f"%{generic}%"))
                med_info = cursor.fetchone()

                if med_info:
                    salt = med_info['salt_composition'] or ""
                    tags = med_info['tags'] or ""
                    print(f"DEBUG: med_data → salt='{salt[:60]}' tags='{tags}'")
                else:
                    print(f"DEBUG: med_data → no match for generic '{generic}'")

            # even if no salt/tags found, include the medicine so pair
            # combinations still work for medlookup-based interactions
            if salt or tags or generic:
                enriched_list.append({
                    "name":    med_name,
                    "generic": generic or med_name.lower(),
                    "salt":    salt,
                    "tags":    tags,
                })
            # else:
            #     print(f"DEBUG: Skipping '{med_name}' — no data found in either table")
        
        # print(f"\nDEBUG: Enriched {len(enriched_list)} medicines total")
        # ready to send to gui
        return {
            "patient":          {"name": patient_name},
            "total_medicines":  len(enriched_list),
            "interactions":     score_all(enriched_list),
        }

    except Exception as e:
        # print(f"[risk_logic] Error: {e}")
        return {"interactions": [], "total_medicines": 0, "patient": {}}
    finally:
        cursor.close()
        conn.close()