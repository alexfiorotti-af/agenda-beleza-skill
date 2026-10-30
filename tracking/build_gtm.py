"""Gera o container do GTM (formato de importação v2) para o site Agenda Beleza.

Uso: python3 tracking/build_gtm.py  ->  tracking/gtm-container-GTM-W97LQMJD.json
Depois de importar, preencha as duas constantes (GA4 e Pixel) no GTM.
"""
import json, pathlib

ACC, CON = "0", "0"
ALL_PAGES = "2147479553"  # gatilho nativo "All Pages"

def P(t, k, v): return {"type": t, "key": k, "value": v}
def T(k, v): return P("TEMPLATE", k, v)

variaveis, gatilhos, tags = [], [], []
vid = iter(range(20, 100)); gid = iter(range(10, 20)); tid = iter(range(1, 10))

def const(nome, valor):
    variaveis.append({"accountId": ACC, "containerId": CON, "variableId": str(next(vid)), "name": nome, "type": "c",
                      "parameter": [T("value", valor)], "fingerprint": "0"})

def dlv(chave):
    variaveis.append({"accountId": ACC, "containerId": CON, "variableId": str(next(vid)), "name": f"DLV - {chave}", "type": "v",
                      "parameter": [P("INTEGER", "dataLayerVersion", "2"), P("BOOLEAN", "setDefaultValue", "false"), T("name", chave)],
                      "fingerprint": "0"})

def ce(nome, evento, regex=False, filtros=None):
    g = {"accountId": ACC, "containerId": CON, "triggerId": str(next(gid)), "name": nome, "type": "CUSTOM_EVENT",
         "customEventFilter": [{"type": "MATCH_REGEX" if regex else "EQUALS",
                                "parameter": [T("arg0", "{{_event}}"), T("arg1", evento)]}],
         "fingerprint": "0"}
    if filtros: g["filter"] = filtros
    gatilhos.append(g); return g["triggerId"]

def tag(nome, tipo, params, disparo, bloqueio=None, uma_vez=False):
    t = {"accountId": ACC, "containerId": CON, "tagId": str(next(tid)), "name": nome, "type": tipo, "parameter": params,
         "fingerprint": "0", "firingTriggerId": disparo,
         "tagFiringOption": "ONCE_PER_LOAD" if uma_vez else "ONCE_PER_EVENT",
         "monitoringMetadata": {"type": "MAP"}, "consentSettings": {"consentStatus": "NOT_SET"}}
    if bloqueio: t["blockingTriggerId"] = bloqueio
    tags.append(t)

# ---- Variáveis
const("CONST - GA4 Measurement ID", "G-XXXXXXXXXX")
const("CONST - Meta Pixel ID", "000000000000000")
PARAMS = ["event_id", "cta_id", "cta_location", "cta_text", "section_id", "scroll_percent", "mockup_screen", "faq_question"]
for k in PARAMS + ["consent_ads"]: dlv(k)

# ---- Gatilhos
EVENTOS_GA4 = ["open_app", "whatsapp_click", "cta_click", "section_view", "scroll_depth", "mockup_interaction", "faq_open", "view_features"]
g_ga4 = ce("CE - Eventos do site (GA4)", "^(" + "|".join(EVENTOS_GA4) + ")$", regex=True)
g_consent = ce("CE - consent_update", "consent_update")
g_open = ce("CE - open_app", "open_app")
g_wa = ce("CE - whatsapp_click", "whatsapp_click")
g_view = ce("CE - view_features", "view_features")
g_bloq = ce("Bloqueio - sem consentimento de anúncios", ".*", regex=True, filtros=[{
    "type": "EQUALS", "parameter": [T("arg0", "{{DLV - consent_ads}}"), T("arg1", "granted"), P("BOOLEAN", "negate", "true")]}])

# ---- Tags GA4
tag("GA4 - Tag do Google", "googtag", [T("tagId", "{{CONST - GA4 Measurement ID}}")], [ALL_PAGES])
tag("GA4 - Eventos do site", "gaawe", [
    P("BOOLEAN", "sendEcommerceData", "false"),
    T("eventName", "{{Event}}"),
    T("measurementIdOverride", "{{CONST - GA4 Measurement ID}}"),
    {"type": "LIST", "key": "eventSettingsTable", "list": [
        {"type": "MAP", "map": [T("parameter", k), T("parameterValue", "{{DLV - %s}}" % k)]} for k in PARAMS]},
], [g_ga4])

# ---- Tags Meta (só com consentimento: gatilho de bloqueio)
PIXEL_BASE = """<script>
!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', {{CONST - Meta Pixel ID}});
fbq('track', 'PageView', {}, {eventID: {{DLV - event_id}}});
</script>"""

def pixel_evento(nome_meta):
    return ("<script>\nif (typeof fbq === 'function') {\n  fbq('track', '%s', {content_name: {{DLV - cta_location}} || {{DLV - section_id}}}, {eventID: {{DLV - event_id}}});\n}\n</script>" % nome_meta)

def html(code): return [T("html", code), P("BOOLEAN", "supportDocumentWrite", "false")]

tag("Meta - Pixel base + PageView", "html", html(PIXEL_BASE), [g_consent], bloqueio=[g_bloq], uma_vez=True)
tag("Meta - Lead (WhatsApp)", "html", html(pixel_evento("Lead")), [g_wa], bloqueio=[g_bloq])
tag("Meta - StartTrial (abrir o app)", "html", html(pixel_evento("StartTrial")), [g_open], bloqueio=[g_bloq])
tag("Meta - ViewContent (telas do app)", "html", html(pixel_evento("ViewContent")), [g_view], bloqueio=[g_bloq])

container = {
    "exportFormatVersion": 2,
    "exportTime": "2026-10-30 18:00:00",
    "containerVersion": {
        "path": f"accounts/{ACC}/containers/{CON}/versions/0",
        "accountId": ACC, "containerId": CON, "containerVersionId": "0",
        "container": {"path": f"accounts/{ACC}/containers/{CON}", "accountId": ACC, "containerId": CON,
                      "name": "Agenda Beleza - site", "publicId": "GTM-W97LQMJD", "usageContext": ["WEB"],
                      "fingerprint": "0", "tagManagerUrl": "https://tagmanager.google.com/"},
        "tag": tags, "trigger": gatilhos, "variable": variaveis,
        "builtInVariable": [{"accountId": ACC, "containerId": CON, "type": t, "name": n} for t, n in
                            [("PAGE_URL", "Page URL"), ("PAGE_HOSTNAME", "Page Hostname"), ("PAGE_PATH", "Page Path"),
                             ("REFERRER", "Referrer"), ("EVENT", "Event")]],
        "fingerprint": "0",
    },
}
out = pathlib.Path(__file__).with_name("gtm-container-GTM-W97LQMJD.json")
out.write_text(json.dumps(container, ensure_ascii=False, indent=2), encoding="utf-8")
print(out, f"{len(tags)} tags, {len(gatilhos)} gatilhos, {len(variaveis)} variáveis")
