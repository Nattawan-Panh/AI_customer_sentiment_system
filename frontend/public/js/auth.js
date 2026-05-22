import{firebaseConfig}from'./firebase-config.js';
import{initializeApp}from'https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js';
import{getAuth,signInWithEmailAndPassword,onAuthStateChanged}from'https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js';

const app=initializeApp(firebaseConfig);
const auth=getAuth(app);onAuthStateChanged(auth,u=>{if(u)window.location.href='index.html'});

loginBtn.addEventListener('click',async()=>{
    try{
        await signInWithEmailAndPassword(auth,email.value,password.value);
        loginMessage.textContent='Login success';window.location.href='index.html'
    }
    catch(e){
        loginMessage.textContent='Login failed: '+e.message
    }
});
