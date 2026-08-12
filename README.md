# 👔 PickFit — Smart Wardrobe

> **내가 가진 옷을 실제로 기억하고, 지금 입을 수 있는 옷을 골라주는 옷장.**

**PickFit**은 사용자의 실제 옷장 상태를 IoT 센서로 감지하고, 이를 Digital Twin으로 관리하여 날씨·의류 상태·착용 이력·사용자 취향을 기반으로 코디를 추천하는 **AIoT 기반 Smart Wardrobe Platform**입니다.

단순히 앱에 등록된 옷을 추천하는 것이 아니라,

**실제 옷장에 존재하고 현재 착용 가능한 옷만을 대상으로 추천하는 것**

을 핵심 목표로 합니다.

---

## 📌 Project Overview

기존 Digital Closet 서비스는 사용자가 등록한 데이터를 기반으로 옷을 관리합니다.

하지만 현실에서는 옷이

- 외출 중일 수도 있고
- 세탁 중일 수도 있고
- 관리가 필요할 수도 있으며
- 실제 옷장에 존재하지 않을 수도 있습니다.

PickFit은 이러한 **Physical Wardrobe와 Digital Wardrobe 사이의 차이**를 해결하는 것을 목표로 합니다.

```text
Real Clothes
    ↓
IoT Sensor
    ↓
Physical Wardrobe State
    ↓
Digital Twin
    ↓
Care / Usage History
    ↓
Weather + User Context
    ↓
Recommendation Engine
    ↓
Today's Outfit
    ↓
Physical LED Guide
    ↓
Real Wearing
    ↓
Camera / Feedback
    ↓
Personalization
```

---

# ✨ Core Concept

PickFit의 핵심은 **Physical Wardrobe Awareness**입니다.

기존 서비스가

```text
등록된 옷
↓
AI 추천
```

이라면 PickFit은

```text
실제 옷 존재 여부
+
현재 착용 가능 상태
+
날씨
+
사용자 취향
+
과거 착장 경험
↓
추천
```

구조를 사용합니다.

### 핵심 USP

**1. 현재 실제 옷장에 존재하는 옷을 안다.**

**2. 그 옷이 지금 실제로 착용 가능한 상태인지 안다.**

**3. 사용자가 그 옷을 실제로 어떻게 입었고 얼마나 만족했는지 안다.**

```text
Physical State
+
Care State
+
Real Outfit Experience
=
Personal Wardrobe Intelligence
```

---

# 🏗 System Architecture

```text
                     ┌───────────────┐
                     │     User      │
                     └───────┬───────┘
                             │
                             ▼
                   ┌─────────────────┐
                   │ Smart Mirror UI │
                   └────────┬────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
     Recommendation Engine            Lookbook
              │                           │
              └─────────────┬─────────────┘
                            ▼
                   ┌─────────────────┐
                   │ Digital Twin DB │
                   └────────┬────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ▼                 ▼                 ▼
      Presence           Care State      Outfit History
       State
                            │
                            ▼
                   ┌─────────────────┐
                   │ IoT Controller  │
                   └────────┬────────┘
                            │
       ┌────────────┬───────┼───────┬────────────┐
       ▼            ▼       ▼       ▼            ▼
   Presence        RFID    Door     LED      Temp/Humidity
    Sensor                Sensor   Guide        Sensor
```

---

# 🔄 Digital Twin

각 의류는 하나의 `Garment Object`로 관리됩니다.

예시:

```text
GARMENT_ID : G0031
```

각 Garment는 크게 다음 데이터를 가집니다.

### Identity

- Brand
- Product Name
- Category
- Color
- Material
- Size
- Purchase Information

### Physical

- Wardrobe ID
- Slot
- Sensor ID
- Presence State
- Last Presence Change

### Care

- Care State
- Wear Count
- Last Wash Date
- Material Care Profile

### Usage

- Total Wear Count
- Last Worn Date
- Average Rating
- Favorite Score

### Recommendation

- Season
- Temperature Range
- Style
- Formality
- Color
- Rain Compatibility
- Thickness

---

# 👕 Garment State

## Presence State

실제 옷장에 의류가 존재하는지 나타냅니다.

```text
IN_WARDROBE
OUT
UNKNOWN
```

예:

```text
IN_WARDROBE
      │
      │ Remove
      ▼
     OUT
      │
      │ Return
      ▼
IN_WARDROBE
```

---

## Care State

현재 해당 옷을 착용하는 것이 적절한지 관리합니다.

```text
CLEAN
REWEARABLE
NEED_WASH
WASHING
CARE_REQUIRED
```

추천 시스템에서는 Presence와 Care State를 함께 사용합니다.

```text
AVAILABLE =
    Presence == IN_WARDROBE
AND Care State ∈ {CLEAN, REWEARABLE}
AND Weather Compatible
```

---

# 🧠 Recommendation Engine

추천 시스템은 처음부터 모든 판단을 AI에게 맡기지 않습니다.

## Stage 1 — Hard Filter

```text
Presence
↓
Care State
↓
Weather
↓
Category
```

현재 실제로 입을 수 없는 옷을 먼저 제거합니다.

