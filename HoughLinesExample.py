import numpy as np
import cv2
import matplotlib.pyplot as plt

# 이미지 로드
img = cv2.imread('TileExample01.jpg')

# 이미지를 그레이스케일로 변환
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 가우시안 블러 필터 적용
blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

# 캐니 엣지 검출기 적용
edges = cv2.Canny(blur_img, 50, 100, apertureSize=3)

# 허프 변환 수행
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=40, minLineLength=50, maxLineGap=10)

# 검출된 직선들을 그리기 위해 이미지 복사
line_img = np.copy(img)

# 검출된 직선들을 이미지에 그리기
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

# 결과 이미지 출력
cv2.imshow('Edges', edges)
cv2.imshow('Result', line_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 라인 교체점 찾고, 상대면적 구하기
# 호모그래피 해야 세야지 , 모서리를 펼쳐서.
#네 점 잡는거를 이미지 프로세싱을 통해 정확하게.
# 공정 진척도 관리를 위한. ?
# 진척도+ 타일이 몇장 쓰였다. 라고 알려주기.
# 점을 어떻게 잡을건데?
# 허프라인 노이즈를 해결하는 알고리즘, Ransac/선형회귀 알고리즘을 통한.
# 온장 세기도 문제임.s
# 흰색 타일로 하자.
#라인 교차점 따고 상대면적 계산하기.
# 세그멘테이션으로 벽 단위로 호모그래피하세요.


