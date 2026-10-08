from app.schemas.enums import (
    AttemptStatus,
    LearningMode,
    Subject,
    TutorAction,
    TutorIntent,
)
from app.tutor.decision_models import (
    TutorDecisionInput,
    TutorDecisionResult,
)
from app.tutor.hint_ladder import (
    calculate_next_hint_level,
    get_hint_action,
)
from app.tutor.session_state import (
    TutorSessionState,
)


class TutorPolicyEngine:

    def decide(
        self,
        state: TutorSessionState,
        decision_input: TutorDecisionInput,
    ) -> TutorDecisionResult:

        intent = decision_input.intent

        # ----------------------------------
        # 1. Safety has highest priority
        # ----------------------------------

        if intent == TutorIntent.SAFETY_SENSITIVE:

            return self._result(
                state=state,
                intent=intent,
                action=TutorAction.ESCALATE_SAFETY,
                hint_level=state.hint_level,
                allow_final_answer=False,
                reason=(
                    "Safety-sensitive input overrides "
                    "normal tutoring behavior."
                ),
            )

        # ----------------------------------
        # 2. Mock Test restriction
        # ----------------------------------

        if state.mode == LearningMode.MOCK_TEST:

            return self._handle_mock_test(
                state=state,
                decision_input=decision_input,
            )

        # ----------------------------------
        # 3. Policy bypass
        # ----------------------------------

        if intent == TutorIntent.POLICY_BYPASS:

            return self._result(
                state=state,
                intent=intent,
                action=TutorAction.REFUSE_POLICY_BYPASS,
                hint_level=state.hint_level,
                allow_final_answer=False,
                policy_bypass_detected=True,
                reason=(
                    "The request attempts to bypass "
                    "the Tutor Policy."
                ),
            )

        # ----------------------------------
        # 4. New problem
        # ----------------------------------

        if decision_input.new_problem:

            return self._result(
                state=state,
                intent=intent,
                action=TutorAction.ASK_ATTEMPT,
                hint_level=0,
                allow_final_answer=False,
                reason=(
                    "A new problem resets the hint ladder."
                ),
            )

        # ----------------------------------
        # 5. Prerequisite problem
        # ----------------------------------

        if decision_input.prerequisite_gap:

            return self._result(
                state=state,
                intent=intent,
                action=(
                    TutorAction.SWITCH_TO_PREREQUISITE
                ),
                hint_level=state.hint_level,
                allow_final_answer=False,
                reason=(
                    "A prerequisite knowledge gap "
                    "was detected."
                ),
            )

        # ----------------------------------
        # 6. Direct answer request
        # ----------------------------------

        if (
            intent
            == TutorIntent.DIRECT_ANSWER_REQUEST
        ):

            return self._handle_direct_answer_request(
                state=state,
                intent=intent,
            )

        # ----------------------------------
        # 7. Homework Help
        # ----------------------------------

        if intent == TutorIntent.HOMEWORK_REQUEST:

            if state.attempt_count == 0:

                return self._result(
                    state=state,
                    intent=intent,
                    action=TutorAction.ASK_ATTEMPT,
                    hint_level=state.hint_level,
                    allow_final_answer=False,
                    reason=(
                        "Homework Help requires "
                        "an initial learner attempt."
                    ),
                )

            return self._result(
                state=state,
                intent=intent,
                action=TutorAction.ASK_GUIDING_QUESTION,
                hint_level=max(
                    state.hint_level,
                    2,
                ),
                allow_final_answer=False,
                reason=(
                    "The learner has already attempted "
                    "the problem, so guided help "
                    "is appropriate."
                ),
            )

        # ----------------------------------
        # 8. Hint / Confusion / I don't know
        # ----------------------------------

        if intent in {
            TutorIntent.HINT_REQUEST,
            TutorIntent.CONFUSION,
            TutorIntent.I_DONT_KNOW,
        }:

            return self._handle_help_request(
                state=state,
                decision_input=decision_input,
            )

        # ----------------------------------
        # 9. Student Attempt
        # ----------------------------------

        if intent == TutorIntent.STUDENT_ATTEMPT:

            return self._handle_attempt(
                state=state,
                decision_input=decision_input,
            )

        # ----------------------------------
        # 10. Learn Mode
        # ----------------------------------

        if intent == TutorIntent.LEARN_CONCEPT:

            return self._result(
                state=state,
                intent=intent,
                action=TutorAction.ASK_PRIOR_KNOWLEDGE,
                hint_level=0,
                allow_final_answer=False,
                reason=(
                    "Learn Mode begins by checking "
                    "the learner's prior knowledge."
                ),
            )

        # ----------------------------------
        # 11. Explanation request
        # ----------------------------------

        if (
            intent
            == TutorIntent.EXPLANATION_REQUEST
        ):

            if state.mode == LearningMode.LEARN:

                return self._result(
                    state=state,
                    intent=intent,
                    action=(
                        TutorAction
                        .GIVE_FULL_TEACHING_EXPLANATION
                    ),
                    hint_level=7,
                    allow_final_answer=True,
                    reason=(
                        "A complete concept explanation "
                        "is appropriate in Learn Mode."
                    ),
                )

            return self._result(
                state=state,
                intent=intent,
                action=TutorAction.ASK_GUIDING_QUESTION,
                hint_level=max(
                    state.hint_level,
                    2,
                ),
                allow_final_answer=False,
                reason=(
                    "Problem-solving modes should "
                    "provide guidance before a "
                    "full solution."
                ),
            )

        # ----------------------------------
        # 12. Practice request
        # ----------------------------------

        if intent == TutorIntent.PRACTICE_REQUEST:

            return self._result(
                state=state,
                intent=intent,
                action=(
                    TutorAction
                    .GENERATE_PRACTICE_QUESTION
                ),
                hint_level=0,
                allow_final_answer=False,
                reason=(
                    "Practice Mode should generate "
                    "a new question without revealing "
                    "the answer."
                ),
            )

        # ----------------------------------
        # 13. Off topic
        # ----------------------------------

        if intent == TutorIntent.OFF_TOPIC:

            return self._result(
                state=state,
                intent=intent,
                action=TutorAction.REDIRECT_TO_LEARNING,
                hint_level=state.hint_level,
                allow_final_answer=False,
                reason=(
                    "The conversation should gently "
                    "return to learning."
                ),
            )

        # ----------------------------------
        # Default
        # ----------------------------------

        return self._result(
            state=state,
            intent=intent,
            action=TutorAction.ASK_GUIDING_QUESTION,
            hint_level=state.hint_level,
            allow_final_answer=False,
            reason="Default guided-learning behavior.",
        )

    # ======================================================
    # DIRECT ANSWER HANDLER
    # ======================================================

    def _handle_direct_answer_request(
        self,
        state: TutorSessionState,
        intent: TutorIntent,
    ) -> TutorDecisionResult:

        if state.attempt_count == 0:

            action = TutorAction.ASK_ATTEMPT

            reason = (
                "The learner requested the answer "
                "before attempting the problem."
            )

        else:

            action = TutorAction.ASK_GUIDING_QUESTION

            reason = (
                "The learner has attempted the problem, "
                "but guided help should be provided "
                "before answer disclosure."
            )

        return self._result(
            state=state,
            intent=intent,
            action=action,
            hint_level=state.hint_level,
            allow_final_answer=False,
            reason=reason,
        )

    # ======================================================
    # HELP REQUEST HANDLER
    # ======================================================

    def _handle_help_request(
        self,
        state: TutorSessionState,
        decision_input: TutorDecisionInput,
    ) -> TutorDecisionResult:

        next_level = calculate_next_hint_level(
            current_level=state.hint_level,
            age_group=state.age_group,
            repeated_confusion=(
                decision_input.repeated_confusion
            ),
        )

        action = get_hint_action(
            next_level
        )

        allow_answer = (
            next_level >= 7
        )

        return self._result(
            state=state,
            intent=decision_input.intent,
            action=action,
            hint_level=next_level,
            allow_final_answer=allow_answer,
            reason=(
                "Assistance was increased using "
                "the progressive hint ladder."
            ),
        )

    # ======================================================
    # ATTEMPT HANDLER
    # ======================================================

    def _handle_attempt(
        self,
        state: TutorSessionState,
        decision_input: TutorDecisionInput,
    ) -> TutorDecisionResult:

        attempt_status = (
            decision_input.attempt_status
        )

        if attempt_status == AttemptStatus.CORRECT:

            return self._result(
                state=state,
                intent=decision_input.intent,
                action=(
                    TutorAction.GIVE_MASTERY_QUESTION
                ),
                hint_level=state.hint_level,
                allow_final_answer=True,
                requires_mastery_check=True,
                reason=(
                    "The learner's attempt is correct. "
                    "An independent mastery check "
                    "should follow."
                ),
            )

        if (
            attempt_status
            == AttemptStatus.PARTIALLY_CORRECT
        ):

            return self._result(
                state=state,
                intent=decision_input.intent,
                action=(
                    TutorAction.ASK_GUIDING_QUESTION
                ),
                hint_level=max(
                    state.hint_level,
                    2,
                ),
                allow_final_answer=False,
                reason=(
                    "Partially correct work should "
                    "receive targeted guidance."
                ),
            )

        if attempt_status == AttemptStatus.INCORRECT:

            next_level = calculate_next_hint_level(
                current_level=max(
                    state.hint_level,
                    1,
                ),
                age_group=state.age_group,
                repeated_confusion=(
                    decision_input.repeated_confusion
                ),
            )

            return self._result(
                state=state,
                intent=decision_input.intent,
                action=get_hint_action(
                    next_level
                ),
                hint_level=next_level,
                allow_final_answer=(
                    next_level >= 7
                ),
                reason=(
                    "The incorrect attempt requires "
                    "additional scaffolding."
                ),
            )

        if attempt_status == AttemptStatus.INCOMPLETE:

            return self._result(
                state=state,
                intent=decision_input.intent,
                action=(
                    TutorAction.ASK_GUIDING_QUESTION
                ),
                hint_level=max(
                    state.hint_level,
                    2,
                ),
                allow_final_answer=False,
                reason=(
                    "The attempt is incomplete and "
                    "needs a next-step question."
                ),
            )

        return self._result(
            state=state,
            intent=decision_input.intent,
            action=TutorAction.ASK_GUIDING_QUESTION,
            hint_level=state.hint_level,
            allow_final_answer=False,
            reason=(
                "The learner's attempt could not "
                "be clearly classified."
            ),
        )

    # ======================================================
    # MOCK TEST
    # ======================================================

    def _handle_mock_test(
        self,
        state: TutorSessionState,
        decision_input: TutorDecisionInput,
    ) -> TutorDecisionResult:

        if decision_input.intent in {
            TutorIntent.MOCK_TEST_RESPONSE,
            TutorIntent.STUDENT_ATTEMPT,
        }:

            action = TutorAction.RECORD_TEST_RESPONSE

            reason = (
                "Mock Test Mode records learner "
                "answers without providing hints."
            )

        else:

            action = (
                TutorAction.CLARIFY_TEST_INSTRUCTION
            )

            reason = (
                "Hints and explanations are disabled "
                "during Mock Test Mode."
            )

        return self._result(
            state=state,
            intent=decision_input.intent,
            action=action,
            hint_level=state.hint_level,
            allow_final_answer=False,
            requires_rag=False,
            requires_validation=False,
            reason=reason,
        )

    # ======================================================
    # COMMON RESULT BUILDER
    # ======================================================

    def _result(
        self,
        state: TutorSessionState,
        intent: TutorIntent,
        action: TutorAction,
        hint_level: int,
        allow_final_answer: bool,
        reason: str,
        requires_mastery_check: bool = False,
        policy_bypass_detected: bool = False,
        requires_rag: bool | None = None,
        requires_validation: bool | None = None,
    ) -> TutorDecisionResult:

        if requires_rag is None:

            requires_rag = (
                state.subject
                in {
                    Subject.SCIENCE,
                    Subject.GENERAL,
                }
            )

        if requires_validation is None:

            requires_validation = (
                state.subject == Subject.MATH
                and intent
                == TutorIntent.STUDENT_ATTEMPT
            )

        return TutorDecisionResult(
            session_id=state.session_id,
            student_id=state.student_id,
            subject=state.subject,
            mode=state.mode,
            age_group=state.age_group,
            intent=intent,
            next_action=action,
            hint_level=hint_level,
            allow_final_answer=allow_final_answer,
            requires_rag=requires_rag,
            requires_validation=requires_validation,
            requires_mastery_check=(
                requires_mastery_check
            ),
            policy_bypass_detected=(
                policy_bypass_detected
            ),
            reason=reason,
        )