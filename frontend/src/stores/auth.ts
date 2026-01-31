import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { 
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  type User
} from 'firebase/auth';
import { auth } from '@/services/firebase/config';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const loading = ref(true);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!user.value);

  // Initialize auth listener
  const initAuth = () => {
    onAuthStateChanged(auth, (firebaseUser) => {
      user.value = firebaseUser;
      loading.value = false;
    });
  };

  // Sign in
  const signIn = async (email: string, password: string) => {
    try {
      error.value = null;
      loading.value = true;
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      user.value = userCredential.user;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Sign up
  const signUp = async (email: string, password: string) => {
    try {
      error.value = null;
      loading.value = true;
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      user.value = userCredential.user;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  // Sign out
  const logout = async () => {
    try {
      await signOut(auth);
      user.value = null;
    } catch (err: any) {
      error.value = err.message;
      throw err;
    }
  };

  return {
    user,
    loading,
    error,
    isAuthenticated,
    initAuth,
    signIn,
    signUp,
    logout
  };
});
EOF