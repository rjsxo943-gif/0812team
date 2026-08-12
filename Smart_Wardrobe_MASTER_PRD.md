# Smart Wardrobe Master PRD & Business Plan
## AIoT 기반 Physical-Digital Twin 스마트 옷장 통합 기획서

> **문서 성격:** 프로젝트 최종 기준 기획안(Master Planning Document)  
> **프로젝트 가칭:** PickFit / Smart Wardrobe  
> **작성 기준일:** 2026-08-12  
> **팀 규모:** 5명  
> **현재 단계:** 기획 / 시장검증 / 기술 타당성 검토

---

# 0. Executive Summary

Smart Wardrobe는 단순히 "AI가 오늘 입을 옷을 추천하는 서비스"가 아니다.

본 프로젝트는 **실제 옷장에 어떤 옷이 존재하는지, 현재 그 옷을 다시 입을 수 있는지, 사용자가 과거에 어떤 조합으로 실제 착용했는지**를 하나의 Digital Twin으로 관리하고, 이를 날씨·일정·개인 취향과 결합하여 실제 착용 가능한 코디를 추천하는 **AIoT 기반 Physical Wardrobe Platform**을 목표로 한다.

핵심 흐름은 다음과 같다.

```text
실제 옷
   ↓
Presence Sensor
   ↓
Physical Wardrobe State
   ↓
Digital Twin
   ↓
Care / Usage / Outfit History
   ↓
Weather + Schedule + Preference
   ↓
AI / Recommendation Engine
   ↓
추천 코디
   ↓
Smart Mirror / Physical Guide
   ↓
실제 착용
   ↓
Camera Outfit Capture
   ↓
Feedback / Lookbook
   ↓
Personalization
```

핵심 차별점은 **AI 코디 자체가 아니라 Physical Wardrobe Awareness**이다.

> **“AI가 옷을 추천한다”가 아니라  
> “현재 내 실제 옷장에 존재하고, 지금 입을 수 있는 옷만을 대상으로 추천한다.”**

---

# 1. 프로젝트 정의

## 1.1 프로젝트명

### 공식 가칭
**Smart Wardrobe**

### 제품 브랜드 후보
**PickFit**

### 기술 프로젝트명 후보
**Wardrobe Twin**

---

## 1.2 One-Line Definition

> **사용자의 실제 보유 의류의 존재·관리·착용 상태를 Digital Twin으로 관리하고, 날씨·일정·착용 이력·개인 취향을 결합해 현재 실제로 입을 수 있는 코디를 추천하고 그 착장 경험까지 기록·학습하는 AIoT 스마트 옷장 시스템.**

---

# 2. 문제 정의

사용자는 실제 생활에서 다음 문제를 겪는다.

## 2.1 옷은 많은데 실제로 무엇이 있는지 기억하기 어렵다

- 보유 의류가 많아질수록 전체 구성을 기억하기 어려움
- 자주 입는 옷만 반복 착용
- 장기간 입지 않는 Dead Stock 발생

## 2.2 디지털 옷장과 현실 옷장이 쉽게 불일치한다

일반 디지털 옷장 서비스는 사용자가 직접 옷을 등록하고 관리해야 한다.

그러나 현실에서는:

- 옷을 입고 외출
- 세탁
- 수선
- 여행
- 대여
- 분실

등이 발생하면서 앱의 데이터와 실제 옷장 상태가 달라질 수 있다.

## 2.3 기존 코디 추천은 "현재 입을 수 있는가"를 충분히 반영하지 못한다

추천 시스템에 해당 옷이 등록되어 있더라도 실제로는:

- 세탁 중
- 세탁 필요
- 옷장 밖에 있음
- 수선 중
- 관리 필요

일 수 있다.

## 2.4 사용자의 실제 착장 경험이 충분히 데이터화되지 않는다

"어떤 옷을 보유하고 있는가"와

"내가 그 옷을 실제로 어떻게 입었고 만족했는가"

는 다른 데이터다.

## 2.5 신규 의류 구매 시 기존 옷장과의 호환성을 알기 어렵다

예:

- 이미 비슷한 검정 후드가 3벌 있음
- 사고 싶은 바지가 현재 보유 상의 대부분과 어울리지 않음
- 활용도 낮은 옷을 반복 구매

---

# 3. Product Vision

Smart Wardrobe의 핵심 질문은 다음과 같다.

> **“오늘 내가 실제로 입을 수 있는 옷 중에서 무엇을 입는 것이 가장 좋은가?”**

이를 위해 시스템은 네 가지 세계를 연결한다.

### 1. Physical Wardrobe
실제 옷의 존재와 위치

### 2. Digital Twin
각 옷의 정보·상태·이력

### 3. Wear Experience
실제 착장 사진·평가·날씨·상황

### 4. AI Recommendation
현재 조건과 과거 경험을 이용한 추천

---

# 4. 핵심 설계 원칙

## 4.1 센서가 확실히 알 수 있는 사실과 추정 정보를 분리한다

예를 들어 옷이 옷장에서 사라졌다고 해서 시스템이 곧바로:

> "사용자가 착용 중이다"

라고 단정해서는 안 된다.

센서가 아는 사실은:

> `IN_WARDROBE → OUT`

뿐이다.

착용 여부, 세탁 여부 등은 별도의 이벤트와 상태로 관리한다.

---

## 4.2 카메라와 Presence Sensor의 책임을 분리한다

### Presence Sensor의 역할
**옷의 유무 / 물리적 상태 감지**

후보:
- Load Cell
- RFID / NFC
- Hanger Switch
- Magnetic Sensor
- 기타 개별 슬롯 센서

### Camera의 핵심 역할
**사용자가 실제로 해당 옷을 착용한 모습 기록**

즉:

```text
Presence Sensor
= "옷이 어디 있는가?"

Camera
= "내가 이 옷을 어떻게 입었는가?"
```

카메라를 재고 판단의 주 센서로 사용하지 않는다.

---

## 4.3 하나의 거대한 상태머신을 만들지 않는다

의류의 "상태"는 서로 다른 의미를 가진다.

따라서 최소 다음 영역을 분리한다.

1. Presence State
2. Care State
3. Outfit / Usage Event History
4. Environment State

---

# 5. 핵심 시스템 구조

```text
┌──────────────────────── SMART WARDROBE ────────────────────────┐

                      [ 사용자 ]

                          │
                          ▼

                ┌──────────────────┐
                │ Smart Mirror / UI│
                └────────┬─────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Recommendation            Lookbook
          Engine                 / History
             │                       │
             └───────────┬───────────┘
                         ▼

                 ┌────────────────┐
                 │ Digital Twin DB│
                 └───────┬────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
  Presence State     Care State      Usage / Outfit
                                        History

                         │
                         ▼

                 ┌────────────────┐
                 │ IoT Controller │
                 └───────┬────────┘
                         │
        ┌──────────┬─────┼─────┬──────────┐
        ▼          ▼     ▼     ▼          ▼
      Weight      RFID  Door   LED    Environment
      Sensor            Sensor Guide     Sensor

                         +

                    Outfit Camera
                         │
                         ▼
                 Personal Lookbook
```

---

# 6. Digital Twin Data Model

각 의류는 하나의 `Garment Object`로 관리한다.

```text
GARMENT_ID : G0031
```

## 6.1 Identity

- Brand
- Product Name
- Product Code
- Category
- Subcategory
- Color
- Pattern
- Material
- Size
- Product Image
- Purchase URL
- Purchase Date
- Purchase Price

---

## 6.2 Physical

- Wardrobe ID
- Zone / Slot
- Reference Weight
- Presence State
- Presence Sensor ID
- Last Presence Change

---

## 6.3 Care

- Care State
- Wear Count Since Wash
- Recommended Max Wear
- Last Wash Date
- Last Care Date
- Material Care Profile

---

## 6.4 Usage

- Total Wear Count
- Last Worn Date
- Average Rating
- Favorite Score
- Last Outfit ID
- Consecutive Wear Count

---

## 6.5 Recommendation Attributes

- Season
- Recommended Temperature Range
- Style
- Formality
- Color Group
- Rain Compatibility
- Thickness
- Layer Type

---

# 7. 의류 상태 설계

## 7.1 Presence State

물리적으로 옷장에 존재하는지 관리한다.

```text
IN_WARDROBE
OUT
UNKNOWN
```

기본 전환:

```text
IN_WARDROBE
      │
      │ 제거 감지
      ▼
     OUT
      │
      │ 복귀 감지
      ▼
IN_WARDROBE
```

센서 값이 모호하거나 통신 오류가 발생한 경우:

```text
IN / OUT
   ↓
UNKNOWN
```

으로 전환할 수 있다.

---

# 8. Care State

"현재 이 옷을 입는 것이 적절한가?"를 관리한다.

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
  │ 실제 착용
  ▼
REWEARABLE
  │
  │ 착용 횟수 / 사용자 판단
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

별도의 관리가 필요하면:

```text
REWEARABLE
     │
     ▼
CARE_REQUIRED
```

---

## 8.1 옷 종류별 정책

고정된 보편 규칙으로 강제하지 않고 **사용자 조정 가능한 기본 정책**으로 제공한다.

예시:

| 종류 | 기본 관리 규칙 예 |
|---|---|
| 티셔츠 | 1회 착용 후 세탁 권장 |
| 셔츠 | 1~2회 |
| 청바지 | 3~5회 |
| 자켓 | 5~10회 |
| 코트 | 장기 관리 주기 적용 |

※ 실제 위생·세탁 판단은 소재, 오염도, 착용 시간, 사용자 습관 등에 따라 달라질 수 있으므로 절대 기준으로 사용하지 않는다.

---

# 9. Derived Availability

추천 시스템에서 중요한 것은 단순 Presence가 아니라 **현재 추천 가능한지 여부**이다.

예:

```text
AVAILABLE =
    Presence == IN_WARDROBE
AND Care State ∈ {CLEAN, REWEARABLE}
AND Season / Weather Compatible
```

추천에서 기본 제외:

- OUT
- UNKNOWN
- NEED_WASH
- WASHING
- CARE_REQUIRED
- 현재 날씨에 명백히 부적합

---

# 10. Outfit Event