## Stage 2 — Outfit Generation

```text
Top × Bottom × Outer × Shoes
```

가능한 코디 후보를 생성합니다.

## Stage 3 — Scoring

```text
Outfit Score =
Weather Suitability
+ Style Compatibility
+ Color Compatibility
+ User Preference
+ Previous Rating
+ Wear Frequency Balance
+ Occasion Suitability
```

## Stage 4 — AI Ranking

AI는 생성된 후보를 재정렬하고 추천 이유를 제공합니다.

예:

> 오늘은 비가 예상되어 방수 가능한 아우터를 포함하고, 최근 착용 빈도가 낮은 Grey Knit를 활용한 코디를 추천합니다.

---

# 💡 Physical Guide

추천된 옷을 실제 옷장에서 쉽게 찾을 수 있도록 해당 옷이 위치한 Slot의 LED를 활성화합니다.

```text
Recommendation
↓
Garment ID
↓
Slot ID
↓
LED ON
↓
사용자가 실제 옷 선택
```

---

# 📸 Outfit Lookbook

추천 이후 사용자가 실제로 착용한 모습을 기록합니다.

```text
추천 코디
↓
옷 선택
↓
실제 착용
↓
[오늘 착장 저장]
↓
Camera Capture
↓
Outfit Event 생성
↓
Lookbook 저장
↓
사용자 평가
```

예:

```text
2026-08-12

Top    : Grey T-Shirt
Bottom : Black Pants
Outer  : Light Jacket

Weather : 23°C
Purpose : School
Style   : Casual

Rating : ★★★★★
```

이 데이터는 이후 개인화 추천에 사용됩니다.

---

# 🌡 Wardrobe Environment

옷장 내부 환경도 관리합니다.

### MVP

- Temperature
- Humidity
- Humidity Warning
- Environment Monitoring

### Future

- VOC
- Air Quality
- Odor Detection
- Automatic Ventilation
- Dehumidification

---

# 🔐 Privacy by Design

Smart Mirror에 카메라가 사용되는 만큼 Privacy를 핵심 요구사항으로 다룹니다.

- 사용자의 명시적인 요청이 있을 때만 촬영
- Camera Indicator LED
- Physical Shutter
- Local First Processing
- 사진 직접 삭제
- Camera Disable
- Lookbook Disable
- Continuous Surveillance 금지

---

# 🚀 MVP

프로젝트의 MVP는 다음 기능을 목표로 합니다.

| ID | Feature |
|---|---|
| M01 | Garment Registration |
| M02 | Physical Presence Detection |
| M03 | Presence State |
| M04 | Care State |
| M05 | Digital Twin DB |
| M06 | Weather API |
| M07 | Available Garment Filter |
| M08 | Outfit Recommendation |
| M09 | Physical LED Guide |
| M10 | Outfit Camera Capture |
| M11 | Outfit Event / Lookbook |
| M12 | User Rating |
| M13 | Temperature / Humidity |
| M14 | Smart Mirror Dashboard |

---

# 🛠 Technology Stack

현재 기획 단계의 후보 기술 스택입니다.

### Device

```text
Arduino UNO
ESP32
```

### Sensor

```text
Load Cell
RFID / NFC
Magnetic Sensor
Micro Switch
Temperature / Humidity Sensor
```

최종 Presence Sensor 방식은 PoC 이후 결정합니다.

### Backend

```text
Python
FastAPI
SQLite
→ MySQL / PostgreSQL
```

### Communication

```text
HTTP / REST API
MQTT
WebSocket
```

### AI / Recommendation

```text
Rule-Based Filtering
+
Weighted Scoring
+
User Preference Model
+
AI Recommendation
```

### Frontend

```text
Web Dashboard
Smart Mirror Kiosk UI
```

---

# 🌐 Communication Architecture

```text
Physical Sensor
      ↓
Arduino / ESP32
      ↓
Device API / MQTT / WebSocket
      ↓
Backend
      ↓
Digital Twin DB
      ↓
Recommendation Engine
      ↓
Smart Mirror UI
```

센서 이벤트 예시:

```json
{
  "event": "GARMENT_REMOVED",
  "garment_id": "G0031",
  "slot_id": "H07",
  "timestamp": "2026-08-12T08:11:21"
}
```

---

# 👥 Team

본 프로젝트는 **5인 팀 프로젝트**입니다.

### Member 1 — Embedded / Physical Sensor

- Presence Sensor
- Load Cell / RFID Test
- Door Sensor
- LED
- Environment Sensor
- MCU Firmware

### Member 2 — IoT / Device Communication

- Arduino / ESP32
- Wi-Fi / LAN / USB
- Device API
- Event Messaging
- Hardware Integration

### Member 3 — Backend / Digital Twin

- Garment DB
- Presence State
- Care State
- Outfit Event
- REST API
- Event Log

### Member 4 — Recommendation / AI

- Weather Data
- Outfit Filter
- Outfit Scoring
- Personalization
- Dead Stock Recommendation
- Wardrobe Analysis

### Member 5 — Frontend / Smart Mirror

