import cv2
import numpy as np

prev_left = None
prev_right = None

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    return cv2.Canny(blur, 50, 150)

def region_of_interest(image):
    height, width = image.shape
    polygons = np.array([
        [(0, height), (width, height), (width//2, int(height*0.6))]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    return cv2.bitwise_and(image, mask)

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []

    if lines is None:
        return None, None

    height, width, _ = image.shape

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)

        if x2 - x1 == 0:
            continue

        slope = (y2 - y1) / (x2 - x1)
        intercept = y1 - slope * x1

        if abs(slope) < 0.5:
            continue

        #Classify lines based on slope and screen position
        if slope < 0 and x1 < width / 2 and x2 < width / 2:
            left_fit.append((slope, intercept))
        elif slope > 0 and x1 > width / 2 and x2 > width / 2:
            right_fit.append((slope, intercept))

    left_line = np.average(left_fit, axis=0) if left_fit else None
    right_line = np.average(right_fit, axis=0) if right_fit else None

    return left_line, right_line

def make_coordinates(image, line_params):
    if line_params is None:
        return None

    slope, intercept = line_params
    y1 = image.shape[0]
    y2 = int(y1 * 0.6)

    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)

    return np.array([x1, y1, x2, y2])

def display_lines(image, lines):
    global prev_left, prev_right

    line_image = np.zeros_like(image)

    left_line, right_line = average_slope_intercept(image, lines)

    # smoothing
    if left_line is not None:
        if prev_left is not None:
            left_line = 0.9 * prev_left + 0.1 * left_line
        prev_left = left_line

    if right_line is not None:
        if prev_right is not None:
            right_line = 0.9 * prev_right + 0.1 * right_line
        prev_right = right_line

    for line in [left_line, right_line]:
        coords = make_coordinates(image, line)
        if coords is not None:
            x1, y1, x2, y2 = coords
            cv2.line(line_image, (x1, y1), (x2, y2), (0,255,0), 10)

    return line_image

cap = cv2.VideoCapture("test.mp4")

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break

    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)

    lines = cv2.HoughLinesP(
        cropped_image,
        2,
        np.pi/180,
        100,
        np.array([]),
        minLineLength=50,
        maxLineGap=10
    )

    line_image = display_lines(frame, lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)

    cv2.imshow("Lane Detection", combo_image)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()