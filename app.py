
from flask import Flask, render_template_string, request, redirect, session
import requests, json, os
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "icab-secret-2026-change-this")

FIREBASE_CONFIG = {
    "apiKey": "AIzaSyB8ecXem-I3tYEUV-p1krPz7o-TbKxiABhIAE",
    "authDomain": "islami-chatro-andolon-92237.firebaseapp.com",
    "projectId": "islami-chatro-andolon-92237",
    "storageBucket": "islami-chatro-andolon-92237.firebasestorage.app",
    "messagingSenderId": "130569159989",
    "appId": "1:130569159989:web:6d3e9649436b908e766ac1c"
}
PROJECT_ID = FIREBASE_CONFIG["projectId"]
API_KEY = FIREBASE_CONFIG["apiKey"]
FIRESTORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/icab_site/main?key={API_KEY}"

DEFAULT_DATA = {
    "site": {"name": "ইসলামী ছাত্র আন্দোলন বাংলাদেশ","name_en": "Islami Chhatra Andolan Bangladesh","domain": "chhatraandolan.org","slogan": "সত্যের প্রতিষ্ঠা ও অন্যায়ের প্রতিরোধ","tagline": "মুক্তির মূলমন্ত্র ইসলামী শাসনতন্ত্র","address": "৫৫/বি (৩য় তলা), পুরানা পল্টন, ঢাকা-১০০০","phone": "02-9557131","email": "info@chhatraandolan.org","whatsapp": "","facebook": "https://facebook.com/icabd91","youtube": "https://youtube.com/@icabd91","instagram": "https://instagram.com/icabd91","about_text": "সত্যের প্রতিষ্ঠা ও অন্যায়ের প্রতিরোধ এর মধ্যেই মুসলমানদের শ্রেষ্ঠত্ব নিহিত। ইসলামী ছাত্র আন্দোলন বাংলাদেশ একটি আদর্শিক","aim": "জাহিলিয়াতের সকল প্রকার আধিপত্যের অবসান ঘটিয়ে কুরআন-সুন্নাহ অনুযায়ী মানবজীবন গঠন ও সমাজের সর্বস্তরে পূর্ণ দ্বীন বাস্তবায়ন।","purpose": "আল্লাহ তায়ালার সন্তুষ্টি অর্জন","footer_text": "© ২০২৬ ইসলামী ছাত্র আন্দোলন বাংলাদেশ","bkash": "", "nagad": "", "rocket": "", "bank": "","admin_pass": "admin123"},
    "slider": [{"title": "কেন্দ্রীয় সম্মেলন ২০২৭ - ১১ ডিসেম্বর ২০২৬, শুক্রবার, ইনশাআল্লাহ", "subtitle": "Kendriyo Sommelon 2027", "image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=900&q=80"}],
    "programs": [{"title": "জ্ঞান অর্জন ও প্রশিক্ষণ", "desc": "ইসলামী জ্ঞান অর্জনের মাধ্যমে নিজেকে গড়ে তোলা।"},{"title": "আমল ও আত্মশুদ্ধি", "desc": "আমল ও আত্মশুদ্ধির মাধ্যমে চরিত্র গঠন।"},{"title": "দাওয়াত", "desc": "আল্লাহর দিকে আহ্বান।"},{"title": "সংগঠন", "desc": "ছাত্রদের সংগঠিত করা।"},{"title": "বিপ্লব", "desc": "শান্তিপূর্ণ গণআন্দোলনের মাধ্যমে ইসলামী বিপ্লব।"}],
    "leaders": [{"name": "মুনতাছির আহমাদ", "post": "সভাপতি", "image": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80"},{"name": "সুলতান মাহমুদ", "post": "সেক্রেটারি জেনারেল", "image": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80"},{"name": "ইমতিয়াজ আহমেদ", "post": "সাংগঠনিক সম্পাদক", "image": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&q=80"}],
    "news": [{"title": "সারাদেশে বন্যার্তদের মাঝে ত্রাণ বিতরণ কার্যক্রম অব্যাহত", "date": "২৪ নভেম্বর ২০২৬", "cat": "ফিচার", "image": "https://images.unsplash.com/photo-1594708767771-a7502209ff51?w=800&q=80", "desc": "ইসলামী ছাত্র আন্দোলন বাংলাদেশ এর উদ্যোগে দেশের বিভিন্ন বন্যাকবলিত এলাকায় শুকনো খাবার ও ত্রাণ সামগ্রী বিতরণ করা হয়েছে..."},{"title": "কেন্দ্রীয় সম্মেলন ২০২৪ সফলভাবে সম্পন্ন", "date": "২২ নভেম্বর ২০২৬", "cat": "কার্যক্রম", "image": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&q=80", "desc": "রাজধানীর একটি মিলনায়তনে দুই দিনব্যাপী কেন্দ্রীয় সম্মেলন অনুষ্ঠিত হয়েছে..."},{"title": "নতুন সদস্য ভর্তি কার্যক্রম শুরু হয়েছে", "date": "২০ নভেম্বর ২০২৬", "cat": "ভর্তি", "image": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&q=80", "desc": "সংগঠনের নতুন সদস্য ভর্তি কার্যক্রম চলছে।"}],
    "videos": [{"title": "সন্ত্রাসবিরোধী পদযাত্রা", "url": "https://www.youtube.com/embed/dQw4w9WgXcQ"}],
    "library": [{"title": "ইসলামী ছাত্র আন্দোলনের পরিচিতি", "author": "প্রকাশনা বিভাগ", "level": "সদস্য", "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&q=80", "file": "#", "desc": "নতুন সদস্যদের জন্য।"}],
    "members": [], "events": [{"title": "কেন্দ্রীয় সম্মেলন ২০২৭", "date": "১১ ডিসেম্বর ২০২৬", "place": "সোহরাওয়ার্দী উদ্যান, ঢাকা", "image": "https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=800&q=80", "desc": "সারা দেশের ছাত্ররা জমায়েত হবে।"}],
    "gallery": [{"title": "পদযাত্রা", "image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600&q=80"},{"title": "সম্মেলন", "image": "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=600&q=80"}],
    "press": [{"title": "সন্ত্রাসবিরোধী অবস্থান", "date": "২০ নভেম্বর ২০২৬", "desc": "কেন্দ্রীয় সভাপতির প্রেস বিজ্ঞপ্তি।"}], "contacts": []
}
def from_firestore_value(v):
    if "stringValue" in v: return v["stringValue"]
    if "arrayValue" in v: return [from_firestore_value(x) for x in v["arrayValue"].get("values", [])]
    if "mapValue" in v: return {k: from_firestore_value(val) for k, val in v["mapValue"].get("fields", {}).items()}
    return ""
def to_firestore_value(v):
    if isinstance(v, str): return {"stringValue": v}
    if isinstance(v, list): return {"arrayValue": {"values": [to_firestore_value(x) for x in v]}}
    if isinstance(v, dict): return {"mapValue": {"fields": {k: to_firestore_value(val) for k, val in v.items()}}}
    return {"stringValue": str(v)}
def load_from_firebase():
    try:
        r = requests.get(FIRESTORE_URL, timeout=5)
        if r.status_code == 200:
            fields = r.json().get("fields", {}); data = {k: from_firestore_value(val) for k, val in fields.items()}
            for k, v in DEFAULT_DATA.items():
                if k not in data: data[k] = v
            return data
    except: pass
    return json.loads(json.dumps(DEFAULT_DATA))
CACHE = {"data": load_from_firebase()}
def get_data(): return CACHE["data"]
def save_data(data):
    CACHE["data"] = data
    try: requests.patch(FIRESTORE_URL, json={"fields": {k: to_firestore_value(val) for k, val in data.items()}}, timeout=8)
    except: pass
    return True
@app.route("/")
def home(): return render_template_string(HOME_TEMPLATE, d=get_data())
@app.route("/join", methods=["GET","POST"])
def join():
    d=get_data()
    if request.method=="POST":
        d.setdefault("members",[]).append({"name":request.form.get("name"),"phone":request.form.get("phone"),"district":request.form.get("district"),"institution":request.form.get("institution"),"class":request.form.get("class")}); save_data(d); return render_template_string(JOIN_SUCCESS_TEMPLATE,d=d)
    return render_template_string(JOIN_TEMPLATE,d=d)
@app.route("/contact", methods=["GET","POST"])
def contact():
    d=get_data()
    if request.method=="POST":
        d.setdefault("contacts",[]).append({"name":request.form.get("name"),"phone":request.form.get("phone"),"subject":request.form.get("subject"),"message":request.form.get("message")}); save_data(d); return render_template_string(CONTACT_SUCCESS_TEMPLATE,d=d)
    return render_template_string(CONTACT_TEMPLATE,d=d)
@app.route("/donate")
def donate(): return render_template_string(DONATE_TEMPLATE,d=get_data())
@app.route("/admin", methods=["GET","POST"])
def admin():
    d=get_data(); P=d["site"].get("admin_pass","admin123")
    if request.method=="POST":
        if request.form.get("username")=="admin" and request.form.get("password")==P: session["admin"]=True; return redirect("/admin/dashboard")
        return "ভুল পাসওয়ার্ড! <a href='/admin'>আবার চেষ্টা করুন</a>"
    if session.get("admin"): return redirect("/admin/dashboard")
    return render_template_string(LOGIN_TEMPLATE)
@app.route("/admin/dashboard")
def dashboard():
    if not session.get("admin"): return redirect("/admin")
    return render_template_string(ADMIN_TEMPLATE,d=get_data())
@app.route("/admin/save", methods=["POST"])
def admin_save():
    if not session.get("admin"): return redirect("/admin")
    d=get_data()
    for k,f in [("name","site_name"),("slogan","slogan"),("tagline","tagline"),("address","address"),("phone","phone"),("whatsapp","whatsapp"),("about_text","about_text"),("aim","aim"),("purpose","purpose"),("facebook","facebook"),("youtube","youtube"),("footer_text","footer_text"),("bkash","bkash"),("nagad","nagad"),("rocket","rocket"),("bank","bank")]: d["site"][k]=request.form.get(f,d["site"].get(k,""))
    save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/change-password", methods=["POST"])
def change_password():
    if not session.get("admin"): return redirect("/admin")
    d=get_data()
    if request.form.get("old_pass")==d["site"].get("admin_pass","admin123") and len(request.form.get("new_pass",""))>=6: d["site"]["admin_pass"]=request.form.get("new_pass"); save_data(d); return "বদলে গেছে! <a href='/admin/dashboard'>ফিরুন</a>"
    return "ভুল! <a href='/admin/dashboard'>ফিরুন</a>"
@app.route("/admin/add-news", methods=["POST"])
def add_news():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d["news"].append({"title":request.form.get("title"),"date":request.form.get("date"),"image":request.form.get("image"),"desc":request.form.get("desc"),"cat":request.form.get("cat","সংবাদ")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/add-leader", methods=["POST"])
def add_leader():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d["leaders"].append({"name":request.form.get("name"),"post":request.form.get("post"),"image":request.form.get("image")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/add-slider", methods=["POST"])
def add_slider():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d["slider"].append({"title":request.form.get("title"),"subtitle":request.form.get("subtitle"),"image":request.form.get("image")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/add-video", methods=["POST"])
def add_video():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d["videos"].append({"title":request.form.get("title"),"url":request.form.get("url")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/add-book", methods=["POST"])
def add_book():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d.setdefault("library",[]).append({"title":request.form.get("title"),"author":request.form.get("author"),"level":request.form.get("level"),"image":request.form.get("image"),"file":request.form.get("file"),"desc":request.form.get("desc")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/add-event", methods=["POST"])
def add_event():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d.setdefault("events",[]).append({"title":request.form.get("title"),"date":request.form.get("date"),"place":request.form.get("place"),"image":request.form.get("image"),"desc":request.form.get("desc")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/add-gallery", methods=["POST"])
def add_gallery():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d.setdefault("gallery",[]).append({"title":request.form.get("title"),"image":request.form.get("image")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/add-press", methods=["POST"])
def add_press():
    if not session.get("admin"): return redirect("/admin")
    d=get_data(); d.setdefault("press",[]).append({"title":request.form.get("title"),"date":request.form.get("date"),"desc":request.form.get("desc")}); save_data(d); return redirect("/admin/dashboard")
@app.route("/admin/delete/<ctype>/<int:index>")
def delete_item(ctype,index):
    if not session.get("admin"): return redirect("/admin")
    d=get_data()
    if ctype in d and 0<=index<len(d[ctype]): d[ctype].pop(index); save_data(d)
    return redirect("/admin/dashboard")
@app.route("/admin/logout")
def logout(): session.clear(); return redirect("/admin")

HOME_TEMPLATE = """
<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{d.site.name}} | {{d.site.tagline}}</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Hind Siliguri,sans-serif}
body{background:#F8F9FA;color:#222}
header{background:#fff;padding:8px 10px;display:flex;align-items:center;gap:8px;position:sticky;top:0;z-index:100;border-bottom:1px solid #eee;flex-wrap:nowrap}
.logo{width:40px;height:40px;flex-shrink:0;display:block}
.logo svg{width:100%;height:100%;display:block}
.brand{flex:1;font-size:17px;font-weight:700;color:#111;line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.search-btn{width:34px;height:34px;flex-shrink:0;background:#F1F5F1;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;text-decoration:none}
.btn-donate{background:#FDB913;color:#000;padding:8px 12px;border-radius:10px;text-decoration:none;font-weight:700;font-size:14px;white-space:nowrap;flex-shrink:0}
.menu-btn{font-size:25px;cursor:pointer;flex-shrink:0}
#mcheck{display:none}
.mmenu{display:none;background:#fff;border-bottom:1px solid #eee;padding:8px 14px}
.mmenu a{display:block;padding:13px 6px;text-decoration:none;color:#111;font-weight:600;font-size:16px;border-bottom:1px solid #F1F1F1}
#mcheck:checked ~ .mmenu{display:block}
.hero{max-width:520px;margin:auto;padding:16px 20px 0;text-align:center;background:#fff}
.hero p{font-size:19px;line-height:1.6;color:#4A4A4A}
.hero p b{color:#333}
.btn-yellow{background:#FDB913;color:#fff;padding:14px 28px;border-radius:12px;text-decoration:none;font-weight:700;font-size:18px;display:inline-block;margin:20px 0 12px;box-shadow:0 4px 12px rgba(253,185,19,0.4)}
.link-green{display:block;color:#0F4A2E;text-decoration:none;font-weight:700;font-size:17px;margin-bottom:8px}
.kaaba-box{max-width:520px;margin:auto;background:#fff;text-align:center;padding:20px 0 12px}
.kaaba-circle{width:210px;height:210px;margin:auto;background:#0F4A2E;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 25px rgba(15,74,46,0.25);border:4px solid #FDB913}
.kaaba-circle svg{width:150px}
.cards{max-width:520px;margin:auto;padding:14px 14px 20px;background:#F8F9FA}
.card{background:#fff;border-radius:18px;padding:10px 10px 16px;box-shadow:0 4px 16px rgba(0,0,0,0.06);margin-bottom:16px;overflow:hidden}
.card-top{background:#0B5A34;border-radius:14px;height:170px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:44px;overflow:hidden;position:relative}
.card-top img{width:100%;height:100%;object-fit:cover}
.card-top span{white-space:nowrap}
.card h3{font-size:22px;color:#0F4A2E;text-align:center;line-height:1.4;margin:14px 8px 6px}
.card p{color:#555;text-align:center;line-height:1.6;padding:0 8px}
.btn2{background:#0F4A2E;color:#fff;padding:10px 18px;border-radius:10px;text-decoration:none;display:inline-block;font-weight:700;margin-top:10px}
.section{max-width:520px;margin:auto;padding:14px;background:#F8F9FA}
.section h2{font-size:22px;color:#0F4A2E;margin-bottom:12px;text-align:center}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.mini{background:#fff;border-radius:14px;padding:12px;text-align:center}
.mini img{width:100%;height:120px;object-fit:cover;border-radius:10px}
.mini h3{font-size:15px;margin-top:8px;color:#111;line-height:1.4}
footer{background:#0A2E18;color:#fff;padding:28px 16px;text-align:center}
footer a{color:#A7F3C0;text-decoration:none}
@media(min-width:768px){.hero,.kaaba-box,.cards,.section{max-width:820px}.grid{grid-template-columns:repeat(3,1fr)}.card-top{height:220px}.brand{font-size:22px}}
</style></head><body>
<header>
  <a class="logo" href="/"><svg viewBox="0 0 60 60"><path d="M 38 4 A 28 28 0 1 0 38 56 A 22 22 0 1 1 38 4 Z" fill="#0F4A2E"/><polygon points="48,18 49.5,23 54.5,23 50.5,26 52,31 48,28 44,31 45.5,26 41.5,23 46.5,23" fill="#0F4A2E"/></svg></a>
  <div class="brand">ইসলামী ছাত্র আন্দোলন বাংলাদেশ</div>
  <a class="search-btn" href="#news">🔍</a>
  <a class="btn-donate" href="/donate">দান করুন</a>
  <label class="menu-btn" for="mcheck">☰</label>
</header>
<input type="checkbox" id="mcheck"><div class="mmenu"><a href="/">হোম</a><a href="#about">আমাদের সম্পর্কে</a><a href="#program">কার্যক্রম</a><a href="#library">প্রকাশনা</a><a href="#news">সংবাদ</a><a href="#gallery">গ্যালারি</a><a href="#gallery2">মিডিয়া</a><a href="/contact">যোগাযোগ</a><a href="/join" style="color:#0F4A2E">যোগ দিন →</a></div>
<div class="hero"><p><b>সত্যের প্রতিষ্ঠা ও অন্যায়ের প্রতিরোধ</b> - সত্যের প্রতিষ্ঠা ও অন্যায়ের প্রতিরোধ এর মধ্যেই মুসলমানদের শ্রেষ্ঠত্ব নিহিত। {{d.site.name}} একটি আদর্শিক</p><a class="btn-yellow" href="#program">আমাদের প্রকল্প দেখুন</a><a class="link-green" href="#about">→ কীভাবে আমরা সাহায্য করি জানুন</a></div>
<div class="kaaba-box">
  <div class="kaaba-circle">
    <svg viewBox="0 0 200 170">
      <defs><linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE27A"/><stop offset="1" stop-color="#D4AF37"/></linearGradient></defs>
      <polygon points="25,58 100,28 175,58 175,148 25,148" fill="#0A0A0A"/>
      <polygon points="100,28 175,58 175,148 100,148" fill="#222"/>
      <polygon points="25,76 100,50 175,76 175,92 100,66 25,92" fill="url(#gold)"/>
      <polygon points="100,50 175,76 175,92 100,66" fill="#FDB913"/>
      <circle cx="55" cy="84" r="3" fill="#111"/><circle cx="75" cy="79" r="3" fill="#111"/><circle cx="125" cy="79" r="3" fill="#111"/><circle cx="150" cy="84" r="3" fill="#111"/>
      <rect x="115" y="102" width="30" height="42" rx="3" fill="url(#gold)" stroke="#8A6D00" stroke-width="1"/>
      <rect x="119" y="106" width="22" height="34" rx="2" fill="#FFD700"/>
      <circle cx="130" cy="124" r="3" fill="#111"/>
      <rect x="124" y="110" width="12" height="6" rx="2" fill="#8A6D00"/>
      <ellipse cx="100" cy="150" rx="78" ry="6" fill="#000" opacity="0.25"/>
    </svg>
  </div>
  <p style="font-size:14px;color:#0F4A2E;font-weight:700;margin-top:12px"> ইসলামী ছাত্র আন্দোলন বাংলাদেশ</p>
</div>
<div class="cards">
{% for s in d.slider %}<div class="card"><div class="card-top"><span>{{s.subtitle}}</span></div><h3>{{s.title}}</h3><p>{{d.site.slogan}} - সত্যের কাফেলায় আপনিও শরিক হোন।</p><div style="text-align:center"><a class="btn2" href="/join">যোগ দিন →</a></div></div>{% endfor %}
{% for n in d.news %}<div class="card"><div class="card-top"><img src="{{n.image}}"></div><h3>{{n.title}}</h3><p>{{n.date}} | {{n.get('cat','সংবাদ')}}<br>{{n.desc}}</p></div>{% endfor %}
</div>
<div class="section" id="about"><h2>আমাদের সম্পর্কে</h2><div class="card" style="text-align:center"><p>{{d.site.about_text}}</p><br><p><b>লক্ষ্য:</b> {{d.site.aim}}</p><p><b>উদ্দেশ্য:</b> {{d.site.purpose}}</p></div></div>
<div class="section" id="program"><h2>আমাদের প্রকল্প / কার্যক্রম</h2><div class="grid">{% for p in d.programs %}<div class="mini"><h3 style="font-size:20px">📖</h3><h3>{{p.title}}</h3><p style="color:#666;font-size:13px;line-height:1.5">{{p.desc}}</p></div>{% endfor %}</div></div>
<div class="section" id="leaders"><h2>নেতৃত্ব</h2><div class="grid">{% for l in d.leaders %}<div class="mini"><img src="{{l.image}}"><h3>{{l.name}}</h3><p style="color:#666;font-size:13px">{{l.post}}</p></div>{% endfor %}</div></div>
<div class="section" id="library"><h2>প্রকাশনা / লাইব্রেরী</h2><div class="grid">{% for b in d.library %}<div class="mini"><img src="{{b.image}}"><h3>{{b.title}}</h3><p style="color:#666;font-size:13px">{{b.author}}</p><br><a class="btn2" href="{{b.file}}">বই পড়ুন</a></div>{% endfor %}</div></div>
<div class="section" id="gallery"><h2>গ্যালারি</h2><div class="grid">{% for g in d.gallery %}<div class="mini"><img src="{{g.image}}"><h3>{{g.title}}</h3></div>{% endfor %}</div></div>
<div class="section" id="gallery2"><h2>মিডিয়া - ভিডিও</h2>{% for v in d.videos %}<div class="card"><h3>{{v.title}}</h3><iframe width="100%" height="220" src="{{v.url}}" frameborder="0" allowfullscreen style="border-radius:12px;margin-top:10px"></iframe></div>{% endfor %}</div>
<div class="section" id="press"><h2>প্রেস বিজ্ঞপ্তি</h2>{% for p in d.press %}<div class="card"><h3>{{p.title}}</h3><p>{{p.date}}<br>{{p.desc}}</p></div>{% endfor %}</div>
<div class="section" style="text-align:center"><h2>ছাত্র আন্দোলনে যোগ দিন</h2><a class="btn-yellow" href="/join">সদস্য হোন</a><br><a class="link-green" href="/donate">→ সহযোগিতা করুন</a></div>
<footer><p><b>{{d.site.name}}</b></p><p>{{d.site.address}} | {{d.site.phone}}</p><br><p>{{d.site.footer_text}} | <a href="/admin">Admin</a></p></footer>
</body></html>
"""
JOIN_TEMPLATE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;background:#F8F9FA;padding:20px} .box{background:#fff;padding:24px;border-radius:16px;max-width:480px;margin:auto} input{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:10px} button{background:#FDB913;color:#fff;padding:14px;width:100%;border:none;border-radius:12px;font-weight:bold;font-size:17px}</style></head><body><div class="box"><h2 style="text-align:center;color:#0F4A2E">সদস্য হোন</h2><form method="POST">নাম <input name="name" required>মোবাইল <input name="phone" required>জেলা <input name="district" required>প্রতিষ্ঠান <input name="institution" required>শ্রেণী <input name="class"><button>আবেদন পাঠান</button></form><p style="text-align:center;margin-top:10px"><a href="/">← হোমে ফিরুন</a></p></div></body></html>"""
JOIN_SUCCESS_TEMPLATE = """<html><head><meta charset="UTF-8"><style>body{background:#0F4A2E;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif} .box{background:#fff;padding:30px;border-radius:16px;text-align:center}</style></head><body><div class="box"><h1>আলহামদুলিল্লাহ!</h1><p>আপনার আবেদন গ্রহণ করা হয়েছে।</p><br><a href="/">হোমে ফিরুন</a></div></body></html>"""
CONTACT_TEMPLATE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;background:#F8F9FA;padding:20px} .box{background:#fff;padding:24px;border-radius:16px;max-width:480px;margin:auto} input,textarea{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:10px} button{background:#0F4A2E;color:#fff;padding:14px;width:100%;border:none;border-radius:12px}</style></head><body><div class="box"><h2 style="text-align:center;color:#0F4A2E">যোগাযোগ করুন</h2><p style="text-align:center;color:#666">{{d.site.address}}<br>ফোন: {{d.site.phone}}</p><form method="POST">নাম <input name="name" required>মোবাইল <input name="phone" required>বিষয় <input name="subject" required>বার্তা <textarea name="message" rows="4" required></textarea><button>বার্তা পাঠান</button></form><p style="text-align:center;margin-top:10px"><a href="/">← হোমে ফিরুন</a></p></div></body></html>"""
CONTACT_SUCCESS_TEMPLATE = """<html><head><meta charset="UTF-8"><style>body{background:#0F4A2E;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif} .box{background:#fff;padding:30px;border-radius:16px;text-align:center}</style></head><body><div class="box"><h1>আলহামদুলিল্লাহ!</h1><p>আপনার বার্তা পাঠানো হয়েছে।</p><br><a href="/">হোমে ফিরুন</a></div></body></html>"""
DONATE_TEMPLATE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;background:#F8F9FA;padding:20px} .box{background:#fff;padding:24px;border-radius:16px;max-width:480px;margin:auto} .pay{background:#FFF8E1;padding:14px;border-radius:10px;margin:10px 0;border-left:4px solid #FDB913}</style></head><body><div class="box"><h2 style="text-align:center;color:#0F4A2E">সহযোগিতা করুন</h2>{% if d.site.bkash %}<div class="pay"><b>বিকাশ</b><br>{{d.site.bkash}}</div>{% endif %}{% if d.site.nagad %}<div class="pay"><b>নগদ</b><br>{{d.site.nagad}}</div>{% endif %}{% if d.site.rocket %}<div class="pay"><b>রকেট</b><br>{{d.site.rocket}}</div>{% endif %}{% if d.site.bank %}<div class="pay"><b>ব্যাংক</b><br>{{d.site.bank}}</div>{% endif %}{% if not d.site.bkash %}<p style="text-align:center;color:#888">নম্বর শীঘ্রই আপডেট হবে। ফোন: {{d.site.phone}}</p>{% endif %}<p style="text-align:center"><a href="/">← হোমে ফিরুন</a></p></div></body></html>"""
LOGIN_TEMPLATE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#0F4A2E;display:flex;justify-content:center;align-items:center;height:100vh;font-family:sans-serif} .box{background:#fff;padding:30px;border-radius:16px;width:330px;text-align:center} input{width:100%;padding:12px;margin:8px 0} button{background:#FDB913;color:#fff;padding:12px;width:100%;border:none;border-radius:10px}</style></head><body><div class="box"><h2>এডমিন লগইন</h2><p>ইসলামী ছাত্র আন্দোলন বাংলাদেশ</p><form method="POST"><input name="username" placeholder="ইউজারনেম"><input type="password" name="password" placeholder="পাসওয়ার্ড"><button>লগইন</button></form></div></body></html>"""
ADMIN_TEMPLATE = """<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{font-family:sans-serif;background:#F8F9FA;padding:16px} .box{background:#fff;padding:18px;border-radius:14px;margin-bottom:14px} input,textarea,select{width:100%;padding:10px;margin:5px 0} button{background:#0F4A2E;color:#fff;padding:10px 20px;border:none;border-radius:10px} a{color:#0F4A2E}</style></head><body><h1>এডমিন প্যানেল - {{d.site.name}}</h1><a href="/admin/logout">লগআউট</a> | <a href="/">সাইট দেখুন</a><div class="box"><h2>সাইট সেটিংস</h2><form method="POST" action="/admin/save">নাম <input name="site_name" value="{{d.site.name}}">স্লোগান <input name="slogan" value="{{d.site.slogan}}">ট্যাগলাইন <input name="tagline" value="{{d.site.tagline}}">ঠিকানা <input name="address" value="{{d.site.address}}">ফোন <input name="phone" value="{{d.site.phone}}">হোয়াটসঅ্যাপ <input name="whatsapp" value="{{d.site.get('whatsapp','')}}">সম্পর্কে <textarea name="about_text">{{d.site.about_text}}</textarea>লক্ষ্য <textarea name="aim">{{d.site.aim}}</textarea>উদ্দেশ্য <input name="purpose" value="{{d.site.purpose}}">ফেসবুক <input name="facebook" value="{{d.site.facebook}}">ইউটিউব <input name="youtube" value="{{d.site.youtube}}">ফুটার <input name="footer_text" value="{{d.site.footer_text}}">বিকাশ <input name="bkash" value="{{d.site.get('bkash','')}}">নগদ <input name="nagad" value="{{d.site.get('nagad','')}}">রকেট <input name="rocket" value="{{d.site.get('rocket','')}}">ব্যাংক <input name="bank" value="{{d.site.get('bank','')}}"><button>সেভ করুন</button></form></div><div class="box"><h2>পাসওয়ার্ড বদলান</h2><form method="POST" action="/admin/change-password"><input name="old_pass" type="password" placeholder="পুরনো"><input name="new_pass" type="password" placeholder="নতুন (৬+)"><button>বদলান</button></form></div><div class="box"><h2>স্লাইডার</h2><form method="POST" action="/admin/add-slider"><input name="title" placeholder="শিরোনাম"><input name="subtitle" placeholder="সবুজ বক্সের লেখা"><input name="image" placeholder="ছবি"><button>যোগ করুন</button></form>{% for s in d.slider %}<p>{{s.title}} - <a href="/admin/delete/slider/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>সংবাদ</h2><form method="POST" action="/admin/add-news"><input name="title" placeholder="শিরোনাম"><input name="date" placeholder="তারিখ"><input name="cat" placeholder="ক্যাটাগরি"><input name="image" placeholder="ছবি"><textarea name="desc" placeholder="বিস্তারিত"></textarea><button>যোগ করুন</button></form>{% for n in d.news %}<p>{{n.title}} - <a href="/admin/delete/news/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>নেতৃত্ব</h2><form method="POST" action="/admin/add-leader"><input name="name" placeholder="নাম"><input name="post" placeholder="পদ"><input name="image" placeholder="ছবি"><button>যোগ করুন</button></form>{% for l in d.leaders %}<p>{{l.name}} - <a href="/admin/delete/leaders/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>লাইব্রেরী</h2><form method="POST" action="/admin/add-book"><input name="title" placeholder="বইয়ের নাম"><input name="author" placeholder="লেখক"><select name="level"><option>সদস্য</option><option>কর্মী</option><option>মুবাল্লিগ</option><option>প্রত্যাশী মুবাল্লিগ</option></select><input name="image" placeholder="কভার"><input name="file" placeholder="PDF"><textarea name="desc" placeholder="বিবরণ"></textarea><button>যোগ করুন</button></form>{% for b in d.library %}<p>{{b.title}} - <a href="/admin/delete/library/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>সদস্য - {{d.members|length}} জন</h2>{% for m in d.members %}<p>{{m.name}} - {{m.phone}} - <a href="/admin/delete/members/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>ইভেন্ট</h2><form method="POST" action="/admin/add-event"><input name="title" placeholder="নাম"><input name="date" placeholder="তারিখ"><input name="place" placeholder="স্থান"><input name="image" placeholder="ছবি"><textarea name="desc" placeholder="বিস্তারিত"></textarea><button>যোগ করুন</button></form>{% for e in d.events %}<p>{{e.title}} - <a href="/admin/delete/events/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>গ্যালারী</h2><form method="POST" action="/admin/add-gallery"><input name="title" placeholder="নাম"><input name="image" placeholder="ছবি"><button>যোগ করুন</button></form>{% for g in d.gallery %}<p>{{g.title}} - <a href="/admin/delete/gallery/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>প্রেস</h2><form method="POST" action="/admin/add-press"><input name="title" placeholder="শিরোনাম"><input name="date" placeholder="তারিখ"><textarea name="desc" placeholder="বিস্তারিত"></textarea><button>যোগ করুন</button></form>{% for p in d.press %}<p>{{p.title}} - <a href="/admin/delete/press/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div><div class="box"><h2>মেসেজ - {{d.contacts|length}} টি</h2>{% for c in d.contacts %}<p>{{c.name}} ({{c.phone}}) - {{c.subject}} - <a href="/admin/delete/contacts/{{loop.index0}}">ডিলিট</a></p>{% endfor %}</div></body></html>"""
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)); app.run(host="0.0.0.0", port=port)
