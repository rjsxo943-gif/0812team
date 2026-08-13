# PickFit Smart Wardrobe — Cloud / IoT Architecture 조사

> 담당: 팀원 2 — Cloud / IoT Architecture  
> 목적: Arduino Nano ESP32가 생성한 Sensor Event가 Cloud까지 전달되고, Cloud의 명령이 다시 Device로 내려오는 구조를 현실적인 수준에서 정의한다.  
> 현재 단계: **기획 검증 단계**. Cloud Server 구축, MQTT Broker 구축, DB 구현, 펌웨어 구현은 범위 밖이다.  
> 결론 원칙: **HTTP와 MQTT 중 하나를 이 문서에서 확정하지 않는다.** 두 방식의 차이를 비교하고 PickFit의 MVP/제품화 단계에서 판단할 수 있도록 기준을 제시한다.

---

## 1. 조사 결론 요약

PickFit의 기본 데이터 흐름은 다음과 같이 정리하는 것이 현실적이다.

```text
[Physical Wardrobe]
Sensor
  ↓
Arduino Nano ESP32
  ├─ Sensor Read
  ├─ Debounce
  ├─ IN / OUT 변화 감지
  └─ Sensor Event 생성
  ↓
Wi-Fi
  ↓
Transport Layer
  ├─ Option A: HTTPS
  └─ Option B: MQTT over TLS
  ↓
Cloud Ingress
  ├─ Device 인증
  ├─ Event 유효성 검사
  └─ 중복 Event 방지
  ↓
Cloud Application
  ├─ Device Management
  ├─ Digital Twin
  ├─ Presence History
  ├─ Wear History
  ├─ Care State
  ├─ Recommendation
  └─ AI / Weather
  ↓
Database
  ↓
Command 생성
  ↓
HTTPS Polling 또는 MQTT Subscribe
  ↓
Arduino Nano ESP32
  ↓
LED / Actuator
```

### 핵심 판단

1. **Arduino는 Physical Edge Controller**로 유지한다.
2. **Cloud가 사용자 데이터와 Digital Twin의 기준 상태(Source of Truth)를 관리**한다.
3. Device와 User는 동일 개념으로 취급하지 않는다.
4. 모든 Device에는 서버가 구별 가능한 `deviceId`가 필요하다.
5. Sensor Event는 `deviceId + slotId + eventId + timestamp + state`를 기본 단위로 설계한다.
6. 인터넷이 끊겨도 Arduino의 Sensor Read / Debounce / Event 생성은 계속되어야 한다.
7. 인터넷 단절 중 발생한 Event는 로컬 Queue에 임시 저장하고, 재연결 후 원래 발생 시각과 함께 전송하는 구조를 권장한다.
8. HTTP는 MVP 구현이 단순한 반면, MQTT는 Event 기반 양방향 IoT 구조와 지속 연결에 더 적합하다.
9. 따라서 **기획 단계에서는 Transport를 추상화**하고, 구현 Freeze 시 MVP 난이도와 실시간성 요구에 따라 최종 선택하는 것이 안전하다.

---

# 2. 공식 표준 기준의 HTTP / MQTT 개념

## 2.1 HTTP

HTTP는 IETF RFC 9110에서 정의하는 **stateless application-level request/response protocol**이다.

기본 구조:

```text
Device
   │
   │ Request
   ▼
Cloud API
   │
   │ Response
   ▼
Device
```

예:

```http
POST /v1/devices/PF-D-001/events
Content-Type: application/json

{
  "eventId": "EVT-00001281",
  "slotId": "H03",
  "eventType": "PRESENCE_CHANGED",
  "state": "OUT"
}
```

Cloud가 Device로 명령을 전달하려면 일반적인 HTTP 방식에서는 Device가 서버에 요청해야 한다.

예:

```text
Device
  ↓
GET /commands
  ↓
Cloud
  ↓
Pending Command 반환
```

즉 Cloud가 Arduino에 직접 임의 시점에 HTTP Request를 보내는 구조보다, Arduino가 일정 주기로 Pending Command를 조회하는 **Polling 방식**이 현실적이다.

### 공식 출처
- IETF RFC 9110 — HTTP Semantics  
  https://www.rfc-editor.org/rfc/rfc9110.html

---

## 2.2 MQTT

MQTT 5.0은 OASIS가 표준화한 **Client–Server Publish/Subscribe Messaging Transport Protocol**이다.

기본 구조:

