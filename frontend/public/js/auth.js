import{firebaseConfig}from'./firebase-config.js';
import{initializeApp}from'https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js';
import{
    getAuth,
    signInWithEmailAndPassword,
    setPersistence,
    browserSessionPersistence
}from'https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js';

const app=initializeApp(firebaseConfig);
const auth=getAuth(app);

await setPersistence(auth,browserSessionPersistence);

loginBtn.addEventListener('click',async()=>{
    try{
        await signInWithEmailAndPassword(auth,email.value,password.value);

        sessionStorage.setItem('isLoggedIn','true');

        loginMessage.textContent='Login success';
        window.location.replace('dashboard.html');
    }
    catch(e){
        loginMessage.textContent='Login failed : Invalid email or password';
    }
});