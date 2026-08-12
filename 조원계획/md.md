# 👕 AI 옷장 프로젝트

> Arduino를 이용해 옷장에 보관된 옷을 관리하고, 매일 날씨를 확인하여 **현재 가지고 있는 옷 중에서 그날 가장 적합한 코디를 자동으로 추천해주는 AI 옷장**을 만든다.

---

## 1. 프로젝트 개요

### 목표

사용자가 옷장에 있는 옷을 등록해 놓으면 시스템이 매일 날씨 정보를 받아 다음과 같은 정보를 분석한다.

* 🌡️ 현재 기온
* 🌡️ 최고 / 최저 기온
* 🌧️ 강수 확률
* 💧 습도
* 💨 풍속
* ☀️ 날씨 상태
* 📅 요일 / 계절

그리고 옷장에 등록된 옷의 정보를 이용해 그날 입기 좋은 코디를 추천한다.

### 최종 동작 예시

```text
오늘 날씨
↓
기온 27℃
습도 75%
비 올 확률 70%
↓
AI 분석
↓
추천 코디
👕 흰색 반팔 티셔츠
👖 연청 와이드 팬츠
👟 흰색 운동화
☂️ 우산
```

---

# 2. 전체 시스템 구조

```text
                    ┌──────────────┐
                    │  날씨 API    │
                    │ OpenWeather  │
                    └──────┬───────┘
                           │
                           ▼
┌─────────────┐      ┌──────────────┐
│ 옷장 센서   │ ───▶ │ Arduino/ESP32 │
│ RFID/버튼 등│      │              │
└─────────────┘      └──────┬───────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ 서버 / AI    │
                    │ 코디 추천    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ LCD / OLED   │
                    │ 추천 결과 표시│
                    └──────────────┘
```

---

# 3. 추천하는 하드웨어

## 필수

| 부품          | 용도              |
| ----------- | --------------- |
| ESP32       | 메인 컨트롤러 + Wi-Fi |
| OLED 또는 LCD | 오늘의 코디 표시       |
| DHT22       | 옷장 내부 온도/습도 측정  |
| 버튼          | 코디 다시 추천        |
| LED         | 추천 상태 표시        |
| 부저          | 추천 완료 알림        |
| 전원 공급장치     | 시스템 전원          |

## 선택 부품

| 부품          | 용도                  |
| ----------- | ------------------- |
| RFID RC522  | 옷에 RFID 태그를 붙여 옷 인식 |
| 서보모터        | 옷장 문 자동 개폐          |
| 초음파 센서      | 옷장 문/사람 접근 감지       |
| WS2812B LED | 옷장 조명               |
| 카메라         | 옷 인식                |
| SD 카드       | 옷 정보 저장             |

---

# 4. 왜 Arduino보다 ESP32를 추천하는가?

일반 Arduino UNO도 센서 제어에는 좋지만 인터넷 연결이 필요하기 때문에 이 프로젝트에서는 **ESP32**를 추천한다.

ESP32에는 기본적으로 Wi-Fi 기능이 있기 때문에 날씨 API와 통신하기 쉽다.

```text
ESP32
 ├─ Wi-Fi
 ├─ 온도/습도 센서
 ├─ OLED
 ├─ RFID
 └─ 버튼
```

따라서 프로젝트의 메인 보드는 다음과 같이 구성한다.

> **ESP32 + Arduino IDE**

---

# 5. 옷 데이터 구조

AI가 코디를 추천하려면 단순히 옷 이름만 저장하면 안 된다.

각 옷에 다음 정보를 저장한다.

```json
{
  "id": 1,
  "name": "흰색 반팔 티셔츠",
  "category": "top",
  "color": "white",
  "material": "cotton",
  "season": ["spring", "summer"],
  "min_temp": 20,
  "max_temp": 32,
  "rain": false,
  "style": ["casual", "basic"]
}
```

예를 들어 바지라면:

```json
{
  "id": 2,
  "name": "연청 와이드 팬츠",
  "category": "bottom",
  "color": "light_blue",
  "material": "denim",
  "season": ["spring", "summer", "fall"],
  "min_temp": 15,
  "max_temp": 30,
  "rain": false,
  "style": ["casual", "street"]
}
```

