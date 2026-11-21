"""Shared pieces for the wave 3 design templates (P064 menu, P066 Aufguss board, P067 membership card, P068 poster).

Each template is ONE self-contained HTML file (fonts embedded, no network) that is:
  - editable in a browser: every text field is contenteditable, edits are kept in localStorage, Reset restores the sample
  - printable at the right paper size: ?size=<key> switches the page size and the matching @page rule
  - the single source for the PDFs, PNGs and the Figma SVGs: w3_run.js renders it and converts the laid-out page
    into plain SVG (rects, lines, <text> with real font names, nested icon SVGs, groups named after the fields)

Layout lengths are written in "u" (1u = 1/100 of the page width) and turned into calc() here,
so one stylesheet serves Letter, A4, A3, Tabloid and screen sizes.
License of the templates: CC BY 4.0 - DIVELUX, https://diveluxsaunahat.com
"""
import json
import os
import re
import sys

sys.path.insert(0, "/root/divelux/freebies/printables/_build")
import common as PC  # noqa: E402  (fonts and escaping only; that module is not changed)

ROOT = "/root/divelux/freebies/templates"
GFX = "/root/divelux/freebies/gfx"
SITE = "https://diveluxsaunahat.com"
TOOLS = "https://diveluxsaunahat.com/pages/sauna-tools"
esc = PC.esc

PX = {"in": 96.0, "mm": 96.0 / 25.4, "px": 1.0}


def px(v):
    m = re.fullmatch(r"([\d.]+)(in|mm|px)", v)
    return float(m.group(1)) * PX[m.group(2)]


def U(css):
    """'12.5u' -> 'calc(12.5*var(--u))'."""
    return re.sub(r"(?<![\w#.-])(-?\d*\.?\d+)u\b", r"calc(\1*var(--u))", css)


def size(label, w, h, pdf=True, png=False):
    return dict(label=label, w=w, h=h, wpx=round(px(w), 3), hpx=round(px(h), 3), pdf=pdf, png=png)


BASE = """
:root{--paper:#f6f3ee;--paper-2:#ede8df;--card:#fffdf9;--ink:#1b1512;--ink-2:#3d332c;--muted:#6f655c;--line:#dcd4c8;
--line-2:#b9afa2;--wood:#c99b6c;--wood-2:#ecd6b2;--night:#1c110b;--night-2:#2a1b13;--ember:#f0762e;--t1:#f0a877;--t2:#f5c7a0;--t3:#f8dfc6;--t4:#fbf1e5;
--water:#a9c3c8;--water-2:#7ea3ab;--r:6px;--display:"Bricolage Grotesque",Arial,sans-serif;--body:"Inter",Arial,sans-serif}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:var(--body);color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact;line-height:1.35}
h1,h2,h3,p,ul,ol{margin:0;padding:0;font-weight:inherit;font-size:inherit}
ul,ol{list-style:none}
a{color:inherit;text-decoration:none}
.d{font-family:var(--display);font-optical-sizing:auto}
.num{font-variant-numeric:tabular-nums lining-nums}
.page{position:relative;width:var(--pw);height:var(--ph);overflow:hidden;background:var(--paper);display:flex;flex-direction:column;
break-after:page;page-break-after:always}
.page:last-child{break-after:auto;page-break-after:auto}
[contenteditable]{outline:none;border-radius:2px}
.credit{font-family:var(--body);font-weight:400;color:var(--muted);white-space:nowrap}
.credit a{color:inherit;font-weight:600}
svg.ill,svg.ico{display:block;flex:none}
@media print{.screen-only,.ctl{display:none!important}}
@media screen{
  html{background:#cfc9c0}
  body{padding:0 0 40px}
  #doc{margin-top:22px;display:flex;flex-direction:column;align-items:center;gap:22px}
  .page{zoom:var(--z,1);box-shadow:0 2px 14px rgba(27,21,18,.25)}
  [contenteditable]:hover{box-shadow:0 0 0 1px rgba(240,118,46,.55)}
  [contenteditable]:focus{box-shadow:0 0 0 2px #f0762e;background:rgba(255,255,255,.35)}
  .bar{position:sticky;top:0;z-index:9;display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;padding:10px 16px;
    background:#1b1512;color:#f6f3ee;font:14px/1.3 var(--body)}
  .bar b{font-family:var(--display);font-weight:700;font-size:15px}
  .bar .grp{display:flex;gap:6px;flex-wrap:wrap}
  .bar a,.bar button{font:600 13px/1 var(--body);color:#f6f3ee;background:#3d332c;border:0;border-radius:6px;padding:9px 12px;cursor:pointer;min-height:34px;display:inline-flex;align-items:center}
  .bar a[aria-current]{background:#f6f3ee;color:#1b1512}
  .bar button.main{background:#f0762e;color:#1b1512}
  .bar .hint{color:#c9bfb3;font-size:13px;flex:1 1 260px}
  .bar a:focus-visible,.bar button:focus-visible{outline:2px solid #f0762e;outline-offset:2px}
  .ctl{position:absolute;z-index:3;font:600 11px/1 var(--body);border:0;border-radius:6px;background:#1b1512;color:#f6f3ee;padding:5px 8px;cursor:pointer;opacity:.85}
  .ctl:hover{opacity:1;background:#f0762e;color:#1b1512}
  .ctl.del{right:-4px;top:50%;transform:translateY(-50%);display:none}
  [data-item]{position:relative}
  [data-item]:hover>.ctl.del{display:block}
  .ctl.add{position:static;margin-top:4px;align-self:flex-start;opacity:.7}
}
"""