착장 사진과 코디는 의류 상태가 아니라 **Event History**로 관리한다.

```text
OUTFIT_EVENT #20260812-001

Date        : 2026-08-12
Time        : 08:21

Top         : G0012
Bottom      : G0027
Outer       : G0031
Shoes       : G0045

Weather     : 23°C / Cloudy
Humidity    : 68%
Purpose     : School
Style       : Casual

Photo       : IMG_20260812_001

Rating      : 5 / 5
Feedback    : Color Good / Comfortable
```

이 기록이 Personal Lookbook과 AI 개인화 데이터가 된다.

---

# 11. 카메라 기능

## 11.1 핵심 목적

카메라의 기본 목적은:

> **“내가 실제로 이 코디를 입었을 때의 모습”을 저장하는 것**

이다.

---

## 11.2 Outfit Capture Flow

```text
추천 코디 선택
↓
옷 꺼냄
↓
착용
↓
거울 앞
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

---

## 11.3 Personal Lookbook

예:

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

사용자는:

- 날짜
- 날씨
- 장소/목적
- 코디
- 만족도

를 함께 볼 수 있다.

---

## 11.4 Future AI Analysis

사진 데이터가 축적되면 향후:

- 실제 착장 색상 조화
- 자주 선택하는 실루엣
- 스타일 분포
- 과거 높은 만족도 조합
- 비슷한 착장 탐색
- 계절별 개인 선호
- 사용자 체감온도 선호

등을 분석할 수 있다.

---

# 12. Privacy by Design

카메라는 침실 또는 개인 공간에 위치할 수 있으므로 보안은 핵심 요구사항이다.

## 필수 원칙

### Manual / Explicit Capture
기본값은 사용자가 촬영을 명시적으로 요청했을 때만 촬영.

### Camera Indicator
카메라 활성 시 물리 LED 표시.

### Physical Shutter
가능하면 물리 셔터 적용.

### Local First
가능하면 이미지는 로컬 장치에서 처리·저장.

### User Control
사용자는:

- 카메라 완전 비활성화
- 사진 삭제
- Lookbook 기능 비활성화

가 가능해야 한다.

### No Continuous Surveillance
상시 영상 감시는 기본 기능에 포함하지 않는다.

---

# 13. 옷 등록 시스템

옷 등록의 번거로움은 제품 사용성을 결정하는 중요한 요소다.

따라서 여러 입력 방식을 제공한다.

## 13.1 Product Code / Model Search

대형 브랜드 의류:

```text
제품 코드 입력
↓
제품 DB / 검색 API
↓
상품 정보 불러오기
```

가져올 수 있는 정보:

- 브랜드
- 제품명
- 이미지
- 색상
- 소재
- 카테고리

---

## 13.2 URL Import

소형 브랜드 / 쇼핑몰:

```text
상품 URL 입력
↓
접근 가능한 정보 분석
↓
사용자 확인
↓
등록
```

※ 사이트별 이용약관·API 정책·robots 정책을 고려해야 한다.

---

## 13.3 Purchase History Import

향후:

- 이메일 영수증
- 쇼핑몰 주문 내역
- 패션 플랫폼 계정

등을 통한 자동 등록을 고려한다.

---

## 13.4 Direct Registration

자동 등록이 어려운 경우:

- 사진
- 카테고리
- 색상
- 소재
- 계절
- 스타일

직접 입력.

---

# 14. Presence Sensor 전략

현재 최종 센서 방식은 확정하지 않는다.

프로토타입에서 비교 후 선정한다.

## Candidate A — Load Cell

장점:
- 직접적인 물리 변화 감지
- 저비용
- 착용 빈도 데이터 수집 용이

단점:
- 동일 레일에 여러 벌이 걸리면 개별 식별 어려움
- 센서 수 증가 시 구조 복잡

---

## Candidate B — RFID / NFC

장점:
- 개별 의류 식별 명확
- DB 연결 용이

단점:
- 각 옷 또는 옷걸이에 태그 필요
- 리더 위치/거리 문제
- 사용자에게 태그 부착 부담

---

## Candidate C — Smart Hanger Slot

옷걸이 위치별:

- Micro Switch
- Magnetic Sensor
- Load Cell
- Contact Sensor

등을 배치.

장점:
- 슬롯별 Presence 관리 쉬움
- 추천 위치 LED와 결합하기 좋음

---

## Candidate D — Hybrid

예:

```text
RFID
= Identity

Load Cell / Hanger Sensor
= Presence
```

또는

```text
Smart Slot
= Presence

DB Slot Binding
= Identity
```

프로젝트에서는 **정확도 / 비용 / 배선 / 사용성** 비교 후 결정한다.

---

# 15. Smart Hanger / Sensor Rail

기존 옷장 Retrofit을 고려하면 Smart Hanger 또는 Sensor Rail이 핵심 하드웨어 후보가 된다.

기능:

- 옷 유무 감지
- Slot ID
- 추천 LED
- 착용 횟수 기록
- 장기 미착용 판단

향후:

- 개별 환경센서
- RFID
- 전동 이동

등으로 확장 가능.

---

# 16. Environment Monitoring

옷장 내부 환경을 측정한다.

기본 센서:

- Temperature
- Humidity

확장:

- VOC / Air Quality
- Dust
- Odor Proxy Sensor

표시 예:

```text
Wardrobe Environment

