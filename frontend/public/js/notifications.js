import{db,ref,onValue,badge}from'./firebase-service.js';

onValue(ref(db,'notifications'),
snap=>{
    notificationsTable.innerHTML=Object.entries(snap.val()||{}).map(
        ([id,v])=>({id,...v})
    ).reverse().map(
        r=>`<tr>
        <td>${r.created_at||'-'}</td>
        <td>${badge(r.type)}</td>
        <td>${r.channel||'-'}</td>
        <td>${badge(r.status)}</td>
        <td>${r.subject||'-'}</td>
        <td>${r.comment_id||'-'}</td>
        </tr>`
    ).join('')
});
