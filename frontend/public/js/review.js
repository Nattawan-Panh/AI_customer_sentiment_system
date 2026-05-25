import{db,ref,onValue,update,push,set,badge,escapeHtml}from'./firebase-service.js';

const API_BASE_URL='https://customer-sentiment-system-production.up.railway.app';
async function saveFeedback(cid,p){
    const f=push(ref(db,'feedback'));
    await set(f,{comment_id:cid,...p,created_at:new Date().toISOString()})
}

const ADMIN_API_KEY = 'pudding_petals_admin_secure_key';

async function sendLineReply(cid, msg) {
    const r = await fetch(`${API_BASE_URL}/admin/send-line-reply`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Admin-Key': ADMIN_API_KEY
        },
        body: JSON.stringify({
            comment_id: cid,
            message: msg
        })
    });

    if (!r.ok) {
        const err = await r.text();
        throw new Error(`Send failed: ${r.status} ${err}`);
    }

    return r.json();
}
    
onValue(ref(db,'comments'),
snap=>{
    const rows=Object.entries(snap.val()||{}).map(([id,v])=>({id,...v})).filter(r=>
        ['pending_review','draft_ready','edited'].includes(r.status)).reverse();
    reviewList.innerHTML=rows.map(r=>
        `<div class='card'>
            <h3>LINE User: ${escapeHtml(r.customer_name||r.line_user_id||'-')} ${badge(r.sentiment)} ${badge(r.risk_level)} ${badge(r.status)}</h3>
            <p><b>Customer:</b> ${escapeHtml(r.original_text||'')}</p>
            <p><b>Intent:</b> ${escapeHtml(r.intent||'-')} | <b>Confidence:</b> ${escapeHtml(r.intent_confidence||'-')}</p>
            <p>${escapeHtml(r.ai_reply||r.template_reply||'')}</p>
            <textarea id='reply-${r.id}'>${escapeHtml(r.final_reply||r.ai_reply||r.template_reply||'')}</textarea>
            <br><br><button class='success' data-action='approve' data-id='${r.id}'>Approve & Send</button> 
            <button class='secondary' data-action='edit' data-id='${r.id}'>Save Edit</button> 
            <button class='danger' data-action='reject' data-id='${r.id}'>Reject</button>
        </div>`
    ).join('');
    document.querySelectorAll('button[data-action]').forEach(btn=>btn.addEventListener('click',
        async()=>
            {
                const id=btn.dataset.id,
                action=btn.dataset.action,
                finalReply=document.getElementById(`reply-${id}`).value;
                    
                if(action==='approve')
                    {
                        try {
                            await sendLineReply(id, finalReply);
                            alert('Approved and sent');
                        } catch(e) {
                            console.error(e);
                            alert('ส่ง LINE ไม่สำเร็จ กรุณาตรวจสอบระบบ');
                        }
                    }

                if(action==='edit')
                    {
                        await update(ref(db,`comments/${id}`),{
                                status:'edited',
                            final_reply:finalReply,
                            reviewed_at:new Date().toISOString()
                        });
                                        
                        await saveFeedback(id,{
                            admin_action:'edited',
                            edited_reply:finalReply
                        });
                        alert('Edit saved')
                    }
                if(action==='reject')
                    {
                        await update(ref(db,`comments/${id}`),
                        {
                            status:'rejected',final_reply:finalReply,reviewed_at:new Date().toISOString()
                        });
                    
                        await saveFeedback(id,{
                            admin_action:'rejected',
                            edited_reply:finalReply
                        });
                        alert('Rejected')
                    }
                }
            )
        )
    }
);
