from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_procurement_transaction_history() -> str:
    """
    Retrieve mock procurement transaction history as a CSV-formatted string.

    This includes product purchases before, during, and after March 2025.

    :returns: A CSV-formatted string with procurement transaction records.
    """
    try:
        return """transaction_id,product_id,product_name,quantity,price_per_unit,total_price,transaction_date
T0001,O79TEE,Men & Shoulder Soap,1,650,650,2025-03-08
T0002,AIT8HJ,Apple,4,120,480,2025-02-18
T0003,U00Y7M,Ramen Noodles,5,150,750,2025-02-21
T0004,EUGJNE,Mango,2,150,300,2025-02-28
T0005,XQVC7F,Rice,1,200,200,2025-02-07
T0006,U3YM36,CA-R-BON,2,250,500,2025-03-21
T0007,84P0M3,Chicken Breast,3,220,660,2025-04-02
T0008,SP53JN,Vegetables,4,130,520,2025-04-04
T0009,NSO16Q,Leather Wallet,1,1990,1990,2025-04-06
T0010,I8SJE2,Butter,2,250,500,2025-02-26
T0011,F5O0XC,Banana,2,90,180,2025-03-19
T0012,H4OLDA,Tomato Sauce,1,180,180,2025-04-11
T0013,ZBT51C,Eucerine Shampoo,1,890,890,2025-02-13
T0014,C3A558,Avocado,2,170,340,2025-02-14
T0015,DFTYQK,Smartphone,1,29990,29990,2025-04-15
T0016,PPQ4OU,Eggs,1,90,90,2025-03-29
T0017,63ITC3,Strawberries,1,180,180,2025-04-01
T0018,ENT9NY,Eucerine Body Lotion,2,1200,2400,2025-02-05
T0019,F5O0XC,Banana,1,90,90,2025-04-03
T0020,BEFVVH,LED Desk Lamp,1,1299,1299,2025-02-03
T0021,3Z7ZRB,Digital Watch,1,7500,7500,2025-02-28
T0022,XQVC7F,Rice,3,200,600,2025-03-06
T0023,NSO16Q,Leather Wallet,1,1990,1990,2025-04-09
T0024,A5Q71L,Cheese,2,300,600,2025-02-17
T0025,6RGN4U,Orange,3,110,330,2025-02-20
T0026,ZBT51C,Eucerine Shampoo,1,890,890,2025-03-26
T0027,O79TEE,Men & Shoulder Soap,1,650,650,2025-04-07
T0028,SP53JN,Vegetables,2,130,260,2025-02-22
T0029,ZBT51C,Eucerine Shampoo,1,890,890,2025-03-26
T0030,63ITC3,Strawberries,3,180,540,2025-03-20"""
    except Exception as e:
        return f"❌ An error occurred while retrieving transaction history: {str(e)}"