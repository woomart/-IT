import cv2
import numpy as np


# 마우스 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global pt_list, count, img

    if event == cv2.EVENT_LBUTTONDOWN:
        if count < 4:
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
            pt_list.append([x, y])
            count += 1
            if count > 1:
                cv2.line(img, (x, y), tuple(pt_list[-2]), (255, 0, 0), thickness=2)
            cv2.imshow('image', img)


# 이미지 로드
img = cv2.imread('Base01.jpg')

# 마우스 이벤트 처리를 위한 변수 초기화
pt_list = []
count = 0

# 이미지 표시 및 마우스 이벤트 처리
cv2.imshow('image', img)
cv2.setMouseCallback('image', mouse_callback)

# 마우스 이벤트 처리 완료 후, 호모그래피 계산
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to exit
        break
    elif count == 4:
        pts1 = np.float32(pt_list)
        pts2 = np.float32([[0, 0], [0, 1000], [1000, 1000], [1000, 0]])
        h, _ = cv2.findHomography(pts1, pts2)
        img_out = cv2.warpPerspective(img, h, (1000, 1000))
        # img_out = cv2.rotate(img_out, cv2.ROTATE_90_CLOCKWISE)  # 이미지 90도 회전

        # 그레이 스케일 변환
        gray_img = cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)

        # 가우시안 블러 필터 적용
        blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

        # 캐니 엣지 검출기 적용
        edges = cv2.Canny(blur_img, 50, 150, apertureSize=3)



        # 허프 변환 수행
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=150, minLineLength=100, maxLineGap=70)


        # 검출된 직선들을 그리기 위해 이미지 복사
        line_img = np.copy(img_out)

        # 검출된 직선들을 이미지에 그리기
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # 이미지 합치기
        result_img = np.concatenate((img_out, cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR), line_img), axis=1)
        cv2.imshow('Result', result_img)

        cv2.waitKey(0)
        break

cv2.destroyAllWindows()

# 온장 구하기, 테트리스 알고리즘 하자!
# 온장 맞추기 먼저하세요, 각도별로 나누기는 그냥 두고
# 물류 쪽 테트리스 알고리즘
# 데이터셋은 계속 생성

