# 👔 PickFit — AIoT Smart Wardrobe / Closet Twin

> **실제 옷장 상태를 디지털화하고, 지금 사용할 수 있는 옷을 추천해 실제 옷장에서 안내하는 스마트 옷장 시스템**

PickFit은 사용자의 실제 보유 의류와 Smart Wardrobe의 물리 상태를 연결하는 **AIoT 기반 Smart Wardrobe 프로젝트**입니다.

단순히 앱에 등록된 의류를 추천하는 것이 아니라,

- 사용자가 실제로 어떤 옷을 보유하고 있는지
- 현재 Smart Wardrobe에 어떤 옷이 배치되어 있는지
- 해당 옷이 Assigned Slot에 실제로 존재하는지
- 최근 실제로 어떤 옷을 착용했는지
- 현재 보관환경과 Care State가 어떤지

를 Cloud의 **Closet Twin**과 이력 데이터로 관리하고, 그 상태를 기반으로 Outfit을 추천한 뒤 **Assigned Smart Slot의 LED로 실제 의류 선택까지 연결**하는 것을 목표로 합니다.

---

## 📌 Current Status

**Planning Freeze v1.0 완료 → Phase 1 PoC 준비 단계**

현재 프로젝트의 최우선 목표는 기능을 계속 추가하는 것이 아니라 다음 End-to-End Closed Loop를 실제 환경에서 검증하는 것입니다.

```text
Registration
    ↓
Digital Garment Inventory
    ↓
Assigned Smart Slot Binding
    ↓
Presence IN / OUT
    ↓
Arduino Nano ESP32
    ↓
MQTT over TLS
    ↓
Cloud Closet Twin
    ↓
Available Filter / Outfit Recommendation
    ↓
LED Guide
    ↓
Wear Confirm Session
    ↓
Wear History / Care / Feedback
```

Phase 1에서는 **AI 추천의 우수성보다 Registration → Physical State → Cloud → LED → Wear Confirm이 하나의 Closed Loop로 동작하는지**를 우선 검증합니다.

---

## 📚 Project Baseline

현재 기획의 기준은 다음 순서로 봅니다.

| 문서 | 역할 |
|---|---|
| `PickFit_회사내부_제품기획서_v1.0_Planning_Freeze.docx` | **현재 Planning Freeze 기준 문서** |
| `README.md` | 저장소 전체 개요 및 현재 상태 |
| `CLOUD_IOT_ARCHITECTURE.md` | Cloud / IoT 통신 조사 및 설계 근거 |
| `AIoT_Smart_Wardrobe_Launch_수정.pptx` | 발표 자료 |
| `Smart_Wardrobe_MASTER_PRD.md` | 초기 통합 기획안 / 이전 단계 참고자료 |
| `조원계획/` | 초기 아이디어·팀원별 기획·조사 참고자료 |

> `Smart_Wardrobe_MASTER_PRD.md`와 `조원계획/`의 일부 내용은 Planning Freeze 이전 아이디어를 포함할 수 있습니다. 충돌할 경우 **Planning Freeze v1.0을 우선**합니다.

---

# 🎯 Product Concept

PickFit의 핵심은 **AI 코디 자체가 아니라 Physical Wardrobe State와 Digital Data를 연결하는 것**입니다.

```text
SENSE
현실 옷장의 상태를 감지

↓

REMEMBER
Closet Twin과 History에 상태를 기록

↓

RECOMMEND
현재 실제로 사용할 수 있는 의류 중 Outfit 추천

↓

GUIDE
Assigned Smart Slot LED로 실제 의류 안내
```

---

# 🧩 Core Design Principles

## 1. Sensor Fact와 의미를 분리한다

Sensor가 알 수 있는 것은 물리적인 상태 변화입니다.

```text
Slot H03 = OUT
```

이 사실만으로 사용자가 실제로 옷을 입었다고 판단하지 않습니다.

```text
OUT ≠ WEARING
```

실제 착용 여부는 **Wear Confirm Session**에서 사용자가 확정합니다.