```text
Arduino
   │
   │ Publish
   ▼
MQTT Broker
   │
   ├───────────────→ Cloud Consumer
   │
   │ Subscribe
   ▼
Arduino
```

Device가 특정 Topic에 Event를 Publish하고, Cloud 또는 다른 서비스가 해당 Topic을 Subscribe하는 방식이다.

Cloud → Device 명령도 반대 방향 Topic을 사용하여 전달할 수 있다.

```text
Device → Cloud
pickfit/v1/devices/{deviceId}/events/...

Cloud → Device
pickfit/v1/devices/{deviceId}/commands/...
```

MQTT 표준은 QoS 0, QoS 1, QoS 2의 전달 수준과 Session 개념을 정의한다.

PickFit Sensor Event처럼 상태 변화가 중요한 Event에는 제품화 단계에서 **QoS 1 + Cloud 중복 제거** 방식이 현실적인 후보가 될 수 있다.

> QoS 1은 "적어도 한 번(at least once)" 전달이므로 같은 Event가 중복 전달될 수 있다. 따라서 `eventId`를 기준으로 Cloud에서 중복 Event를 제거하는 설계를 함께 가져가는 것이 안전하다.

### 공식 출처
- OASIS — MQTT Version 5.0  
  https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html

---

# 3. HTTP vs MQTT 비교

| 항목 | HTTP / HTTPS | MQTT |
|---|---|---|
| 기본 모델 | Request / Response | Publish / Subscribe |
| 연결 방식 | 요청 중심 | Broker와 지속 연결 가능 |
| Device → Cloud Event | 쉬움 | 매우 적합 |
| Cloud → Device Command | Polling 등의 추가 구조 필요 | Subscribe Topic으로 자연스럽게 가능 |
| 이벤트 중심 IoT | 가능 | 구조적으로 적합 |
| 양방향 통신 | 가능하나 별도 설계 필요 | 기본 구조에 잘 맞음 |
| 구현 난이도 | 상대적으로 낮음 | Broker / Topic / Session 개념 필요 |
| 디버깅 | REST API 도구로 비교적 쉬움 | MQTT Client/Broker 도구 필요 |
| 네트워크 단절 대응 | Device Queue와 재전송을 직접 설계 | Session/QoS를 활용 가능하나 Device Queue도 권장 |
| 전송 중복 고려 | Retry 설계 시 필요 | QoS 1 사용 시 반드시 고려 |
| Device 상태 유지 | 별도 DB/API 구현 | Broker Session + Cloud DB/Twin 조합 가능 |
| 대회 MVP | 유리 | 구현 경험이 있다면 가능 |
| 제품화 확장 | 가능 | 다수 Device / Event / Command에 유리 |
| PickFit 적합성 | 단순 MVP에 적합 | 장기 Architecture에 더 자연스러움 |

### 중요한 해석

**HTTP가 IoT에 부적합하다는 뜻은 아니다.**

Sensor Event가 드물고 Cloud → Device 명령의 즉시성이 중요하지 않다면 HTTPS만으로도 PickFit MVP를 구현할 수 있다.

반대로 다음 조건이 중요해질수록 MQTT의 장점이 커진다.

- 여러 Device가 동시에 연결됨
- Event가 지속적으로 발생함
- Cloud → Device 명령이 즉시 전달되어야 함
- LED / Actuator를 Cloud 상태와 빠르게 동기화해야 함
- Device Online / Offline 상태를 체계적으로 관리해야 함

---

# 4. PickFit에서 권장하는 Transport 판단 기준

현재는 아래와 같이 문서화하고 최종 구현 단계에서 결정하는 것이 적절하다.

## Option A — MVP 우선: HTTPS

```text
Sensor
↓
Arduino
↓
HTTPS POST
↓
Cloud REST API
↓
DB / Digital Twin

Cloud Command
↓
Command DB
↓
Arduino가 GET /commands
↓
LED Control
```

### 장점

- REST API 구조가 단순하다.
- Postman / curl 등으로 테스트하기 쉽다.
- 별도 MQTT Broker 개념을 학습하지 않아도 된다.
- 대회용 MVP에서 통신 Flow를 설명하기 쉽다.

### 단점

- Cloud → Device 즉시 명령을 위해 Polling이 필요하다.
- Polling 주기를 짧게 하면 불필요한 요청이 증가한다.
- Device가 많아질수록 Command Polling 구조 관리가 복잡해질 수 있다.

---