Temperature : 22.1°C
Humidity    : 67%
Air Quality : Good

Condition Score : 86 / 100
```

---

# 17. Smart Care

본 프로젝트에서 **LG Styler / Samsung AirDresser 수준의 의류관리기 구현을 핵심 목표로 하지 않는다.**

MVP:

- 환경 모니터링
- 습도 경고
- 환기
- 필요 시 팬 제어
- 관리 필요 알림

확장:

- 자동 제습
- 탈취
- 소재 기반 관리
- Wear-Ready

---

# 18. Wear-Ready Concept

상위 제품 또는 Future Work로 다음 개념을 유지한다.

```text
오늘 추천 의류 결정
↓
소재 확인
↓
안전 관리 Profile 확인
↓
필요 시 제습 / 환기 / 온도 조절
↓
착용 준비 완료
```

예:

- 여름: 제습 중심
- 겨울: 안전 범위 내 예열
- 장마철: 습도 관리

중요 원칙:

> AI가 임의로 의류 관리 온도를 결정하지 않고,  
> 소재별 정의된 안전 범위 안에서 제어한다.

---

# 19. Smart Cell Concept

고급형에서는 옷장을 여러 Smart Cell 또는 관리 Zone으로 나눌 수 있다.

```text
Central Care Unit
      │
 ┌────┼────┬────┐
 ▼    ▼    ▼    ▼
C1   C2   C3   C4
```

각 Cell:

- Presence
- Identification
- LED
- Air Flow
- Damper
- Environment
- Optional Motor

MVP에서는 과도하므로 구현 우선순위를 낮춘다.

---

# 20. Automatic Retrieval

Future / Premium 기능.

추천된 옷을 자동으로 앞으로 이동시키거나 인출한다.

로봇팔보다:

> **공용 Shuttle + Hanger Carriage**

구조가 현실적이다.

```text
CELL 1
CELL 2
CELL 3
CELL 4
=================
Shared Shuttle
←──────────────→
        │
        ▼
     Pick-up
```

단, 이는 MVP가 아니다.

---

# 21. Recommendation Engine

## 21.1 추천 입력

### Physical Data
- Presence
- Care State
- Slot
- Usage Count

### External Context
- 기온
- 체감온도
- 최고/최저 기온
- 강수
- 습도
- 계절

### User Context
- 일정
- 목적
- 스타일
- Formality
- 더위/추위 민감도

### Historical Data
- 이전 Outfit Rating
- 착용 빈도
- 최근 착용일
- 선호 색상
- 선호 조합

---

# 22. Recommendation Pipeline

처음부터 생성형 AI 하나에 전부 맡기지 않는다.

## Stage 1 — Hard Filter

```text
Presence
↓
Care
↓
Weather
↓
Category
```

추천 불가능한 옷 제거.

---

## Stage 2 — Candidate Outfit Generation

예:

```text
Top × Bottom × Outer × Shoes
```

조합 생성.

---

## Stage 3 — Scoring

```text
Outfit Score
=
Weather Suitability
+ Style Compatibility
+ Color Compatibility
+ User Preference
+ Previous Outfit Rating
+ Wear Frequency Balance
+ Occasion Suitability
```

---

## Stage 4 — AI Explanation / Ranking

AI는 후보 코디를 재정렬하거나 설명을 생성할 수 있다.

예:

> "오늘은 14°C이고 오후에 비가 예상됩니다. 최근 20일간 입지 않은 Grey Knit와 방수성이 있는 Jacket 조합을 추천합니다."

---

# 23. 개인화 학습

착장 후 사용자 피드백:

### Quick
- 👍
- 👎

### Rating
- ★★★★★

### Reason
- 핏이 좋음
- 색이 좋음
- 너무 더움
- 너무 추움
- 불편함
- 상황에 안 맞음

이 데이터를 다음 추천에 반영한다.

---

# 24. Dead Stock / Wardrobe Utilization

단순히 자주 입는 옷만 추천하면 추천 시스템이 취향을 고착화할 수 있다.

따라서:

```text
Weather Fit
+
Style Fit
+
Long Time No Wear
+
Existing Combination Compatibility
```

를 이용한 **Rediscovery Recommendation**을 제공한다.

예:

> **오늘의 재발견 코디**  
> 47일 동안 입지 않은 베이지 셔츠를 활용합니다.

---

# 25. Wardrobe Gap Analysis

내 옷장에서 부족한 영역을 분석한다.

```text
Black Tops   : 7
White Tops   : 5
Grey Tops    : 4

Black Pants  : 5
Blue Pants   : 4
Beige Pants  : 0
```

단순 "유행 상품 광고"가 아니라:

> 현재 옷장에 어떤 유형을 추가했을 때 활용 가능한 코디가 가장 많이 증가하는가?

를 계산한다.

---

# 26. Purchase Compatibility

예:

```text
Candidate
Beige Chino Pants

Compatibility Score : 92 / 100

New Outfit Potential : +14

Similar Items Owned : 0

