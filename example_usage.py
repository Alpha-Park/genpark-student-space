# -*- coding: utf-8 -*-
from client import GenParkStudentSpace

space = GenParkStudentSpace()

# 1. SuperMemo SM-2 Interval
sm2 = space.calculate_sm2_interval_and_ease(repetition_count=2, previous_interval_days=6, previous_ease_factor=2.5, response_quality=4)
print(f"SM-2 Spaced Repetition: Next Interval={sm2['next_interval_days']} days (New EF={sm2['new_ease_factor']}, {sm2['learning_status']})")

# 2. Ebbinghaus Forgetting Curve
ret = space.forecast_ebbinghaus_retention(memory_stability_days=20.0, elapsed_days=7.0)
print()
print(f"Ebbinghaus Recall: {ret['projected_retention_pct']}% retention at day {ret['elapsed_days']} ({ret['review_recommendation']}, Half-Life={ret['memory_half_life_days']}d)")

# 3. Rasch IRT Adaptive Calibration
irt = space.calibrate_rasch_item_difficulty(student_ability_theta=1.5, item_difficulty_beta=1.2)
print()
print(f"Rasch IRT Model: P(Correct)={irt['probability_correct']} (Fisher Info={irt['fisher_information']}, {irt['item_suitability']})")