## Option B — IoT 구조 우선: MQTT

```text
Sensor
↓
Arduino
↓
MQTT Publish
↓
Broker
↓
Cloud Subscriber
↓
Digital Twin / DB

Cloud
↓
MQTT Publish
↓
Device Command Topic
↓
Arduino Subscribe
↓
LED Control
```

### 장점

- Sensor Event 전달 구조가 자연스럽다.
- Cloud → Device Command를 지속 연결을 통해 전달하기 쉽다.
- Device별 Topic 분리가 가능하다.
- IoT 확장 시 유리하다.

### 단점

- MQTT Broker가 필요하다.
- Topic 권한과 Device 인증 정책을 설계해야 한다.
- QoS / Session / Reconnect 개념이 추가된다.
- HTTP API만 사용하는 것보다 초기 구현 요소가 많다.

---

# 5. PickFit 통신 Architecture 제안

Protocol과 무관하게 Cloud 내부 구조는 동일하게 유지하는 것을 권장한다.

```text
                            ┌───────────────────────┐
                            │     PickFit App       │
                            │ Web / Mobile UI       │
                            └──────────┬────────────┘
                                       │
                                       ▼
┌──────────┐    Wi-Fi     ┌──────────────────────────┐
│ Arduino  │ ───────────→ │ Cloud Ingress            │
│ Nano     │              │                          │
│ ESP32    │ ←───────────  │ HTTPS API or MQTT Broker │
└────┬─────┘              └───────────┬──────────────┘
     │                                │
     │                                ▼
     │                     ┌──────────────────────────┐
     │                     │ Event / Command Service  │
     │                     └───────────┬──────────────┘
     │                                 │
     │                ┌────────────────┼─────────────────┐
     │                ▼                ▼                 ▼
     │          ┌───────────┐   ┌──────────────┐   ┌──────────────┐
     │          │Device Mgmt│   │Digital Twin  │   │Recommendation│
     │          └───────────┘   └──────────────┘   └──────────────┘
     │                                 │
     │                                 ▼
     │                         ┌──────────────┐
     │                         │ Database     │
     │                         └──────────────┘
     │
     └── Sensor / LED / Actuator
```

---

# 6. Device → Cloud Event 구조

## 6.1 Sensor Fact와 Cloud 판단을 분리한다

Arduino가 보내는 데이터는 가능한 한 **사실(Fact)** 중심이어야 한다.

잘못된 예:

```json
{
  "slotId": "H03",
  "userWoreGarment": true
}
```

Sensor는 사용자가 실제로 옷을 입었는지 알 수 없다.

권장:

```json
{
  "eventId": "EVT-01JABC...",
  "deviceId": "PF-D-0001",
  "wardrobeId": "PF-W-0001",
  "slotId": "H03",
  "eventType": "PRESENCE_CHANGED",
  "state": "OUT",
  "observedAt": "2026-08-13T11:02:13+09:00",
  "sequence": 1281,
  "firmwareVersion": "0.1.0"
}
```

### 필수 권장 항목

| 필드 | 역할 |
|---|---|
| `eventId` | Event 고유 ID, 중복 제거 |
| `deviceId` | 어떤 물리 Device에서 발생했는지 |
| `slotId` | 어떤 Sensor Channel인지 |
| `eventType` | Event 종류 |
| `state` | Sensor가 관찰한 상태 |
| `observedAt` | 실제 발생 시각 |
| `sequence` | Device 내 Event 순서 검증 |
| `firmwareVersion` | 문제 추적용 |

`wardrobeId`는 Device 인증 후 Cloud에서 Device 관계를 조회할 수 있다면 Payload에서 생략할 수도 있다.

---

# 7. Cloud → Device Command 구조

Cloud Command도 추적 가능한 객체로 설계하는 것이 좋다.

예:

```json
{
  "commandId": "CMD-01JXYZ...",
  "deviceId": "PF-D-0001",
  "target": "LED:H03",
  "commandType": "SET_LED",
  "payload": {
    "mode": "ON"
  },
  "createdAt": "2026-08-13T11:02:15+09:00",
  "expiresAt": "2026-08-13T11:02:45+09:00"
}
```

Device 실행 후:

```json
{
  "commandId": "CMD-01JXYZ...",
  "deviceId": "PF-D-0001",
  "status": "EXECUTED",
  "executedAt": "2026-08-13T11:02:16+09:00"
}
```

### Command에 ID가 필요한 이유

