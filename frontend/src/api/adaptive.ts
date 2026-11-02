import {
  apiRequest,
} from "./client";

import type {
  AdaptivePlan,
} from "../types/adaptive";


export function getAdaptivePlan(
  studentId: string,
  conceptCode: string,
): Promise<AdaptivePlan> {
  return apiRequest<
    AdaptivePlan
  >(
    (
      "/adaptive/students/"
      + `${studentId}`
      + "/concepts/"
      + `${conceptCode}`
      + "/plan"
    ),
  );
}