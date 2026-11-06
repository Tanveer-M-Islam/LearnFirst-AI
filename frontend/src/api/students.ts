import {
  apiRequest,
} from "./client";

import type {
  Student,
  StudentCreatePayload,
} from "../types/student";


export interface StudentLoginPayload {
  username: string;
  password: string;
}


export interface StudentCredentialsPayload {
  username: string;
  password: string;
  current_password?: string | null;
}


export function createStudent(
  payload: StudentCreatePayload,
): Promise<Student> {

  return apiRequest<Student>(
    "/students",
    {
      method: "POST",

      body:
        JSON.stringify(
          payload,
        ),
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


export function loginStudent(
  payload: StudentLoginPayload,
): Promise<Student> {

  return apiRequest<Student>(
    "/students/login",
    {
      method: "POST",

      body:
        JSON.stringify(
          payload,
        ),
    },
  );
}


export function updateStudentCredentials(
  studentId: string,
  payload: StudentCredentialsPayload,
): Promise<Student> {

  return apiRequest<Student>(
    (
      `/students/${studentId}`
      + "/credentials"
    ),
    {
      method: "PATCH",

      body:
        JSON.stringify(
          payload,
        ),
    },
  );
}