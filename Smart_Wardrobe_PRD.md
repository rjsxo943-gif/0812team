# Smart Wardrobe PRD

## 1. 문서 개요

### 1.1 프로젝트명
**Smart Wardrobe**  
가칭: **PickFit**

### 1.2 프로젝트 목적
사용자의 실제 옷장을 디지털화하여 보유 의류의 **유무, 관리 상태, 착용 이력, 코디 이력**을 관리하고, 날씨·일정·개인 취향을 기반으로 실제 착용 가능한 의류 조합을 추천하는 AIoT 기반 스마트 옷장을 개발한다.

단순한 패션 추천 서비스가 아니라, **실제 옷장 안에 존재하는 옷과 그 옷의 현재 상태를 기반으로 추천한다는 점**을 핵심 차별점으로 한다.

---

## 2. 문제 정의

현재 패션 추천 서비스는 다음과 같은 한계가 있다.

1. 사용자가 실제로 보유한 옷을 정확하게 알지 못한다.
2. 특정 의류가 세탁 중인지, 착용 가능한 상태인지 판단하지 못한다.
3. 추천한 옷이 실제 옷장 어디에 있는지 알려주지 못한다.
4. 사용자가 실제로 해당 조합을 입었을 때 만족했는지 학습하기 어렵다.
5. 의류 관리와 코디 추천 서비스가 분리되어 있다.
6. 옷은 많지만 실제로 자주 입는 옷만 반복적으로 착용하는 경우가 많다.
7. 새 옷을 구매할 때 현재 보유 의류와 얼마나 잘 조합되는지 판단하기 어렵다.

Smart Wardrobe는 이를 하나의 시스템으로 통합한다.

---

## 3. 제품 비전

> **“내 옷장이 현재 가지고 있는 옷 중에서, 지금 실제로 입을 수 있는 가장 적합한 옷을 추천한다.”**

제품은 다음 네 가지 정보를 결합한다.

- **Physical Wardrobe** → 실제 옷의 존재 여부
- **Digital Twin** → 각 의류의 정보 및 현재 상태
- **Wear History** → 사용자가 실제로 입었던 코디 및 착장 사진
- **AI Recommendation** → 날씨, 일정, 취향, 과거 평가를 기반으로 한 개인화 추천

---

## 4. 핵심 가치

### 4.1 Real Wardrobe Based Recommendation
인터넷에 존재하는 임의의 옷이 아니라 **현재 사용자의 옷장 안에 실제 존재하는 옷**을 대상으로 추천한다.

### 4.2 Wearable State Awareness
옷의 존재 여부뿐만 아니라 현재 착용 가능 상태까지 고려한다.

예:
- CLEAN
- REWEARABLE
- NEED_WASH
- WASHING
- CARE_REQUIRED

### 4.3 Personal Look History
카메라를 통해 사용자가 해당 옷을 실제 착용한 모습을 기록한다.

이를 이용하여 개인 Lookbook을 생성한다.

### 4.4 Personalized Recommendation
사용자가 실제로 선택하고 평가한 코디 이력을 기반으로 추천을 개인화한다.

### 4.5 Wardrobe Digital Twin
물리적인 옷장을 디지털 환경에 복제하여 각 의류의 상태와 이력을 관리한다.

---

## 5. 목표 사용자

### Primary Target
일반 소비자

특히 다음 특성을 가진 사용자를 우선 대상으로 한다.

- 보유 의류가 많음
- 아침마다 코디 선택에 시간이 오래 걸림
- 자주 입는 옷만 반복해서 입음
- 패션에 관심은 있지만 코디 선택이 어려움
- 자신의 착장 기록을 남기고 싶음

### Secondary Target
의류 브랜드 / 의류 매장

향후 B2B 형태로 확장할 수 있다.

예:
- 보유 옷 기반 신규 상품 추천
- 매장 룩북 추천
- 기존 옷과 신규 상품의 조합 추천

---

## 6. 전체 시스템 구조

```text
사용자
 │
 ▼
Smart Mirror / Display
 │
 ├───────────────┐
 ▼               ▼
Recommendation   Lookbook
Engine            System
 │
 ▼
Digital Wardrobe DB
 │
 ├────────────────────────────┐
 ▼                            ▼
Garment State               Outfit History
 │
 ▼
IoT Controller
 │
 ├─────────┬─────────┬─────────┐
 ▼         ▼         ▼         ▼
Weight    Temp/     Door      LED
Sensor    Humidity  Sensor    Guide

                 Camera
                    │
                    ▼
              Outfit Capture
```

