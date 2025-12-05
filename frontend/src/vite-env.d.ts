/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_FIREBASE_API_KEY?: string
  readonly VITE_FIREBASE_AUTH_DOMAIN?: string
  readonly VITE_FIREBASE_PROJECT_ID?: string
  readonly VITE_FIREBASE_STORAGE_BUCKET?: string
  readonly VITE_FIREBASE_MESSAGING_SENDER_ID?: string
  readonly VITE_FIREBASE_APP_ID?: string
  readonly VITE_FIREBASE_MEASUREMENT_ID?: string
  readonly VITE_USE_EMULATOR?: string
  readonly VITE_API_TODOS_LIST_ENDPOINT?: string
  readonly VITE_API_TODOS_GET_ENDPOINT?: string
  readonly VITE_API_TODOS_CREATE_ENDPOINT?: string
  readonly VITE_API_TODOS_UPDATE_ENDPOINT?: string
  readonly VITE_API_TODOS_DELETE_ENDPOINT?: string
  readonly VITE_API_HEALTH_ENDPOINT?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
