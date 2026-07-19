from __future__ import annotations
import math
from statistics import mean
from backend.services.ocr.ocr_models import OCRResult
from .calibration_models import PhysicalMetrics

class PhysicalMetricsExtractor:
    """
    Extracts physical characteristics of a student's handwriting from OCR bounding boxes.
    """
    @staticmethod
    def extract(ocr_result: OCRResult) -> PhysicalMetrics:
        total_height = 0.0
        total_width = 0.0
        total_chars = 0
        total_slant = 0.0
        line_count = len(ocr_result.lines)

        if line_count == 0:
            return PhysicalMetrics(
                average_height=18.0,
                average_width=10.0,
                word_spacing=12.0,
                line_spacing=32.0,
                slant=0.0
            )

        for line in ocr_result.lines:
            box = line.box
            # box format: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]] (clockwise from top-left)
            if box and len(box) >= 4:
                x1, y1 = box[0]
                x2, y2 = box[1]
                x3, y3 = box[2]
                x4, y4 = box[3]

                # Line height (average of left and right vertical edges)
                h_left = math.sqrt((x4 - x1)**2 + (y4 - y1)**2)
                h_right = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)
                total_height += (h_left + h_right) / 2.0

                # Line width (average of top and bottom horizontal edges)
                w_top = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                w_bottom = math.sqrt((x3 - x4)**2 + (y3 - y4)**2)
                total_width += (w_top + w_bottom) / 2.0

                total_chars += len(line.text) if line.text else 0

                # Slant angle: deviation of left edge from vertical y-axis
                dy = y4 - y1
                dx = x4 - x1
                if dy != 0:
                    total_slant += math.degrees(math.atan2(dx, dy))

        avg_height = total_height / line_count
        avg_char_width = total_width / total_chars if total_chars > 0 else 10.0
        avg_slant = total_slant / line_count

        # Sort lines vertically to measure spacing between consecutive lines
        sorted_lines = sorted(
            ocr_result.lines, 
            key=lambda l: sum(pt[1] for pt in l.box) / len(l.box) if l.box else 0
        )
        line_spacings = []
        for i in range(len(sorted_lines) - 1):
            curr_box = sorted_lines[i].box
            next_box = sorted_lines[i + 1].box
            if curr_box and next_box and len(curr_box) >= 4 and len(next_box) >= 4:
                curr_bottom_y = (curr_box[2][1] + curr_box[3][1]) / 2.0
                next_top_y = (next_box[0][1] + next_box[1][1]) / 2.0
                spacing = next_top_y - curr_bottom_y
                if spacing > 0:
                    line_spacings.append(spacing)

        avg_line_spacing = mean(line_spacings) if line_spacings else 32.0
        word_spacing = avg_char_width * 1.2

        return PhysicalMetrics(
            average_height=round(avg_height, 1),
            average_width=round(avg_char_width, 1),
            word_spacing=round(word_spacing, 1),
            line_spacing=round(avg_line_spacing, 1),
            slant=round(avg_slant, 1)
        )