---

## 7. 의류 데이터 모델

각 의류는 하나의 `Garment Object`로 관리한다.

```text
GARMENT_ID : G0031

Identity
- Brand
- Product Name
- Category
- Color
- Material
- Size
- Product Image

Physical
- Wardrobe Slot
- Reference Weight
- Presence State

Care
- Care State
- Wear Count After Wash
- Maximum Recommended Wear
- Last Wash Date

Usage
- Total Wear Count
- Last Worn Date
- Average Rating

Recommendation
- Season
- Temperature Range
- Style
- Formality
- Color Group
```

---

## 8. 옷 등록 방식

### 8.1 브랜드 제품 검색

대형 브랜드 제품의 경우 사용자가 다음 정보를 검색한다.

- 제품명
- 모델명
- 제품 코드

시스템은 가능한 제품 정보를 자동으로 불러온다.

예:
- 브랜드
- 제품 이미지
- 카테고리
- 색상
- 소재

### 8.2 URL 기반 등록

소형 쇼핑몰 또는 일반 온라인 구매 제품의 경우 사용자가 상품 URL을 입력한다.

시스템은 접근 가능한 정보를 기반으로 다음 항목을 가져온다.

- 상품명
- 이미지
- 가격
- 색상
- 소재
- 카테고리

> 실제 서비스에서는 각 사이트의 API, 이용약관 및 데이터 접근 정책을 준수한다.

### 8.3 직접 등록

검색이나 URL 기반 등록이 불가능한 의류는 사용자가 직접 등록한다.

입력 예:
- 사진
- 종류
- 색
- 계절
- 소재
- 스타일

향후 이미지 분석 AI를 통해 일부 입력을 자동화할 수 있다.

---

## 9. 의류 상태 모델

의류 상태는 하나의 거대한 상태머신으로 관리하지 않고 다음 세 영역을 분리한다.

### 9.1 Presence State

물리적으로 옷장 안에 존재하는지를 의미한다.

상태:
```text
IN_WARDROBE
OUT
UNKNOWN
```

기본 전환:
```text
IN_WARDROBE
      │
      │ 옷 제거 감지
      ▼
     OUT
      │
      │ 옷 복귀 감지
      ▼
IN_WARDROBE
```

`OUT` 상태에서는 해당 옷이 실제로 착용 중인지, 세탁 중인지 등은 별도의 Care State를 통해 관리한다.

### 9.2 Care State

해당 의류를 현재 착용할 수 있는지 관리한다.

상태:
```text
CLEAN
REWEARABLE
NEED_WASH
WASHING
CARE_REQUIRED
```

예:
```text
CLEAN
 │
 │ 착용
 ▼
REWEARABLE
 │
 ├──────── 다시 착용
 │
 ▼
NEED_WASH
 │
 │ 세탁 시작
 ▼
WASHING
 │
 │ 세탁 완료
 ▼
CLEAN
```

옷 종류별 정책을 다르게 설정할 수 있다.

| 종류 | 추천 착용 횟수 |
|---|---:|
| 티셔츠 | 1 |
| 셔츠 | 1~2 |
| 청바지 | 3~5 |
| 자켓 | 5~10 |
| 코트 | 10회 이상 |

사용자는 시스템 추천을 직접 수정할 수 있다.

### 9.3 Outfit Event

착장 사진과 실제 코디 기록은 상태가 아니라 **Event History**로 관리한다.

```text
OUTFIT_EVENT #20260812-001

Date
2026-08-12

Top
G0012

Bottom
G0027

Outer
G0031

Weather
23°C / Cloudy

Purpose
School

Photo
IMG_20260812_001

Rating
5 / 5
```

---

## 10. 옷 유무 감지

카메라는 옷 유무 감지의 주 센서로 사용하지 않는다.

옷 유무는 물리 센서를 통해 판단한다.

검토 가능한 방식:

### Load Cell
옷걸이 또는 레일의 무게 변화로 존재 여부 판단.

### Individual Hanger Sensor
옷걸이 단위로 스위치 또는 압력 센서 적용.

### RFID / NFC
옷 또는 옷걸이에 태그를 부착하여 식별.

### Magnetic Sensor
옷걸이의 특정 위치 장착 여부 판단.

최종 센서 방식은 프로토타입 제작 과정에서 비교 실험 후 결정한다.

