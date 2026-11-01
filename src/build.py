import html, os, shutil, json
from content_en import EN, UPDATED
from content_zh import ZH
from content_ja import JA
from content_ko import KO
from content_es import ES
from content_fr import FR
from content_de import DE
LANGS = [("en","English",EN),("zh-Hans","简体中文",ZH),("ja","日本語",JA),("ko","한국어",KO),("es","Español",ES),("fr","Français",FR),("de","Deutsch",DE)]
DATES = {"en":"2 November 2026","zh-Hans":"2026年11月2日","ja":"2026年11月2日","ko":"2026년 11월 2일","es":"2 de noviembre de 2026","fr":"2 novembre 2026","de":"2. November 2026"}
PAGES = ["privacy","terms","support","delete-account"]
OUT = "/workspace/kxq-legal-site"
BASE = "https://tj-nova-ltd.github.io/kxq-legal"
E = html.escape
CSS = """
:root{--ink:#0B0B0C;--bone:#F2EEE6;--sig:#FF4F00;--dim:#8C877E;--line:#2A2927}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ink);color:var(--bone);font:16px/1.65 -apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI","Hiragino Sans","PingFang SC","Apple SD Gothic Neo","Noto Sans",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--sig);text-underline-offset:3px}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px clamp(16px,5vw,48px);border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(11,11,12,.94);backdrop-filter:blur(8px);z-index:2}
.mark{display:flex;align-items:center;gap:10px;color:var(--bone);text-decoration:none;font-weight:900;letter-spacing:.08em;font-stretch:condensed}
.mark i{width:14px;height:14px;background:var(--sig);display:inline-block;transform:rotate(45deg)}
.mark b{font-size:20px}.mark span{font-size:11px;color:var(--dim);letter-spacing:.22em;text-transform:uppercase}
select{background:var(--ink);color:var(--bone);border:1px solid var(--line);border-radius:0;padding:6px 8px;font:inherit;font-size:14px}
nav.tabs{display:flex;flex-wrap:wrap;gap:0;padding:0 clamp(16px,5vw,48px);border-bottom:1px solid var(--line)}
nav.tabs a{color:var(--dim);text-decoration:none;text-transform:uppercase;letter-spacing:.14em;font-size:12px;font-weight:800;padding:14px 16px 12px;border-bottom:3px solid transparent}
nav.tabs a[aria-current]{color:var(--bone);border-color:var(--sig)}
main{max-width:860px;margin:0 auto;padding:clamp(28px,6vw,64px) clamp(16px,5vw,48px)}
.kicker{color:var(--sig);font-weight:800;letter-spacing:.24em;text-transform:uppercase;font-size:12px}
h1{font-family:"Arial Narrow","Helvetica Neue Condensed","Roboto Condensed",Impact,sans-serif;font-stretch:condensed;font-weight:900;text-transform:uppercase;font-size:clamp(40px,8vw,76px);line-height:.92;letter-spacing:-.01em;margin:10px 0 18px}
:lang(zh-Hans) h1,:lang(ja) h1,:lang(ko) h1{text-transform:none;font-family:inherit;letter-spacing:0;line-height:1.1}
.lead{font-size:19px;color:#D9D4CA;max-width:640px}
.upd{color:var(--dim);font-size:13px;margin-top:6px}
section{border-top:1px solid var(--line);padding:22px 0 6px;display:grid;grid-template-columns:44px 1fr;gap:0 14px}
section .n{font-weight:900;color:var(--sig);font-size:14px;padding-top:4px;font-variant-numeric:tabular-nums}
h2{margin:0 0 8px;font-size:20px;font-weight:850;letter-spacing:.01em}
p{margin:0 0 14px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:28px}
.cards a{display:block;border:1px solid var(--line);padding:18px;color:var(--bone);text-decoration:none;font-weight:850;text-transform:uppercase;letter-spacing:.08em;font-size:14px}
.cards a:hover{border-color:var(--sig)}.cards a:after{content:" →";color:var(--sig)}
footer{border-top:3px solid var(--sig);padding:28px clamp(16px,5vw,48px) 40px;color:var(--dim);font-size:13px}
footer .tag{color:var(--bone);font-weight:900;letter-spacing:.2em;text-transform:uppercase;font-size:13px;margin-bottom:10px}
footer .links a{color:var(--bone);margin-right:16px;text-decoration:none;border-bottom:1px solid var(--line)}
footer .links{margin:10px 0}
@media (max-width:520px){section{grid-template-columns:1fr}section .n{padding:0 0 4px}}
"""
def page_url(lang, page): return f"{BASE}/{lang}/{page}.html"
def shell(lang, D, page, title, body):
    ui = D["ui"]
    rel = "index.html" if page is None else f"{page}.html"
    opts = "".join(f'<option value="../{c}/{rel}"{" selected" if c==lang else ""}>{E(n)}</option>' for c,n,_ in LANGS)
    tabs = "".join(f'<a href="{p}.html"{" aria-current=\"page\"" if p==page else ""}>{E(ui["nav"][p])}</a>' for p in PAGES)
    alts = "".join(f'<link rel="alternate" hreflang="{c}" href="{BASE}/{c}/{rel}">' for c,_,_ in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{BASE}/en/{rel}">'
    flinks = "".join(f'<a href="{p}.html">{E(ui["nav"][p])}</a>' for p in PAGES)
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · KXQ</title><meta name="description" content="{E(ui['home_lead'])}"><meta name="theme-color" content="#0B0B0C">
<link rel="canonical" href="{BASE}/{lang}/{rel}">{alts}
<style>{CSS}</style></head><body>
<header class="bar"><a class="mark" href="index.html"><i></i><b>KXQ</b><span>Pack Rip Club</span></a>
<label><span hidden>{E(ui['lang'])}</span><select aria-label="{E(ui['lang'])}" onchange="location.href=this.value">{opts}</select></label></header>
<nav class="tabs">{tabs}</nav>
<main>{body}</main>
<footer><div class="tag">{E(ui['footer_tag'])}</div><div class="links">{flinks}</div>
<p>{E(ui['footer_op'])}</p><p>{E(ui['contact'])}: <a href="mailto:info@tjnovaltd.com">info@tjnovaltd.com</a> · © 2026 TJ NOVA LTD</p></footer>
</body></html>
"""
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
for lang, name, D in LANGS:
    os.makedirs(f"{OUT}/{lang}")
    ui = D["ui"]
    for p in PAGES:
        d = D[p]
        secs = "".join(f'<section><div class="n">{i:02d}</div><div><h2>{E(h)}</h2>{"".join(f"<p>{E(x)}</p>" for x in ps)}</div></section>' for i,(h,ps) in enumerate(d["sections"],1))
        body = f'<div class="kicker">KXQ · {E(ui["nav"][p])}</div><h1>{E(d["title"])}</h1><p class="lead">{E(d["lead"])}</p><p class="upd">{E(ui["updated"])}: {E(DATES[lang])}</p>{secs}'
        open(f"{OUT}/{lang}/{p}.html","w").write(shell(lang, D, p, d["title"], body))
    cards = "".join(f'<a href="{p}.html">{E(ui["nav"][p])}</a>' for p in PAGES)
    body = f'<div class="kicker">TJ NOVA LTD</div><h1>{E(ui["home_title"])}</h1><p class="lead">{E(ui["home_lead"])}</p><div class="cards">{cards}</div>'
    open(f"{OUT}/{lang}/index.html","w").write(shell(lang, D, None, ui["home_title"], body))
codes = [c for c,_,_ in LANGS]
redir = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KXQ · Legal</title>
<meta name="theme-color" content="#0B0B0C"><noscript><meta http-equiv="refresh" content="0;url=en/index.html"></noscript>
<script>(function(){var A=%s;var p=(location.search.match(/[?&]page=([a-z-]+)/)||[])[1];var P=%s;var page=P.indexOf(p)>=0?p+'.html':'index.html';
var ls=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'en']);var pick='en';
for(var i=0;i<ls.length;i++){var l=(ls[i]||'').toLowerCase();var b=l.split('-')[0];if(b==='zh'){pick='zh-Hans';break}if(A.indexOf(b)>=0){pick=b;break}}
location.replace(pick+'/'+page);})();</script>
<style>body{margin:0;background:#0B0B0C;color:#F2EEE6;font:16px -apple-system,Segoe UI,Roboto,sans-serif;display:grid;place-items:center;min-height:100vh}a{color:#FF4F00}</style></head>
<body><p><a href="en/index.html">KXQ — Legal &amp; Help</a></p></body></html>
""" % (json.dumps(codes), json.dumps(PAGES))
open(f"{OUT}/index.html","w").write(redir)
open(f"{OUT}/404.html","w").write(redir.replace("<title>KXQ · Legal</title>","<title>KXQ · Not found</title>"))
open(f"{OUT}/.nojekyll","w").write("")
open(f"{OUT}/README.md","w").write("# KXQ — legal & help pages\n\nPrivacy, terms (EULA), support and account deletion pages for KXQ — Pack Rip Club, operated by TJ NOVA LTD.\n\nURLs: `https://tj-nova-ltd.github.io/kxq-legal/<lang>/<page>.html` — lang: " + ", ".join(codes) + "; page: " + ", ".join(PAGES) + ".\n\nGenerated from the content files in `src/` by `src/build.py`.\n")
os.makedirs(f"{OUT}/src")
for fn in ["build.py","content_en.py","content_zh.py","content_ja.py","content_ko.py","content_es.py","content_fr.py","content_de.py"]: shutil.copy(fn, f"{OUT}/src/{fn}")
print("ok", sum(len(f) for _,_,f in os.walk(OUT)))
