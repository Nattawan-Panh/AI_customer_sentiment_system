import { db, ref, onValue, badge, escapeHtml } from './firebase-service.js';

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
                <td>${escapeHtml(formatThaiDateTime(r.created_at || r.createdAt || r.sent_at))}</td>
                <td>${badge(r.type)}</td>
                <td>${escapeHtml(r.channel || '-')}</td>
                <td>${badge(r.status)}</td>
                <td>${escapeHtml(r.subject || '-')}</td>
            </tr>
        `)
        .join('');
});