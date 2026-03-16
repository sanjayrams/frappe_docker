# Force-update any rogue leads trapped in the 'Working' state
import frappe

rogue_leads = frappe.db.sql("""
    SELECT name FROM `tabNT Lead` WHERE status = 'Working'
""", as_dict=True)

if rogue_leads:
    print(f"🧹 Purging 'Working' status from {len(rogue_leads)} leads...")
    frappe.db.sql("""
        UPDATE `tabNT Lead` 
        SET status = 'Contacted' 
        WHERE status = 'Working'
    """)
    frappe.db.commit()
    print("✅ Database Purge Complete.")
else:
    print("✅ No rogue leads found in database.")

