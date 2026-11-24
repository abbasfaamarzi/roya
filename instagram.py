"""Instagram-style interactive demo for the Roya component library.

Run from the Roya project root with: python instagram.py
Then open http://127.0.0.1:8090. This is a local demo with sample data,
not a real Instagram integration or a production backend.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import mimetypes, os, threading, webbrowser

ROOT = Path(__file__).resolve().parent
HOST, PORT = "127.0.0.1", int(os.environ.get("ROYA_INSTAGRAM_PORT", "8090"))

HTML = r"""<!doctype html>
<html lang="fa" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Roya Social — Instagram Demo</title>
__ROYA_CSS__
<style>
*{box-sizing:border-box}body{margin:0;background:#fafafa;color:#262626;font-family:Tahoma,Arial,sans-serif}
button,input,textarea{font:inherit}button{cursor:pointer}.topbar{height:64px;background:#fff;border-bottom:1px solid #ddd;position:sticky;top:0;z-index:5}
.top-inner{max-width:1050px;height:100%;margin:auto;display:flex;align-items:center;justify-content:space-between;padding:0 18px;gap:20px}
.brand{font: bold 27px Georgia,serif}.search{background:#efefef;border:0;border-radius:9px;padding:11px 16px;width:250px}
.top-icons{display:flex;gap:16px;align-items:center}.icon-btn{border:0;background:transparent;font-size:25px;padding:3px 6px}
.layout{max-width:950px;margin:28px auto;display:grid;grid-template-columns:minmax(0,600px) 290px;gap:32px;padding:0 16px}
.stories{display:flex;gap:17px;overflow:auto;background:white;border:1px solid #ddd;border-radius:8px;padding:16px;margin-bottom:22px}
.story{flex:0 0 64px;text-align:center;font-size:11px;white-space:nowrap}.ring{width:62px;height:62px;border-radius:50%;padding:3px;margin:auto auto 6px;background:linear-gradient(45deg,#feda75,#d62976,#962fbf,#4f5bd5)}
.ring img{width:100%;height:100%;object-fit:cover;border:2px solid white;border-radius:50%}
.post{background:white;border:1px solid #ddd;border-radius:8px;margin-bottom:22px;overflow:hidden}
.post-head{height:62px;display:flex;align-items:center;padding:0 14px;gap:10px}.avatar{width:38px;height:38px;border-radius:50%;object-fit:cover}
.post-user{display:grid;gap:3px;font-size:13px;flex:1}.post-user small{color:#888;font-size:11px}
.post-image{width:100%;display:block;aspect-ratio:1/1;object-fit:cover;background:#eee}
.post-actions{display:flex;align-items:center;padding:10px 12px 2px;gap:12px}.save{margin-right:auto}.active{color:#ed4956}
.post-body{padding:3px 15px 14px;font-size:13px;line-height:1.8}.post-body p{margin:5px 0}.muted{border:0;background:none;color:#888;padding:0;font-size:12px}
.comments{display:none;color:#555}.comments.show{display:block}.comment-form{display:flex;border-top:1px solid #eee;margin-top:10px;padding-top:9px;gap:8px}
.comment-form input{border:0;outline:0;flex:1;min-width:0}.comment-form button,.link-btn{border:0;background:none;color:#3897f0;font-weight:bold}
.sidebar{position:sticky;top:88px;height:max-content;padding-top:8px}.profile-row,.suggestion{display:flex;align-items:center;gap:10px;margin:13px 0}
.profile-row .avatar{width:48px;height:48px}.profile-row div,.suggestion div{display:grid;gap:4px;flex:1;font-size:12px}
.profile-row small,.suggestion small{color:#888}.suggest-title{display:flex;justify-content:space-between;color:#888;font-size:13px;margin:22px 0}
.suggestion .avatar{width:34px;height:34px}.side-foot{font-size:10px;color:#bbb;line-height:2;margin-top:28px}
.bottom-nav{display:none;position:fixed;bottom:0;left:0;right:0;height:55px;background:white;border-top:1px solid #ddd;z-index:6;justify-content:space-around;align-items:center}
.modal{display:none;position:fixed;inset:0;background:#0008;z-index:10;align-items:center;justify-content:center;padding:18px}.modal.open{display:flex}
.modal-card{background:white;border-radius:14px;width:min(440px,100%);padding:20px}.modal-card input,.modal-card textarea{width:100%;padding:12px;border:1px solid #ddd;border-radius:8px;margin:8px 0}
.primary{border:0;border-radius:8px;background:#a13aa8;color:white;padding:10px 18px;font-weight:bold}
.toast{position:fixed;bottom:25px;left:50%;transform:translateX(-50%);background:#262626;color:white;padding:10px 18px;border-radius:22px;opacity:0;z-index:20;transition:.2s}.toast.show{opacity:1}
@media(max-width:760px){.layout{display:block;margin:14px auto;padding:0}.sidebar{display:none}.stories{border-left:0;border-right:0;border-radius:0;margin-bottom:12px}.post{border-left:0;border-right:0;border-radius:0}.search{display:none}.bottom-nav{display:flex}.layout{margin-bottom:65px}}
</style></head><body>
<header class="topbar"><div class="top-inner"><div class="brand">Roya Social</div>
<input class="search" id="search" placeholder="جست‌وجو" oninput="searchPosts(this.value)">
<nav class="top-icons"><button class="icon-btn">⌂</button><button class="icon-btn" onclick="toast('پیام‌ها در نسخه نمایشی هستند')">➤</button>
<button class="icon-btn" onclick="openModal()">⊞</button><button class="icon-btn">♡</button><img class="avatar" src="https://i.pravatar.cc/120?img=5"></nav></div></header>
<main class="layout"><section class="feed">
<div class="stories">
<div class="story"><div class="ring"><img src="https://i.pravatar.cc/120?img=5"></div>استوری شما</div>
<div class="story"><div class="ring"><img src="https://i.pravatar.cc/120?img=47"></div>sara.design</div>
<div class="story"><div class="ring"><img src="https://i.pravatar.cc/120?img=12"></div>ali.travels</div>
<div class="story"><div class="ring"><img src="https://i.pravatar.cc/120?img=44"></div>mina.food</div>
<div class="story"><div class="ring"><img src="https://i.pravatar.cc/120?img=32"></div>niloofar</div>
<div class="story"><div class="ring"><img src="https://i.pravatar.cc/120?img=18"></div>amir</div>
</div>
<article class="post"><header class="post-head"><img class="avatar" src="https://i.pravatar.cc/120?img=47"><div class="post-user"><b>sara.design</b><small>تهران، ایران</small></div><button class="icon-btn">•••</button></header>
<img class="post-image" src="https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=1100" ondblclick="likePost(this.closest('.post'))">
<div class="post-actions"><button class="icon-btn like" onclick="likePost(this.closest('.post'))">♡</button><button class="icon-btn" onclick="focusComment(this.closest('.post'))">♧</button><button class="icon-btn">➤</button><button class="icon-btn save" onclick="this.classList.toggle('active')">♧</button></div>
<div class="post-body"><b class="like-count" data-count="1284">1,284 پسند</b><p><b>sara.design</b> گاهی زیبایی توی ساده‌ترین جزئیاته 🌿</p>
<button class="muted" onclick="toggleComments(this)">مشاهده دیدگاه‌ها</button><div class="comments"><p><b>sara.design</b> چقدر لطیف و زیبا ✨</p><p><b>roya.user</b> ترکیب رنگ‌ها عالیه</p></div>
<form class="comment-form" onsubmit="addComment(event,this)"><input placeholder="افزودن دیدگاه..." required><button>ارسال</button></form></div></article>
<article class="post"><header class="post-head"><img class="avatar" src="https://i.pravatar.cc/120?img=12"><div class="post-user"><b>ali.travels</b><small>شمال ایران</small></div><button class="icon-btn">•••</button></header>
<img class="post-image" src="https://images.unsplash.com/photo-1470770841072-f978cf4d019e?w=1100" ondblclick="likePost(this.closest('.post'))">
<div class="post-actions"><button class="icon-btn like" onclick="likePost(this.closest('.post'))">♡</button><button class="icon-btn" onclick="focusComment(this.closest('.post'))">♧</button><button class="icon-btn">➤</button><button class="icon-btn save" onclick="this.classList.toggle('active')">♧</button></div>
<div class="post-body"><b class="like-count" data-count="856">856 پسند</b><p><b>ali.travels</b> یک صبح آرام کنار طبیعت؛ همین کافیست 🌄</p>
<button class="muted" onclick="toggleComments(this)">مشاهده دیدگاه‌ها</button><div class="comments"><p><b>mina.food</b> چه منظره‌ای!</p></div>
<form class="comment-form" onsubmit="addComment(event,this)"><input placeholder="افزودن دیدگاه..." required><button>ارسال</button></form></div></article>
<article class="post"><header class="post-head"><img class="avatar" src="https://i.pravatar.cc/120?img=44"><div class="post-user"><b>mina.food</b><small>کافه‌گردی</small></div><button class="icon-btn">•••</button></header>
<img class="post-image" src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=1100" ondblclick="likePost(this.closest('.post'))">
<div class="post-actions"><button class="icon-btn like" onclick="likePost(this.closest('.post'))">♡</button><button class="icon-btn" onclick="focusComment(this.closest('.post'))">♧</button><button class="icon-btn">➤</button><button class="icon-btn save" onclick="this.classList.toggle('active')">♧</button></div>
<div class="post-body"><b class="like-count" data-count="2301">2,301 پسند</b><p><b>mina.food</b> قهوه، کتاب و چند دقیقه آرامش ☕</p>
<button class="muted" onclick="toggleComments(this)">مشاهده دیدگاه‌ها</button><div class="comments"><p><b>roya.user</b> بهترین ترکیب دنیا</p></div>
<form class="comment-form" onsubmit="addComment(event,this)"><input placeholder="افزودن دیدگاه..." required><button>ارسال</button></form></div></article>
</section><aside class="sidebar"><div class="profile-row"><img class="avatar" src="https://i.pravatar.cc/120?img=5"><div><b>roya.user</b><small>کاربر رویا</small></div><button class="link-btn">تغییر</button></div>
<div class="suggest-title"><b>پیشنهاد برای شما</b><span>مشاهده همه</span></div>
<div class="suggestion"><img class="avatar" src="https://i.pravatar.cc/120?img=32"><div><b>niloofar.art</b><small>پیشنهاد برای شما</small></div><button class="link-btn" onclick="follow(this)">دنبال کردن</button></div>
<div class="suggestion"><img class="avatar" src="https://i.pravatar.cc/120?img=18"><div><b>amir.photo</b><small>پیشنهاد برای شما</small></div><button class="link-btn" onclick="follow(this)">دنبال کردن</button></div>
<div class="suggestion"><img class="avatar" src="https://i.pravatar.cc/120?img=23"><div><b>parisa.life</b><small>پیشنهاد برای شما</small></div><button class="link-btn" onclick="follow(this)">دنبال کردن</button></div>
<div class="side-foot">درباره ما · راهنما · حریم خصوصی · شرایط<br>© ۲۰۲۶ ROYA SOCIAL — DEMO</div></aside></main>
<nav class="bottom-nav"><button class="icon-btn">⌂</button><button class="icon-btn">⌕</button><button class="icon-btn" onclick="openModal()">⊞</button><button class="icon-btn">♡</button><button class="icon-btn">◉</button></nav>
<div class="modal" id="modal" onclick="if(event.target===this)closeModal()"><form class="modal-card" onsubmit="publish(event)"><h3>ایجاد پست جدید</h3>
<input id="imageUrl" type="url" placeholder="آدرس تصویر (URL)" required><textarea id="caption" rows="3" placeholder="کپشن خود را بنویسید..."></textarea>
<button class="primary">انتشار</button> <button type="button" onclick="closeModal()">انصراف</button></form></div><div class="toast" id="toast"></div>
<script>
function likePost(p){let b=p.querySelector('.like'),c=p.querySelector('.like-count'),n=Number(c.dataset.count),yes=b.classList.toggle('active');n+=yes?1:-1;c.dataset.count=n;c.textContent=n.toLocaleString('en-US')+' پسند';b.textContent=yes?'♥':'♡'}
function focusComment(p){p.querySelector('.comment-form input').focus();p.querySelector('.comments').classList.add('show')}
function toggleComments(b){b.nextElementSibling.classList.toggle('show')}
function addComment(e,f){e.preventDefault();let p=document.createElement('p'),b=document.createElement('b'),i=f.querySelector('input');b.textContent='roya.user';p.append(b,document.createTextNode(' '+i.value));f.previousElementSibling.append(p);f.previousElementSibling.classList.add('show');i.value=''}
function follow(b){b.textContent=b.textContent==='دنبال کردن'?'دنبال‌شده':'دنبال کردن'}
function searchPosts(q){document.querySelectorAll('.post').forEach(p=>p.hidden=!!q&&!p.textContent.toLowerCase().includes(q.toLowerCase()))}
function openModal(){document.getElementById('modal').classList.add('open')}function closeModal(){document.getElementById('modal').classList.remove('open')}
function publish(e){e.preventDefault();let p=document.createElement('article'),url=document.getElementById('imageUrl').value,cap=document.getElementById('caption').value;p.className='post';p.innerHTML='<header class="post-head"><img class="avatar" src="https://i.pravatar.cc/120?img=5"><div class="post-user"><b>roya.user</b><small>همین الان</small></div></header><img class="post-image"><div class="post-actions"><button class="icon-btn like">♡</button></div><div class="post-body"><b class="like-count" data-count="0">0 پسند</b><p><b>roya.user</b> </p></div>';p.querySelector('.post-image').src=url;p.querySelector('.post-body p').append(document.createTextNode(cap));p.querySelector('.like').onclick=()=>likePost(p);document.querySelector('.feed').insertBefore(p,document.querySelector('.stories').nextSibling);closeModal();toast('پست نمایشی منتشر شد')}
let timer;function toast(s){let t=document.getElementById('toast');t.textContent=s;t.classList.add('show');clearTimeout(timer);timer=setTimeout(()=>t.classList.remove('show'),2000)}
</script></body></html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            data = HTML.replace("__ROYA_CSS__", '<link rel="stylesheet" href="/static/roya/css/roya.css">' if (ROOT / "static/roya/css/roya.css").is_file() else "").encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        target = (ROOT / path.lstrip("/")).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            self.send_error(403)
            return
        if target.is_file() and "static" in target.parts:
            data = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
            self.end_headers()
            self.wfile.write(data)
            return
        self.send_error(404)

    def log_message(self, fmt, *args):
        print("[Roya Social] " + (fmt % args))

def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}"
    print(f"Roya Social demo: {url}\nبرای توقف سرور Ctrl+C را بزنید.")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
