import { create } from "zustand";

export const useToastStore = create((set, get) => ({
  toasts: [],

  addToast: (message, type = "info") => {
    const id = Date.now();
    const toast = { id, message, type };

    set((state) => ({
      toasts: [...state.toasts, toast],
    }));

    setTimeout(() => {
      get().removeToast(id);
    }, 4000);
  },

  removeToast: (id) => {
    set((state) => ({
      toasts: state.toasts.filter((toast) => toast.id !== id),
    }));
  },
}));