Preference Match : High
```

반대:

```text
Black Hoodie

Compatibility Score : 34 / 100

Similar Items Owned : 3
Recent Hoodie Usage : Low
```

구매를 무조건 유도하기보다 **중복구매 방지**도 가치로 제시한다.

---

# 27. Smart Mirror / Display

옷장 문 또는 옆면에:

- 실제 거울
- Display
- Camera

를 결합한다.

주요 화면:

## HOME

- 날짜
- 시간
- 날씨
- 옷장 상태

## TODAY'S LOOK

- 추천 코디
- 추천 이유
- 다른 코디

## WARDROBE

- 현재 보유 옷
- OUT
- 세탁 필요
- 관리 필요

## LOOKBOOK

- 과거 착장
- 만족도
- 날씨
- 목적

## ENVIRONMENT

- 온도
- 습도
- 공기질

---

# 28. Convenience Layer

다음은 핵심 기능이 아닌 편의 기능으로 분리한다.

- Calendar
- Schedule
- Bus / Subway
- 출근/등교 정보
- 알람
- 스마트홈 정보

특히 대중교통은 제품 USP가 아니라 **아침 준비 경험을 개선하는 Smart Mirror Widget**으로 정의한다.

---

# 29. DX / AX 정의

## DX

기존 가구인 옷장을 데이터 기반 시스템으로 전환한다.

```text
Physical Clothes
↓
Sensor
↓
Digital Twin
↓
Usage History
↓
Management
```

DX 핵심:

- 옷 재고 디지털화
- 상태 기록
- 사용 기록
- 환경 기록
- 데이터 기반 관리

---

## AX

DX를 통해 생성된 데이터를 이용해 AI가 판단한다.

AX:

- 코디 추천
- 개인화
- 스타일 분석
- Dead Stock 추천
- Wardrobe Gap Analysis
- 구매 적합도 분석
- 관리 시점 추천

---

# 30. 시장 조사 요약

## 30.1 Digital Closet / AI Styling

현재 시장에는 이미 다음 기능을 제공하는 서비스가 존재한다.

대표 예:
- Acloset
- Google Photos Wardrobe
- 기타 Digital Closet 서비스

Acloset은:
- 디지털 옷장
- 날씨 기반 추천
- 상황/TPO 기반 추천
- AI Styling
- 구매내역 기반 의류 등록

등을 제공하고 있다.

Google Photos도 2026년 Wardrobe 기능을 통해:
- 사진 속 옷 자동 카탈로그
- 옷 조합
- Virtual Try-On

방향으로 확장하고 있다.

### 결론

> **"AI가 내 옷으로 코디를 추천한다"만으로는 차별화가 부족하다.**

---

# 31. 의류관리기 시장

Samsung AirDresser와 LG Styler 등은:

- 스팀
- 건조
- 탈취
- 살균
- 주름 관리
- AI 기반 관리

등에서 매우 강하다.

따라서 본 프로젝트는:

> **의류관리기 자체로 삼성/LG와 경쟁하지 않는다.**

Care 기능은 보조 역할로 유지한다.

---

# 32. Smart Mirror / Smart Furniture Market

시장조사기관 추정치에 따르면 스마트미러와 스마트가구는 성장 시장으로 평가된다.

참고 조사:
- Fortune Business Insights: 2026년 글로벌 스마트미러 시장 약 33.8억 달러, 2034년 약 103.7억 달러 전망
- Grand View Research: 글로벌 스마트가구 시장 2026년 약 2.808억 달러, 2033년 약 7.864억 달러 전망

시장조사기관별 정의가 다르므로 숫자를 절대값으로 사용하지 않고 **성장 방향성 참고 자료**로 사용한다.

---

# 33. Competitive Positioning

| 기능 | 일반 Digital Closet | AI Styling App | 의류관리기 | Smart Wardrobe |
|---|---:|---:|---:|---:|
| 디지털 옷장 | O | O | △ | O |
| 날씨 코디 | △ | O | X | O |
| 개인화 추천 | △ | O | △ | O |
| 실제 옷 존재 감지 | X | X | X | **O** |
| Presence State | X | X | X | **O** |
| Care State | △ | X | O | **O** |
| 실제 착장 기록 | O | O | X | **O** |
| 착장과 실제 센서 데이터 연결 | X | X | X | **O** |
| Smart Mirror | X | X | △ | O |
| 환경 모니터링 | X | X | O | O |
| 추천 옷 물리 위치 안내 | X | X | X | **O** |
| Retrofit | X | X | X | **O** |

---

# 34. 핵심 USP

본 제품의 핵심 USP는 다음 세 문장으로 정의한다.

## USP 1

> **현재 실제 옷장에 존재하는 옷을 안다.**

## USP 2

> **그 옷이 지금 실제로 착용 가능한 상태인지 안다.**

## USP 3

> **사용자가 그 옷을 실제로 어떻게 입었고 얼마나 만족했는지 안다.**

결국:

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

# 35. 제품 포지셔닝

잘못된 표현:

> AI 코디 스마트 옷장

추천 표현:

> **Physical-Digital Twin 기반 AIoT Smart Wardrobe Platform**

소비자용 표현:

> **“내 옷을 실제로 기억하는 옷장.”**

또는:

> **“가지고 있는 옷 중, 지금 입을 수 있는 옷을 골라주는 옷장.”**

---

# 36. Retrofit 전략

초기 사업화에서는 옷장 전체보다 **기존 옷장을 스마트화하는 Retrofit Kit**를 우선 검토한다.

## 이유

완제품 옷장은:

- 배송비
- 설치
- 크기
- 디자인 취향
- 주거 구조
- 가구 제조

문제가 발생한다.

Retrofit:

- 기존 옷장 활용
- 크기별 Rail만 변경
- 제조비 절감
- 테스트 용이
- 진입장벽 감소

---

# 37. 제품 라인업 가설

## PickFit Retrofit Basic

가격 가설:
**약 ₩299,000**

기능:

- Presence Sensor
- Smart Rail
- Environment
- LED Guide
- Digital Closet
- Basic Recommendation

---

## PickFit Mirror

가격 가설:
**약 ₩699,000**

추가:

- Smart Mirror
- Display
- Outfit Camera
- Lookbook
- Personalization
- Advanced Recommendation

---

## PickFit Premium

가격 가설:
**₩1,000,000+**

추가:

- Smart Cell
- Wear-Ready
- Advanced Care
- Automatic Retrieval
- Premium Display

※ 가격은 현재 사업 가설이며 BOM, 경쟁제품, 소비자 지불의사 검증 후 확정한다.

---

# 38. 수익 모델

## Hardware

- Retrofit Kit
- Smart Mirror
- Smart Rail
- Premium Wardrobe

## Software

- 기본 기능 무료
- 고급 AI Personalization 구독
- Lookbook Analytics
- Family Account

## Commerce

- Purchase Compatibility
- 브랜드 제휴
- 상품 추천

단, **광고가 제품의 핵심 가치처럼 보이지 않도록 주의한다.**

## Platform

- 중고 플랫폼 연동
- 세탁 서비스 연동
- 의류 브랜드 연동

---

# 39. MVP 정의

## 반드시 구현

### M01 — Garment Registration
의류 등록

### M02 — Physical Presence Detection
각 옷의 유무 확인

### M03 — Presence State
IN / OUT / UNKNOWN

### M04 — Care State
CLEAN / REWEARABLE / NEED_WASH / WASHING / CARE_REQUIRED

### M05 — Digital Twin DB

### M06 — Weather API

### M07 — Available Garment Filter

### M08 — Outfit Recommendation

### M09 — Physical Guide
추천 옷 위치 LED

### M10 — Outfit Camera Capture

### M11 — Outfit Event / Lookbook

### M12 — User Rating

### M13 — Temperature / Humidity

### M14 — Basic Smart Mirror / Dashboard

---

# 40. Should Have

- 개인화 추천
- 미착용 의류 추천
- 착용횟수 기반 관리 알림
- Product Code Import
- URL Import
- Wardrobe Gap Analysis
- Purchase Compatibility
- VOC
- 자동 환기
- 일정 연동

---

# 41. Could Have

- 대중교통
- 모바일 앱
- 가족 프로필
- 중고 판매 추천
- 세탁 서비스
- 스마트홈 연동
- 음성 인터페이스

---

# 42. Future Work

- AI Outfit Image Analysis
- Virtual Try-On
- Purchase History Auto Import
- Smart Cell
- Wear-Ready
- Automatic Retrieval
- Advanced Deodorization
- Automatic Drying
- Laundry Machine Integration
- Fashion Brand API
- Retail B2B Version

---

# 43. 핵심 시연 시나리오

## STEP 1 — 사용자 접근

Smart Mirror:

```text
2026-08-12

