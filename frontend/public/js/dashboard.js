import{db,ref,onValue,badge,short}from'./firebase-service.js';

onValue(ref(db,'comments'),
snap=>{
    const rows=Object.entries(snap.val()||{}).map(([id,v])=>({id,...v}));

    totalMessages.textContent=rows.length;
    highRisk.textContent=rows.filter(r=>r.risk_level==='HIGH').length;
    pendingReview.textContent=rows.filter(r=>r.status==='pending_review').length;
    autoSent.textContent=rows.filter(r=>r.status==='auto_sent').length;
    
    const s={positive:0,neutral:0,negative:0};
    rows.forEach(r=>s[r.sentiment]=(s[r.sentiment]||0)+1);
    
    sentimentSummary.innerHTML=Object.entries(s).map(([k,v])=>`<p>${badge(k)} ${v} comments</p>`).join('');
    latestMessages.innerHTML=rows.slice(-5).reverse().map(r=>
        `<div class='card'>
        <b>${r.customer_name||r.line_user_id||'-'}</b>
        <p>${short(r.original_text)}</p>
        ${badge(r.sentiment)} ${badge(r.risk_level)} ${badge(r.status)}
        </div>`).join('')
    }
);
