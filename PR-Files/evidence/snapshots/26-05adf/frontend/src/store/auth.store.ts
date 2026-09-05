// store/auth.store.ts

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { STORAGE_KEYS } from "../constants/keys";

type AuthState = {
  token: string | null;

  authServiceUnavailable: boolean;

  setToken: (token: string | null) => void;
  setAuthServiceUnavailable: (value: boolean) => void;

  login: (token: string) => void;
  logout: () => void;
};

export const useAuthStore = create(
  persist<AuthState>(
    (set) => ({
      token: null,

      authServiceUnavailable: false,

      setToken: (token) =>
        set({
          token,
          authServiceUnavailable: false,
        }),

      setAuthServiceUnavailable: (value) =>
        set({
          authServiceUnavailable: value,
        }),

      login: (token) =>
        set({
          token,
          authServiceUnavailable: false,
        }),

      logout: () =>
        set({
          token: null,
          authServiceUnavailable: false,
        }),
    }),
    {
      name: STORAGE_KEYS.auth,
    }
  )
);