오늘
23°C
오후 비 60%
```

---

## STEP 2 — 상태 확인

```text
등록 의류       32
현재 옷장       27
외부             2
세탁 필요        2
세탁 중          1
```

---

## STEP 3 — Context

사용자:

```text
목적 : 학교
Style : Casual
선호 : 조금 시원하게
```

---

## STEP 4 — Recommendation

```text
TODAY'S LOOK

Top
Grey T-Shirt

Bottom
Black Pants

Outer
Light Jacket

Score
92
```

---

## STEP 5 — Physical Guide

추천 옷이 걸린 Slot LED ON.

---

## STEP 6 — Remove

센서:

```text
G0012
IN_WARDROBE
→
OUT
```

Digital Twin 즉시 반영.

---

## STEP 7 — Outfit Capture

사용자가 실제 착용 후 거울 앞에서:

```text
[오늘 착장 저장]
```

Camera Capture.

---

## STEP 8 — Outfit Event

```text
OUTFIT #120

G0012
G0024
G0031

23°C / School / Casual
```

---

## STEP 9 — Feedback

```text
★★★★★

Color Good
Comfortable
```

---

## STEP 10 — Learning

다음 추천에서 해당 평가 반영.

---

# 44. 5인 팀 역할 분담

프로젝트는 독립 개발보다 인터페이스 기준을 먼저 정해야 한다.

## Member 1 — Embedded / Physical Sensor

담당:

- Presence Sensor
- Load Cell / RFID 실험
- Door Sensor
- LED
- Environment Sensor
- MCU Firmware

산출물:

```text
Sensor Event
→
Device Protocol
```

---

## Member 2 — IoT / Device Communication

담당:

- ESP32 / Arduino
- Wi-Fi / LAN / USB
- Device API
- Event Messaging
- Hardware Integration

---

## Member 3 — Backend / Digital Twin

담당:

- Garment DB
- Presence State
- Care State
- Outfit Event
- REST API
- Event Log

---

## Member 4 — Recommendation / AI

담당:

- Weather
- Outfit Filter
- Scoring
- Personalization
- Dead Stock
- Gap Analysis

---

## Member 5 — Frontend / Smart Mirror / Camera

담당:

- Mirror UI
- Dashboard
- Lookbook
- Camera
- User Interaction
- System Integration UI

---

# 45. 권장 기술 구조

## Device

후보:

```text
ESP32
```

이유:

- Wi-Fi 기본 지원
- IoT 구현 용이
- Arduino IDE 사용 가능

Arduino UNO도 Physical Controller로 사용 가능하다.

---

## Edge / Backend

후보:

```text
Python
FastAPI
SQLite → MySQL/PostgreSQL
```

---

## AI / Data

초기:

```text
Rule-Based Filter
+
Weighted Scoring
```

이후:

```text
User Preference Model
+
LLM / Recommendation
```

---

## Frontend

후보:

```text
Web Dashboard
```

Smart Mirror에서는 Fullscreen / Kiosk Mode 사용.

---

# 46. API Architecture

```text
Physical Sensor
     ↓
