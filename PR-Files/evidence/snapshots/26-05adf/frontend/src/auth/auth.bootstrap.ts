// auth/auth.bootstrap.ts

import { useAuthStore } from "../store/auth.store";
import { queryClient } from "../queryClient";

import {
  refreshToken,
  RefreshTokenError,
} from "../api/http";

import { authKeys } from "./auth.keys";

let bootstrapPromise: Promise<void> | null = null;

export function bootstrapAuth(): Promise<void> {
  if (bootstrapPromise) {
    return bootstrapPromise;
  }

  bootstrapPromise = (async () => {
    try {
      const data = await refreshToken();

      // Refresh 성공
      if (data?.accessToken) {
        useAuthStore
          .getState()
          .setToken(data.accessToken);

        useAuthStore
          .getState()
          .setAuthServiceUnavailable(false);

        return;
      }

      // Refresh Token이 없거나 만료됨
      useAuthStore
        .getState()
        .logout();

      await queryClient.resetQueries({
        queryKey: authKeys.all,
      });

    } catch (error) {

      // 인증 만료 / Refresh Token 무효
      if (
        error instanceof RefreshTokenError &&
        error.status === 401
      ) {
        useAuthStore
          .getState()
          .setAuthServiceUnavailable(false);

        useAuthStore
          .getState()
          .logout();

        await queryClient.resetQueries({
          queryKey: authKeys.all,
        });

        return;
      }

      // 인증 서버 장애
      if (
        error instanceof RefreshTokenError &&
        error.status === 503
      ) {
        useAuthStore
          .getState()
          .setAuthServiceUnavailable(true);

        console.warn(
          "[Auth] Authentication service unavailable."
        );

        // 중요:
        // 여기서는 logout 하지 않는다.
        return;
      }

      // 기타 네트워크 오류
      useAuthStore
        .getState()
        .setAuthServiceUnavailable(true);

      console.warn(
        "[Auth] Authentication service temporarily unavailable.",
        error
      );

    } finally {
      bootstrapPromise = null;
    }
  })();

  return bootstrapPromise;
}