import{firebaseConfig}from'./firebase-config.js';
import{initializeApp}from'https://www.gstatic.com/firebasejs/10.12.4/firebase-app.js';
import{
    getAuth,
    onAuthStateChanged,
    setPersistence,
    browserSessionPersistence
}from'https://www.gstatic.com/firebasejs/10.12.4/firebase-auth.js';

const app=initializeApp(firebaseConfig);
const auth=getAuth(app);

await setPersistence(auth,browserSessionPersistence);

onAuthStateChanged(auth,user=>{
    if(!user || sessionStorage.getItem('isLoggedIn')!=='true'){
        window.location.replace('login.html');
    }
});