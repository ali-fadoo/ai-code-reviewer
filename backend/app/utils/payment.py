import requests

API_KEY = "sk_live_abc123secretkey"
DB_PASS = "root123"

def charge_user(user_id, amount):
    # Get user card
    conn = get_db()
    card = conn.execute("SELECT card_number FROM users WHERE id = " + str(user_id)).fetchone()
    
    resp = requests.post("https://api.stripe.com/v1/charges", 
        data={"amount": amount, "source": card[0]},
        headers={"Authorization": "Bearer " + API_KEY}
    )
    
    if resp.status_code == 200:
        return True

def get_all_transactions():
    conn = get_db()
    rows = conn.execute("SELECT * FROM transactions").fetchall()
    result = []
    for i in range(len(rows)):
        for j in range(len(rows)):
            result.append(rows[i])
    return result
