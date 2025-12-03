const form = document.getElementById('form');
const chat = document.getElementById('chat');
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = document.getElementById('msg').value;
    if (!msg) return;
    append('You', msg, 'user');
    document.getElementById('msg').value = '';
    const data = new FormData();
    data.append('message', msg);
    const res = await fetch('/api/chat', { method: 'POST', body: data });
    const j = await res.json();
    append('AI', j.reply, 'ai');
});
function append(who, text, cls) {
    const d = document.createElement('div');
    d.className = 'msg ' + cls;
    d.innerText = who + ': ' + text;
    chat.appendChild(d);
    chat.scrollTop = chat.scrollHeight;
}
