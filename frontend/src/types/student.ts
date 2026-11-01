export type AgeGroup =
  | "FOUNDATION"
  | "DEVELOPING"
  | "INDEPENDENT";


export interface StudentCreatePayload {
  display_name: string;
  age: number;
  grade: string;
  parent_id?: string | null;
  preferred_language?: string;
  curriculum_profile?: string;
}


export interface Student {
  id: string;
  parent_id: string | null;
  display_name: string;
  age: number;
  grade: string;
  age_group: AgeGroup;
  preferred_language: string;
  curriculum_profile: string;
  created_at: string;
  updated_at: string;
}