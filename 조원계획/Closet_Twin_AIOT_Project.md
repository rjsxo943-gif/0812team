# Closet Twin
## AIoT 기반 스마트 옷장 Digital Twin 프로젝트 기획안

---

## 1. 프로젝트 개요

### 프로젝트명
**Closet Twin**

### 한 줄 정의
기존 옷장에 후장착하는 AIoT 모듈을 통해 의류의 반입·반출을 자동 감지하고, 비전 AI로 개별 의류를 식별하여 현실 옷장의 상태를 가상 옷장(Digital Twin)에 동기화하는 스마트 옷장 서비스.

### 핵심 아이디어
Closet Twin의 핵심은 단순한 코디 추천이 아니라,

> **Physical Closet → Digital Closet 자동 동기화**

이다.

사용자가 옷을 직접 앱에 등록·삭제·수정하지 않아도 실제 옷장에서 옷을 꺼내거나 다시 넣는 행동을 센서와 카메라가 감지하여 가상 옷장에 반영한다.

---

## 2. 해결하려는 문제

기존 패션 관리 앱은 보유 의류를 사용자가 직접 촬영하고 등록해야 하며, 옷을 버리거나 새로 구매할 때마다 정보를 직접 수정해야 한다.

또한 대부분의 패션 추천 서비스는 사용자가 실제로 어떤 옷을 얼마나 자주 입는지에 대한 데이터를 자동으로 확보하기 어렵다.

Closet Twin은 다음 문제를 해결한다.

- 보유 의류 수동 등록의 번거로움
- 실제 착용 여부와 앱 데이터의 불일치
- 비선호 의류 및 장기 미착용 의류 파악의 어려움
- 이미 비슷한 옷을 보유하고 있음에도 발생하는 중복 구매
- 날씨와 실제 보유 의류를 동시에 고려한 코디 추천 부족

---

## 3. 핵심 가치

### 3.1 현실 옷장의 자동 디지털화
센서와 비전 AI를 이용해 현재 옷장에 어떤 옷이 존재하는지 Digital Twin으로 관리한다.

### 3.2 실제 착용 데이터 자동 수집
옷의 반출·반입 이벤트를 통해 사용자가 어떤 옷을 자주 사용하는지 기록한다.

### 3.3 개인 맞춤 스타일 분석
착용 횟수, 최근 착용일, 색상, 종류 등을 분석하여 사용자 선호 스타일을 학습한다.

### 3.4 보유 의류 기반 구매 지원
새로운 의류 구매 시 현재 가진 옷과의 조합 가능성, 유사 의류 보유 여부, 기존 스타일 선호도를 분석한다.

### 3.5 옷장 활용률 향상
오랫동안 입지 않은 옷을 찾아 새로운 코디에 포함하여 불필요한 소비를 줄인다.

---

# 4. 시스템 전체 구조

```text
┌──────────────── 기존 옷장 ────────────────┐
│                                            │
│      [Camera A : 내부 Inventory Camera]    │
│                    ↓                       │
│           👔 👕 🧥 👚 👕                    │
│                                            │
│        IR-A     IR-B       Camera B        │
│          │        │       출입구 Camera     │
│──────────┼────────┼─────────📷───────────│
│               의류 출입 영역                │
│                                            │
│      Door Sensor / 온습도 / 조도 Sensor     │
│                  Arduino UNO               │
└────────────────────────────────────────────┘
                       ↓
                 USB Serial
                       ↓
              PC / Raspberry Pi
                       ↓
         Python / OpenCV / Vision AI
                       ↓
              Closet Twin DB
                       ↓
             Web / Mobile UI
                       ↓
       Recommendation / Analytics AI
```

---

# 5. 하드웨어 구성

## 5.1 Arduino UNO

Arduino는 AI 처리를 담당하지 않는다.

### 역할
- 센서 데이터 수집
- 옷장 문 상태 감지
- 의류 반입/반출 이벤트 감지
- Servo 및 LED 제어
- PC 또는 Raspberry Pi로 이벤트 전달

즉,

> **Physical Event Controller**

역할을 담당한다.

---

## 5.2 Door Sensor

Reed Switch 또는 자석 센서를 이용한다.

