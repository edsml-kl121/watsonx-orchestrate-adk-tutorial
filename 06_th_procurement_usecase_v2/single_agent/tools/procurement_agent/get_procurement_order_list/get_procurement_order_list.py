from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_procurement_order_list() -> str:
    """
    Retrieve all procurement order information as a CSV-formatted string.

    This includes fields like order ID, supplier details, date, product information, quantity, pricing, and order status.
    Useful for procurement workflows, order tracking, supplier performance analysis, and purchase history review.

    :returns: A CSV-formatted string with all procurement order records.
    """
    try:
        return """Order ID,Supplier ID,Supplier Name,Date,Product ID,Product Name,Product Type,Quantity,Unit Price (THB),Total Price (THB),Status
ORD-TH100,SUP-001,บริษัท พรีเมียมออโต้พาร์ทจำกัด,1/7/2024,P016,Michelin Pilot Sport 4,ยางรถยนต์,100,4200,420000,Delivered
ORD-TH101,SUP-001,บริษัท พรีเมียมออโต้พาร์ทจำกัด,2/5/2024,P001,Michelin XM2,ยางรถยนต์,200,3500,700000,Delivered
ORD-TH107,SUP-001,บริษัท พรีเมียมออโต้พาร์ทจำกัด,3/28/2024,P001,Michelin XM2,ยางรถยนต์,400,3500,1400000,Delivered
ORD-TH111,SUP-001,บริษัท พรีเมียมออโต้พาร์ทจำกัด,5/21/2024,P015,Michelin Primacy 4,ยางรถยนต์,100,4000,400000,Delivered
ORD-TH114,SUP-001,บริษัท พรีเมียมออโต้พาร์ทจำกัด,2/29/2024,P015,Michelin Primacy 4,ยางรถยนต์,100,4000,400000,Pending
ORD-TH116,SUP-001,บริษัท พรีเมียมออโต้พาร์ทจำกัด,4/4/2024,P015,Michelin Primacy 4,ยางรถยนต์,200,4000,800000,Delivered
ORD-TH117,SUP-001,บริษัท พรีเมียมออโต้พาร์ทจำกัด,6/28/2024,P016,Michelin Pilot Sport 4,ยางรถยนต์,300,4200,1260000,In Transit"""
    except Exception as e:
        return f"❌ An error occurred while retrieving procurement order data: {str(e)}"