---

# 6. 옷장에 옷 등록하기

가장 간단한 방법은 처음에는 옷을 직접 등록하는 것이다.

예:

```text
1. 흰색 반팔티
2. 검정 반팔티
3. 네이비 셔츠
4. 흰색 셔츠
5. 연청 와이드 팬츠
6. 검정 슬랙스
7. 베이지 치노팬츠
8. 청바지
9. 검정 후드티
10. 회색 니트
```

이후 발전시키면 RFID를 사용할 수 있다.

---

# 7. RFID를 이용한 옷 관리

각 옷에 RFID 태그를 붙인다.

```text
흰색 반팔티
     │
     ▼
 RFID 태그
     │
     ▼
 RFID 리더
     │
     ▼
 ESP32
```

옷을 꺼내거나 넣을 때 RFID를 읽어서 현재 옷장에 어떤 옷이 있는지 확인한다.

예:

```text
RFID UID: A3 91 72 14
        ↓
DB 검색
        ↓
흰색 반팔 티셔츠
```

이를 이용하면 사용자가 옷을 입고 나갔을 때 해당 옷을 `사용 중`으로 표시할 수도 있다.

---

# 8. 날씨 데이터

날씨 데이터는 인터넷의 날씨 API를 사용한다.

추천 구조:

```text
ESP32
 ↓
Wi-Fi
 ↓
날씨 API
 ↓
JSON 데이터
 ↓
ESP32 또는 서버
 ↓
추천 알고리즘
```

날씨 데이터 예시:

```json
{
  "temperature": 27,
  "feels_like": 29,
  "humidity": 75,
  "rain_probability": 70,
  "wind_speed": 4.2,
  "weather": "Rain"
}
```

---

# 9. 코디 추천 알고리즘

처음부터 복잡한 AI를 만들 필요는 없다.

**1단계에서는 점수 기반 알고리즘**으로 만드는 것이 좋다.

각 옷에 점수를 계산한다.

```text
총점 =
온도 적합도
+ 계절 적합도
+ 날씨 적합도
+ 비 적합도
+ 스타일 조합 점수
```

예를 들어:

```text
오늘:

기온 = 28℃
비 확률 = 70%
습도 = 75%

흰색 반팔티
→ 온도 적합 +10
→ 여름 적합 +10
→ 비 적합 +0

점수 = 20
```

---

# 10. 온도별 추천 기준

기본값은 다음처럼 설정할 수 있다.

```text
30℃ 이상
→ 반팔
→ 반바지
→ 얇은 셔츠

25~29℃
→ 반팔
→ 얇은 긴바지
→ 반바지

20~24℃
→ 긴팔
→ 셔츠
→ 얇은 재킷

15~19℃
→ 긴팔
→ 니트
→ 가벼운 아우터

10~14℃
→ 니트
→ 후드
→ 재킷

5~9℃
→ 두꺼운 니트
→ 코트
→ 패딩

4℃ 이하
→ 패딩
→ 두꺼운 바지
→ 방한용품
```

---

# 11. 비가 오는 날

비 확률이 높으면 다음과 같은 조건을 추가한다.

```text
강수확률 > 60%
        ↓
방수 가능한 옷 우선
        ↓
밝은색 바지 우선순위 감소
        ↓
우산 추천
```

예:

```text
🌧️ 오늘 비가 올 가능성이 높습니다.

추천:

👕 검정 반팔티
👖 검정 슬랙스
👟 검정 운동화
☂️ 우산
```

---

# 12. AI 코디 추천

1차 버전에서는 알고리즘으로 충분하지만, 프로젝트를 더 발전시키려면 AI를 사용할 수 있다.

서버에서 다음 정보를 AI에게 전달한다.

```text
오늘 날씨:
기온 27℃
체감온도 29℃
습도 75%
비 확률 70%

사용 가능한 옷:

상의:
- 흰색 반팔티
- 검정 반팔티
- 네이비 셔츠

하의:
- 연청 와이드 팬츠
- 검정 슬랙스
- 베이지 치노팬츠

신발:
- 흰색 운동화
- 검정 운동화
```

AI에게:

```text
오늘 날씨와 사용 가능한 옷을 고려해서
가장 적합한 코디 3개를 추천해줘.

조건:
1. 현재 기온을 고려할 것
2. 비 가능성을 고려할 것
3. 상의/하의/신발이 서로 어울릴 것
4. 색상 조합을 고려할 것
5. 각각 추천 이유를 설명할 것
```

---

# 13. 추천 결과

AI가 다음과 같은 결과를 반환하도록 만든다.

```json
{
  "recommendation": {
    "top": "흰색 반팔티",
    "bottom": "검정 슬랙스",
    "shoes": "흰색 운동화",
    "accessory": "우산",
    "reason": "기온이 높고 습도가 높아 통기성이 좋은 반팔을 추천합니다."
  }
}
```

ESP32는 이 결과를 받아 OLED에 표시한다.

---

# 14. OLED 화면

작은 OLED에서는 모든 정보를 표시하기 어렵기 때문에 여러 화면으로 나눈다.

### 화면 1

```text
================
   AI CLOSET
================

  27°C / 🌧️

Today's Look
```

### 화면 2

```text
TOP
흰색 반팔티

BOTTOM
검정 슬랙스
```

### 화면 3

```text
SHOES
흰색 운동화

☂️ 우산 챙기세요!
```

### 화면 4

```text
[BUTTON]

다른 코디 보기
```

버튼을 누르면 다음 추천 코디를 보여준다.

---

# 15. 시스템 동작 순서

```text
[전원 ON]
      ↓
ESP32 초기화
      ↓
Wi-Fi 연결
      ↓
현재 날씨 가져오기
      ↓
옷장 데이터 가져오기
      ↓
사용 가능한 옷 필터링
      ↓
날씨 조건 분석
      ↓
코디 후보 생성
      ↓
AI/알고리즘 점수 계산
      ↓
최고 점수 코디 선택
      ↓
OLED 표시
      ↓
사용자가 버튼 클릭?
      ↓
YES → 다음 코디
NO  → 대기
```

---

# 16. Arduino 프로그램 구조

프로그램은 다음처럼 분리하는 것을 추천한다.

```text
AI_Closet/
│
├── AI_Closet.ino
│
├── config.h
│
├── weather.cpp
├── weather.h
│
├── clothes.cpp
├── clothes.h
│
├── recommendation.cpp
├── recommendation.h
│
├── display.cpp
├── display.h
│
└── rfid.cpp
    rfid.h
```

---

# 17. Arduino 기본 코드 구조

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

void setup() {
    Serial.begin(115200);

    connectWiFi();

    initDisplay();
    initSensors();
    initRFID();

    getWeather();
    recommendOutfit();

    showRecommendation();
}

void loop() {

    if (buttonPressed()) {
        recommendNextOutfit();
        showRecommendation();
    }

    updateSensors();

    delay(100);
}
```

---

# 18. 날씨 가져오기

개념적으로는 다음과 같이 동작한다.

```cpp
void getWeather() {

    HTTPClient http;

    String url = WEATHER_API_URL;

    http.begin(url);

    int responseCode = http.GET();

    if (responseCode == 200) {

        String payload = http.getString();

        // JSON 파싱

        Serial.println(payload);
    }

    http.end();
}
```

실제 프로젝트에서는 API 키를 코드에 직접 공개하지 않고 별도의 설정 파일에 저장하는 것이 좋다.

---

# 19. 추천 함수

```cpp
Outfit recommendOutfit(
    Weather weather,
    Clothes clothes
) {

    Outfit best;

    int bestScore = -9999;

    for (auto outfit : clothes.outfits) {

        int score = 0;

        score += temperatureScore(
            outfit,
            weather.temperature
        );

        score += rainScore(
            outfit,
            weather.rainProbability
        );

        score += seasonScore(
            outfit,
            weather.season
        );

        score += colorScore(
            outfit
        );

        if (score > bestScore) {

            bestScore = score;
            best = outfit;
        }
    }

    return best;
}
```

---

# 20. 발전 단계

## LEVEL 1 — 기본형

```text
ESP32
+
날씨 API
+
OLED
+
버튼
```

기능:

* 날씨 확인
* 온도 분석
* 등록된 옷 중 코디 추천
* OLED 출력

---

## LEVEL 2 — 스마트 옷장

```text
ESP32
+
RFID
+
DHT22
+
OLED
```

추가 기능:

* 옷 자동 인식
* 옷장에 있는 옷 자동 관리
* 사용 중인 옷 관리
* 옷장 내부 온습도 확인

---

## LEVEL 3 — AI 옷장

```text
ESP32
      ↓
