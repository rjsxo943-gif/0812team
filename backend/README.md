# Member 3 — Backend / Digital Twin MVP

Smart Wardrobe의 **Garment DB / Presence State / Care State / Outfit Event / Event Log / REST API**를 담당하는 MVP 백엔드입니다.

## 핵심 원칙

1. `Presence`와 `Wear`를 분리합니다.
   - 센서가 옷 제거를 감지해도 `OUT`으로만 기록합니다.
   - 실제 착용은 `/wear` API에서 명시적으로 확정합니다.
2. `Care State`는 별도 상태로 관리합니다.
3. 모든 상태 변화는 `event_log`에 남깁니다.
4. Member 2의 센서 이벤트는 `garment_id` 또는 `slot_id`로 Digital Twin과 연결합니다.
5. Member 4는 `available_only=true` API로 현재 추천 가능한 의류만 받을 수 있습니다.

## 실행

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
uvicorn app.main:app --reload
```

API 문서:

```text
http://127.0.0.1:8000/docs
```

## 테스트

```powershell
cd backend
pip install -e ".[dev]"
pytest
```

## 주요 API

| Method | Path | 역할 |
|---|---|---|
| GET | `/health` | 서버 상태 |
| POST | `/api/v1/garments` | 의류 등록 |
| GET | `/api/v1/garments` | 의류 목록 |
| GET | `/api/v1/garments?available_only=true` | 추천 가능 의류 |
| PATCH | `/api/v1/garments/{id}/presence` | Presence 수동 변경 |
| PATCH | `/api/v1/garments/{id}/care` | Care State 변경 |
| POST | `/api/v1/garments/{id}/wear` | 실제 착용 확정 |
| POST | `/api/v1/garments/{id}/wash-complete` | 세탁 완료 |
| POST | `/api/v1/sensor-events` | IoT 센서 이벤트 수신 |
| POST | `/api/v1/outfit-events` | 실제 착장 기록 |
| GET | `/api/v1/outfit-events` | Lookbook/착장 이력 |
| GET | `/api/v1/events` | Event Log |

## Member 2 → Member 3 센서 이벤트 계약

옷 제거:

```json
{
  "event_type": "GARMENT_REMOVED",
  "garment_id": "G0031",
  "slot_id": "H07",
  "sensor_id": "S-H07",
  "metadata": {
    "raw_value": 0
  }
}
```

옷 복귀:

```json
{
  "event_type": "GARMENT_RETURNED",
  "slot_id": "H07",
  "sensor_id": "S-H07"
}
```

`garment_id`가 없어도 등록된 `slot_id`가 고유하면 Garment를 찾아 상태를 변경합니다.

## Member 4가 사용할 데이터

```http
GET /api/v1/garments?available_only=true
```

현재 조건:

```text
Presence == IN_WARDROBE
AND
Care State in {CLEAN, REWEARABLE}
```

날씨/스타일 필터링 및 최종 Scoring은 Recommendation 담당에서 추가합니다.

## 현재 범위 밖

- 날씨 API
- 코디 점수 계산
- 이미지 AI 분석
- 자동 세탁 판정
- 쇼핑몰/브랜드 API
- 인증/다중 사용자

이 기능들은 인터페이스가 안정화된 후 확장합니다.