ESP32
     ↓
Device API / MQTT / WebSocket
     ↓
Backend
     ↓
Digital Twin DB
     ↓
Recommendation Engine
     ↓
Frontend
```

---

# 47. Event Architecture

예:

```json
{
  "event": "GARMENT_REMOVED",
  "garment_id": "G0031",
  "slot_id": "H07",
  "timestamp": "2026-08-12T08:11:21"
}
```

Digital Twin:

```text
Presence
IN_WARDROBE
→
OUT
```

---

# 48. 프로젝트 개발 단계

## PHASE 0 — Planning

현재 단계.

목표:

- PRD 확정
- 시장조사
- 센서 후보
- 역할
- MVP
- 인터페이스

---

## PHASE 1 — Presence PoC

목표:

> 한 벌의 옷이 있는지 없는지 안정적으로 감지.

비교:

- Load Cell
- RFID
- Magnetic
- Switch

---

## PHASE 2 — Digital Twin

목표:

```text
Physical State
↕
Database
```

동기화.

---

## PHASE 3 — Recommendation

- Weather
- Hard Filter
- Scoring
- 3개 추천

---

## PHASE 4 — Mirror / Lookbook

- Display
- Camera
- Outfit Capture
- Rating

---

## PHASE 5 — Integration

```text
Sensor
→ DB
→ AI
→ Mirror
→ Camera
→ Feedback
```

전체 Closed Loop 완성.

---

## PHASE 6 — Productization

- Case
- Wiring
- UX
- Demo
- 가격
- BOM
- Pitch

---

# 49. 기술 리스크

## R1 — Presence Sensor 정확도

로드셀 하나로 여러 옷을 구분하기 어려울 수 있다.

대응:

- Slot-based
- RFID Hybrid
- Prototype Test

---

## R2 — 사용자가 상태를 직접 입력해야 하는 문제

세탁 여부 등을 모두 수동 입력하면 피로도가 커진다.

대응:

- 종류별 기본 정책
- 최소 확인
- 사용자 Override
- 향후 세탁기 연동

---

## R3 — Camera Privacy

대응:

- Manual Capture
- Indicator
- Physical Shutter
- Local Storage

---

## R4 — AI Recommendation 품질

처음부터 AI 정확도를 제품 성공 조건으로 두면 위험하다.

대응:

```text
Rule Filter
→ Scoring
→ AI
```

순으로 발전.

---

## R5 — Scope Explosion

위험 기능:

- Smart Cell
- Style Care
- Automatic Retrieval
- Virtual Try-On
- Transit
- 쇼핑 추천

대응:

MVP와 Future를 엄격히 분리한다.

---

# 50. 사업 리스크

## 50.1 AI 코디만으로 차별화 불가

이미 강력한 Digital Closet 앱이 존재한다.

따라서 판매 포인트는:

> **Physical-Digital Synchronization**

이어야 한다.

---

## 50.2 소비자 가격 민감도

스마트 옷장 기능에 수십만 원을 지불할 고객이 얼마나 되는지는 미검증.

향후:

- 설문
- 인터뷰
- 가격 민감도 조사

필요.

---

## 50.3 초기 설치 번거로움

Sensor Rail 설치와 옷 등록이 복잡하면 이탈한다.

따라서:

> **설치와 등록 경험 자체가 핵심 제품 기능이다.**

---

# 51. 프로젝트 성공 기준

프로젝트 최종 Demo에서 다음이 실제로 동작해야 한다.

1. 옷을 등록한다.
2. 실제 옷장에 있는 옷을 센서가 인식한다.
3. Digital Twin의 Presence가 동기화된다.
4. Care State를 관리한다.
5. Weather 정보를 가져온다.
6. 현재 실제 착용 가능한 옷만 필터링한다.
7. 코디 1개 이상을 추천한다.
8. 추천 옷 위치를 실제 옷장에서 안내한다.
9. 옷을 꺼내면 Digital Twin이 변경된다.
10. 사용자가 실제 착용한 모습을 촬영한다.
11. Outfit Event가 생성된다.
12. Lookbook에서 확인한다.
13. 평가를 저장한다.
14. 과거 평가를 다음 추천에 이용한다.

---

# 52. 최종 제품 Experience

이 제품이 성공하면 사용자는 옷장을 단순 보관함으로 느끼지 않는다.

아침:

```text
오늘 날씨
↓
현재 실제 옷 상태
↓
오늘 일정
↓
추천
↓
실제 옷 위치 표시
↓
착용
↓
착장 기록
```

저녁:

```text
옷 복귀
↓
Presence Update
↓
착용 횟수 Update
↓
Care Recommendation
```

장기:

```text
Wear History
↓
Preference Learning
↓
Dead Stock Discovery
↓
Purchase Compatibility
↓
Better Wardrobe
```

---

# 53. 최종 핵심 메시지

## 기술적 정의

> **Physical Wardrobe의 실시간 상태를 IoT Sensor로 감지하여 Digital Twin으로 관리하고, 개인의 실제 착장 경험을 AI Recommendation과 연결하는 Closed-Loop AIoT Wardrobe System.**

## 소비자 정의

> **“내가 가진 옷을 실제로 기억하고, 지금 입을 수 있는 옷을 골라주는 옷장.”**

## 발표용 정의

> **“기존 패션 AI가 사용자가 등록한 데이터만을 기반으로 추천한다면, Smart Wardrobe는 실제 옷장의 물리 상태와 의류 관리 상태, 그리고 사용자의 실제 착장 경험을 함께 학습합니다.”**

---

# 54. 현재 최종 우선순위

```text
1. Physical Presence
2. Digital Twin
3. Care State
4. Available Garment Filtering
5. Recommendation
6. Physical Guide
7. Outfit Capture
8. Lookbook
9. Personalization
10. Environment
```

이 열 가지를 중심축으로 유지한다.

그 외 기능은 이 중심축을 강화할 때만 추가한다.

---

# 55. 기획 결론

Smart Wardrobe의 경쟁력은 **기능의 개수**가 아니다.

```text
AI
Camera
Sensor
Mirror
Weather
Style Care
```

를 많이 붙이는 것이 목표가 아니다.

가장 중요한 것은 다음 Closed Loop를 실제로 구현하는 것이다.

```text
REAL CLOSET
    ↓