---

## 11. 카메라 기능

카메라의 핵심 목적은 **옷장 재고 판단이 아니라 착장 기록**이다.

### 11.1 Outfit Capture
사용자가 추천 코디를 실제로 착용한 후 거울 앞에서 사진을 촬영한다.

촬영 결과는 해당 Outfit Event와 연결된다.

### 11.2 Personal Lookbook
저장된 사진을 기반으로 사용자 개인 Lookbook을 제공한다.

```text
08/03
White Shirt + Jeans
★★★★★

08/07
Black Hoodie + Cargo Pants
★★★★☆

08/12
Grey Knit + Slacks + Jacket
★★★★★
```

### 11.3 Future AI Analysis
향후 AI를 활용하여 다음 분석을 수행할 수 있다.

- 전체적인 색상 조화
- 스타일 유형
- 기존 코디와 유사성
- 사용자가 자주 선택하는 조합
- 사용자의 선호 스타일

---

## 12. 추천 시스템

추천 시스템은 다음 요소를 이용한다.

```text
Outfit Score

= Weather Suitability
+ Style Compatibility
+ Color Compatibility
+ Garment Availability
+ Care State
+ User Preference
+ Previous Outfit Rating
+ Wear Frequency
```

---

## 13. 추천 필터

추천 과정의 첫 단계는 후보 제거이다.

다음 의류는 추천에서 제외한다.

- OUT
- NEED_WASH
- WASHING
- CARE_REQUIRED
- 계절 부적합 의류

이후 남은 의류 조합을 대상으로 점수를 계산한다.

---

## 14. 추천 입력 정보

사용자가 직접 선택할 수 있는 정보:

- 목적
- 스타일
- 포멀 정도
- 추위/더위 민감도

예:
```text
오늘 일정
학교

스타일
Casual

선호
조금 따뜻하게
```

외부 API:
- 현재 기온
- 최고/최저 기온
- 강수
- 습도
- 체감온도

---

## 15. 추천 결과

```text
오늘의 추천

상의
Grey Knit

하의
Black Slacks

아우터
Black Jacket

추천 점수
91 / 100

추천 이유
- 현재 14°C
- 강수 가능성 낮음
- Casual 설정
- 최근 14일간 미착용
- 유사 코디 만족도 4.7 / 5
```

실제 옷장에서는 추천된 의류 위치를 LED 등으로 표시할 수 있다.

---

## 16. 개인화 학습

사용자는 착장 후 다음 피드백을 입력한다.

기본 평가:
- ★★★★★
- 👍 / 👎

상세 평가:
- 핏이 좋음
- 색 조합이 좋음
- 너무 더움
- 너무 추움
- 불편함
- 상황에 맞지 않음

추천 시스템은 해당 데이터를 사용자 프로필에 반영한다.

---

## 17. Wardrobe Gap Analysis

보유 의류 데이터를 분석하여 부족한 카테고리나 색상을 파악한다.

```text
현재 옷장

Black Tops    7
White Tops    5
Grey Tops     4

Black Pants   5
Blue Pants    4
Beige Pants   0
```

시스템:

> 베이지 팬츠를 추가하면 현재 보유 의류와 구성 가능한 추천 조합이 증가합니다.

이를 이용해 신규 의류를 추천할 수 있다.

---

## 18. 구매 추천

단순 광고가 아니라 **현재 보유 의류와의 Compatibility**를 기반으로 추천한다.

```text
Recommended Purchase

Beige Chino Pants

현재 옷과 생성 가능한 추가 코디
+14

Compatibility
92%

현재 옷장 부족 카테고리
Neutral Bottom
```

향후 브랜드 API 또는 쇼핑 플랫폼과 연결할 수 있다.

---

## 19. Smart Mirror / Display

옷장 문에는 거울과 디스플레이를 결합할 수 있다.

주요 화면:

### Home
- 시간
- 날짜
- 날씨
- 옷장 상태

### Today's Outfit
- 추천 코디
- 추천 이유

### Wardrobe
- 현재 보유 옷
- 세탁 필요
- 외부에 있는 옷

### Lookbook
- 과거 착장

### Environment
- 온도
- 습도
- 공기질

---

## 20. 생활 정보

부가기능으로 다음 정보를 표시할 수 있다.

- 날씨
- 일정
- 대중교통
- 출근/등교 정보

대중교통 정보는 제품 핵심 기능이 아닌 Convenience Feature로 분류한다.