- 동일 Command가 중복 전송되는 상황 방지
- 실행 성공/실패 추적
- 네트워크 재연결 후 오래된 LED 명령 실행 방지
- Cloud와 Device 상태 불일치 진단

`expiresAt`을 두면 오래된 추천 LED 명령이 나중에 재연결되었을 때 실행되는 문제를 줄일 수 있다.

---

# 8. MQTT를 사용할 경우 Topic 구조 예시

```text
# Device → Cloud
pickfit/v1/devices/{deviceId}/events/presence
pickfit/v1/devices/{deviceId}/telemetry/environment
pickfit/v1/devices/{deviceId}/acks

# Cloud → Device
pickfit/v1/devices/{deviceId}/commands/led
pickfit/v1/devices/{deviceId}/commands/system
```

예:

```text
pickfit/v1/devices/PF-D-0001/events/presence
pickfit/v1/devices/PF-D-0001/commands/led
```

### 권장 권한 원칙

Device `PF-D-0001`은:

```text
Publish 허용
→ pickfit/v1/devices/PF-D-0001/events/*
→ pickfit/v1/devices/PF-D-0001/acks

Subscribe 허용
→ pickfit/v1/devices/PF-D-0001/commands/*
```

다른 Device의 Topic에는 접근하지 못하도록 한다.

---

# 9. HTTP를 사용할 경우 Endpoint 구조 예시

```text
POST /v1/devices/{deviceId}/events
GET  /v1/devices/{deviceId}/commands
POST /v1/devices/{deviceId}/commands/{commandId}/ack
POST /v1/devices/{deviceId}/heartbeat
```

Flow:

```text
Arduino
  │
  ├─ POST Event
  │
  ├─ GET Pending Commands
  │
  └─ POST Command ACK
```

MVP에서는 복잡한 실시간 Channel을 추가하지 않고 이 정도로도 Closed Loop를 설명할 수 있다.

---

# 10. Device ID 개념

## 10.1 Device ID의 정의

`deviceId`는 Cloud에서 **하나의 물리 Arduino/Controller를 고유하게 식별하기 위한 ID**다.

예:

```text
PF-D-0001
PF-D-0002
PF-D-0003
```

다음 항목과 분리한다.

```text
User ID       ≠ Device ID
Wardrobe ID   ≠ Device ID
Garment ID    ≠ Device ID
Slot ID       ≠ Device ID
```

### 관계 예

```text
User U001
  │
  └─ Wardrobe W001
       │
       └─ Device D001
            ├─ Slot H01
            ├─ Slot H02
            └─ Slot H03
```

사용자에게 Device가 여러 개 있을 수도 있다.

```text
User U001
 ├─ Wardrobe W001
 │    └─ Device D001
 │
 └─ Wardrobe W002
      └─ Device D008
```

---

## 10.2 Device ID에 개인정보를 넣지 않는다

권장:

```text
PF-D-A7F2C91E
```

비권장:

```text
HONGGILDONG_HOME_WARDROBE
01012345678_DEVICE
```

AWS IoT와 Azure IoT 공식 문서도 Device/Thing 이름에 개인 식별 정보를 넣지 않도록 주의하고 있다.

---

# 11. User와 Device 관계

PickFit은 **기기 중심이 아니라 사용자 중심 데이터 구조**가 적절하다.

```text
USER
  │
  └─ WARDROBE
       │
       └─ DEVICE
            │
            └─ SLOT
                 │
                 └─ GARMENT Binding
```

Device는 Sensor Event를 생성하는 하드웨어이고, User의 의류 데이터 자체를 소유하지 않는다.

따라서 Device가 고장나 교체되어도:

```text
User
Garment
Wear History
Care State
Recommendation History
```

등은 Cloud에 유지되어야 한다.

### Device 교체 예

```text
Before
User U001
 └─ Wardrobe W001
      └─ Device D001

D001 고장

After
User U001
 └─ Wardrobe W001
      └─ Device D021
```

User의 Garment DB와 Wear History는 유지한다.

---

# 12. 사용자별 Cloud 데이터 관리 구조

최소 데이터 모델:

```text
User
│
├─ Wardrobe
│   ├─ Device
│   │   ├─ DeviceStatus
│   │   └─ Slot
│   │
│   └─ Garment
│
├─ PresenceEvent
├─ WearEvent
├─ RecommendationEvent
└─ CareState
```

예시 Entity:

### User

```text
user_id
created_at
```

