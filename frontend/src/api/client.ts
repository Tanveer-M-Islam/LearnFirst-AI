
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL?.trim()
  || "/api/v1"
).replace(/\/+$/, "");


interface ApiErrorPayload {
  detail?: unknown;
}


export class ApiError extends Error {
  status: number;

  constructor(
    message: string,
    status: number,
  ) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}


export class ApiNetworkError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ApiNetworkError";
  }
}


export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {

  const headers = new Headers(
    options.headers,
  );

  if (
    options.body !== undefined
    && options.body !== null
    && !headers.has("Content-Type")
  ) {
    headers.set(
      "Content-Type",
      "application/json",
    );
  }

  let response: Response;

  // ======================================
  // Network request
  // ======================================

  try {
    response = await fetch(
      `${API_BASE_URL}${path}`,
      {
        ...options,
        headers,
      },
    );

  } catch (err) {

    if (
      err instanceof DOMException
      && err.name === "AbortError"
    ) {
      throw err;
    }

    throw new ApiNetworkError(
      "Cannot connect to LearnFirst AI. "
      + "Check your internet connection "
      + "or backend service."
    );
  }


  // ======================================
  // HTTP errors
  // ======================================

  if (!response.ok) {
    let message =
      `API request failed (HTTP ${response.status}).`;

    try {
      const body =
        (await response.json()) as ApiErrorPayload;

      if (typeof body.detail === "string") {
        message = body.detail;
      }

    } catch {
      // Keep the HTTP error message.
    }

    throw new ApiError(
      message,
      response.status,
    );
  }


  // ======================================
  // Successful response
  // ======================================

  if (response.status === 204) {
    return undefined as T;
  }

  try {
    return (await response.json()) as T;
  } catch {
    throw new ApiNetworkError(
      "The server returned an invalid JSON response."
    );
  }
}
