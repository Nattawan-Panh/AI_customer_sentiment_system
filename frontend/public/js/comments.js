import{db,ref,onValue,badge,short}from'./firebase-service.js';

let rows=[];
function render(){
    const sf=sentimentFilter.value,
    st=statusFilter.value;
    commentsTable.innerHTML=rows.filter(
        r=>(!sf||r.sentiment===sf)&&(!st||r.status===st)
    ).map
    (
        r=>`<tr>
        <td>${r.customer_name||r.line_user_id||'-'}</td>
        <td>${short(r.original_text,120)}</td>
        <td>${badge(r.sentiment)}</td><td>${r.intent||'-'}</td>
        <td>${badge(r.risk_level)}</td><td>${badge(r.status)}</td>
        <td>${r.created_at||'-'}</td>
        </tr>`
    ).join('')
}

onValue(ref(db,'messages'),
snap=>{rows=Object.entries(snap.val()||{}).map(([id,v])=>({id,...v})).reverse();render()});
sentimentFilter.addEventListener('change',render);
statusFilter.addEventListener('change',render);
