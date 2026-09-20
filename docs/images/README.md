# 키맵 다이어그램

`config/charybdis.keymap`의 현재 핫키/숏컷을 레이어별로 이미지화한 것.
`&trans` 키는 실제로 활성화되는 하위 레이어의 값으로 채워서(effective binding)
"이 레이어를 켜면 각 키가 실제로 뭘 하는지" 바로 보이도록 했다.

- `layer0_base.png` — 기본 레이어 (타이핑 + 트랙볼)
- `layer2_mac.png` — Mac 모드 오버레이 (`Fn+M`, `&tog 2`)
- `layer3_numpad_bt.png` — 넘패드 / 블루투스 (엄지 홀드, `&lt 3 CAPSLOCK`)
- `layer5_fn_scroll.png` — Fn / 트랙볼 스크롤 (`&tog 5`, `&lt 5 RETURN`)
- `combos.png` — J+L, Q+W 콤보 위치

노란색 = 해당 레이어에서 base와 달라지는 키, 파란색 = mod-tap/hold-tap 키.

## 재생성

```
pip install matplotlib
# Noto Sans CJK 계열 폰트 필요 (한글 라벨 렌더링용), 예: apt install fonts-noto-cjk
cd docs/images && python3 ../scripts/gen_keymap_images.py
```

`config/charybdis.keymap`을 수정하면 `docs/scripts/gen_keymap_images.py`의
해당 레이어 데이터를 맞춰 갱신하고 다시 실행한다.
