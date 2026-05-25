import{db,ref,onValue,badge,short,escapeHtml}from'./firebase-service.js';

let rows=[];

function formatDateTime(value){
    if(!value) return '-';

    const date=new Date(value);
    if(isNaN(date.getTime())) return '-';

    return date.toLocaleString('en-GE', {
        timeZone: 'Asia/Bangkok',
        year:'numeric',
        month:'2-digit',
        day:'2-digit',
        hour:'2-digit',
        minute:'2-digit'
    });
}

function render(){
    const sf=sentimentFilter.value,
    st=statusFilter.value;

    commentsTable.innerHTML=rows.filter(
        r=>(!sf||r.sentiment===sf)&&(!st||r.status===st)
    ).map(r=>{
        const userName =
            r.line_display_name ||
            r.displayName ||
            r.customer_name ||
            r.line_user_id ||
            '-';

        const created =
            formatDateTime(r.created_at || r.createdAt || r.timestamp);

        return `<tr>
            <td>${escapeHtml(userName)}</td>
            <td>${escapeHtml(short(r.original_text || r.message || r.text,120))}</td>
            <td>${badge(r.sentiment)}</td>
            <td>${escapeHtml(r.intent||'-')}</td>
            <td>${badge(r.risk_level)}</td>
            <td>${badge(r.status)}</td>
            <td>${escapeHtml(created)}</td>
        </tr>`;
    }).join('');
}

onValue(ref(db,'comments'),
snap=>{
    rows=Object.entries(snap.val()||{}).map(([id,v])=>({id,...v})).reverse();
    render();
});

sentimentFilter.addEventListener('change',render);
statusFilter.addEventListener('change',render);