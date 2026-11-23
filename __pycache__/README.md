# LEC17 좀비 걷기 시험용

LEC17에 걷는 좀비 4마리와 충돌 박스를 추가한 실습 코드입니다.

## 실행

Python, Pico2D, transitions가 설치된 환경에서 이 폴더를 VS Code로 열고 `main.py`를 실행합니다. Esc 또는 창 닫기 버튼으로 종료합니다.

화면 크기는 기존 수업 코드와 같은 1600×600이며, 좀비는 화면 오른쪽 구간(x=800~1600)을 오갑니다.

## 파일 사용

`zombie.py`의 `Zombie` 클래스가 걷기 애니메이션, 이동과 방향 전환, 충돌 박스 표시를 담당합니다. 같은 폴더의 `zombie/Walk (1).png`부터 `Walk (10).png`까지 필요합니다.

`play_mode.py`에서 `from zombie import Zombie`로 클래스를 불러오고, `init()`에서 좀비 4개를 생성해 게임 월드에 등록합니다.

```python
zombies = [Zombie() for _ in range(4)]
game_world.add_objects(zombies, 1)
```

좀비의 이동은 `game_framework.frame_time`을 사용합니다. 이 프로젝트에서는 좀비 공격과 죽음 동작을 추가하지 않았습니다.
