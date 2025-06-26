from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_procurement_product_list() -> str:
    """
    Retrieve all procurement product information as a CSV-formatted string.

    This includes fields like product ID, name, description, price, stock availability per store, and promotion.
    Useful for procurement workflows or product comparison.

    :returns: A CSV-formatted string with all procurement product records.
    """
    try:
        return """id,Product Name,Description,Price (THB),Stock Availability,Promotion
BEFVVH,LED Desk Lamp,Energy-efficient lighting with adjustable brightness.,1299,"Selfridges: 50000000, Central World: 30000000, Paragon: 20000000, The Mall Bangkapi: 40000000","Buy 1 Get 1 Free"
XM9OMF,Gaming Laptop,High-performance laptop for gaming and work.,49999,"Selfridges: 20000000, Central World: 10000000, Paragon: 10000000","Free gaming mouse with purchase"
NSO16Q,Leather Wallet,Premium leather with multiple compartments.,1990,"Central World: 50000000, Paragon: 30000000, The Mall Bangkapi: 20000000","10% off for members"
4YAHI8,Electric Kettle,Fast boiling with auto shut-off safety feature.,890,"Selfridges: 40000000, Paragon: 30000000","Free tea sample included"
NHX15H,Office Chair,Ergonomic design for maximum comfort.,5990,"Selfridges: 30000000, Central World: 20000000, Paragon: 10000000","20% off this month"
39UB6H,Running Shoes,"Lightweight and durable, perfect for jogging.",3200,"Selfridges: 60000000, Central World: 40000000, Paragon: 20000000","Buy 2 pairs, get 15% off"
RZ7KO9,Noise-Canceling Headphones,High-quality audio with active noise cancellation.,8990,"Selfridges: 50000000, Central World: 30000000","Free carrying case included"
DFTYQK,Smartphone,Latest model with advanced features.,29990,"Selfridges: 40000000, Central World: 20000000, Paragon: 20000000","Free screen protector"
0XBJ9O,Bluetooth Speaker,Portable and wireless with excellent sound quality.,3990,"Selfridges: 50000000, Central World: 30000000, Paragon: 30000000","10% off for first-time buyers"
3Z7ZRB,Digital Watch,Stylish design with multiple smart functions.,7500,"Selfridges: 20000000, Central World: 30000000, Paragon: 10000000","5% cashback"
U00Y7M,Ramen Noodles,High-quality noodles for making ramen.,150,"Selfridges: 100000000, Central World: 70000000, Paragon: 50000000","Buy 3, get 1 free"
FHNUIM,Pork Belly,"Sliced pork belly, ideal for ramen toppings.",300,"Selfridges: 80000000, Central World: 50000000","15% off on weekends"
P5DTNY,Green Onions,Freshly chopped green onions for garnishing.,50,"Selfridges: 120000000, Central World: 60000000","Free with purchase over 500 THB"
0T9CLI,Soy Sauce,Rich and savory soy sauce for ramen broth.,120,"Selfridges: 50000000, Central World: 40000000","Buy 1 Get 1 at 50% off"
PPQ4OU,Eggs,Perfect for soft-boiled ramen eggs.,90,"Selfridges: 120000000, Central World: 80000000","5% off for bulk purchases"
XQVC7F,Rice,"Steamed rice, a base for omurice.",200,"Selfridges: 100000000, Central World: 50000000","10% off for members"
84P0M3,Chicken Breast,Diced chicken breast for stir-frying.,220,"Selfridges: 70000000, Central World: 40000000","Buy 2, get 1 free"
H4OLDA,Tomato Sauce,Tangy tomato sauce for omurice flavor.,180,"Selfridges: 50000000, Central World: 30000000","5% off for students"
SP53JN,Vegetables,Mixed vegetables for stir-frying.,130,"Selfridges: 100000000, Central World: 50000000","15% off"
I8SJE2,Butter,Adds a rich flavor to the omelet.,250,"Selfridges: 60000000, Central World: 40000000","Buy 2, get 1 free"
A5Q71L,Cheese,Melted cheese for topping the omurice.,300,"Selfridges: 50000000, Central World: 30000000","Free sample included"
AIT8HJ,Apple,"Fresh and crisp, sourced locally.",120,"Selfridges: 100000000, Central World: 60000000","20% off seasonal sale"
F5O0XC,Banana,"Rich in potassium, perfect for a quick snack.",90,"Selfridges: 120000000, Central World: 80000000","Buy 1, get 1 at 50% off"
6RGN4U,Orange,"Juicy and sweet, packed with vitamin C.",110,"Selfridges: 80000000, Central World: 60000000","Free gift for purchases over 500 THB"
EUGJNE,Mango,"Ripe and delicious, perfect for smoothies.",150,"Selfridges: 70000000, Central World: 50000000","Free mango recipe booklet"
63ITC3,Strawberries,"Sweet and tangy, ideal for desserts.",180,"Selfridges: 60000000, Central World: 40000000","10% off bulk purchase"
C3A558,Avocado,"Creamy texture, great for salads.",170,"Selfridges: 50000000, Central World: 30000000","Free avocado cutter"
ENT9NY,Eucerine Body Lotion,Spotless brightening body lotion.,1200,"Selfridges: 60000000, Central World: 40000000, Paragon: 30000000","25% off for loyalty members"
U3YM36,CA-R-BON,ยาถ่านแก้ท้องเสีย (antidiarrheal) 10 capsules.,250,"Selfridges: 100000000, Central World: 60000000","Buy 2, get 1 free"
ZBT51C,Eucerine Shampoo,Gentle cleansing for scalp health.,890,"Selfridges: 50000000, Central World: 30000000, Paragon: 20000000","Buy 1, get a free travel-size bottle"
O79TEE,Men & Shoulder Soap,Deep cleansing for men’s skin.,650,"Selfridges: 40000000, Central World: 30000000, Paragon: 10000000","Free exfoliating scrub with purchase"
"""
    except Exception as e:
        return f"❌ An error occurred while retrieving procurement product data: {str(e)}"