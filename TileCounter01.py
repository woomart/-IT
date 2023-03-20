import cv2
import numpy as np

# 이미지 불러오기
img = cv2.imread('Base01.jpg')

# 이미지 전처리
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 100)

# Canny 엣지 검출 시각화
edges_visualize = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
edges_visualize[edges != 0] = [0, 0, 255]  # 빨간색으로 표시

# 선분 검출
lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=40, minLineLength=50, maxLineGap=10)

# 수평선, 수직선 필터링
horizontal_lines = []
vertical_lines = []
for line in lines:
    x1, y1, x2, y2 = line[0]
    if abs(y2 - y1) < abs(x2 - x1):
        horizontal_lines.append(line[0])
    else:
        vertical_lines.append(line[0])

# 수평선, 수직선 정렬
horizontal_lines = sorted(horizontal_lines, key=lambda x: x[1])
vertical_lines = sorted(vertical_lines, key=lambda x: x[0])

# 수평선, 수직선 병합
horizontal_merged = []
vertical_merged = []
if horizontal_lines:
    horizontal_merged.append(horizontal_lines[0])
    for line in horizontal_lines[1:]:
        if abs(line[1] - horizontal_merged[-1][1]) < 10:
            horizontal_merged[-1][2] = line[2]
        else:
            horizontal_merged.append(line)

if vertical_lines:
    vertical_merged.append(vertical_lines[0])
    for line in vertical_lines[1:]:
        if abs(line[0] - vertical_merged[-1][0]) < 10:
            vertical_merged[-1][3] = line[3]
        else:
            vertical_merged.append(line)

# 타일 검출
tiles = []
for hline in horizontal_merged:
    for vline in vertical_merged:
        x1, y1, x2, y2 = vline
        if x1 > hline[0] and x1 < hline[2] and y1 > hline[1] and y2 < hline[3]:
            tile = img[hline[1]:hline[3], vline[0]:vline[2]]
            tiles.append(tile)

# 타일 온장 갯수 출력
print(len(tiles))

# 온장 영역 시각화
for hline in horizontal_merged:
    for vline in vertical_merged:
        x1, y1, x2, y2 = vline
        if x1 > hline[0] and x1 < hline[2] and y1 > hline[1] and y2 < hline[3]:
            cv2.rectangle(img, (vline[0], hline[1]), (vline[2], hline[3]), (0, 0, 255), 2)

# 케니 엣지 검출 시각화
cv2.imshow('edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 결과 이미지 출력
cv2.imshow('result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()