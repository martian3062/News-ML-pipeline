'use client';

import { AnimatePresence } from 'framer-motion';
import { useRouter, usePathname } from 'next/navigation';
import { useModals } from '@/context/ModalContext';
import Navbar from './Navbar';
import SignInModal from '../modals/SignInModal';
import DemoModal from '../modals/DemoModal';
import ConciergePanel from '../modals/ConciergePanel';

export default function NavbarWrapper() {
  const { 
    showSignIn, setShowSignIn, 
    showDemo, setShowDemo, 
    showConcierge, setShowConcierge 
  } = useModals();
  
  const router = useRouter();
  const pathname = usePathname();

  const handleSearch = (query: string) => {
    if (pathname === '/') {
       const el = document.getElementById('trending');
       if (el) el.scrollIntoView({ behavior: 'smooth' });
    } else {
       router.push(`/#trending?search=${encodeURIComponent(query)}`);
    }
  };

  return (
    <>
      <Navbar 
        onSignIn={() => setShowSignIn(true)} 
        onSearch={handleSearch}
      />
      
      <AnimatePresence>
        {showSignIn && <SignInModal onClose={() => setShowSignIn(false)} />}
        {showDemo && <DemoModal onClose={() => setShowDemo(false)} />}
        {showConcierge && <ConciergePanel onClose={() => setShowConcierge(false)} />}
      </AnimatePresence>

      {/* Floating Concierge Trigger (optional, or rely on Navbar) */}
      {!showConcierge && (
        <button 
          onClick={() => setShowConcierge(true)}
          className="fixed-concierge-trigger"
          style={{
            position: 'fixed',
            bottom: 32,
            right: 32,
            width: 56,
            height: 56,
            borderRadius: '50%',
            background: 'var(--gradient-primary)',
            color: 'white',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-lg)',
            zIndex: 40,
            cursor: 'pointer',
            border: 'none',
          }}
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/></svg>
        </button>
      )}
    </>
  );
}