### Wardrobe

```text
wardrobe_id
user_id
name
```

### Device

```text
device_id
wardrobe_id
status
firmware_version
last_seen_at
```

### Slot

```text
slot_id
device_id
sensor_channel
led_channel
garment_id (nullable)
```

### PresenceEvent

```text
event_id
device_id
slot_id
state
observed_at
sequence
received_at
```

### DeviceCommand

```text
command_id
device_id
target
command_type
payload
status
created_at
expires_at
executed_at
```

---

# 13. 인터넷 단절 시 고려사항

인터넷 단절은 IoT 기획에서 정상적으로 발생할 수 있는 상태로 취급해야 한다.

```text
Sensor
↓
Arduino
↓
Wi-Fi 끊김
↓
Event 삭제 ❌
↓
Local Queue
↓
Wi-Fi 복구
↓
미전송 Event 재전송
↓
Cloud Deduplication
```

## 13.1 Device가 계속 해야 하는 일

인터넷이 없어도 다음은 Edge에서 계속 동작해야 한다.

```text
Sensor Read
Debounce
IN / OUT 변화 감지
Event 생성
Local Queue 저장
```

## 13.2 인터넷 단절 중 Event

권장:

```text
Event 발생
↓
eventId 생성
↓
observedAt 기록
↓
Local Queue 저장
↓
Reconnect
↓
Cloud 전송
```

Cloud는 `receivedAt`과 `observedAt`을 분리한다.

예:

```text
observedAt = 10:02
receivedAt = 10:15
```

이를 통해 인터넷이 13분 끊겼더라도 실제 Sensor Event가 발생한 순서를 복원할 수 있다.

---

## 13.3 Event 중복 제거

재전송 과정에서는 동일 Event가 두 번 도착할 가능성을 고려해야 한다.

```text
Event ID = EVT-1007
```

Cloud 처리:

```text
EVT-1007 처음 수신
→ DB 저장

EVT-1007 재수신
→ 이미 처리됨
→ 무시 / ACK
```

이를 **Idempotent Event Processing** 방식으로 설계한다.

---

## 13.4 Cloud → Device 명령

Device가 Offline인 동안 LED Command가 생성될 수도 있다.

따라서 Command에는:

```text
commandId
createdAt
expiresAt
status
```

등을 둔다.

예:

```text
12:00 추천 LED ON 생성
12:01 Device Offline
12:30 Device Reconnect
```

30분 전 추천을 이제 실행하는 것이 의미가 없다면:

```text
expiresAt = 12:05
```

로 설정하고 폐기한다.

---

## 13.5 Device Online 상태

Cloud는 다음 값을 관리할 수 있다.

```text
last_seen_at
connection_status
```

예:

```text
device_id       D001
last_seen_at    2026-08-13 11:42
status          OFFLINE
```

중요:

> `OFFLINE`은 옷장이 비어 있다는 뜻이 아니라 **Cloud와 Device가 현재 통신되지 않는다는 뜻**이다.

---

# 14. MQTT Offline 관련 참고

MQTT 5.0은 Session Expiry와 QoS를 정의하여 연결이 일시적으로 끊기는 상황을 다룰 수 있다.

또한 AWS IoT Device Shadow와 같은 상용 IoT Cloud 서비스에서는 Device가 Offline이어도 Cloud에 Device 상태 표현을 유지하는 패턴을 제공한다.

PickFit에서는 특정 Cloud 제품을 지금 확정할 필요는 없지만, **Device의 실제 연결 상태와 Cloud에 저장된 Digital Twin 상태를 분리한다**는 설계 원칙은 참고할 가치가 있다.

### 공식 출처

- OASIS MQTT 5.0 — Session / QoS  
  https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html

- AWS IoT Device Shadow  
  https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html

---

# 15. Cloud가 메인 연산을 담당하는 이유

PickFit에서는 Cloud를 단순 저장 서버가 아니라 **사용자 데이터와 서비스 로직의 중심 계층**으로 두는 것이 현실적이다.

## 15.1 데이터 지속성

Arduino가 교체되어도 다음 데이터는 유지되어야 한다.

```text
Garment DB
Digital Twin
Wear History
Care State
Recommendation History
User Feedback
```

따라서 Device 로컬 메모리보다 Cloud DB가 적합하다.

---

## 15.2 여러 Device 통합

한 User가 여러 Wardrobe / Device를 사용할 경우:

