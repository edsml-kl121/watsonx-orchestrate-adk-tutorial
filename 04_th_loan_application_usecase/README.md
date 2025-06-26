### Important

- The email and google calendar has been prepopulated already do not add it using adk otherwise you will destroy the skill.
- Don't forget to rename the agents including the main agent and the collaborator agents.


### Locating to single agent

Please locate to the `agents/loan_agent.yaml` and `agents/loan_knowledge_agent.yaml` change the name of the agent so it does not override the old agent.
```
cd single_agent
bash import-all.sh
```

### Locating to multi agent

Please locate to the `agents/loan_agent.yaml` and `agents/loan_knowledge_agent.yaml` change the name of the agent so it does not override the old agent.
```
cd single_agent
bash import-all.sh
```

### Storyline queries:

ขอดูรายชื่อผู้สมัครสินเชื่อทั้งหมดหน่อย
ช่วยตัดสินใจให้หน่อยว่า สมชาย ใจดี ควรอนุมัติไหม
ช่วยร่างอีเมลเขียนแบบเป็นทางการแจ้งอนุมัติให้คุณสมชายด้วย และ ลงท้ายด้วย Watsonx Orchestrate

ช่วยส่งอีเมลแจ้งผล และ CC: mew.chayutaphong@gmail.com, Kandanai.Leenutaphong@ibm.com, Natthaphol.Khantikulanon@ibm.com

นโยบายการติดตามหนี้พูดถึงอะไรเกี่ยวกับลูกค้าที่มีความเสี่ยงต่ำ?
ขั้นตอนที่สองของการติดตามหนี้คืออะไร?
จะได้รับจดหมายเตือนเมื่อไรตามนโยบาย?