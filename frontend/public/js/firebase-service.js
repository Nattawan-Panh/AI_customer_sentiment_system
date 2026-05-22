import { firebaseConfig } from './firebase-config.js';

import {
  initializeApp
} from 'https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js';

import {
  getDatabase,
  ref,
  onValue,
  push,
  set,
  update
} from 'https://www.gstatic.com/firebasejs/10.12.4/firebase-database.js';

import {
  getAuth,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut
} from 'https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js';

export const app = initializeApp(firebaseConfig);
export const db = getDatabase(app);
export const auth = getAuth(app);

export {
  ref,
  onValue,
  push,
  set,
  update,
  onAuthStateChanged,
  signInWithEmailAndPassword,
  signOut
};

export function badge(v) {
  const t = String(v || 'unknown');
  return `<span class="badge ${t} ${t.toLowerCase()}">${t}</span>`;
}

export function short(text, max = 90) {
  text = String(text || '');
  return text.length > max ? text.slice(0, max) + '...' : text;
}