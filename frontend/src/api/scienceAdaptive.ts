import {
  apiRequest,
} from "./client";

import type {
  ScienceAdaptivePlan,
} from "../types/scienceAdaptive";


export function getScienceAdaptivePlan(
  studentId: string,
  conceptCode: string,
): Promise<ScienceAdaptivePlan> {

  return apiRequest<
    ScienceAdaptivePlan
  >(
    (
      "/science/adaptive/students/"
      + studentId
      + "/concepts/"
      + conceptCode
      + "/plan"
    ),
  );
}