---

## 2. Product와 Garment를 분리한다

외부 상품 식별정보와 사용자가 실제 보유한 한 벌은 다른 Entity입니다.

```text
External Product ID / GTIN
            ≠
     PickFit Garment ID
```

동일 상품·색상·사이즈의 옷을 여러 벌 보유하더라도 각각 별도의 `Garment ID`를 생성합니다.

---

## 3. Assigned Slot을 사용하고 자동 위치 추적은 하지 않는다

Smart Slot은 다음 Mapping을 위한 내부 단위입니다.

```text
Slot ID
├─ Sensor Channel
├─ LED Channel
└─ Bound Garment
```

Presence Sensor는 의류의 Identity를 판별하지 않습니다.

다른 Slot으로 옷을 옮긴 경우 자동 위치 추론 대신 **Re-Binding**으로 수정합니다.

---

## 4. Arduino와 Cloud의 책임을 분리한다

```text
Arduino Nano ESP32
= Sensor Read / Debounce / Event / Wi-Fi / MQTT / Local Output

Cloud
= User Data / Product & Garment / Closet Twin / History
  / Weather / Recommendation / AI
```

Arduino는 물리 상태를 관찰하고 Event를 생성하며, Cloud는 사용자 Context와 서비스 로직을 관리합니다.

---

## 5. AI가 Physical Fact를 결정하지 않는다

AI는 다음 영역을 보조합니다.

- Garment Attribute 제안
- Wardrobe Profile 초안
- Outfit Ranking
- Recommendation Explanation / Personalization

반면 Presence, Assigned Slot Binding 같은 Physical Fact는 Sensor와 명시적인 상태 모델이 관리합니다.

---

# 🏗 System Architecture

```text
┌────────────────────────────────────┐
│            Web / App UI            │
│ Registration · Profile · Recommend │
│ Wear Confirm · Care · Feedback     │
└────────────────┬───────────────────┘
                 │ HTTPS REST API
                 ▼
┌────────────────────────────────────┐
│           CLOUD / SYSTEM           │
│ User / Device Management           │
│ Product / Garment Inventory        │
│ Wardrobe Profile                   │
│ Closet Twin Current State          │
│ Presence / Wear History            │
│ Care / Weather / Recommendation    │
└────────────────┬───────────────────┘
                 │ MQTT over TLS
       Event ↑   │   ↓ Command
                 │
┌────────────────────────────────────┐
│       Arduino Nano ESP32           │
│ Sensor Read · Debounce · Event     │
│ Wi-Fi · MQTT Client · LED Control  │
│ Local Queue / Reconnect            │
└────────────────┬───────────────────┘
                 │
                 ▼
┌────────────────────────────────────┐
│         PHYSICAL WARDROBE          │
│ Smart Slot / Presence Sensor       │
│ Temperature / Humidity Sensor      │
│ LED Guide                          │
│ Optional User-initiated Camera     │
└────────────────────────────────────┘
```

### Communication

```text
Device ↔ Cloud   : MQTT over TLS
Web/App ↔ Cloud  : HTTPS REST API
```

중요 Event는 `eventId`, `sequence`, `observedAt` 등을 사용하고, 네트워크 단절 시 Edge Local Queue에 임시 보존한 뒤 재연결 후 전송하는 구조를 검증합니다.

Cloud → Device 명령은 `commandId`, `expiresAt`, ACK를 사용하며 가능한 한 `SET_LED ON/OFF`와 같은 멱등 명령으로 설계합니다.

---

# 👕 Digital Garment Inventory

PickFit은 **전체 보유 의류**와 **현재 Smart Wardrobe에 배치된 의류**를 분리합니다.

```text
Digital Garment Inventory
│
├─ ACTIVE
│   현재 Smart Wardrobe에 배치
│
└─ STORED
    서랍 / 창고 / 리빙박스 등 외부 보관
```

`STORED` 상태에는 선택적으로 자유 입력 `Storage Label`을 사용할 수 있습니다.

---

