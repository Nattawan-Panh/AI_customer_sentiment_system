import {
  auth,
  onAuthStateChanged,
  signOut
} from './firebase-service.js';

onAuthStateChanged(auth, (user) => {
  const currentPage = window.location.pathname;

  if (!user && !currentPage.includes('login.html')) {
    window.location.href = 'login.html';
  }

  if (user && currentPage.includes('login.html')) {
    window.location.href = 'index.html';
  }
});

window.logout = async function () {
  try {
    await signOut(auth);
    window.location.href = 'login.html';
  } catch (error) {
    alert('Logout failed: ' + error.message);
  }
};