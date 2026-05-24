import { db, ref, onValue, badge } from './firebase-service.js';

function formatThaiDateTime(value) {
    if (!value) return '-';

    const date = new Date(value);
    if (isNaN(date.getTime())) return '-';

    return date.toLocaleString('en-GE', {
        timeZone: 'Asia/Bangkok',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}



onValue(ref(db, 'notifications'), snap => {
    notificationsTable.innerHTML = Object.entries(snap.val() || {})
        .map(([id, v]) => ({ id, ...v }))
        .reverse()
        .map(r => `
            <tr>
                <td>${formatThaiDateTime(r.created_at || r.createdAt || r.sent_at)}</td>
                <td>${badge(r.type)}</td>
                <td>${r.channel || '-'}</td>
                <td>${badge(r.status)}</td>
                <td>${r.subject || '-'}</td>
            </tr>
        `)
        .join('');
});