# Size switch: runs in <head> before the page is laid out.
HEAD_JS = """<script>(function(){var S=%s,D='%s',L=%s,DL='%s',d=document.documentElement,q=new URLSearchParams(location.search);
var k=(q.get('size')||D).toLowerCase();if(!S[k])k=D;var s=S[k];d.classList.add('size-'+k);d.dataset.size=k;
d.style.setProperty('--pw',s.wpx+'px');d.style.setProperty('--ph',s.hpx+'px');d.style.setProperty('--u',(s.wpx/100)+'px');
if(L){var l=(q.get('layout')||DL).toLowerCase();if(L.indexOf(l)<0)l=DL;d.classList.add('layout-'+l);d.dataset.layout=l;}
var st=document.createElement('style');st.textContent=q.has('pdfpad')?'@page{size:'+(Math.ceil(s.wpx)+4)+'px '+(Math.ceil(s.hpx)+4)+'px;margin:0}':'@page{size:'+s.w+' '+s.h+';margin:0}';document.head.appendChild(st);})();</script>"""

EDIT_JS = r"""<script>(function(){
var d=document.documentElement,root=document.getElementById('doc'),KEY=d.dataset.key,view=d.dataset.view||'main';
if(d.dataset.layout)view+='-'+d.dataset.layout;
var hk=KEY+':'+view,sk=KEY+':sync',timer=null,resetting=false;
function ls(){try{return window.localStorage}catch(e){return null}}
var st=ls();
function clean(){var c=root.cloneNode(true);c.querySelectorAll('.ctl').forEach(function(e){e.remove()});return c.innerHTML}
function save(){if(!st||resetting)return;try{st.setItem(hk,clean())}catch(e){}}
function later(){clearTimeout(timer);timer=setTimeout(save,250)}
function syncMap(){try{return JSON.parse(st&&st.getItem(sk)||'{}')}catch(e){return {}}}
function applySync(){var m=syncMap();Object.keys(m).forEach(function(k){root.querySelectorAll('[data-sync="'+k+'"]').forEach(function(e){if(e.textContent!==m[k])e.textContent=m[k]})})}
function controls(){
  root.querySelectorAll('[data-item]').forEach(function(it){if(it.querySelector(':scope>.ctl.del'))return;var b=document.createElement('button');
    b.type='button';b.className='ctl del';b.textContent='Remove';b.title='Remove this line';b.setAttribute('contenteditable','false');
    b.onclick=function(){it.remove();save()};it.appendChild(b)});
  root.querySelectorAll('[data-list]').forEach(function(l){if(l.nextElementSibling&&l.nextElementSibling.classList.contains('add'))return;
    var b=document.createElement('button');b.type='button';b.className='ctl add';b.textContent='+ Add line';
    b.onclick=function(){var src=l.querySelector('[data-item]:last-of-type');if(!src)return;var n=src.cloneNode(true);
      n.querySelectorAll('.ctl').forEach(function(e){e.remove()});l.appendChild(n);controls();save();
      var f=n.querySelector('[contenteditable]');if(f)f.focus()};
    l.parentNode.insertBefore(b,l.nextSibling)});
}
if(st){var h=st.getItem(hk);if(h)root.innerHTML=h;}
applySync();controls();
root.addEventListener('input',function(e){var el=e.target.closest('[data-sync]');
  if(el&&st){var k=el.dataset.sync,v=el.textContent;root.querySelectorAll('[data-sync="'+k+'"]').forEach(function(o){if(o!==el)o.textContent=v});
    var m=syncMap();m[k]=v;try{st.setItem(sk,JSON.stringify(m))}catch(x){}}
  later()});
root.addEventListener('focusout',function(){clearTimeout(timer);save()});
window.addEventListener('pagehide',function(){clearTimeout(timer);save()});
root.addEventListener('keydown',function(e){var el=e.target.closest('[contenteditable]');if(el&&e.key==='Enter'&&!el.hasAttribute('data-multi')){e.preventDefault();el.blur()}});
root.addEventListener('paste',function(e){var el=e.target.closest('[contenteditable]');if(!el)return;e.preventDefault();
  var t=(e.clipboardData||window.clipboardData).getData('text/plain');if(!el.hasAttribute('data-multi'))t=t.replace(/\s*\n\s*/g,' ');
  document.execCommand('insertText',false,t)});
function vis(){return [].slice.call(root.querySelectorAll('.page')).filter(function(p){return p.getClientRects().length})[0]}
function fit(){var p=vis();if(!p)return;var w=parseFloat(getComputedStyle(d).getPropertyValue('--pw'));
  var z=Math.min(w<500?2.5:1,(window.innerWidth-40)/w);d.style.setProperty('--z',z.toFixed(4))}
fit();window.addEventListener('resize',fit);
var bp=document.getElementById('b-print'),br=document.getElementById('b-reset'),bf=document.getElementById('b-full');
if(bp)bp.onclick=function(){window.print()};
if(br)br.onclick=function(){if(!confirm('Reset this template to the sample text? Your edits in this browser will be removed.'))return;resetting=true;clearTimeout(timer);
  if(st){Object.keys(st).forEach(function(k){if(k.indexOf(KEY+':')===0)st.removeItem(k)})}location.reload()};
if(bf)bf.onclick=function(){var p=vis();if(p.requestFullscreen)p.requestFullscreen()};
document.addEventListener('fullscreenchange',function(){var p=vis();if(document.fullscreenElement){
  var w=parseFloat(getComputedStyle(d).getPropertyValue('--pw')),h=parseFloat(getComputedStyle(d).getPropertyValue('--ph'));
  p.style.zoom=Math.min(screen.width/w,screen.height/h)}else{p.style.zoom=''}});
})();</script>"""


