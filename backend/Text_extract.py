import cv2
import numpy as np
import pytesseract
import re
from PIL import Image

def process(pil_image):
    def time_str_to_seconds(t):
        t = str(t).strip().replace(',', '.').replace(" ", "")
        t = re.sub(r'[^0-9:.]', '', t)

        if t.isdigit():
            if len(t) == 3:
                t = f"{t[0]}.{t[1:]}"
            elif len(t) == 4:
                t = f"{t[:2]}.{t[2:]}"
            elif len(t) == 5:
                t = f"{t[:2]}:{t[2:4]}.{t[4]}0"
            elif len(t) == 6:
                t = f"{t[:2]}:{t[2:4]}.{t[4:]}"

        if ':' in t:
            try:
                mins, secs = t.split(':')
                return float(mins) * 60 + float(secs)
            except:
                raise ValueError(f"Invalid time: {t}")

        return float(t)

    def format_result_time(t):
        if t >= 60:
            mins = int(t // 60)
            secs = t % 60
            return f"{mins}:{secs:05.2f}"
        else:
            return f"{t:.2f}"

    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 10)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    rects = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect_ratio = w / float(h)

        if 1000 < area < 15000 and 2.0 < aspect_ratio < 6.0:
            rects.append((x, y, w, h))

    rects = sorted(rects, key=lambda r: r[1])
    skip_indices = [0, 6]

    ocr_results = []
    for i, (x, y, w, h) in enumerate(rects):
        if i in skip_indices:
            continue
        cropped = img[y:y+h, x:x+w]
        text = pytesseract.image_to_string(cropped)
        cleaned_text = text.strip().replace("\n", "")
        ocr_results.append(cleaned_text)

    num_array = []
    for x in ocr_results:
        try:
            seconds = time_str_to_seconds(x)
            num_array.append(seconds)
        except ValueError:
            continue

    if len(num_array) < 3:
        return {"error": "Need at least 3 valid solve times"}

    sorted_times = sorted(num_array)
    best = round(sorted_times[0], 2)
    worst = round(sorted_times[-1], 2)

    middle_times = sorted_times[1:-1] if len(sorted_times) > 2 else sorted_times
    avg = round(sum(middle_times) / len(middle_times), 2)

    solves = [format_result_time(t) for t in num_array]

    return {
        "solves": solves,
        "best": format_result_time(best),
        "worst": format_result_time(worst),
        "average": format_result_time(avg)
    }
