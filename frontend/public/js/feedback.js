import{db,ref,onValue}from'./firebase-service.js';

onValue(ref(db,'feedback'),
snap=>{
    feedbackList.innerHTML=Object.values(snap.val()||{}).reverse().map(
        r=>`<div class='card'><b>${r.admin_action||'-'}</b>
        <p>${r.edited_reply||''}</p>
        <p class='small'>comment_id: ${r.comment_id||'-'} | ${r.created_at||'-'}</p>
        </div>`
    ).join('')
});
