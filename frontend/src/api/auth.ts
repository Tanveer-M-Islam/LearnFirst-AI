import {
  apiRequest,
} from "./client";

import type {
  Student,
} from "../types/student";


export interface LoginPayload {
  username:
    string;

  password:
    string;
}


export function loginStudent(
  payload: LoginPayload,
): Promise<Student> {

  return apiRequest<Student>(
    "/students/login",

    {
      method:
        "POST",

      body:
        JSON.stringify(
          payload,
        ),
    },
  );
}