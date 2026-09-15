# zmk-config for charybdis (4x6)

MiaoMiao 무선 Charybdis (트랙볼 스플릿) 용 개인 ZMK 설정.
컨트롤러 **nice_nano_v2** (nRF52840, BLE), 트랙볼 **PMW3610**, ZMK는 `config/west.yml`에서 **v0.3 고정**.

Upstream: `Vzhao-L/zmk-for-charybdis` ← `HeeTuic/zmk-for-charybdis`
브랜치: **`main-20250226`** (4x6 + 트랙볼)

---

## 레이어 구성

| # | 이름 | 켜는 법 |
|---|---|---|
| 0 | Base | 기본 |
| 1 | *(비어 있음)* | 없음 — 번호 유지용 placeholder |
| 2 | **Mac 모드** | `Fn + M` (`&tog 2`) — 토글 |
| 3 | 넘패드 / BT | 왼쪽 가운데 엄지 홀드 (`&lt 3 CAPSLOCK`) |
| 4 | *(비어 있음)* | 없음 |
| 5 | **Fn + 트랙볼 스크롤** | ① apostrophe 아래 키 토글 (`&tog 5`) ② 엄지 Enter 홀드 (`&lt 5 RETURN`) ③ 트랙볼 오른쪽 버튼 홀드 |

### Mac 모드 (layer 2)
켜면 OS별로 동작이 갈리는 것들만 Cmd 계열로 바뀐다. 나머지 키는 전부 `&trans`라 타이핑엔 영향 없음.

| | Windows (layer 0) | Mac 모드 (layer 2) |
|---|---|---|
| J + L 콤보 | 한/영 전환 (`LANG1`) | `Ctrl+Space` |
| Q + W 콤보 | 캡처 도구 `Win+Shift+S` | 영역 스크린샷 `Cmd+Shift+4` |
| Z / X / C / V 홀드 | `Ctrl+Z/X/C/V` | `Cmd+Z/X/C/V` |

---

## 콤보

전부 `timeout-ms=50`, `require-prior-idle-ms=150` (타이핑 중 롤링 오발동 방지).

| 콤보 | 포지션 | 기능 |
|---|---|---|
| J + L | 31, 33 | 한/영 전환 (OS별 분기) |
| Q + W | 13, 14 | 스크린샷 (OS별 분기) |

## Mod-Tap

`&mt` 전역: `tapping-term-ms=300`, `flavor=balanced`

| 키 | 탭 | 홀드 |
|---|---|---|
| Z / X / C / V | 글자 그대로 | Undo / 잘라내기 / 복사 / 붙여넣기 |
| 트랙볼 오른쪽 버튼 | 우클릭 | 레이어 5 → 트랙볼이 스크롤로 전환 |

---

## 포지션 넘버링

`config/boards/shields/charybdis/charybdis.dtsi`의 `default_transform` map 순서 = `bindings` 배열 순서.

| 줄 | 포지션 |
|---|---|
| row0 (ESC 줄) | 0–11 |
| row1 (QWERTY 줄) | 12–23 |
| row2 (홈로우) | 24–35 |
| row3 (바텀로우) | 36–47 |
| 엄지 5키 | 48–52 |
| 엄지 3키 | 53–55 |

---

## ⚠️ 알려진 함정

### 1. ZMK Studio 저장 키맵이 펌웨어를 덮어쓴다
Studio로 키맵을 한 번이라도 저장하면 그 키맵이 기기 settings 영역에 남고, **이후 펌웨어를 새로 플래시해도 컴파일된 키맵이 무시된다.** 플래시가 "안 먹는" 것처럼 보이면 이걸 의심할 것.

**해결**: ZMK Studio에서 **Restore Stock Settings** 실행. (또는 `settings_reset-nice_nano_v2-zmk.uf2` 플래시 — BLE 본딩도 같이 지워져 재페어링 필요)

### 2. `scroll-layers` / `snipe-layers` / `automouse-layer` 는 "최상위 활성 레이어"와 비교한다
`pmw3610.c`가 `zmk_keymap_highest_layer_active()`를 쓰고 **등호 비교**를 한다. 그래서 Mac 모드(2) 같은 토글 레이어가 켜져 있으면 그보다 낮은 스크롤 레이어가 가려져 스크롤이 죽는다.

**규칙**: 트랙볼 관련 레이어는 **토글 레이어(2)보다 높은 번호**를 쓸 것. 지금 Fn/스크롤이 5인 이유. 나중에 snipe·automouse를 켤 때도 6, 7 등으로.

