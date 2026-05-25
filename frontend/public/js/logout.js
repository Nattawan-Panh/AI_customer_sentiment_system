import { auth, signOut } from './firebase-service.js';

window.logout = async function () {
  await signOut(auth);
  sessionStorage.removeItem('isLoggedIn');
  window.location.replace('login.html');
};