```text
Device A ─┐
          ├─→ Cloud User Account
Device B ─┘
```

Cloud에서 한 사용자 기준으로 통합할 수 있다.

---

## 15.3 외부 데이터 연동

PickFit의 Recommendation에는 향후 다음과 같은 외부 데이터가 사용될 수 있다.

```text
Weather API
AI API
Recommendation Logic
Shopping / Product Data
```

이런 외부 서비스의 API Credential과 로직을 Arduino마다 넣는 것보다 Cloud에서 중앙 관리하는 편이 구조적으로 적절하다.

---

## 15.4 사용자별 Digital Twin

Arduino가 알고 있는 정보:

```text
H03 = IN
```

Cloud가 알고 있는 정보:

```text
User U001
Wardrobe W001
Slot H03
Garment G0031
Presence = IN
Care = READY
Last Worn = ...
Wear Count = ...
```

즉 Sensor Fact보다 훨씬 많은 Context를 Cloud가 가지고 있기 때문에 Recommendation과 사용자 상태 판단은 Cloud가 담당하는 것이 적절하다.

---

## 15.5 보안 및 변경 관리

Cloud에 다음을 집중할 수 있다.

```text
User Authentication
Device Authentication
API Credential
Authorization
Business Rule
Recommendation Logic
AI Integration
```

Arduino에는 필요한 Device Credential과 최소 Edge Logic만 유지한다.

---

# 16. Digital Twin 최소 구조 제안

PickFit에서 Digital Twin을 지나치게 거창한 개념으로 표현하지 않고, MVP에서는 **Cloud가 유지하는 현재 상태 표현(Current State Representation)** 정도로 정의하는 것이 적절하다.

예:

```json
{
  "wardrobeId": "W001",
  "deviceId": "D001",
  "deviceStatus": "ONLINE",
  "slots": {
    "H01": {
      "presence": "IN",
      "garmentId": "G0031"
    },
    "H02": {
      "presence": "OUT",
      "garmentId": "G0088"
    }
  },
  "environment": {
    "temperature": 24.1,
    "humidity": 51.8
  },
  "updatedAt": "2026-08-13T11:40:00+09:00"
}
```

주의:

```text
Digital Twin
≠ Sensor Raw Data 전체
≠ Wear History 전체
≠ AI Model
```

Digital Twin은 **현재 상태**, History DB는 **과거 Event 기록**으로 분리하는 것이 명확하다.

---

# 17. PickFit Closed Loop

PickFit Architecture에서 중요한 것은 단방향 센서 수집이 아니라 **Closed Loop**다.

```text
① Sensor 변화
      ↓
② Arduino Debounce
      ↓
③ Sensor Event 생성
      ↓
④ Cloud 전달
      ↓
⑤ Event 검증 / 저장
      ↓
⑥ Digital Twin 갱신
      ↓
⑦ Rule / Recommendation
      ↓
⑧ Device Command 생성
      ↓
⑨ Arduino 명령 수신
      ↓
⑩ LED Control
      ↓
⑪ Command ACK
```

이 구조가 완성되면 PickFit의 핵심 IoT Loop가 성립한다.

---

# 18. Device → Cloud / Cloud → Device를 분리해서 표현

PPT에서는 아래 두 Flow를 분리해서 보여주는 것이 이해하기 쉽다.

## Device → Cloud

```text
Sensor
→ Arduino
→ Event
→ Wi-Fi
→ HTTP/MQTT
→ Cloud
→ Digital Twin
→ DB
```

## Cloud → Device

```text
Recommendation / User Action
→ Cloud Command
→ HTTP Polling 또는 MQTT
→ Arduino
→ LED / Actuator
→ ACK
```

---

# 19. MQTT / HTTP 선택에 대한 PickFit 기획 판단

## 현재 단계의 권장 문구

### 사용하면 좋은 표현

> PickFit은 Arduino Nano ESP32와 Cloud 간 Wi-Fi 기반 통신 구조를 사용하며, Sensor Event 전달 및 Device Command 수신을 위해 HTTP 또는 MQTT 기반 IoT 통신 방식을 검토한다.

### 피해야 할 표현

> PickFit은 MQTT를 사용한다.

현재 구현 검증 전에는 확정 표현을 피한다.

---

# 20. 구현 Freeze 시 Decision Rule

다음 조건이면 HTTP를 우선 검토한다.

