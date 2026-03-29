'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

interface ModalContextType {
  showSignIn: boolean;
  setShowSignIn: (show: boolean) => void;
  showDemo: boolean;
  setShowDemo: (show: boolean) => void;
  showConcierge: boolean;
  setShowConcierge: (show: boolean) => void;
}

const ModalContext = createContext<ModalContextType | undefined>(undefined);

export function ModalProvider({ children }: { children: ReactNode }) {
  const [showSignIn, setShowSignIn] = useState(false);
  const [showDemo, setShowDemo] = useState(false);
  const [showConcierge, setShowConcierge] = useState(false);

  return (
    <ModalContext.Provider value={{
      showSignIn, setShowSignIn,
      showDemo, setShowDemo,
      showConcierge, setShowConcierge
    }}>
      {children}
    </ModalContext.Provider>
  );
}

export function useModals() {
  const context = useContext(ModalContext);
  if (context === undefined) {
    throw new Error('useModals must be used within a ModalProvider');
  }
  return context;
}