---

## 21. 옷장 환경 관리

센서를 이용하여 옷장 내부 환경을 측정한다.

측정 항목:
- 온도
- 습도
- VOC / 공기질

```text
Wardrobe Environment

Temperature
22.1°C

Humidity
67%

Air Quality
Good

Condition Score
86 / 100
```

---

## 22. Smart Care

프로토타입에서는 스타일러 전체 기능을 구현하지 않는다.

대신 다음 기능을 목표로 한다.

- 자동 환기
- 습도 관리
- 내부 환경 모니터링
- 관리 필요 알림

향후 상용 제품에서는:
- 건조
- 탈취
- 스팀
- 주름 관리

기능으로 확장 가능하다.

---

## 23. Privacy

옷장은 침실 등에 설치될 수 있으므로 카메라 보안을 핵심 요구사항으로 정의한다.

### 기본 원칙

#### Camera On Indicator
카메라 작동 시 물리 LED를 통해 사용자에게 명확하게 표시한다.

#### Manual Capture
기본 제품에서는 사용자가 명시적으로 착장 촬영을 요청했을 때만 사진을 촬영한다.

#### Local First
가능하면 착장 사진과 영상 처리를 로컬 환경에서 수행한다.

#### User Control
사용자는 언제든 다음 기능을 수행할 수 있다.

- 사진 삭제
- 카메라 비활성화
- 자동 촬영 비활성화

---

## 24. IoT

Smart Wardrobe Controller는 외부 시스템과 통신한다.

지원 후보:
- Wi-Fi
- Ethernet
- Bluetooth

프로토타입에서는 Wi-Fi 또는 PC USB 연결을 우선 검토한다.

---

## 25. 옷장 크기

완성 제품은 옷장 크기에 따라 여러 모델을 제공할 수 있다.

### Compact
1인 가구용

### Standard
일반 가정용

### Large
대형 옷장용

---

## 26. Retrofit 전략

옷장 전체를 새로 구매하는 대신 기존 옷장에 설치할 수 있는 확장형 제품도 고려한다.

### Smart Wardrobe Retrofit Kit

구성:
- Smart Hanger Rail
- Presence Sensor
- Environment Sensor
- Camera
- Controller
- Display

옷장 크기에 따라 Rail 및 센서 수만 조절한다.

제품 사업화 시 완성형 옷장보다 시장 접근성이 높을 수 있다.

---

## 27. MVP

프로젝트에서 반드시 구현해야 하는 최소 기능.

- MVP-01: 의류 등록
- MVP-02: 각 의류의 옷장 내 존재 여부 확인
- MVP-03: Presence State 관리
- MVP-04: Care State 관리
- MVP-05: 날씨 정보 수집
- MVP-06: 보유 의류 기반 코디 추천
- MVP-07: 추천 의류 위치 표시
- MVP-08: 착장 카메라 촬영
- MVP-09: Outfit History 저장
- MVP-10: 착장 사용자 평가
- MVP-11: 옷장 온습도 측정
- MVP-12: 기본 Smart Mirror / Dashboard

---

## 28. Should Have

시간이 허용될 경우 구현한다.

- 개인화 추천
- 착용 횟수 기반 세탁 알림
- Wardrobe Gap Analysis
- 의류 URL 자동 등록
- 미착용 의류 추천
- 공기질 측정
- 대중교통 API
- 일정 연동
- 옷장 자동 환기

---

## 29. Future Work

장기 확장 항목.

- AI 착장 분석
- AI 이미지 기반 의류 자동 등록
- Virtual Try-On
- 브랜드 상품 API 연동
- 구매 추천
- 모바일 앱
- 사용자별 프로필
- 가족 옷장
- 세탁기 연동
- 완전 자동 스타일러
- 스마트홈 플랫폼 연동

---

## 30. 5인 팀 역할 예시

### Member 1 — Embedded / Sensor
- Arduino
- Presence Sensor
- 환경센서
- LED
- 장치 제어

### Member 2 — IoT / Communication
- MCU-PC 통신
- Wi-Fi
- API
- Device Protocol

### Member 3 — Backend / Data
- Garment DB
- State Machine
- Outfit History
- API Server

### Member 4 — AI / Recommendation
- 코디 추천
- 개인화
- Wardrobe Gap Analysis

### Member 5 — Frontend / System Integration
- Smart Mirror UI
- Dashboard
- Lookbook
- 전체 시스템 통합