SENSING
    ↓
DIGITAL TWIN
    ↓
RECOMMENDATION
    ↓
REAL WEARING
    ↓
CAMERA / FEEDBACK
    ↓
LEARNING
    ↓
BETTER RECOMMENDATION
```

이 구조가 유지된다면 Smart Wardrobe는 단순 스마트 가구가 아니라 **사용자의 실제 의생활을 데이터화하는 Personal Wardrobe Intelligence Platform**으로 발전할 수 있다.

---

# 56. 참고 시장 자료

본 통합 기획의 시장 방향성 검토에 참고한 공개 자료:

- Acloset 공식 서비스 및 지원 문서 — Digital Closet, AI Styling, Weather / Occasion 기반 추천, 주문 이력 기반 등록
- Google 공식 블로그 — Google Photos Wardrobe (2026), 사진 기반 의류 카탈로그 및 Virtual Try-On
- Samsung Newsroom — 2026 Bespoke AI AirDresser
- Fortune Business Insights — Smart Mirror Market 2026–2034
- Grand View Research — Smart Furniture Market 2026–2033

> 시장조사기관의 시장규모 수치는 각 기관의 시장 정의가 다르므로 절대값보다 성장 방향성 확인에 사용한다.

---

# 57. 본 문서의 기준 결정 사항

여러 초기 기획안에서 충돌했던 요소는 다음과 같이 정리한다.

### 결정 1
**카메라의 주목적은 옷 재고 판별이 아니라 실제 착장 기록이다.**

### 결정 2
**Presence는 무게/RFID/Smart Hanger 등 물리 센서가 담당한다.**

### 결정 3
**Presence State와 Care State는 분리한다.**

### 결정 4
**Outfit은 상태가 아니라 Event History로 저장한다.**

### 결정 5
**AI 코디는 제품의 전부가 아니라 Digital Twin을 활용하는 서비스 Layer다.**

### 결정 6
**Smart Mirror는 주요 UX지만 Physical Digital Twin보다 우선하지 않는다.**

### 결정 7
**스타일러급 의류관리 기능은 MVP가 아니다.**

### 결정 8
**Smart Cell / Wear-Ready / Automatic Retrieval은 Premium 또는 Future Work로 유지한다.**

### 결정 9
**사업화 초기 형태는 완성형 옷장보다 Retrofit Kit를 우선 검토한다.**

### 결정 10
**최종 제품의 USP는 Physical Wardrobe Awareness이다.**
