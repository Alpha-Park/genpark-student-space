# -*- coding: utf-8 -*-
"""
GenPark Student Space Client
Pure Python Standard Library (Zero External Dependencies)
Implements SuperMemo SM-2 spaced repetition interval calculation,
Ebbinghaus forgetting curve retention forecasting, and Rasch Item Response Theory (IRT) adaptive calibration.
"""

import math
from typing import Dict, Any, List, Optional

class GenParkStudentSpace:
    """
    Cognitive learning optimization, memory retention modeling, and adaptive testing engine.
    """

    def __init__(self):
        pass

    def calculate_sm2_interval_and_ease(
        self,
        repetition_count: int,
        previous_interval_days: int,
        previous_ease_factor: float = 2.5,
        response_quality: int = 4
    ) -> Dict[str, Any]:
        """
        Calculates next review interval and new ease factor using SuperMemo SM-2 algorithm:
          q in [0, 5]
          EF' = max(1.3, EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
          If q < 3: interval = 1, repetition = 0
          If q >= 3:
            rep == 0 -> I = 1
            rep == 1 -> I = 6
            rep >= 2 -> I = ceil(prev_interval * EF')
        """
        q = min(5, max(0, int(response_quality)))
        ef = max(1.3, float(previous_ease_factor))
        rep = max(0, int(repetition_count))

        # Update ease factor
        new_ef = ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        new_ef = round(max(1.3, new_ef), 3)

        if q < 3:
            # Memory failure, reset cycle
            next_interval = 1
            new_rep = 0
            status = "MEMORY_RELAPSE_RESET"
        else:
            if rep == 0:
                next_interval = 1
            elif rep == 1:
                next_interval = 6
            else:
                next_interval = math.ceil(max(1, previous_interval_days) * new_ef)
            new_rep = rep + 1
            status = "SUCCESSFUL_CONSOLIDATION"

        return {
            "response_quality_q": q,
            "previous_ease_factor": ef,
            "new_ease_factor": new_ef,
            "new_repetition_count": new_rep,
            "next_interval_days": next_interval,
            "learning_status": status
        }

    def forecast_ebbinghaus_retention(
        self,
        memory_stability_days: float = 14.0,
        elapsed_days: float = 5.0
    ) -> Dict[str, Any]:
        """
        Forecasts probability of recall using exponential Ebbinghaus forgetting curve:
          R(t) = exp( -t / S )
        """
        stability = max(0.1, float(memory_stability_days))
        elapsed = max(0.0, float(elapsed_days))

        retention = math.exp(-elapsed / stability)
        retention_pct = round(retention * 100.0, 1)

        # Half-life of memory
        half_life = round(stability * math.log(2.0), 2)

        if retention_pct >= 85.0:
            posture = "STABLE_HIGH_RECALL"
        elif retention_pct >= 70.0:
            posture = "OPTIMAL_REVIEW_WINDOW"
        elif retention_pct >= 50.0:
            posture = "VULNERABLE_REVIEW_OVERDUE"
        else:
            posture = "HIGH_FORGETTING_PROBABILITY"

        return {
            "memory_stability_days": stability,
            "elapsed_days": elapsed,
            "projected_retention_pct": retention_pct,
            "memory_half_life_days": half_life,
            "review_recommendation": posture
        }

    def calibrate_rasch_item_difficulty(
        self,
        student_ability_theta: float = 1.2,
        item_difficulty_beta: float = 0.8
    ) -> Dict[str, Any]:
        """
        Computes probability of correct answer using Rasch 1-parameter Item Response Theory (IRT):
          P(correct) = 1 / (1 + exp( -(theta - beta) ))
          Fisher Information: I(theta) = P * (1 - P)
        """
        diff = student_ability_theta - item_difficulty_beta
        prob = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, diff))))
        prob = round(prob, 4)

        info = round(prob * (1.0 - prob), 4)

        # Suitability for assessment (Fisher info maximized when theta ~= beta)
        if info >= 0.20:
            suitability = "OPTIMAL_DISCRIMINATION"
        elif info >= 0.10:
            suitability = "ACCEPTABLE_CHALLENGE"
        else:
            suitability = "TOO_EASY_OR_TOO_DIFFICULT"

        return {
            "student_ability_theta": student_ability_theta,
            "item_difficulty_beta": item_difficulty_beta,
            "probability_correct": prob,
            "fisher_information": info,
            "item_suitability": suitability
        }
