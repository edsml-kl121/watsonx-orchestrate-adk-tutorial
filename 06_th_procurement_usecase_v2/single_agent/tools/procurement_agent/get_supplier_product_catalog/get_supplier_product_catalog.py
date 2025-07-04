from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_supplier_product_catalog() -> str:
    """
    Retrieve all supplier product catalog information as a CSV-formatted string.

    This includes fields like supplier ID, supplier name, product ID, product name, unit price, and quality score.
    Useful for procurement workflows, supplier comparison, product sourcing, and quality analysis.

    :returns: A CSV-formatted string with all supplier product catalog records.
    """
    try:
        return """Supplier ID,Supplier Name,Product ID,Product Name,Unit Price (THB),Quality Score
SUP-001,บริษัท พรีเมียมออโต้พาร์ท จำกัด,P001,Michelin XM2,"3,500",97
SUP-001,บริษัท พรีเมียมออโต้พาร์ท จำกัด,P015,Michelin Primacy 4,"4,000",94
SUP-001,บริษัท พรีเมียมออโต้พาร์ท จำกัด,P016,Michelin Pilot Sport 4,"4,200",96
SUP-003,บริษัท เบสท์ไทร์ อินเตอร์เนชันแนล,P007,Bridgestone Ecopia,"3,200",90
SUP-003,บริษัท เบสท์ไทร์ อินเตอร์เนชันแนล,P008,Goodyear EfficientGrip,"3,000",88
SUP-003,บริษัท เบสท์ไทร์ อินเตอร์เนชันแนล,P009,Continental ComfortContact,"3,100",89
SUP-003,บริษัท เบสท์ไทร์ อินเตอร์เนชันแนล,P017,Dunlop SP Sport LM705,"2,900",85
SUP-003,บริษัท เบสท์ไทร์ อินเตอร์เนชันแนล,P018,Hankook Ventus Prime 3,"2,850",86
SUP-006,บริษัท ไทยออโต้ซัพพลาย จำกัด,P012,Deestone Premium Tires,"2,800",84
SUP-006,บริษัท ไทยออโต้ซัพพลาย จำกัด,P019,Otani KC2000,"2,700",82
SUP-006,บริษัท ไทยออโต้ซัพพลาย จำกัด,P020,Maxxis Victra MA-Z3,"2,900",83
SUP-007,บริษัท ยูโรพาร์ทส์แอนด์แอคเซสซอรี่,P013,Pirelli P-Zero,"3,900",90
SUP-007,บริษัท ยูโรพาร์ทส์แอนด์แอคเซสซอรี่,P021,Continental UltraContact,"3,700",91
SUP-007,บริษัท ยูโรพาร์ทส์แอนด์แอคเซสซอรี่,P022,Michelin Latitude Sport,"4,100",93"""
    except Exception as e:
        return f"❌ An error occurred while retrieving supplier product catalog data: {str(e)}"