### 상태

```text
Door Closed
→ 시스템 대기

Door Open
→ Garment Detection Mode 활성화
```

옷장이 닫혀 있을 때 불필요한 촬영과 센서 동작을 제한한다.

---

## 5.3 IR Sensor A / B

옷장 출입구에 IR 센서 2개를 설치한다.

두 센서의 감지 순서를 이용해 의류가 옷장에서 나가는지 들어오는지 판단한다.

### 의류 반출

```text
IR-A
 ↓
IR-B

A → B
= OUT
```

### 의류 반입

```text
IR-B
 ↓
IR-A

B → A
= IN
```

Arduino는 이벤트를 생성한다.

```text
CLOTHING_OUT
CLOTHING_IN
```

---

# 6. 카메라 구성

## 6.1 Camera A — Inventory Camera

### 설치 위치
옷장 내부 상단 또는 후면 상단.

### 목적
정밀한 개별 의류 식별보다는 옷장 전체 상태 확인에 사용한다.

### 확인 정보
- 대략적인 옷 개수
- 옷이 존재하는 영역
- 색상 분포
- 상의/하의/아우터 등의 대략적 카테고리
- Digital Twin과 실제 옷장의 상태 차이

### 역할
**Inventory Verification Camera**

예:

```text
DB 예상
- 검정 후드
- 흰 셔츠
- 회색 맨투맨
- 청색 셔츠

Camera A 확인
→ 실제 옷장에 약 3벌만 존재

결과
→ Digital Twin 불일치 가능성 감지
```

---

## 6.2 Camera B — Identification Camera

Closet Twin의 핵심 카메라.

### 설치 위치
- 옷장 문 안쪽 가장자리
- 또는 옷장 프레임 내부

카메라가 방 전체가 아닌 **옷이 출입하는 좁은 영역만 촬영**하도록 설치한다.

### 목적
한 번에 한 벌의 옷이 카메라 앞을 지나갈 때 해당 옷의 특징을 분석한다.

### 분석 정보 예시

```text
Category : TOP
Type     : Hoodie
Color    : Black
Sleeve   : Long
Pattern  : Graphic
```

---

# 7. Privacy by Design

Closet Twin은 홈캠처럼 실내 공간을 지속적으로 촬영하지 않는 방향으로 설계한다.

## 7.1 Event-based Capture

상시 녹화하지 않는다.

```text
IR Event 발생
↓
Camera Capture
↓
AI 분석
↓
Capture 종료
```

---

## 7.2 제한된 카메라 FOV

카메라가 방 전체를 촬영하지 않도록 렌즈 앞 구조물 또는 설치 각도를 이용해 촬영 범위를 의류 통과 영역으로 제한한다.

---

## 7.3 Physical Privacy Shutter

Servo Motor를 이용해 물리적 셔터를 구현할 수 있다.

### 평상시

```text
Camera Lens
📷 █

Shutter Closed
```

### 의류 감지 시

```text
IR Event
↓
Servo 작동
↓
Shutter Open
↓
촬영
↓
Shutter Close
```

사용자가 카메라 활성 여부를 물리적으로 확인할 수 있다.

---

# 8. 전체 동작 시나리오

## Case 1. 옷을 꺼낼 때

### STEP 1. 옷장 문 열기

```text
Door Sensor
→ DOOR_OPEN
```

Arduino가 Garment Detection Mode를 활성화한다.

---

### STEP 2. 의류 통과

검정 후드티를 꺼낸다.

```text
IR-A
 ↓
IR-B
```

Arduino 판단:

```text
EVENT = CLOTHING_OUT
```

---

### STEP 3. 카메라 촬영

Arduino가 PC 또는 Raspberry Pi에 이벤트를 전달한다.

```text
OUT_EVENT
14:43:21
```

Camera B가 의류가 통과하는 순간 여러 Frame을 촬영한다.

```text
Frame 1
Frame 2
Frame 3
Frame 4
Frame 5
```

가장 선명한 Frame을 선택한다.

---

### STEP 4. AI 의류 분석

```text
Camera Image
↓
Object Detection
↓
Garment Segmentation
↓
Feature Extraction
```

분석 결과:

```text
Category : TOP
Type     : Hoodie
Color    : Black
Sleeve   : Long
Pattern  : Graphic
```

---

### STEP 5. 기존 의류와 비교

단순히 `검정 후드`라고만 저장하면 같은 종류의 옷을 구분할 수 없다.

따라서 각 의류 이미지에서 Feature Vector를 추출한다.

```text
Black Hoodie #01
[0.213, 0.634, 0.123 ...]

Black Hoodie #02
[0.183, 0.472, 0.813 ...]

Black Hoodie #03
[0.534, 0.236, 0.715 ...]
```

현재 촬영된 옷과 기존 DB의 Feature Vector를 비교한다.

```text
Black Hoodie #01 : 42%
Black Hoodie #02 : 57%
Black Hoodie #03 : 94%
```

결과:

```text
Detected
→ Black Hoodie #03
```

---

### STEP 6. Digital Twin 업데이트

```text
Black Hoodie #03

Before
STATUS = IN

After
STATUS = OUT

Last Used = 2026-08-12 14:43
Usage Count = 14 → 15
```

앱에서는:

```text
MY CLOSET

🟢 흰 셔츠
🟢 청색 셔츠
🔴 검정 후드
🟢 회색 맨투맨
🟢 청바지
```

처럼 상태가 변경된다.

---

# 9. 옷을 다시 넣을 때

의류가 반대 방향으로 이동한다.

```text
IR-B
 ↓
IR-A

B → A
= IN
```

Camera B가 의류를 촬영하고 AI가 동일한 옷을 확인한다.

```text
Black Hoodie #03
Similarity = 94%
```

DB:

```text
OUT → IN
```

Digital Twin도 자동으로 업데이트된다.

---

# 10. 최초 의류 등록

제품 설치 시 모든 옷을 상단 카메라만으로 정확히 식별하는 것은 현실적으로 어렵다.

따라서 최초 1회 **Setup Mode**를 사용한다.

사용자가 옷을 한 벌씩 Identification Gate를 통과시킨다.

```text
Garment
↓
Camera B
↓
Vision AI
↓
New Item
```

AI 자동 분석:

```text
Category : TOP
Type     : Hoodie
Color    : Black
```

사용자가 결과를 확인하면:

```text
ITEM_001
Black Hoodie
```

로 등록한다.

이후 일상 사용에서는 자동으로 반입·반출을 추적한다.

---

# 11. AI 오인식 처리

AI가 모든 옷을 완벽하게 구분할 수 있다고 가정하지 않는다.

Confidence 기반으로 처리한다.

예시 기준:

```text
Confidence ≥ 0.85
→ 자동 처리

0.60 ≤ Confidence < 0.85
→ 사용자 확인 요청

Confidence < 0.60
→ Unknown Garment
```

예:

```text
Black Hoodie #01 : 51%
Black Hoodie #02 : 48%
```

앱에서 두 후보를 보여주고 사용자가 선택하도록 한다.

선택 결과는 향후 모델 개선용 데이터로 다시 활용할 수 있다.

---

# 12. Digital Twin Database

최소 데이터 구조:

| Field | Description |
|---|---|
| item_id | 의류 고유 ID |
| category | 상의 / 하의 / 아우터 |
| type | 후드 / 셔츠 / 맨투맨 등 |
| color | 주요 색상 |
| pattern | 무지 / 프린팅 / 체크 등 |
| feature_vector | 이미지 특징 벡터 |
| status | IN / OUT |
| usage_count | 누적 사용 횟수 |
| last_used | 마지막 사용 일시 |
| preference | 사용자 선호도 |
| location | 옷장 내 Zone |
| image_path | 대표 이미지 |

이 DB가 현실 옷장을 복제한 **Digital Closet**이다.

---

# 13. 추천 서비스

Digital Twin이 구축되면 다양한 서비스를 추가할 수 있다.

## 13.1 날씨 기반 착장 추천

외부 Weather API와 Closet Twin DB를 결합한다.

입력 예:

```text
Temperature : 28℃
Humidity    : 81%
Rain        : 70%
```

+

```text
현재 옷장에 있는 의류
```

결과 예:

```text
오늘의 추천

상의 : 흰색 반팔
하의 : 검정 반바지
아우터 : 얇은 방수 아우터
```

---

## 13.2 개인 선호 스타일 분석

실제 착용 데이터를 이용한다.

예:

```text
최근 3개월

검정색 상의 착용률 : 42%
밝은색 상의 착용률 : 11%
후드/맨투맨 착용률 : 61%
셔츠 착용률 : 18%
```

이 데이터를 이용해 사용자의 실제 선호도를 학습한다.

---

# 14. Dead Stock 분석

장기간 사용하지 않은 의류를 탐지한다.

예:

```text
최근 90일 미착용

베이지 셔츠 : 104일
체크 셔츠   : 126일
회색 니트   : 93일
```

이를 기반으로:

- 비선호 스타일 분석
- 장기 미착용 의류 알림
- 새로운 코디 추천
- 중고판매 또는 정리 제안

등을 제공할 수 있다.

---

# 15. 안 입는 옷 살려주기

일반 추천 알고리즘은 사용자가 자주 입는 옷만 계속 추천할 가능성이 있다.

Closet Twin은 **Wardrobe Utilization** 개념을 추가한다.

예:

```text
오늘 날씨 적합
+
최근 30일 미착용
+
다른 보유 의류와 조합 가능
```

조건을 만족하는 옷을 추천한다.

예:

> **오늘의 재발견 코디**  
> 47일 동안 입지 않은 베이지 셔츠를 활용한 코디입니다.

목표:

> 새로운 옷 구매를 유도하는 AI가 아니라  
> **현재 가진 옷의 활용률을 높이는 AI**

---

# 16. 신규 의류 구매 지원

쇼핑 중 구매를 고려하는 옷의 사진을 입력한다.

예:

```text
신규 의류
→ Beige Cardigan
```

AI가 Closet Twin DB와 비교한다.

### 구매 적합도 예

```text
Purchase Compatibility Score
87 / 100
```

판단 근거:

- 현재 보유 의류 18개 중 11개와 코디 가능
- 유사 의류 보유 없음
- 사용자 선호 색상 계열
- 최근 자주 착용하는 스타일과 유사

반대 사례:

```text
Purchase Compatibility Score
32 / 100
```

판단 근거:

- 유사한 검정 후드 3벌 보유
- 최근 6개월 후드 착용률 낮음
- 기존 유사 의류 평균 착용횟수 월 0.4회

---

# 17. 기술 구성 예시

## Hardware

- Arduino UNO
- USB Camera × 2
- IR Sensor × 2
- Reed Switch
- Servo Motor
- LED
- 온습도 센서
- 조도 센서
- PC 또는 Raspberry Pi

## Software

### Arduino
- 센서 제어
- 이벤트 생성
- Serial 통신

### Edge / Server

```text
Python
OpenCV
Vision AI
FastAPI
SQLite / MySQL
```

### Frontend

- Web Dashboard
- 또는 Mobile UI

---

# 18. MVP 범위

처음부터 실제 가정의 수십~수백 벌 의류를 완벽하게 인식하는 것을 목표로 하지 않는다.

### Demo Closet

약 8~12벌로 테스트한다.

예:

```text
검정 후드
회색 맨투맨
흰 셔츠
파란 셔츠
검정 반팔
흰 반팔
청바지
검정 바지
베이지 바지
검정 자켓
```

### MVP 핵심 기능

1. 옷장 문 열림/닫힘 감지
2. 의류 IN/OUT 방향 감지
3. Camera B 의류 촬영
4. 의류 카테고리 및 색상 분석
5. 등록된 의류 재식별
6. Digital Twin DB 자동 업데이트
7. Web 화면에서 현재 옷장 상태 확인
8. 날씨 기반 기본 코디 추천

---

# 19. 프로젝트 KPI

아래 수치는 초기 목표값이며 실험을 통해 실제 값을 측정한다.

| KPI | 목표 |
|---|---:|
| 문 열림 감지 정확도 | ≥ 95% |
| 의류 IN/OUT 감지 정확도 | ≥ 95% |
| 의류 카테고리 분류 정확도 | ≥ 90% |
| 등록 의류 재식별 정확도 | ≥ 85% |
| Digital Twin 반영 시간 | ≤ 3초 |
| 사용자 수동 입력 | 최소화 |

