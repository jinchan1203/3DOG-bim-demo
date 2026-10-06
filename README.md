# 3DOG: BIM으로 배우고, BIM 없이 스캔한다

4족보행 로봇(Unitree Go2 + VLP-16)의 3D 스캔 자율탐사 정책을 **BIM 기반 최적 계획을 따라 배우도록** 학습시키는 연구의 시연 코드다. 학습할 때만 BIM을 쓰고, 현장에서는 BIM 없이 라이다로 본 것만으로 탐사한다.

- 팀 메인 레포: [gkgk0119gmail-arch/3DOG_Go2-exploration](https://github.com/gkgk0119gmail-arch/3DOG_Go2-exploration) (Isaac Sim, Go2 보행, ARiADNE 재학습)
- 이 저장소: 그 레포 위에 얹는 **BIM 관련 추가분**(1단계 + 2단계 시연)
- 연구 목표 정리: [docs/3DOG_연구목표_정리.docx](docs/3DOG_연구목표_정리.docx)

## 전체 계획

| 단계 | 내용 | 상태 |
|---|---|---|
| 1 | BIM(IFC) → 2.5D 학습 맵 변환 | **완료** (공개 IFC 3개 → 맵 11장) |
| 2 | BIM 기반 최적 계획을 따라 탐사 정책 학습 | **계획 시연까지** (실제 학습은 아직) |
| 3 | 백양누리 BIM → Isaac Sim | 예정 |
| 4~5 | Isaac Sim에서 시험 (백양누리, 다른 현장) | 예정 |
| 6 | 실제 백양누리에서 Go2 실증 (PRAXIS) | 예정 |

## 시연

**1단계: BIM → 2.5D 학습 맵 → 탐사**

![1단계](figures/demo_bim_to_exploration.png)

**2단계: BIM 기반 계획 vs 지금 정책** — 지금 정책은 3D 81%에서 멈추고, BIM을 아는 계획은 92%까지 찍는다. 이 차이를 학습으로 메우는 것이 목표다.

![2단계](figures/demo_step2_duplex_Level_1_0.png)

변환된 맵 전체: [figures/maps/](figures/maps/), 공개 BIM 캡처: [figures/bim_captures/](figures/bim_captures/)

## 파일

| 경로 | 내용 |
|---|---|
| `tools/bim_to_25d.py` | IFC 한 층 → 2.5D 맵(`.npz`) + 미리보기 |
| `ariadne3d/bim_env.py` | BIM 맵 학습 환경 (`--world bim`) |
| `ariadne3d/bim_expert.py` | BIM 기반 계획 (정답 맵을 보고 계산하는 상한선) |
| `patches/3DOG_Go2-exploration.patch` | 메인 레포에 위 파일 + `driver3d.py`·`eval3d.py`의 `--world bim` 옵션을 한 번에 적용 |
| `maps_bim/` | 변환된 맵 11장 |

## 사용법 (메인 레포에서)

```bash
cd 3DOG_Go2-exploration
git apply ../3DOG-bim-demo/patches/3DOG_Go2-exploration.patch
pip install ifcopenshell

python tools/bim_to_25d.py model.ifc ariadne3d/maps_bim
cd ariadne3d && mkdir -p gifs/go2_turn_3d
python eval3d.py ../weights/ariadne3d_go2_turn_3d_ep4000_policy.pth --world bim --n 11 --node_res 2
```

## 사용한 공개 IFC

IFC 원본은 저장소에 넣지 않았다. 아래에서 받는다. 모두 소프트웨어 테스트용 공개 파일이라, 학습·논문에 쓰기 전 이용 조건을 확인해야 한다.

| 건물 | 출처 |
|---|---|
| Duplex (2층 주택) | [youshengCode/IfcSampleFiles](https://github.com/youshengCode/IfcSampleFiles) `Ifc2x3_Duplex_Architecture.ifc` |
| Dental clinic (2층 치과) | [ThatOpen/web-ifc](https://github.com/ThatOpen/web-ifc) `tests/ifcfiles/public/dental_clinic.ifc` |
| DigitalHub (사무, 지하 포함) | [ThatOpen/web-ifc](https://github.com/ThatOpen/web-ifc) `tests/ifcfiles/public/FM_ARC_DigitalHub.ifc` |

## 한계 (현재)

- 2.5D라서 칸마다 높이가 하나다. 문 위 인방·보, 계단·다층은 표현하지 못한다.
- BIM 기반 계획은 단순 그리디라 진짜 최적은 아니다. 큰 맵에서는 경로가 지나치게 길어진다.
- 좁은 문(약 1 m)이 많은 건물에서는 탐사 그래프 노드 간격(2~4 m) 때문에 탐사가 일찍 멈추는 경우가 있다.
- ARiADNE 원본 코드의 라이선스 표기가 없어 메인 레포 공개 전 확인이 필요하다.
