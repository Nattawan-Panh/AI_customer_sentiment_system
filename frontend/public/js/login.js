import {
  auth,
  signInWithEmailAndPassword
} from './firebase-service.js';

const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const errorText = document.getElementById('errorText');

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  try {
    errorText.textContent = '';

    await signInWithEmailAndPassword(auth, email, password);

    window.location.href = 'index.html';

  } catch (error) {
    errorText.textContent = 'อีเมลหรือรหัสผ่านไม่ถูกต้อง';
  }
});