def bar(title, sizes, cur_note, layouts=None, extra_buttons=""):
    """Screen-only toolbar: size links, layout links, Print, Reset. JS marks the current ones."""
    sz = "".join(f'<a href="?size={k}" data-k="{k}">{esc(v["label"])}</a>' for k, v in sizes.items())
    lay = ""
    if layouts:
        lay = '<span class="grp" data-g="layout">' + "".join(
            f'<a href="?layout={k}" data-k="{k}">{esc(v)}</a>' for k, v in layouts.items()) + "</span>"
    return (f'<nav class="bar screen-only" aria-label="Template tools"><b>{esc(title)}</b>'
            f'<span class="grp" data-g="size">{sz}</span>{lay}'
            f'<button type="button" id="b-print" class="main">Print / Save PDF</button>{extra_buttons}'
            f'<button type="button" id="b-reset">Reset</button>'
            f'<span class="hint">Click any text to edit it. Edits stay in this browser. {cur_note}</span></nav>'
            """<script>(function(){var d=document.documentElement,q=new URLSearchParams(location.search);
document.querySelectorAll('.bar .grp').forEach(function(g){var key=g.dataset.g,cur=d.dataset[key];
g.querySelectorAll('a').forEach(function(a){var p=new URLSearchParams(location.search);p.set(key,a.dataset.k);a.href='?'+p.toString();
if(a.dataset.k===cur)a.setAttribute('aria-current','true')})})})();</script>""")


