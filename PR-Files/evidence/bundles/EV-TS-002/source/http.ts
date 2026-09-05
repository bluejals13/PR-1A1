// api/http.ts

import { useAuthStore } from "../store/auth.store";

type TokenResponse = {
  accessToken: string;
  grantType: string;
};

type ApiResponse<T> = {
  status: string;
  message: string;
  data: T;
};

type ErrorResponse = {
  code?: string;
  message?: string;
};

export class HttpError extends Error {
  constructor(
    public readonly status: number,
    message: string,
  ) {
    super(message);
    this.name = "HttpError";
  }
}

export class RefreshTokenError extends HttpError {
  constructor(
    status: number,
    message = "Refresh token request failed",
  ) {
    super(status, message);
    this.name = "RefreshTokenError";
  }
}

export class AccountSuspendedError extends HttpError {
  constructor(
    message = "Account suspended",
  ) {
    super(403, message);
    this.name = "AccountSuspendedError";
  }
}

// 여러 요청이 동시에 401을 받아도 refresh는 한 번만 실행
let refreshPromise: Promise<TokenResponse | null> | null = null;

const REFRESH_TIMEOUT = 5000;

export async function refreshToken(): Promise<TokenResponse | null> {
  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise = (async () => {
    const controller = new AbortController();

    const timeoutId = window.setTimeout(() => {
      controller.abort();
    }, REFRESH_TIMEOUT);

    try {
      const res = await fetch("/api/auth/refresh", {
        method: "POST",
        credentials: "include",
        signal: controller.signal,
      });

      if (!res.ok) {
        throw new RefreshTokenError(
          res.status,
          "Refresh token request failed",
        );
      }

      const response: ApiResponse<TokenResponse> =
        await res.json();

      // ApiResponse.data 안에 LoginResponse가 들어 있음
      return response.data;

    } catch (error) {
      if (
        error instanceof DOMException &&
        error.name === "AbortError"
      ) {
        throw new RefreshTokenError(
          503,
          "Authentication service timeout",
        );
      }

      if (error instanceof RefreshTokenError) {
        throw error;
      }

      throw new RefreshTokenError(
        503,
        "Authentication service unavailable",
      );
    } finally {
      window.clearTimeout(timeoutId);
      refreshPromise = null;
    }
  })();

  return refreshPromise;
}

export async function request<T>(
  url: string,
  options: RequestInit = {},
  retry = true,
): Promise<T> {

  const token = useAuthStore.getState().token;

  const res = await fetch(url, {
    ...options,

    credentials: "include",

    headers: {
      "Content-Type": "application/json",

      ...(token
        ? {
          Authorization: `Bearer ${token}`,
        }
        : {}),

      ...(options.headers || {}),
    },
  });

  // Access Token 만료
  if (res.status === 401 && retry) {

    const newToken = await refreshToken();

    if (!newToken?.accessToken) {
      throw new RefreshTokenError(
        401,
        "Unauthorized",
      );
    }

    // 새 Access Token 저장
    useAuthStore
      .getState()
      .login(newToken.accessToken);

    // 원래 요청 다시 실행
    return request<T>(
      url,
      {
        ...options,

        headers: {
          ...options.headers,
          Authorization: `Bearer ${newToken.accessToken}`,
        },
      },
      false,
    );
  }

  if (!res.ok) {

    const text = await res.text();

    let body: ErrorResponse = {};

    try {
      body = text ? JSON.parse(text) : {};
    } catch {
      // JSON이 아닌 응답
    }

    // 계정 정지
    if (
      res.status === 403 &&
      body.code === "ACCOUNT_SUSPENDED"
    ) {
      useAuthStore.getState().logout();

      throw new AccountSuspendedError(
        body.message ?? "Account suspended",
      );
    }

    throw new HttpError(
      res.status,
      body.message ?? (text || "Request failed"),
    );
  }

  // DELETE 등 응답 body가 없을 수도 있음
  if (res.status === 204) {
    return undefined as T;
  }

  const response: ApiResponse<T> = await res.json();

  return response.data;
}

export const http = {

  get: <T>(url: string): Promise<T> =>
    request<T>(url, {
      method: "GET",
    }),

  post: <T>(
    url: string,
    body?: unknown,
    options?: RequestInit,
  ): Promise<T> =>
    request<T>(url, {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },

      body:
        body !== undefined
          ? JSON.stringify(body)
          : undefined,

      ...options,
    }),

  patch: <T>(
    url: string,
    body?: unknown,
  ): Promise<T> =>
    request<T>(url, {
      method: "PATCH",

      headers: {
        "Content-Type": "application/json",
      },

      body:
        body !== undefined
          ? JSON.stringify(body)
          : undefined,
    }),

  put: <T>(
    url: string,
    body?: unknown,
  ): Promise<T> =>
    request<T>(url, {
      method: "PUT",

      headers: {
        "Content-Type": "application/json",
      },

      body:
        body !== undefined
          ? JSON.stringify(body)
          : undefined,
    }),

  delete: <T>(url: string): Promise<T> =>
    request<T>(url, {
      method: "DELETE",
    }),
};