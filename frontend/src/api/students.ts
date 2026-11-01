import { apiRequest } from "./client";

import type {
  Student,
  StudentCreatePayload,
} from "../types/student";


export function createStudent(
  payload: StudentCreatePayload,
): Promise<Student> {
  return apiRequest<Student>(
    "/students",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );
}


export function getStudent(
  studentId: string,
): Promise<Student> {
  return apiRequest<Student>(
    `/students/${studentId}`,
  );
}