def doc(key, title, desc, sizes, default, css, body, layouts=None, default_layout=None, view="main", note="", extra_buttons=""):
    sj = json.dumps({k: dict(w=v["w"], h=v["h"], wpx=v["wpx"], hpx=v["hpx"]) for k, v in sizes.items()})
    lj = json.dumps(list(layouts)) if layouts else "null"
    return f"""<!doctype html>
<html lang="en-US" data-key="{key}" data-view="{view}"><head><meta charset="utf-8">
<title>{esc(title)}</title>
<meta name="author" content="DIVELUX">
<meta name="description" content="{esc(desc)}">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Editable template by DIVELUX (https://diveluxsaunahat.com), CC BY 4.0. Open in Chrome, Edge, Firefox or Safari.
     Sizes: {", ".join(f"?size={k} ({v['label']})" for k, v in sizes.items())}{"; layouts: " + ", ".join("?layout=" + k for k in layouts) if layouts else ""}.
     Print at 100% (actual size), margins None, background graphics on. -->
{HEAD_JS % (sj, default, lj, default_layout or "")}
<style>{BASE}
{U(css)}
</style>
<style>/* Fonts: Bricolage Grotesque and Inter, SIL Open Font License 1.1 */
{PC.font_css()}
</style>
</head><body>
{bar(title, sizes, note, layouts, extra_buttons)}
<div id="doc">
{body}
</div>
{EDIT_JS}
</body></html>
"""


def ed(tag, name, text, cls="", multi=False, sync=None, attrs=""):
    """Editable text element. name -> data-name (becomes the layer name in the SVG)."""
    c = f' class="{cls}"' if cls else ""
    m = " data-multi" if multi else ""
    s = f' data-sync="{sync}"' if sync else ""
    a = f" {attrs}" if attrs else ""
    return f'<{tag}{c} data-name="{name}" contenteditable="true" spellcheck="false"{m}{s}{a}>{text}</{tag}>'


def credit(cls="credit"):
    return f'<p class="{cls}" data-name="credit">Template by DIVELUX · <a href="{SITE}">diveluxsaunahat.com</a> · CC BY 4.0</p>'


def _inner(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<title>.*?</title>", "", s, flags=re.S)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    return vb, s[s.index(">") + 1:s.rindex("</svg>")]


def art(name, cls="ill", drop_disc=False, uid=None, label=None):
    """One of the DIVELUX Sauna Illustrations (CC BY 4.0, gfx/sauna-illustrations/svg)."""
    vb, inner = _inner(os.path.join(GFX, "sauna-illustrations", "svg", name + ".svg"))
    if drop_disc:  # the soft background disc and floor shadow, for dark or busy backgrounds
        inner = re.sub(r'^<circle cx="300" cy="305" r="250" fill="#efe9df"/>', "", inner)
        inner = re.sub(r'^<ellipse cx="300" cy="5\d\d" rx="\d+" ry="\d+" fill="#dfd7ca"/>', "", inner)
    if uid:
        inner = inner.replace('id="cabin-clip"', f'id="{uid}"').replace("url(#cabin-clip)", f"url(#{uid})")
        inner = inner.replace('id="interior-clip"', f'id="{uid}"').replace("url(#interior-clip)", f"url(#{uid})")
    lab = f' data-name="{label}"' if label else ""
    return f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" aria-hidden="true"{lab}>{inner}</svg>'


def icon(name, cls="ico", label=None):
    """One of the DIVELUX filled sauna icons (CC BY 4.0, gfx/sauna-icons-filled/svg), fill = currentColor."""
    vb, inner = _inner(os.path.join(GFX, "sauna-icons-filled", "svg", name + ".svg"))
    lab = f' data-name="{label}"' if label else ""
    return f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="currentColor" aria-hidden="true"{lab}>{inner}</svg>'


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
