import{db,ref,onValue,push,set}from'./firebase-service.js';

addKb.addEventListener('click',async()=>{
    const r=push(ref(db,'knowledge_base'));
    await set(r,{
        title:kbTitle.value,
        type:kbType.value,
        content:kbContent.value,
        updated_at:new Date().toISOString()
    });
    
    kbTitle.value='';
    kbContent.value=''
});

onValue(ref(db,'knowledge_base'),
snap=>{
    kbList.innerHTML=Object.values(snap.val()||{}).map(
        i=>`<div class='card'>
        <b>${i.title}</b> 
        <span class='badge neutral'>${i.type}</span>
        <p>${i.content}</p>
        </div>`
    ).join('')
});
