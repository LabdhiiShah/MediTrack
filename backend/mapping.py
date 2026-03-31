import requests
from tkinter import messagebox
from backend.db import getConnection

def fda(medname):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{medname}&limit=1"
    try:
        response = requests.get(url, timeout=4)
        if response.status_code == 200:
            data = response.json()
            
            # Use .get() to avoid error if data not found
            results = data.get('results', [])
            if results:
                openfda = results[0].get('openfda', {})
                generic_list = openfda.get('generic_name', [])
                
                if generic_list:
                    return generic_list[0].lower()
        
        # If any of the above are missing, return None gracefully
    except Exception as e:
        print(f"Error during API call: {e}")
    
    return None

def medicine_name_mapping(medname):
    name = medname.strip()

    try:
        conn = getConnection()
        cursor = conn.cursor(dictionary=True)

        # check if already in db (cache)
        checkquery = "SELECT * FROM medlookup WHERE LOWER(input_name) = LOWER(%s)"
        cursor.execute(checkquery, (name, ))
        cache = cursor.fetchone()

        # if name matches then see if it's already a medicine or a brand
        if cache:
            # if it's brand name (bool = 1) map it to generic name
            if cache['is_brand'] and cache['generic_name'].lower() != name.lower():                                
                return f"{cache['generic_name'].title()} ({name.title()})"
            # else continue
            else:
                return name.title()
            
        # call api vala function
        generic_name_raw = fda(name)

        if generic_name_raw:
            user_input = name.lower().strip()
            generic_name = generic_name_raw.lower().strip()

            if user_input in generic_name or generic_name in user_input:
                final_generic = user_input
                is_brand = 0
            else:
                final_generic = generic_name
                is_brand = 1

        else:
            final_generic = name.lower()
            is_brand = 0

        insertquery = """
        INSERT INTO medlookup (input_name, generic_name, is_brand)
        VALUES(%s, %s, %s)
        """

        cursor.execute(insertquery, (name, final_generic, is_brand))
        conn.commit()

        if is_brand:
            return f"{final_generic.title()} ({name.title()})"
        return name.title()

    except Exception as e:
        messagebox.showerror("Database error",e)

    finally:
        cursor.close()
        conn.close()

    pass

'''

Future Scope:
Did you mean? for medicines while patient types

'''