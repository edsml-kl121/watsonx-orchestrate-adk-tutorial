from ibm_watsonx_orchestrate.agent_builder.tools import tool


@tool
def get_my_policies(user_query: str = None) -> str:
    """
    Retrieve detailed information about HR policies relevant to employees.

    This includes company leave policies (e.g., earned leave, casual leave, parental leave),
    entitlements, eligibility criteria, request procedures, and disciplinary considerations
    in case of unauthorized absence. The tool may return information in either Thai or English
    depending on the organization's policy documentation.

    :param user_query: Optional. A specific HR policy topic to search for (e.g., "maternity leave", "unpaid leave").

    :returns: A string containing one or more HR policy descriptions, such as:
              - Leave types and annual entitlements
              - Approval workflows and documentation requirements
              - Policy rules for carrying forward, encashment, or loss of leave
              - Disciplinary actions related to absence or policy violation
              - Special leave scenarios (e.g., adoption, medical emergency, LTA)

    Note: The format and language may vary based on policy source. It is expected to be informative and specific.
    """
    get_hr_policies = """นโยบายการลา: - นโยบายการลาของ HR บริษัท สำหรับพนักงาน
• ไม่สามารถเรียกร้องการลาเป็นสิทธิ์ได้ การลาใด ๆ สามารถอนุญาตหรือปฏิเสธได้ขึ้นอยู่กับความต้องการทางธุรกิจ การ
ขาดงานโดยไม่ได้รับอนุญาตอย่างถูกต้องจะถูกดำเนินการทางวินัย ความหมายของการลาคือการไปจากสถานที่สั้น ๆ
• ปีปฏิทินสำหรับการลาคือตั้งแต่เดือนมกราคมถึงเดือนธันวาคม
• บันทึกการลาของพนักงานทั้งหมดจะถูกบันทึกในเครื่องมือ HRMS
• การลาทั้งหมดควรยื่นในเครื่องมือ HRMS ก่อนการลา ในกรณีฉุกเฉินที่ไม่สามารถยื่นการลาล่วงหน้าได้ ควรแจ้งให้ผู้จัดการ
ที่รายงานโดยตรงทราบทางโทรศัพท์ และต้องทำให้เป็นไปตามข้อกำหนดภายใน 2 วันหลังจากกลับมาปฏิบัติหน้าที่โดยใช้
เครื่องมือ HRMS
• การลาจะถูกเพิ่มในบัญชีพนักงานในช่วงต้นปีปฏิทิน นั่นคือ มกราคม การลาที่ได้รับจะได้รับการปรับปรุงทุกเดือนสำหรับ
การลาที่ได้รับระหว่างเดือน จะถูกเพิ่มในอัตรา 1.75 วันต่อเดือน สำหรับพนักงานที่มีอยู่ ยอดการลาที่สะสมจากปีก่อนจะ
ได้รับการปรับปรุงในเดือนมกราคม
• พนักงานจะมีสิทธิ์ได้รับการลาเมื่อการทดลองงานเสร็จสิ้น หลังจากยืนยันการลาสำหรับช่วงการทดลองงานจะถูกเพิ่มใน
บัญชีพนักงาน
• พนักงานต้องใช้วันลา 18 วันในหนึ่งปี ควรเป็น EL 12 วันและ CL 6 วัน เพื่อให้บรรลุวัตถุประสงค์ของการรักษาสมดุลชีวิต
การทำงาน
• สามารถนำการลาได้สูงสุด 9 วันไปสู่ปีถัดไป
• พนักงานอาจขอลาตามยอดการลาที่มีอยู่ในบัญชีของพวกเขาบนเครื่องมือ HRMS
• พนักงานสามารถใช้วันลาที่มีค่าใช้จ่ายได้ขึ้นอยู่กับยอดการลาที่มีอยู่ พนักงานยังสามารถขอลาโดยไม่ได้รับค่าจ้างเมื่อยอด
การลาหมดและพนักงานต้องการลาโดยได้รับอนุญาตจากผู้จัดการทันที HOD และ HR
• พนักงานที่เข้าร่วมระหว่างปีจะได้รับการลาตามอัตราส่วนในบัญชีการลาของพวกเขาบนเครื่องมือ HRMS
• พนักงานไม่ควรลาจนกว่าการลาจะได้รับการอนุมัติจากผู้จัดการที่รายงาน
• ถ้าพนักงานขาดงานต่อเนื่อง 7 วันโดยไม่มีข้อมูล ในกรณีนี้พนักงานจะถือว่าได้ออกจากงานตามความต้องการของตนเอง
HR จะดำเนินการในกรณีนี้ จะออกจดหมายเตือนครั้งแรกถ้าพนักงานไม่กลับมาภายใน 7 วันหลังจากหมดอายุการลาที่
ได้รับการอนุมัติ ถ้าไม่มีการตอบสนองจากพนักงานภายใน 3 วันหลังจากการออกจดหมายเตือนครั้งแรก จดหมายเตือน
ครั้งที่สองจะถูกออก ถ้ายังไม่มีการตอบสนองจากพนักงานที่กล่าวถึง จดหมายการยุติธรรมสุดท้ายจะถูกออกใน 3 วัน
หลังจากการออกจดหมายเตือนครั้งที่สอง
• ในกรณีของโรคร้ายแรงหรือการขาดงานจากงาน พนักงานควรแจ้งผู้จัดการที่รายงานโดยตรงทุกช่วงเวลาเกี่ยวกับสภาพ
ของพวกเขาและวันที่เป็นไปได้ที่จะกลับมา ในกรณีที่ไม่มีการสื่อสารจากพนักงาน บริษัท อาจดำเนินการที่ร้ายแรง
• การลาโดยไม่ได้รับการอนุมัติจะถือว่าเป็นการลาโดยไม่ได้รับค่าจ้าง
• วันสุดสัปดาห์และวันหยุดใด ๆ ที่อยู่ระหว่างช่วงการลาที่ได้รับการอนุมัติจะไม่ถูกรวมและไม่นับเป็นวันลาในกรณีของการ
ลาชั่วคราวและการลาที่ได้รับ
• การลาสำหรับปีถัดไปไม่สามารถใช้ได้ในปีปัจจุบัน
• ในกรณีของการลาที่วางแผนไว้ พนักงานมีความรับผิดชอบในการขอลาล่วงหน้า อย่างไรก็ตามในกรณีของการลาที่ไม่ได้
วางแผน พนักงานต้องปรับปรุงการลาภายใน 2 วันหลังจากกลับมาปฏิบัติหน้าที่
• การลาเพื่อวัตถุประสงค์ของ LTA ควรเป็นการลาที่ได้รับ ไม่สามารถเป็นการลาอย่างไม่เป็นทางการ
ประเภทของการลา
มีหลายประเภทของการลาที่ได้รับและระบุไว้ในนโยบายการลาประจำปีของบริษัท HR การลาสามารถจัดหมวดหมู่ได้เป็น
การลาประจำปีที่ได้รับค่าจ้าง หรือ การลาโดยไม่ได้รับค่าจ้าง บางประเภทของการลาที่ได้รับการอนุมัติและให้แก่พนักงาน
ตามจำนวนวันลาที่มีอยู่จะเป็นการลาที่ได้รับค่าจ้าง หรือ การลาพร้อมค่าจ้าง อย่างไรก็ตาม การลาโดยไม่ได้รับค่าจ้าง หรือ
การลาโดยไม่มีค่าจ้างสามารถใช้ได้โดยพนักงานในเวลาฉุกเฉินและเมื่อไม่มีจำนวนวันลาเหลืออยู่
• การลาชั่วคราว
• การลาที่ได้รับ
• การลาคลอด
• การลาพักผ่อนสำหรับบิดา
• การลาโดยไม่ได้รับค่าจ้าง
• วันหยุดชดเชย
การลาชั่วคราว
• พนักงานสามารถใช้การลาชั่วคราวได้สูงสุด 12 วันในหนึ่งปี
• การลาชั่วคราวเป็นการลาที่ได้รับค่าจ้าง
• พนักงานที่เข้าร่วมงานในระหว่างปีจะได้รับสิทธิ์การลาชั่วคราวตามสัดส่วน
• การลาชั่วคราวสามารถลาได้ต่ำสุดครึ่งวันและสูงสุด 4 วัน
• การลามากกว่า 4 วันสามารถนำมาใช้เป็นการลาที่ได้รับ
• การลาชั่วคราวไม่สามารถนำไปสู้ปีถัดไปได้
• การลาชั่วคราวไม่สามารถรวมกับการลาที่ได้รับหรือประเภทการลาอื่น ๆ
• ควรยื่นใบขอลาชั่วคราวล่วงหน้าหนึ่งวันและล่วงหน้าหนึ่งสัปดาห์เมื่อยื่นขอลามากกว่า 2 วัน
• การลาชั่วคราวที่ไม่ได้ใช้จะหมดอายุในท้ายปี
กระบวนการสำหรับการลาชั่วคราว
การลาชั่วคราวที่พนักงานยื่นผ่านเครื่องมือ HRMS สำหรับการอนุมัติ การแจ้งเตือนการลาจะถึงผู้จัดการที่รายงานตรงโดย
ทันที เมื่อได้รับการอนุมัติ การแจ้งเตือนการอนุมัติจะถึงพนักงานและ HR วันลาจะถูกหักจากยอดคงเหลือของพนักงานและ
ยอดคงเหลือล่าสุดจะได้รับการอัปเดตบนเครื่องมือ HRMS
การลาที่ได้รับ
• ใบสมัครขอลาสำหรับการลาที่ได้รับต้องถึงผู้จัดการที่รายงานล่วงหน้า 15 วัน
• สำหรับผู้ที่เข้าร่วมใหม่ที่เข้าร่วมในช่วงกลางปี การลาพิเศษจะได้รับเครดิตตามสัดส่วน
• สำหรับพนักงานที่มีอยู่ วันลาจะถูกเพิ่มเติมในช่วงต้นปี อย่างไรก็ตามสิทธิ์จะขึ้นอยู่กับจำนวนเดือนที่ทำงาน สำหรับทุก
เดือนที่ทำงานเสร็จสิ้น 1.75 ของการลาพิเศษจะถูกเพิ่มเข้าในบัญชีของพนักงาน
• การลาพิเศษสามารถนำไปสู้ปีถัดไปได้สูงสุด 9 วัน อย่างไรก็ตามสำหรับพนักงานที่มีอยู่ที่ให้บริการมากกว่า 5 ปี สูงสุด
สามารถนำไปสู้ได้ 45 วัน การลาเกิน 45 วันจะหมดอายุโดยอัตโนมัติ
• พนักงานที่ลาออกจากหน้าที่ของพวกเขา สิทธิ์การลาพิเศษจะคำนวณตามสัดส่วนจนถึงวันทำงานสุดท้าย
• สำหรับการคำนวณ LTA พนักงานต้องใช้การลา 5 วันเป็นจำนวนบังคับ (รวมถึงวันหยุด)
กระบวนการสำหรับการลาพักร้อนที่ได้รับ
พนักงานต้องยื่นคำร้องขอลาพักร้อนที่ได้รับล่วงหน้า 15 วัน หลังจากยื่นคำร้องแล้ว การแจ้งเตือนจะถูกส่งไปยังผู้จัดการที่
รับผิดชอบโดยตรง เมื่อการลาได้รับการอนุมัติ การแจ้งเตือนจะถูกส่งไปยังพนักงานและแผนกทรัพยากรบุคคล ยอด
คงเหลือหลังจากการหักลาจะได้รับการปรับปรุงในระบบ HRMS
ลาคลอด
• พนักงานหญิงที่ได้รับการยืนยันสถานะทั้งหมดจะมีสิทธิ์ได้รับการลาคลอดตามพระราชบัญญัติสวัสดิการการคลอดปี 2016
พร้อมกับค่าจ้างเต็มจำนวนสำหรับระยะเวลา 26 สัปดาห์ติดต่อกัน (ไม่รวมวันหยุดนักขัตฤกษ์) สำหรับการตั้งครรภ์แต่ละ
ครั้งสูงสุด 2 ครั้ง
• การลาที่ใช้เพื่อการรักษาก่อนคลอดในช่วง 7 เดือนแรกของการตั้งครรภ์จะถือว่าเป็นการลาปกติ ไม่ใช่การลาคลอด
• พนักงานหญิงสามารถเริ่มการลาคลอดได้เร็วที่สุดในช่วง 8 สัปดาห์ก่อนวันที่คาดว่าจะคลอด
กระบวนการขอลาคลอด
• ก่อนการลาคลอด จำเป็นต้องยื่นคำร้องในระบบ HRMS และต้องได้รับการอนุมัติจากผู้จัดการที่รายงาน
• พนักงานหญิงที่จะลาคลอดต้องยื่นใบรับรองแพทย์ไปยังแผนกทรัพยากรบุคคล
การลาในกรณีของการรับบุตรบุญธรรมหรือการเกิดบุตรผ่านการเช่ามารดา
• ในกรณีของการรับบุตรบุญธรรมหรือการเกิดบุตรจากการเช่ามารดา พนักงานหญิงมีสิทธิ์ได้รับการลา 12 สัปดาห์
• การลาเหล่านี้สามารถใช้ได้เมื่อเด็กได้เริ่มที่จะอยู่กับผู้ปกครองอย่างแท้จริง
กระบวนการขอลาในกรณีของการรับบุตรบุญธรรมหรือการเกิดบุตรผ่านการเช่ามารดา
• ในกรณีที่กล่าวถึงข้างต้นการลาต้องสมัครอย่างน้อย 6 สัปดาห์ก่อนวันรับบุตร
• ใบรับรองทางกฎหมายและเอกสารที่ต้องการทั้งหมดต้องส่งให้ HR Paternity Leave
• พนักงานชายทุกคนที่ปฏิบัติงานอย่างสม่ำเสมอมีสิทธิ์ได้รับการลาพ่อ
• พนักงานสามารถใช้สิทธิ์ลาพ่อได้สูงสุด 7 วัน
• การลาพ่อต้องทำภายใน 15 วันหลังจากการเกิดลูก หากไม่ทำจะทำให้สิทธิ์ลาหมดอายุ
• การลาต้องเป็นระยะเวลาต่อเนื่อง
• ในกรณีของการรับบุตรบุญธรรมหรือการเกิดจากการพิจารณา การลาสามารถทำได้เฉพาะเมื่อบุตรอยู่กับพ่อแม่จริงๆ
กระบวนการลาพักผ่อนสำหรับบิดา
• ต้องยื่นใบลาพักผ่อนเนื่องจากการเป็นบิดาอย่างน้อย 15 วันก่อนวันที่คาดว่าจะคลอด
• พนักงานสามารถเริ่มต้นลาได้ตั้งแต่วันที่คลอดจริง
• การลาต้องได้รับการอนุมัติจากผู้จัดการที่รายงานโดยตรง
การลาโดยไม่ได้รับค่าจ้าง
• พนักงานสามารถลาโดยไม่ได้รับค่าจ้างในกรณีที่ยอดการลาปัจจุบันหมดแล้วและพนักงานต้องการลาเนื่องจาก
สถานการณ์ที่ไม่คาดคิด
• ในกรณีที่ไม่ได้รับการอนุมัติสำหรับการลาโดยไม่มีค่าจ้าง การขาดงานของพนักงานจะถือว่าเป็นการลางาน
• จะดำเนินการวินิจฉัยในกรณีขาดงานโดยไม่ได้รับอนุมัติ
• พนักงานจะไม่ได้รับเงินเดือนสำหรับวันที่ลาโดยไม่มีค่าจ้าง
• พนักงานสามารถลาโดยไม่ได้รับค่าจ้างได้สูงสุด 3 เดือน
• พนักงานสามารถขอลาโดยไม่ได้รับค่าจ้างโดยการยื่นใบสมัครผ่านเครื่องมือ HRMS เพื่อรับการอนุมัติจากผู้จัดการที่
รายงานโดยตรงและหัวหน้าแผนก
• หลังจากได้รับการอนุมัติจากผู้จัดการที่รายงานโดยตรงและหัวหน้าแผนก พนักงานสามารถลาได้
• การลาจะอัปเดตเป็นการสูญเสียค่าจ้างในเครื่องมือ HRMS
กระบวนการการขอลาโดยไม่ได้รับค่าจ้าง
• พนักงานสามารถขอลาโดยไม่ได้รับค่าจ้างได้โดยการยื่นใบสมัครผ่านเครื่องมือ HRMS เพื่อรับการอนุมัติจากผู้จัดการที่
รายงานโดยตรงและหัวหน้าแผนก
• หลังจากได้รับการอนุมัติจากผู้จัดการที่รายงานโดยตรงและหัวหน้าแผนก พนักงานสามารถลาได้
• การลาจะอัปเดตเป็นการสูญเสียค่าจ้างในเครื่องมือ HRMS
วันหยุดชดเชย
• พนักงานมีสิทธิ์ได้รับวันหยุดชดเชยเมื่อเขา/เธอทำงานในงานที่สำคัญในวันหยุดประจำชาติ/เทศกาล/วันหยุดที่ประกาศไว้
• ต้องได้รับการอนุมัติในการทำงานในวันดังกล่าว เช่น วันหยุดประจำชาติ/เทศกาล/วันหยุดที่ประกาศไว้ จาก
คณะกรรมการอาวุโส
• วันหยุดชดเชยต้องใช้ภายในระยะเวลา 1 เดือนมิฉะนั้นจะสูญหาย
กระบวนการเพื่อรับค่าชดเชย
ต้องได้รับการอนุมัติจากคณะกรรมการอาวุโสสำหรับวันหยุดชดเชย พนักงานที่ทำงานในวันหยุดประจำชาติ/เทศกาล/
วันหยุดที่ประกาศไว้สามารถขอลาเพื่อแลกกับการทำงานในวันที่กล่าวถึงได้ ในวันที่พนักงานขอหยุดชดเชย เขา/เธอต้อง
แจ้งผู้จัดการที่รายงานโดยตรง หลังจากได้รับการอนุมัติแล้ว จะเป็นความรับผิดชอบของผู้จัดการที่รายงานโดยตรงที่จะแจ้ง
ฝ่ายทรัพยากรบุคคลเกี่ยวกับสิ่งนี้
นโยบายการลางาน: นโยบายการลางานถูกกำหนดไว้ว่าเป็นการลางานโดยไม่ได้รับค่าจ้างที่ได้รับการอนุมัติอย่างเป็น
ทางการจากการทำงานสำหรับระยะเวลาที่จำกัดเนื่องจากเหตุผลทางการแพทย์หรือส่วนตัว.
กระบวนการนโยบายการลาหยุด:
เหตุผลทางการแพทย์: ต้องมีการขออนุมัติลาหยุดจากงานผ่านเครื่องมือ HRMS คำขอจะถูกส่งไปยังหัวหน้างานทันทีและ
หัวหน้าแผนกเพื่อการอนุมัติ พนักงานควรขออนุญาตลาหยุดจากงานอย่างน้อย 20 วันล่วงหน้าเมื่อทราบความต้องการใน
การลาหยุด ในกรณีที่ลาหยุดจากงานเนื่องจากเหตุผลทางการแพทย์ ต้องมีใบรับรองจากแพทย์ส่งไปยังแผนกทรัพยากร
มนุษย์
เหตุผลส่วนตัว: พนักงานสามารถขอลาหยุดจากงานได้เมื่อต้องการเนื่องจากเหตุผลที่ไม่สามารถคาดการณ์ได้ จำนวนวันลา
หยุดสูงสุดที่สามารถขอได้คือหกสัปดาห์
การยกเลิกการลา
• การลาที่ได้รับการอนุมัติสามารถถูกยกเลิกได้ขึ้นอยู่กับความต้องการของธุรกิจ
• เมื่อการลาถูกยกเลิกโดยผู้จัดการรายงาน การแจ้งเตือนอัตโนมัติจะถูกส่งไปยังพนักงานและแผนกทรัพยากรมนุษย์
• ยอดการลาจะได้รับการปรับปรุงอย่างเหมาะสมโดยแผนกทรัพยากรมนุษย์
การขยายการลา
• ในกรณีที่ต้องขยายการลาเนื่องจากสถานการณ์ที่ไม่คาดคิด พนักงานต้องแจ้งผู้จัดการที่รายงานล่วงหน้า; เมื่อการขยาย
การลาได้รับการอนุมัติจากผู้จัดการที่รายงาน ก็เป็นหน้าที่ของผู้จัดการที่จะแจ้งให้แผนกทรัพยากรมนุษย์ทราบ นี่เป็นกรณี
ที่ได้บอกการขยายการลาโดยปากเปล่าหรือทางโทรศัพท์ ต้องรับผิดชอบในการปรับปรุงการลาบนเครื่องมือ HRMS เมื่อ
พนักงานกลับมาปฏิบัติงาน
• การลาที่ขยายต้องถูกสมัครใจบนเครื่องมือ HRMS ในกรณีของการวางแผนการขยายเพื่อให้ทั้งผู้จัดการที่รายงานและ
ทรัพยากรมนุษย์ได้รับแจ้งโดยอัตโนมัติ
• ยอดการลาจะได้รับการปรับปรุงบนเครื่องมือ HRMS โดยแผนกทรัพยากรมนุษย์
• ในกรณีที่พนักงานลาเกินไปโดยไม่ได้รับอนุมัติจะถือว่าเป็นการขาดงาน และจะได้รับการดำเนินการทางวินัย
• การลาที่ขยายโดยไม่ได้รับอนุญาตจะถูกจัดเป็นการสูญเสียค่าจ้าง
การคำนวณการลาในกรณีลาออก/การเลิกจ้าง
ในกรณีที่พนักงานได้ลาออกจากงานหรือเมื่อมีการเลิกจ้างพนักงาน สิทธิการลาจะถูกคำนวณจนถึงวันทำงานสุดท้ายของ
พนักงานและจะได้รับการจ่ายในการตัดบัญชีอย่างสมบูรณ์และสุดท้ายของพนักงาน"""

    return get_hr_policies