Wi-Fi
      ↓
Server
      ↓
Weather API
      ↓
AI
      ↓
추천 코디
      ↓
ESP32
      ↓
OLED
```

추가 기능:

* AI 코디
* 개인 취향 학습
* 자주 입는 옷 분석
* 색상 조합 분석
* 상황별 코디
* 사용자의 코디 평가 학습

---

# 21. 최종 완성 모습

```text
╔══════════════════════════════╗
║          AI CLOSET           ║
║                              ║
║        🌧️  27°C              ║
║        습도 75%               ║
║                              ║
║       TODAY'S LOOK            ║
║                              ║
║  👕 흰색 반팔티               ║
║  👖 검정 슬랙스               ║
║  👟 흰색 운동화               ║
║                              ║
║  ☂️ 우산을 챙기세요!           ║
║                              ║
║       [ NEXT LOOK ]           ║
╚══════════════════════════════╝
```

---

# 22. 가장 추천하는 실제 제작 순서

처음부터 RFID와 AI까지 한 번에 만들지 않는 것을 추천한다.

### STEP 1

ESP32 + OLED 연결

```text
ESP32
 ↓
OLED
```

OLED에 `AI CLOSET` 출력.

### STEP 2

Wi-Fi 연결

```text
ESP32
 ↓
Wi-Fi
 ↓
인터넷
```

### STEP 3

날씨 API 연결

```text
현재 온도
습도
비
날씨 상태
```

를 가져온다.

### STEP 4

옷 데이터 추가

```text
clothes.json
```

또는 ESP32 내부 배열에 옷 정보를 저장한다.

### STEP 5

코디 알고리즘 구현

```text
날씨
+
옷 정보
=
추천 코디
```

### STEP 6

버튼으로 다른 코디 보기

```text
[추천 1]

버튼 ↓

[추천 2]

버튼 ↓

[추천 3]
```

### STEP 7

RFID 추가

옷마다 RFID 태그를 붙인다.

### STEP 8

AI 연결

서버에서 AI를 이용해 색상과 스타일 조합까지 분석한다.

---

# 23. 최종 프로젝트 구성

```text
                 ☁️ WEATHER API
                       │
                       ▼
                 ┌───────────┐
                 │   SERVER  │
                 │    + AI   │
                 └─────┬─────┘
                       │
                    Wi-Fi
                       │
                       ▼
              ┌────────────────┐
              │     ESP32      │
              │                │
              │ Weather        │
              │ Recommendation │
              │ Controller     │
              └───┬────┬───┬───┘
                  │    │   │
                  ▼    ▼   ▼
                OLED RFID DHT22
                  │    │
                  │    ▼
                  │   👕👖👟
                  │
                  ▼
              👤 사용자
```

---

# 24. 프로젝트 핵심 아이디어

이 프로젝트의 핵심은 **Arduino가 모든 AI를 직접 실행하는 것이 아니라 역할을 나누는 것**이다.

```text
ESP32
→ 센서 / RFID / 화면 / 버튼 / 인터넷 통신

서버
→ 데이터 관리

AI
→ 코디 분석 및 추천

날씨 API
→ 실시간 날씨 데이터
```

이렇게 구성하면 훨씬 안정적이고 확장하기 쉽다.

---

# 25. 최종 목표

최종적으로는 아침에 사용자가 옷장 앞에 왔을 때:

```text
👤 사용자 감지
       ↓
🌤️ 오늘 날씨 확인
       ↓
👕 현재 옷장 확인
       ↓
🤖 AI 분석
       ↓
✨ 오늘의 코디 결정
       ↓
📺 옷장 화면에 표시

"오늘은 이 조합을 추천해요!"

👕 흰색 반팔티
👖 검정 슬랙스
👟 흰색 운동화

"오후에 비가 올 예정입니다.
우산을 챙기세요 ☂️"
```

까지 자동으로 실행되는 것을 최종 목표로 한다.