```text
대회 MVP 우선
Device 수가 적음
Event 빈도가 낮음
LED Command 즉시성이 높지 않음
개발 기간이 매우 짧음
팀의 MQTT 경험이 적음
```

다음 조건이면 MQTT를 우선 검토한다.

```text
다수 Device 확장
실시간 Cloud → Device 명령
지속적인 Sensor Event
Online / Offline 관리 중요
IoT 제품화 Architecture 중시
Broker 기반 메시징 경험 있음
```

### 현재 조사 단계 판단

```text
MVP 구현 단순성      → HTTP 우세
Event 기반 구조      → MQTT 우세
Cloud → Device       → MQTT 우세
제품화 확장성        → MQTT 우세
학습/디버깅 단순성   → HTTP 우세
```

따라서 지금은:

> **Architecture는 HTTP/MQTT 모두 수용할 수 있도록 유지하고, 구현 Freeze 단계에서 최종 선택한다.**

---

# 21. PPT Architecture 수정 제안

기존:

```text
Arduino
↓
Wi-Fi
↓
Cloud
```

수정 권장:

```text
Sensor
↓
Arduino Nano ESP32
↓
Sensor Event
↓
Wi-Fi
↓
HTTP / MQTT
↓
Cloud Ingress
↓
Digital Twin / DB
↓
Recommendation
↓
Device Command
↓
HTTP / MQTT
↓
Arduino
↓
LED
```

이렇게 수정하면 **데이터가 올라가는 것뿐 아니라 명령이 다시 내려오는 구조**가 명확해진다.

---

# 22. PPT용 한 장 요약 문구

## 제목
**Edge–Cloud IoT Architecture**

## 본문

```text
Physical Edge
Arduino Nano ESP32
- Sensor Read
- Debounce
- Event 생성
- LED Control

Connectivity
Wi-Fi
- HTTP / MQTT 검토
- Device ↔ Cloud 양방향 통신

Cloud
- Device Management
- Digital Twin
- User / Garment DB
- Wear History
- Recommendation
- AI / Weather
```

## 하단 문구

> Arduino는 Sensor와 Physical Device 제어를 담당하고, 사용자 데이터·Digital Twin·Recommendation 등 주요 서비스 연산은 Cloud에서 담당한다.

---

# 23. PRD용 Architecture 문구

> PickFit의 Arduino Nano ESP32는 Physical Edge Controller로 동작하며 Sensor 상태를 읽고 Debounce 처리 후 `IN/OUT` 변화에 대한 Sensor Event를 생성한다. 생성된 Event는 Wi-Fi를 통해 Cloud로 전달된다. Cloud는 Device Identity를 확인하고 Event를 저장한 뒤 Digital Twin을 갱신한다. 사용자 데이터, Garment DB, Wear History, Care State, Recommendation 및 AI 연산은 Cloud에서 관리한다. Cloud에서 생성된 LED 또는 Actuator Command는 Device로 다시 전달되며, Device는 명령 수행 후 ACK 상태를 반환하도록 설계한다. Device–Cloud Transport는 현재 기획 단계에서 HTTP와 MQTT를 비교 검토하며 구현 Freeze 단계에서 최종 확정한다.

---

# 24. 현재 단계에서 확정할 것 / 확정하지 않을 것

## 확정 가능

```text
✔ Arduino → Wi-Fi → Cloud 구조
✔ Device ID 필요
✔ User와 Device 분리
✔ Device → Cloud Event 필요
✔ Cloud → Device Command 필요
✔ Event ID 필요
✔ Cloud가 사용자 데이터 관리
✔ Digital Twin은 Cloud에 위치
✔ Offline Queue 고려
✔ Arduino와 Cloud 역할 분리
```

## 아직 확정하지 않음

```text
△ HTTP vs MQTT
△ AWS / Azure / GCP
△ MQTT Broker 제품
△ DB 제품
△ 인증 방식 세부 구현
△ Queue 크기
△ Retry 횟수
△ Heartbeat 주기
△ Command Timeout
△ QoS 최종값
```

이 항목들은 PoC / 구현 단계에서 확정한다.

---

# 25. Architecture Decision 초안

