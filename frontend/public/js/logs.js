import{db,ref,onValue,badge,escapeHtml}from'./firebase-service.js';

onValue(ref(db,'logs'),
snap=>{
    logsTable.innerHTML=Object.values(snap.val()||{}).reverse().map(
        r=>`<tr>
        <td>${escapeHtml(r.timestamp||'-')}</td>
        <td>${escapeHtml(r.step||'-')}</td>
        <td>${badge(r.status)}</td>
        <td>${escapeHtml(r.severity||'-')}</td>
        <td>${escapeHtml(r.message||'-')}</td>
        <td>${r.fallback_used?'Yes':'No'}</td>
        </tr>`
    ).join('')
});