---

## 31. 핵심 시연 시나리오

### Step 1
사용자가 옷장 앞에 선다.

```text
오늘 14°C
오후 비 예상
```

### Step 2
사용자가 선택한다.

```text
목적
학교

스타일
Casual
```

### Step 3
시스템이 현재 옷 상태를 확인한다.

```text
등록 의류
32

옷장 내 존재
27

세탁 중
2

세탁 필요
3
```

### Step 4
추천 시스템 실행.

```text
Today's Outfit

Grey Knit
Black Pants
Black Jacket
```

### Step 5
실제 옷장에서 해당 옷 위치에 LED가 켜진다.

### Step 6
사용자가 옷을 꺼낸다.

```text
G003
IN_WARDROBE → OUT
```

### Step 7
사용자가 추천 코디를 착용한다.

거울 앞에서 **오늘 착장 저장** 선택.

### Step 8
카메라 촬영 후 Outfit Event 생성.

### Step 9
사용자가 착장을 평가한다.

```text
★★★★★
```

### Step 10
해당 정보가 향후 추천에 반영된다.

---

## 32. 핵심 차별점

기존 AI 패션 추천:

> 오늘 같은 날에는 니트와 청바지를 추천합니다.

Smart Wardrobe:

> 현재 사용자의 옷장에 실제 존재하며 세탁 가능한 상태인 27벌 중에서 오늘 날씨와 사용자의 선호를 고려해 Grey Knit + Black Pants 조합을 추천합니다.

그리고 사용 후:

> 사용자가 이 조합을 실제 착용했고 만족도 5점을 기록했습니다.

즉,

**Recommendation → Physical Selection → Real Wearing → Feedback → Learning**

이라는 Closed Loop 구조를 가진다.

---

## 33. 제품 포지셔닝

Smart Wardrobe는 단순한 스마트 가구가 아니다.

다음 세 제품의 결합 형태로 정의한다.

**Wardrobe Management System**

+

**Personal Styling Assistant**

+

**Smart Home Furniture**

---

## 34. 사업 모델

### Hardware
Smart Wardrobe 또는 Retrofit Kit 판매.

### Premium Software
고급 개인화 추천 및 데이터 분석.

### Commerce
보유 의류 기반 신규 상품 추천.

### B2B
의류 브랜드 또는 리테일 매장과 연동.

---

## 35. 초기 가격 가설

프로젝트 단계의 초기 가설이며 BOM 확정 후 재산정한다.

### Retrofit Basic
**₩199,000 ~ ₩299,000**

- 의류 존재 감지
- 환경센서
- 기본 추천
- Dashboard

### Smart Wardrobe Standard
**₩399,000 ~ ₩699,000**

- Smart Mirror
- 카메라
- 개인 Lookbook
- AI 추천
- 환경관리

### Premium
**₩1,000,000+**

- 옷장 포함
- 고급 Care System
- 대형 디스플레이
- 고급 센서 및 자동화

---

## 36. 프로젝트 성공 기준

프로젝트 완료 시 다음 시나리오가 실제 동작해야 한다.

1. 사용자가 옷을 등록할 수 있다.
2. 시스템이 옷장에 어떤 옷이 존재하는지 확인할 수 있다.
3. 각 옷의 Care State를 관리할 수 있다.
4. 현재 날씨를 반영할 수 있다.
5. 실제 존재하고 착용 가능한 옷만 추천할 수 있다.
6. 추천된 옷을 사용자가 실제 옷장에서 찾을 수 있다.
7. 추천 코디를 착용한 모습을 촬영할 수 있다.
8. 착장 기록을 Lookbook에서 확인할 수 있다.
9. 사용자의 평가를 저장할 수 있다.
10. 이후 추천에 과거 데이터를 활용할 수 있다.

---

## 37. 프로젝트 핵심 문장

> **Smart Wardrobe는 사용자의 실제 보유 의류와 각 의류의 현재 상태를 Digital Twin으로 관리하고, 날씨·일정·착용 이력·개인 취향을 결합하여 현재 실제로 입을 수 있는 최적의 코디를 추천하고 그 착장 경험까지 기록·학습하는 AIoT 기반 스마트 옷장 시스템이다.**

---

## 38. 프로젝트 핵심 키워드

- AIoT
- Digital Twin
- Smart Furniture
- Personalization
- Recommendation System
- State Machine
- Smart Mirror
- Wearable Data
- DX
- AX