최종 발표에서는 실제 반복시험 결과를 제시한다.

예:

> 총 200회의 의류 반출입 시험 결과 IN/OUT 이벤트 검출 정확도 97.5%, 등록 의류 재식별 정확도 89%를 기록했다.

---

# 20. 5인 팀 역할 분담

| 인원 | 담당 |
|---|---|
| 1 | Arduino / Door·IR Sensor / Servo / Serial 통신 |
| 2 | Camera / OpenCV / Vision AI / 의류 재식별 |
| 3 | Backend / DB / Digital Twin 상태 관리 |
| 4 | Frontend / Web·App UI |
| 5 | Recommendation AI / Weather API / 데이터 분석 |

전체 시스템은 다음 흐름으로 연결한다.

```text
Physical
↓
IoT / Edge
↓
Vision AI
↓
Data
↓
Digital Twin
↓
Recommendation Service
```

---

# 21. 사업화 방향

Closet Twin은 완성된 스마트 옷장을 판매하는 것이 아니라,

> **기존 옷장을 스마트 옷장으로 바꾸는 Retrofit Kit**

형태를 목표로 한다.

## Hardware

**Closet Twin Smart Module**

- Sensor
- Camera
- Controller
- Privacy Shutter

## Software

**AI Wardrobe Platform**

- Digital Closet
- 착용 데이터 분석
- 날씨 코디 추천
- 구매 적합도
- Dead Stock 분석
- 스타일 분석

### 확장 가능한 수익모델 예시

- Hardware Kit 판매
- 기본 앱 무료 제공
- Premium AI 추천 구독
- 패션 플랫폼 제휴
- 구매 추천 및 할인 정보 연동
- 중고 의류 플랫폼 연동

---

# 22. 차별화 포인트

## 기존 스마트 옷장/패션 앱과의 차이

단순 패션 추천:

```text
사용자 입력
↓
AI 추천
```

Closet Twin:

```text
실제 사용자 행동
↓
IoT 자동 감지
↓
Vision AI
↓
Digital Twin
↓
실제 착용 데이터 축적
↓
개인화 추천
```

### 핵심 USP

> **별도의 RFID 태그 없이 기존 옷장의 의류 반입·반출을 자동 감지하고 비전 AI를 통해 현실 옷장과 Digital Twin을 동기화한다.**

---

# 23. 프로젝트 최종 정의

> **Closet Twin은 기존 옷장에 후장착하는 AIoT 모듈을 통해 별도의 RFID 태그나 지속적인 사용자 입력 없이 의류의 반입·반출을 자동 감지하고, 비전 AI를 통해 개별 의류를 식별하여 현실의 옷장 상태를 Digital Twin으로 동기화한다. 축적된 실제 착용 데이터를 기반으로 날씨별 코디, 개인 취향 분석, 비활성 의류 관리 및 신규 의류 구매 의사결정을 지원한다.**

---

# 24. 프로젝트 최우선 성공조건

Closet Twin의 1차 성공조건은 코디 추천 정확도가 아니다.

핵심 Demo는 다음과 같다.

```text
사용자가 옷을 꺼낸다
↓
센서가 OUT Event를 감지한다
↓
카메라가 옷을 촬영한다
↓
AI가 어떤 옷인지 식별한다
↓
Digital Twin에서 해당 옷이 자동으로 OUT 상태가 된다
↓
사용자가 옷을 다시 넣는다
↓
AI가 동일한 옷을 인식한다
↓
Digital Twin에서 자동으로 IN 상태로 복귀한다
```

이 과정이 안정적으로 작동하는 것이 프로젝트의 핵심이다.

그 이후에 날씨 추천, 취향 분석, 구매 추천 등의 서비스를 확장한다.

---

## 핵심 키워드

`Arduino` `AIoT` `Digital Twin` `Computer Vision` `OpenCV` `Edge Computing`  
`Smart Closet` `Object Re-identification` `IoT Sensor` `Recommendation System`  
`Privacy by Design` `Retrofit` `FastAPI` `Database` `Weather API`