### 3. `&to` 는 다른 레이어를 전부 끈다
`&to N`은 "기본 레이어를 제외한 모든 레이어를 끔"이라, 토글해둔 Mac 모드까지 같이 죽인다. 레이어 전환은 **`&tog`** 를 쓸 것.

### 4. 오버레이 레이어에 실제 키를 놓으면 베이스 키를 가린다
Mac 모드(2)는 베이스 위에 상시 얹히는 레이어라, 여기에 `&tog 2` 같은 걸 놓으면 해당 글자 키가 먹통이 된다. 실제로 M이 안 쳐지는 버그가 있었음.

### 5. ZMK 버전을 올리지 말 것
`config/west.yml`이 ZMK **v0.3** 고정. 최신(Zephyr 4.1 기반)에는 *"Studio가 켜져 있으면 central이 딥슬립에서 안 깨어나는"* 회귀 버그가 있고 v0.3엔 없다.

---

## 전원 설정

| 항목 | 상태 |
|---|---|
| RGB 언더글로우 | **비활성** — 이 개체엔 LED가 물리적으로 없음 |
| 딥슬립 (`CONFIG_ZMK_SLEEP`) | **활성** — 15분 무입력 시 진입 |
| BLE 송신 출력 | `TX_PWR_PLUS_8` (최대) — 배터리 문제 생기면 여기부터 낮출 것 |

딥슬립에서 깨우기: 아무 키나 누르면 됨(조합키 아님). 단 좌우가 각각 잠들고, **오른쪽(central)이 깨어나야** 입력이 PC로 전달된다. 재연결까지 1~5초, 그 사이 첫 몇 타는 씹힌다.

---

## TODO — 아직 비어 있는 부분

### 🔴 어느 레이어에도 없어서 아예 못 치는 키
- `[` `]` → 따라서 **`{` `}` 도 불가**
- `` ` `` (백틱) → 따라서 **`~` 도 불가**
- `Delete`

Keymap Editor로 레이어를 재배치하는 과정에서 `LEFT_BRACKET`이 `PERIOD`로 덮이고 `RIGHT_BRACKET`·`GRAVE` 자리가 사라진 결과.

### 🟡 불편한 부분
- `-` `=` 가 베이스에 없고 레이어 3에만 있음 → `_`, `+` 도 전부 레이어 3 경유
- 오른쪽 모디파이어(RSHIFT / RCTRL / RALT) 전무 → 왼손에 조합이 몰림
- `&lt 3 CAPSLOCK` — 엄지 탭이 Caps Lock이라 실수로 잠길 위험
- `&bootloader` 키 없음 → 플래시할 때마다 케이스 열고 RESET 더블탭해야 함

### 배치 후보
layer_5(Fn)의 오른손 쪽이 거의 비어 있어서 여기에 채우면 됨:

| Fn + 키 | 배정 후보 |
|---|---|
| U | `` ` `` |
| O / P | `[` / `]` |
| `;` / `'` | `-` / `=` |
| `,` | `Delete` |
| `/` | `&bootloader` |

---

## 빌드 & 플래시

빌드는 GitHub Actions (`.github/workflows/build.yml`). push 하거나 Actions 탭에서 수동 실행 → 아티팩트 `firmware.zip`에 세 파일:

- `charybdis_left-nice_nano_v2-zmk.uf2`
- `charybdis_right-nice_nano_v2-zmk.uf2` (ZMK Studio 지원 포함)
- `settings_reset-nice_nano_v2-zmk.uf2`

플래시:
1. 해당 절반을 USB-C 연결 → **RESET 버튼 0.5초 이내 두 번 탭**
2. `NICENANO` 드라이브 마운트됨 → `.uf2` 복사
3. 드라이브가 **저절로 사라질 때까지** 대기 (케이블 건드리지 말 것)
4. 반대쪽도 반복 → USB는 다시 오른쪽(central)에
5. 키맵이 반영 안 되면 → **Restore Stock Settings** (위 함정 1번)

좌우 연결은 **BLE 무선**. TRS/TRRS 케이블 불필요.

편집 도구:
- [ZMK Studio](https://zmk.studio/) — 실시간, 단 콤보·behavior 편집 불가, 저장 시 함정 1번 발생
- [Keymap Editor](https://nickcoutsos.github.io/keymap-editor/) — 이 레포에 연결해서 GUI 편집, 저장하면 자동 커밋 + 빌드
