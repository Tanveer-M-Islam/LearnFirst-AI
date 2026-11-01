import type { Student } from "../types/student";


const STORAGE_KEY =
  "learnfirst_active_student";


export function saveStudent(
  student: Student,
): void {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify(student),
  );
}


export function getStoredStudent():
  Student | null {
  const stored =
    localStorage.getItem(
      STORAGE_KEY,
    );

  if (!stored) {
    return null;
  }

  try {
    return JSON.parse(
      stored,
    ) as Student;
  } catch {
    localStorage.removeItem(
      STORAGE_KEY,
    );

    return null;
  }
}


export function clearStoredStudent():
  void {
  localStorage.removeItem(
    STORAGE_KEY,
  );
}