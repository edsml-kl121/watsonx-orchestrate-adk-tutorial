from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_procurement_supplier_list() -> str:
    """
    Retrieve all procurement supplier information as a CSV-formatted string.

    This includes fields like supplier ID, name, product category, contact information, location, and rating.
    Useful for procurement workflows or supplier comparison and selection.

    :returns: A CSV-formatted string with all procurement supplier records.
    """
    try:
        return """Supplier ID,Supplier Name,Product Category,Contact Name,Contact Email,Phone Number,Location (Province),Rating (1–5)
SUP-001,บริษัท พรีเมียมออโต้พาร์ท จำกัด,"ยางรถยนต์, แบตเตอรี่",นายชาญชัย สุขใจ,chanchai@premiumauto.co.th,02-123-4567,กรุงเทพมหานคร,4.7
SUP-002,บริษัท โกลบอลเพ้นท์ ออโต้ จำกัด,สีรถยนต์,น.ส.วิภา วงศ์ทอง,wipa@globalpaint.co.th,02-234-6789,สมุทรปราการ,4.5
SUP-003,บริษัท เบสท์ไทร์ อินเตอร์เนชันแนล,ยางรถยนต์,นายคมกริช รุ่งเรือง,komkrit@besttire.co.th,038-987-6543,ชลบุรี,4.3
SUP-004,บริษัท ซูพีเรียแบตเตอรี่ จำกัด,แบตเตอรี่,น.ส.สุภาพร มีธรรม,supaporn@superiorbattery.co.th,053-123-7890,เชียงใหม่,4.6
SUP-005,บริษัท พรีซิชันเพ้นท์ จำกัด,สีรถยนต์,นายวรวุฒิ อินทรชัย,worawut@precisionpaint.co.th,043-567-1234,ขอนแก่น,4.8
SUP-006,บริษัท ไทยออโต้ซัพพลาย จำกัด,"ยางรถยนต์, แบตเตอรี่, สีรถยนค์",นายนัฐวุฒิ เล็กดี,nattawut@thaiautosupply.co.th,02-998-8877,นนทบุรี,4.4
SUP-007,บริษัท ยูโรพาร์ทส์แอนด์แอคเซสซอรี่,"ยางรถยนต์, แบตเตอรี่",นายลูคัส รอสโซ่,lucas@europarts.co.th,076-665-5566,ภูเก็ต,4.2
SUP-008,บริษัท คัลเลอร์แมทช์ ออโต้ จำกัด,สีรถยนต์,น.ส.มิเชล ดูบัวส์,michelle@colormatch.co.th,074-321-1234,สงขลา,4.6"""
    except Exception as e:
        return f"❌ An error occurred while retrieving procurement supplier data: {str(e)}"