# 🗂 Wardrobe Profile

Wardrobe Profile은 제한된 Smart Slot에 어떤 Garment를 배치할지 저장하는 Preset입니다.

예:

```text
Summer
Work
Daily
Travel
Custom
```

Profile의 Garment 수가 실제 Slot Capacity보다 많으면 시스템은 자리 부족을 알리고 제외 후보를 제안합니다.

Profile을 선택했다고 즉시 상태를 변경하지 않고, 사용자가 실제 옷장 재배치를 완료한 후 **`세팅 완료`**를 눌렀을 때 ACTIVE/STORED와 Slot Binding을 갱신합니다.

---

# 📝 Garment Registration

PickFit은 하나의 등록 방식에 종속되지 않는 **Adaptive Hybrid Registration** 구조를 사용합니다.

```text
Barcode / QR ─┐
              │
판매 URL ──────┼─→ Product Metadata Prefill
              │
Manual ────────┘
                    ↓
             User Confirmation
                    ↓
          누락 Field만 직접 보완
                    ↓
            Product Record
                    ↓
          PickFit Garment ID
                    ↓
          Smart Slot Binding
```

### Registration Principle

- Barcode 자체에 모든 상품정보가 들어 있다고 가정하지 않음
- 모든 QR이 Product 정보를 제공한다고 가정하지 않음
- 모든 쇼핑몰 URL을 자동 분석한다고 주장하지 않음
- External Product Data는 **Prefill Source**로 사용
- 잘못되거나 누락된 Field는 사용자가 확인·수정
- 자동 등록 실패 시 전체를 다시 입력하지 않고 **Field-level Fallback** 적용

---

# 🔄 Presence & Wear Confirm

```text
ACTIVE Garment
      ↓
Assigned Slot = IN
      ↓
사용자가 옷을 꺼냄
      ↓
Presence Event = OUT
      ↓
Wear Confirm 후보 Session
      ↓
사용자가 "착용 완료"
      ↓
실제로 입은 Garment만 선택
      ↓
Wear Event 생성
```

Wear Event가 확정되면 다음 값들을 갱신할 수 있습니다.

- Total Wear Count
- Wear Count Since Wash
- Last Worn
- Wear History
- Implicit Feedback

---

# 🧼 Care

## Garment Care State

```text
CLEAN
REWEARABLE
NEED_WASH
```

`NEED_WASH`는 절대적인 위생 판정이 아니라 **세탁 권장 상태**입니다.

기본 Rule은 Category별 기준으로 제공하고 사용자가 수정할 수 있도록 설계합니다.

### Environment Care — MVP

- Temperature Monitoring
- Humidity Monitoring
- Environment Warning
- Management Alert

### Future

- Automatic Ventilation
- Dehumidification
- Drying / Heating
- Advanced Material Care

---

# 🧠 Outfit Recommendation

추천은 처음부터 모든 판단을 AI에 맡기지 않습니다.

```text
Closet Twin
    ↓
Hard Filter
    ↓
Candidate Outfit
    ↓
Rule / Weighted Scoring
    ↓
AI-assisted Ranking / Explanation
```

### Hard Filter Example

```text
ACTIVE == true
AND Presence == IN
AND Care State != NEED_WASH
```

### Context

- Weather: 자동 반영
- Occasion: 선택 입력
- Garment Attribute
- Wear History
- User Preference / Feedback

MVP에서는 실제로 입을 수 있는 후보를 먼저 만든 뒤 **Outfit 1개를 추천**하는 단순 구조를 우선합니다.

---

# 💡 LED Guide

추천된 Garment는 Assigned Slot과 연결된 LED로 안내합니다.

```text
Outfit Recommendation
        ↓
Garment ID
        ↓
Assigned Slot
        ↓
LED Command
        ↓
Arduino Nano ESP32
        ↓
Slot LED ON
```

LED Guide는 자동 위치 추적이 아니라 **현재 Binding된 Assigned Slot을 물리적으로 안내하는 기능**입니다.

---

# 📸 Camera Strategy

