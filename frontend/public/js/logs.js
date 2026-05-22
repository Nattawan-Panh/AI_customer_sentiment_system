import{db,ref,onValue,badge}from'./firebase-service.js';

onValue(ref(db,'logs'),
snap=>{
    logsTable.innerHTML=Object.values(snap.val()||{}).reverse().map(
        r=>`<tr>
        <td>${r.timestamp||'-'}</td>
        <td>${r.step||'-'}</td>
        <td>${badge(r.status)}</td>
        <td>${r.severity||'-'}</td>
        <td>${r.message||'-'}</td>
        <td>${r.fallback_used?'Yes':'No'}</td>
        </tr>`
    ).join('')
});
