import {
  apiRequest,
} from "./client";

import type {
  EnglishAdaptivePlan,
} from "../types/englishAdaptive";


export function getEnglishAdaptivePlan(
  studentId: string,
  conceptCode: string,
): Promise<EnglishAdaptivePlan> {

  return apiRequest<
    EnglishAdaptivePlan
  >(
    (
      "/english/adaptive/students/"
      + studentId
      + "/concepts/"
      + conceptCode
      + "/plan"
    ),
  );
}