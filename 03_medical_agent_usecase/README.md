### Important

- The email and google calendar has been prepopulated already do not add it using adk otherwise you will destroy the skill.
- Don't forget to rename the agents including the main agent and the collaborator agents.


### Locating to single agent

Please locate to the `agents/medical_agent.yaml` and `agents/diabetes_agent.yaml` change the name of the agent so it does not override the old agent.
```
cd single_agent
bash import-all.sh
```

### Locating to multi agent

Please locate to the `agents/medical_agent.yaml` and `agents/diabetes_agent.yaml` change the name of the agent so it does not override the old agent.
```
cd single_agent
bash import-all.sh
```

### Storyline queries:

Queries:
ขอข้อมูลผู้ป่วยทั้งหมดหน่อย
ครั้งที่แล้ว นายสมชาย ใจดีมาหาหมอเรื่องอะไรบ้าง
สร้าง นัดหมายกับ นายสมชาย ใจดี มาฟังผลตรวจ วันที่ 2 กรกฏาคม 10 โมงถึง เที่ยง เวลากรุงเทพ 2025 และมี Kandanai.Leenutaphong@ibm.com อยู่ในนัดด้วย
กรุณาส่งอีเมลไปให้ นายสมชาย ใจดี เพื่อยืนยันนัดหมายไปเรียบร้อยแล้วเขียนเป็นทางการ ลงท้ายด้วย Kandanai Leenutaphong CC: mew.chayutaphong@gmail.com, Kandanai.Leenutaphong@ibm.com ด้วย

Diabetes Agent:
โรคเบาหวานคืออะไร และเกิดจากอะไร?
อาการสำคัญของผู้ป่วยโรคเบาหวานมีอะไรบ้าง?
ผู้ป่วยเบาหวานควรหลีกเลี่ยงอาหารประเภทใด?
“อาหารแลกเปลี่ยน” หมายถึงอะไร?

Decision queries:
ผมอายุ 35 ปี ค่าดัชนีมวลกาย (BMI) อยู่ที่ 27 ควรตรวจสุขภาพตามแผนไหนครับ?
ผมอายุ 21 ปี ค่าดัชนีมวลกาย (BMI) อยู่ที่ 21 ควรตรวจสุขภาพตามแผนไหนครับ?