- Smart Mirror UI
- Dashboard
- Lookbook
- Camera
- User Interaction
- Integration UI

---

# 🗺 Development Roadmap

## Phase 0 — Planning

- [x] 프로젝트 아이디어 선정
- [x] Master PRD 작성
- [x] MVP 정의
- [x] 시스템 구조 설계
- [ ] 세부 Interface 정의

## Phase 1 — Presence PoC

- [ ] Load Cell Test
- [ ] RFID Test
- [ ] Magnetic Sensor Test
- [ ] Switch Test
- [ ] Presence 방식 선정

목표:

```text
한 벌의 옷이 실제 옷장에 있는지
안정적으로 판단한다.
```

## Phase 2 — Digital Twin

```text
Physical State
↕
Database
```

센서와 DB 상태를 실시간으로 동기화합니다.

## Phase 3 — Recommendation

- [ ] Weather API
- [ ] Hard Filter
- [ ] Outfit Generation
- [ ] Scoring
- [ ] Recommendation

## Phase 4 — Smart Mirror / Lookbook

- [ ] Mirror UI
- [ ] Camera
- [ ] Outfit Capture
- [ ] Rating
- [ ] Lookbook

## Phase 5 — Integration

```text
Sensor
→ DB
→ Recommendation
→ Mirror
→ Camera
→ Feedback
```

Closed Loop를 완성합니다.

## Phase 6 — Productization

- [ ] Hardware Case
- [ ] Wiring
- [ ] UX
- [ ] Demo
- [ ] BOM
- [ ] Pricing
- [ ] Final Pitch

---

# 💰 Business Model

초기 제품은 기존 옷장에 추가할 수 있는 **Retrofit Kit** 방향을 우선 검토합니다.

### PickFit Retrofit Basic

예상 가격 가설:

```text
₩299,000
```

- Presence Sensor
- Smart Rail
- Environment Monitoring
- LED Guide
- Digital Closet
- Basic Recommendation

### PickFit Mirror

예상 가격 가설:

```text
₩699,000
```

추가 기능:

- Smart Mirror
- Display
- Outfit Camera
- Lookbook
- Personalization
- Advanced Recommendation

### PickFit Premium

가격 가설:

```text
₩1,000,000+
```

추가 기능:

- Smart Cell
- Wear-Ready
- Advanced Care
- Automatic Retrieval

> 가격은 현재 사업 가설이며 BOM 및 시장 검증 이후 변경될 수 있습니다.

---

# 🔮 Future Work

- AI Outfit Image Analysis
- Virtual Try-On
- Personal Preference Learning
- Purchase History Auto Import
- Wardrobe Gap Analysis
- Purchase Compatibility
- Dead Stock Discovery
- Smart Cell
- Wear-Ready
- Automatic Retrieval
- Advanced Clothing Care
- Laundry Machine Integration
- Fashion Brand API
- Mobile Application

---

# 📂 Repository Structure

```text
0812team/
│
├── README.md
│
├── Smart_Wardrobe_MASTER_PRD.md
│
├── AIoT_Smart_Wardrobe_Launch_Final.pptx
│
├── 조원계획/
│   ├── AI Smart Closet 기획서.md
│   ├── Closet_Twin_AIOT_Project.md
│   ├── Smart_Wardrobe_PRD.md
│   ├── smart_hanger_proposal.md
│   └── ...
│
└── ...
```

`Smart_Wardrobe_MASTER_PRD.md`를 프로젝트의 통합 기획 기준 문서로 사용합니다.

---

# 🌿 Git Workflow

팀 프로젝트이므로 `main` 브랜치 직접 작업보다 기능별 Branch와 Pull Request를 사용합니다.

```text
main
│
├── feature/sensor
├── feature/iot
├── feature/backend
├── feature/recommendation
└── feature/frontend
```

기본 작업 흐름:

```bash
git checkout main
git pull origin main

git checkout -b feature/기능명

# 작업

git add .
git commit -m "feat: 작업 내용"
git push -u origin feature/기능명
```

이후 GitHub에서

```text
Feature Branch
↓
Pull Request
↓
Review
↓
Merge
↓
main
```

순으로 반영합니다.

---

# 🎯 Success Criteria

최종 Demo에서는 다음 Closed Loop가 실제로 동작하는 것을 목표로 합니다.

```text
옷 등록
↓
실제 옷 Presence 감지
↓
Digital Twin 동기화
↓
현재 착용 가능 의류 필터링
↓
날씨 / 사용자 Context 분석
↓
코디 추천
↓
추천 위치 LED 안내
↓
실제 옷 선택
↓
Presence State 변경
↓
실제 착장 촬영
↓
Outfit Event 생성
↓
사용자 평가
↓
다음 추천에 Feedback 반영
```

---

# 👔 PickFit

### Physical-Digital Twin Based AIoT Smart Wardrobe

> **Real Closet → Sensing → Digital Twin → Recommendation → Real Wearing → Feedback → Learning**

단순히 옷을 보관하는 가구를 넘어,  
**사용자의 실제 의생활을 이해하는 Personal Wardrobe Intelligence Platform**을 만드는 것이 우리의 목표입니다.