| ID | 항목 | 현재 결정 |
|---|---|---|
| ADR-C01 | 메인 연산 위치 | Cloud |
| ADR-C02 | Arduino 역할 | Sensor / Event / Communication / LED |
| ADR-C03 | Network | Wi-Fi |
| ADR-C04 | Transport | HTTP / MQTT 비교 후 Freeze 시 결정 |
| ADR-C05 | Device Identity | Cloud에서 고유 Device ID 관리 |
| ADR-C06 | User–Device 관계 | User → Wardrobe → Device |
| ADR-C07 | Event Identity | Event마다 고유 Event ID 부여 |
| ADR-C08 | Cloud State | Digital Twin + History 분리 |
| ADR-C09 | Offline | Edge Queue + Reconnect Resend 고려 |
| ADR-C10 | Command | Cloud → Device + ACK 구조 |
| ADR-C11 | Device 교체 | User/Garment/History 데이터 유지 |
| ADR-C12 | 개인정보 | Device ID에 개인정보 미포함 |

---

# 26. 조사 결과 최종 결론

PickFit의 현실적인 Cloud / IoT 구조는 다음 세 계층으로 분리하는 것이 적절하다.

```text
1. Physical Edge
Sensor + Arduino + LED

2. Connectivity
Wi-Fi + HTTP/MQTT

3. Cloud
Device Management
Digital Twin
DB
History
Recommendation
AI
```

가장 중요한 Architecture 원칙은 다음과 같다.

> **Arduino는 관찰하고 Event를 만든다.  
> Cloud는 상태를 기억하고 판단한다.  
> Device와 Cloud는 Event와 Command로 연결한다.**

HTTP와 MQTT 중에서는 MQTT가 PickFit의 Event 기반 양방향 IoT 구조에 더 자연스럽지만, 대회 MVP의 개발 단순성은 HTTP가 유리하다. 따라서 현재 단계에서는 특정 Protocol을 확정하지 않고, 상위 Architecture를 Protocol-independent하게 정의한 뒤 구현 Freeze 단계에서 최종 선택하는 것이 가장 현실적이다.

---

# 27. 공식 출처

## MQTT 표준

**OASIS — MQTT Version 5.0**  
https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html

확인 근거:
- Client–Server Publish/Subscribe 구조
- QoS 0 / 1 / 2
- Client Identifier
- Session
- Session Expiry

---

## HTTP 표준

**IETF RFC 9110 — HTTP Semantics**  
https://www.rfc-editor.org/rfc/rfc9110.html

확인 근거:
- HTTP의 Stateless 특성
- Request / Response 모델
- Client / Server 개념

---

## Azure IoT 공식 문서 — Architecture 참고

**What is Azure IoT Hub?**  
https://learn.microsoft.com/en-us/azure/iot-hub/iot-concepts-and-iot-hub

**IoT Hub Endpoints**  
https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-endpoints

**Send Cloud-to-Device Messages**  
https://learn.microsoft.com/en-us/azure/iot-hub/how-to-cloud-to-device-messaging

**Device Identity / Authentication**  
https://learn.microsoft.com/en-us/azure/iot-hub/authenticate-authorize-sas

확인 근거:
- Device-to-Cloud / Cloud-to-Device 분리
- Device Identity Registry
- Device별 인증
- MQTT / HTTPS 등 IoT Protocol Endpoint
- MQTT 기반 C2D Callback과 HTTP Polling 차이

---

## AWS IoT 공식 문서 — Architecture 참고

**Managing Devices with AWS IoT**  
https://docs.aws.amazon.com/iot/latest/developerguide/iot-thing-management.html

**AWS IoT Device Shadow**  
https://docs.aws.amazon.com/iot/latest/developerguide/iot-device-shadows.html

**AWS IoT MQTT Tutorial**  
https://docs.aws.amazon.com/iot/latest/developerguide/sdk-tutorials.html

확인 근거:
- Device Registry
- Device / Logical Entity 관리
- MQTT Client ID
- Publish / Subscribe
- Persistent Session
- Offline 상태와 Cloud Device State 분리

---

# 28. 팀장 전달용 체크리스트

- [x] 전체 통신 구조 조사
- [x] HTTP와 MQTT 비교
- [x] Device → Cloud Event 구조 조사
- [x] Cloud → Device Command 구조 조사
- [x] Device ID 개념 정리
- [x] 사용자와 Device 관계 정리
- [x] 사용자별 Cloud 데이터 관리 구조 조사
- [x] 인터넷 단절 시 고려사항 정리
- [x] Cloud가 메인 연산을 담당하는 이유 정리
- [x] MQTT / IoT 통신 공식 링크 추가
- [x] PPT Architecture 수정안 제시
- [x] PRD 삽입용 문구 제시
- [x] 현재 확정/미확정 항목 구분
