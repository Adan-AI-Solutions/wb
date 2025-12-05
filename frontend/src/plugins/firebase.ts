import { initializeApp } from 'firebase/app'
import { getAuth, connectAuthEmulator } from 'firebase/auth'
import { getFunctions, httpsCallable, connectFunctionsEmulator } from 'firebase/functions'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID,
}

const firebaseApp = initializeApp(firebaseConfig)
export const firebaseAuth = getAuth(firebaseApp)
export const firebaseFunctions = getFunctions(firebaseApp, 'asia-northeast1')

// エミュレーター設定
if (import.meta.env.VITE_USE_EMULATOR === 'true') {
  connectAuthEmulator(firebaseAuth, 'http://localhost:9099')
  connectFunctionsEmulator(firebaseFunctions, 'localhost', 5001)
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const callCloudFunction = async <Response, Request extends Record<string, any> = Record<string, any>>(
  functionName: string,
  request: Request = {} as Request,
): Promise<Response> => {
  const func = httpsCallable<Request, Response>(firebaseFunctions, functionName)
  const result = await func(request)
  return result.data
}
