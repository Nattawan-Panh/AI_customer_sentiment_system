import{db,ref,onValue}from'./firebase-service.js';

onValue(ref(db,'models'),
snap=>{
    modelsTable.innerHTML=Object.values(snap.val()||{}).map(
        r=>`<tr>
        <td>${r.name||'-'}</td>
        <td>${r.version||'-'}</td>
        <td>${r.accuracy||'-'}</td>
        <td>${r.precision||'-'}</td>
        <td>${r.recall||'-'}</td>
        <td>${r.f1_score||'-'}</td>
        <td>${r.updated_at||'-'}</td>
        </tr>`
    ).join('')
});
