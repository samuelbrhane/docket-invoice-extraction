/** A failed API call, with the message FastAPI sent back. */
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

type ValidationDetail = { msg: string; loc?: (string | number)[] }[];

async function errorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as { detail?: string | ValidationDetail };
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) return body.detail.map((item) => item.msg).join(". ");
  } catch {
    // not JSON, fall through
  }
  return `Request failed with status ${response.status}`;
}

export async function ensureOk(response: Response): Promise<Response> {
  if (!response.ok) throw new ApiError(response.status, await errorMessage(response));
  return response;
}

let session: Promise<void> | null = null;

/**
 * Make sure the visitor cookie exists before other calls run.
 * Without this, two calls on a first visit could each create their own visitor.
 */
export function ensureSession(): Promise<void> {
  session ??= fetch("/api/session", { credentials: "same-origin" })
    .then(ensureOk)
    .then(() => undefined)
    .catch((error) => {
      session = null;
      throw error;
    });
  return session;
}

/** Call the API through the Next.js proxy. The visitor cookie goes along automatically. */
export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  await ensureSession();
  const response = await ensureOk(await fetch(`/api${path}`, { ...init, credentials: "same-origin" }));
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export function sendJson<T>(path: string, method: "POST" | "PATCH", body?: unknown): Promise<T> {
  return request<T>(path, {
    method,
    headers: body === undefined ? undefined : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}