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

function actionButton(notificationId, data) {
    const status = String(data.status || '').toLowerCase();
    const commentId = data.comment_id || data.commentId || '';

    if (status === 'failed') {
        return `
            <button class="btn small danger" onclick="retryEmail('${notificationId}')">
                ส่งอีกครั้ง
            </button>
        `;
    }

    return `
        <button class="btn small" onclick="viewNotificationDetail('${commentId}')">
            ดูรายละเอียด
        </button>
    `;
}

window.viewNotificationDetail = function(commentId) {
    if (!commentId || commentId === '-') {
        alert('ไม่พบข้อมูลข้อความที่เกี่ยวข้อง');
        return;
    }

    window.location.href = `notification-detail.html?commentId=${commentId}`;
};

window.retryEmail = async function(notificationId) {
  try {
    const response = await fetch(`${API_BASE_URL}/admin/notifications/${notificationId}/retry`, {
      method: "POST"
    });

    if (!response.ok) {
      throw new Error("Retry failed");
    }

    alert("ส่งอีเมลอีกครั้งสำเร็จ");
    location.reload();

  } catch (error) {
    console.error(error);
    alert("ส่งอีเมลซ้ำไม่สำเร็จ");
  }
};

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
                <td>${actionButton(r.id, r)}</td>
            </tr>
        `)
        .join('');
});