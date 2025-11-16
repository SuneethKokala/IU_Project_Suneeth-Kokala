# IU_Project_Suneeth-Kokala

# Automated Industrial Safety Management System
In industrial areas like factories, building sites and train yards where employees are regularly exposed to dangerous situations safety is still a top priority. Even though personal protective equipment (PPE) including gloves, vests and helmets are readily available, noncompliance with safety regulations continues. In vast industrial locations in particular manual PPE usage oversight is often unreliable, ineffective and unable to generate timely alerts. This lack of precise and continuous monitoring increases the risk of accidents, injuries and inefficiency at work. To address these issues, I have proposed an Automated Industrial Safety Monitoring System that continuously observes workers to ensure compliance with safety requirements. This technology checks to see if workers are wearing the appropriate safety equipment using an intelligent detection model. When a violation is found, it logs the occurrence, instantly notifies supervisors, and saves the information for further review.  Additionally, the system generates visual compliance reports and trend analyses to help management identify recurring issues and improve safety practices. Unlike traditional systems that only focus on gear detection this project integrates end to end functionality from detection to alerting and reporting providing a complete and practical safety management solution. The project is planned to produce an effective, scalable and reliable solution that increases worker safety by automating compliance monitoring. It will encourage proactive safety management, lessen human error and eliminate the need for manual supervision.  In industrial settings the produced data and visual summaries will enhance worker accountability, facilitate data driven decision making and reduce the risk of accidents. The system’s ultimate goal is to improve operational effectiveness and safety culture in all industrial sites.

# Goal:
- **Improve worker safety** by ensuring proper use of personal protective equipment (PPE) in industrial environments.  
- **Automate safety monitoring** to reduce human effort and minimize supervision errors.  
- **Detect safety violations in real time** and notify supervisors instantly for quick action.  
- **Record and store safety data** to maintain a digital log of all detected violations.  
- **Generate detailed compliance reports** for analysis and decision-making.  
- **Design a scalable system** that can be deployed across multiple industrial sites.  
- **Support proactive safety management** through continuous monitoring and data-driven insights.  

# Tech Stack:

| **Category** | **Technology / Tool** | **Purpose / Description** |
|---------------|------------------------|-----------------------------|
| Programming Language | **Python** | Used for detection logic, backend, and data handling |
| Computer Vision & AI Framework | **YOLOv8** | Detects PPE (helmets, vests, gloves) in real-time |
| Backend Framework | **FastAPI** | Handles alerts, API communication, and data management |
| Database | **PostgreSQL** | Stores violation records, compliance data, and user details |
| Real-Time Messaging Protocol | **MQTT** | Sends instant alerts and real-time updates |
| Dashboard & Visualization | **Grafana** | Visualizes safety statistics and compliance trends |
| Containerization / Deployment | **Docker** | Packages and deploys the system efficiently |
| Version Control | **Git & GitHub** | Enables version tracking and team collaboration |
| Development Tools | **VS Code** | Used for coding, testing, and debugging |
| Libraries | **OpenCV**, **NumPy**, **Pandas** | Video frame processing and data analysis |


# Project Risks:
**Technical Risk**
- Hardware malfunction (e.g., camera or sensor failure) may disrupt monitoring.
- Software bugs or crashes in detection or communication modules.
- Integration issues between Python, OpenCV, Twilio, and hardware components.
- Network or internet connectivity failures can interrupt alert transmission.
- False positives or false negatives in motion or face detection.
- Scalability issues when handling multiple devices or large data streams.

**Operational Risks**
- Complex maintenance and need for regular calibration of hardware components.
- Power supply interruptions affecting continuous operation.
- Environmental factors (poor lighting, obstructions, weather) impacting accuracy.
- Human error during system setup or configuration.


# Phase Status
1. Conception Phase - Done
2. Development Phase - Under Progress
