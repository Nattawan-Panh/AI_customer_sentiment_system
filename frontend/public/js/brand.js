import{db,ref,onValue,set}from'./firebase-service.js';

const brandRef=ref(db,'brand_settings/default');

onValue(brandRef,s=>{
    const d=s.val()||{};brandName.value=d.brand_name||'';
    
    tone.value=d.tone||'สุภาพ';persona.value=d.persona||'';
    forbiddenWords.value=(d.forbidden_words||[]).join(', ')
});

saveBrand.addEventListener('click',async()=>{
    await set(brandRef,{
        brand_name:brandName.value,
        tone:tone.value,
        persona:persona.value,
        forbidden_words:forbiddenWords.value.split(',').map(w=>w.trim()).filter(Boolean),
        updated_at:new Date().toISOString()
    });
    alert('Saved')
});