Camera는 MVP의 핵심 Presence Sensor가 아닙니다.

MVP에서 Camera를 사용하는 경우 **사용자가 명시적으로 실행하는 Optional Outfit Capture**로 제한합니다.

```text
Wear Confirm
    ↓
[오늘 착장 저장]
    ↓
User-initiated Camera Capture
    ↓
Lookbook / Outfit History
```

다음 기능은 Future Scope입니다.

- Camera 기반 자동 Garment Identification
- Vision AI Inventory
- Continuous Surveillance

---

# ✅ MVP Scope

## Must Have

- Adaptive Hybrid Garment Registration
- Field-level Manual Fallback
- Product ID / Garment ID 분리
- Digital Garment Inventory
- ACTIVE / STORED
- Wardrobe Profile / Capacity Check
- Assigned Smart Slot Binding / Re-Binding
- Presence IN / OUT
- Arduino Nano ESP32
- MQTT over TLS Event / Command
- Cloud Closet Twin Current State
- Event / History 분리
- Wear Confirm Session
- Wear History
- Basic Garment Care State
- Temperature / Humidity Monitoring
- Weather Context
- Available Garment Hard Filter
- Outfit Recommendation
- Assigned Slot LED Guide
- User Feedback

## Optional Demo Layer

- Web Dashboard
- Smart Mirror UI
- User-initiated Outfit Camera
- Lookbook
- User-configured Morning Recommendation

## Future

- RFID/NFC/Camera 기반 자동 Garment Identity
- 자유 위치 이동 / 자동 위치 추적
- Virtual Try-On
- Accessory Inventory
- Advanced Personalization AI
- Automatic Care
- Shopping / Brand Integration
- No-Buy AI
- Smart Home Integration
- Built-in Smart Wardrobe
- 범용 Retrofit 규격

---

# 🔬 Phase 1 PoC

Phase 1에서는 다음을 실제 환경에서 측정합니다.

| Area | 주요 검증 항목 |
|---|---|
| Registration | Field 반환율, 평균 등록시간, 수정 Field 수, Manual 전환율 |
| Physical State | Presence Event 반복성, 누락/오검출 패턴, Debounce, Binding 오류 |
| MQTT Closed Loop | Event 전달, Offline Queue, Reconnect, Command/ACK, Deduplication |
| UX | Profile 전환, Capacity 안내, Wear Confirm, Re-Binding, LED Guide |
| Retrofit Installation | 설치 시간, 배선/전원, Slot 수, Pin/Power Budget |

### Phase 1 성공 기준

```text
Registration
→ Assigned Slot Binding
→ Presence Event
→ MQTT
→ Closet Twin
→ Outfit Candidate
→ LED Guide
→ Wear Confirm Session
→ History
```

위 흐름이 기준 설치 환경에서 End-to-End로 연결되는지를 우선 확인합니다.

### Phase 1에서 아직 증명하지 않는 것

- AI 추천이 기존 서비스보다 우수한지
- 모든 옷장에 Retrofit 가능한지
- 상용 서비스 규모의 서버 성능
- 완전 자동 Garment Identification
- 검증되지 않은 정확도 / 성능 수치

---

# 🛠 Current Technical Direction

### Edge

```text
Arduino Nano ESP32
ESP32-S3
2.4 GHz Wi-Fi
```

### Hardware

```text
Presence Sensor        : PoC에서 최종 방식 선정
Temperature/Humidity   : MVP
LED Guide              : MVP
Door Sensor            : Optional Context
Camera                 : Optional User-initiated Capture
```

> Nano ESP32 GPIO는 3.3 V Logic 기준입니다. 5 V Logic Sensor와 고전류 LED/Motor/Relay/Fan은 Level/Driver Interface 없이 직접 연결하지 않습니다.

### Communication

```text
Device ↔ Cloud  : MQTT over TLS
Web/App ↔ Cloud : HTTPS REST API
```

### Recommendation

```text
Hard Rule
→ Candidate Generation
→ Weighted Scoring
→ AI-assisted Ranking / Explanation
```

