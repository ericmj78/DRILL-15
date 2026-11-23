# 시작 위치와 방향을 무작위로 정한다.
import random
# 이 파일을 기준으로 이미지 폴더 경로를 찾는다.
from pathlib import Path

# clamp는 범위를 제한하고, draw_rectangle은 박스 표시, load_image는 이미지 불러오기에 사용한다.
from pico2d import clamp, draw_rectangle, load_image

# frame_time은 이전 프레임에 걸린 시간이다.
import game_framework


# 좀비의 걷기 애니메이션, 이동, 그리기와 충돌 범위를 관리한다.
class Zombie:
    # 클래스 변수이므로 좀비들이 이미지를 공유한다. 처음 만들 때만 불러온다.
    images = None
    # zombie.py와 같은 폴더에 있는 zombie 이미지 폴더다.
    IMAGE_DIR = Path(__file__).resolve().parent / 'zombie'
    # 걷기 이미지 Walk (1).png부터 Walk (10).png까지 10장이다.
    FRAME_COUNT = 10
    # 초당 20프레임이므로 10장 한 주기는 약 0.5초다.
    FRAME_RATE = 20.0
    # 시속 10km를 초속 m로 바꾸고 0.3m당 10픽셀을 적용해 픽셀/초로 환산한다.
    SPEED = 10.0 * 1000.0 / 3600.0 * (10.0 / 0.3)

    # 좀비를 만들고 이동 범위를 정한다. x가 없으면 범위 안에서 무작위로 배치한다.
    def __init__(self, x=None, y=150, min_x=400, max_x=1600):
        # 이미지 목록이 없을 때 걷기 이미지 10장을 읽는다.
        # range는 끝 숫자를 포함하지 않아 FRAME_COUNT + 1까지 지정한다.
        if Zombie.images is None:
            Zombie.images = [
                load_image(str(self.IMAGE_DIR / f'Walk ({i}).png'))
                for i in range(1, self.FRAME_COUNT + 1)
            ]

        # 좌우 이동의 경계를 저장한다.
        self.min_x, self.max_x = min_x, max_x
        # x를 지정하면 경계 안으로 제한하고, 생략하면 무작위 위치를 선택한다.
        self.x = random.randint(min_x, max_x) if x is None else clamp(min_x, x, max_x)
        self.y = y
        # -1은 왼쪽, 1은 오른쪽이며 처음 방향을 무작위로 정한다.
        self.dir = random.choice([-1, 1])
        # 각 좀비가 서로 다른 걷기 자세에서 시작하도록 정한다.
        self.frame = random.uniform(0, self.FRAME_COUNT)

    # 매 프레임 좀비의 애니메이션과 위치를 갱신한다.
    def update(self):
        # 직전 프레임에서 흐른 시간(초)을 저장한다.
        dt = game_framework.frame_time
        # 흐른 시간만큼 프레임을 진행하고 % 10으로 마지막 다음에는 처음으로 돌아간다.
        self.frame = (self.frame + self.FRAME_RATE * dt) % self.FRAME_COUNT
        # 방향 × 초당 이동 거리 × 흐른 시간으로 이번 프레임의 이동 거리를 계산한다.
        self.x += self.dir * self.SPEED * dt
        # 오른쪽 끝에서는 왼쪽, 왼쪽 끝에서는 오른쪽으로 방향을 바꾼다.
        if self.x >= self.max_x:
            self.dir = -1
        elif self.x <= self.min_x:
            self.dir = 1
        # 프레임 사이에 경계를 넘어가면 위치를 범위 안으로 제한한다.
        self.x = clamp(self.min_x, self.x, self.max_x)

    # 현재 자세를 그리고 디버그용 충돌 박스를 표시한다.
    def draw(self):
        # frame은 실수로 누적하고 이미지 번호로 사용할 때만 int로 정수로 바꾼다.
        image = Zombie.images[int(self.frame)]
        # 왼쪽 이동 시 h로 이미지를 좌우 반전한다. 0은 회전 각도다.
        if self.dir < 0:
            image.composite_draw(0, 'h', self.x, self.y, 200, 200)
        else:
            image.draw(self.x, self.y, 200, 200)
        # *는 get_bb()가 반환한 좌표 네 개를 각각의 인자로 전달한다.
        draw_rectangle(*self.get_bb())

    # 왼쪽, 아래쪽, 오른쪽, 위쪽 순서로 충돌 박스 좌표를 반환한다.
    # 200×200 크기이므로 중심에서 각 방향으로 100픽셀씩 떨어진다.
    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100