Cloud Provider, DB 제품, MQTT Broker, Presence Sensor 모델, Slot 수, I/O Expansion, Pin/Power Budget 등은 PoC/구현 단계에서 확정합니다.

---

# 🗺 Development Roadmap

## Phase 0 — Planning ✅

- [x] Product Concept
- [x] Reality Check
- [x] Architecture Core
- [x] Adaptive Hybrid Registration
- [x] Digital Inventory / Wardrobe Profile
- [x] MQTT Device–Cloud 방향
- [x] MVP / Future 분리
- [x] Planning Freeze v1.0

## Phase 1 — PoC ⏳

- [ ] Registration PoC
- [ ] Presence Sensor / Slot PoC
- [ ] Arduino Nano ESP32 Firmware
- [ ] MQTT Closed Loop
- [ ] Closet Twin Sync
- [ ] Profile / Capacity UX
- [ ] Wear Confirm Session
- [ ] LED Guide
- [ ] Retrofit 설치 기준 검증

## Phase 2 — MVP

- [ ] Inventory / Profile 연결
- [ ] Care State
- [ ] Garment Attribute
- [ ] Weather / Occasion Context
- [ ] Outfit Recommendation
- [ ] End-to-End MVP

## Phase 3 — Improvement

- [ ] Recommendation / Care Rule 개선
- [ ] Attribute / Profile UX 개선
- [ ] 실제 사용 데이터 기반 개선

## Phase 4 — Productization Review

- [ ] BOM / Cost
- [ ] Stability
- [ ] Privacy Policy
- [ ] Installation / Retrofit Compatibility
- [ ] Operations
- [ ] Productization Decision

---

# 📂 Repository Structure

현재 `main` 기준 주요 파일 구조입니다.

```text
0812team/
│
├── README.md
├── PickFit_회사내부_제품기획서_v1.0_Planning_Freeze.docx
├── AIoT_Smart_Wardrobe_Launch_수정.pptx
├── CLOUD_IOT_ARCHITECTURE.md
├── Smart_Wardrobe_MASTER_PRD.md
│
├── 조원계획/
│   ├── AI Smart Closet 기획서.md
│   ├── Closet_Twin_AIOT_Project.md
│   ├── Smart_Wardrobe_PRD.md
│   ├── smart_hanger_proposal.md
│   └── ...
│
└── 기타 조사 / 기획 산출물
```

---

# 🌿 Git Workflow

팀 프로젝트에서는 `main` 직접 작업보다 **Feature Branch → Pull Request → Merge** 흐름을 권장합니다.

```bash
git switch main
git pull origin main

git switch -c feature/<task-name>

# 작업 후
git add .
git commit -m "feat: describe change"
git push -u origin feature/<task-name>
```

GitHub에서 Pull Request를 생성하고 검토 후 `main`에 Merge합니다.

Office 임시파일은 저장소에 포함하지 않습니다.

```gitignore
~$*
```

---

# 👥 Team

본 프로젝트는 **5인 팀 프로젝트**입니다.

현재 단계에서는 팀원별 조사·기획 결과를 통합하여 Planning Freeze를 완료했고, 이후 Phase 1 PoC에서는 Registration / Hardware / IoT / Cloud / UX Closed Loop 단위로 구현 및 검증 작업을 분담합니다.

---

# 📌 Project Message

> **PickFit은 AI가 옷장을 추측하는 시스템이 아니라, 현실 옷장의 상태를 먼저 디지털화하고 그 신뢰 가능한 상태 위에서 추천과 물리적 안내를 제공하는 시스템입니다.**

```text
PHYSICAL WARDROBE
        ↓
SENSE
        ↓
ARDUINO EVENT
        ↓
CLOSET TWIN
        ↓
OUTFIT RECOMMENDATION
        ↓
LED GUIDE
        ↓
WEAR CONFIRM
        ↓
HISTORY / FEEDBACK
```

**Current Gate: Planning Freeze v1.0 → Phase 1 PoC**
