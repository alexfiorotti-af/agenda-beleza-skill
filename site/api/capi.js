// Agenda Beleza: ponte do site para a API de Conversões (CAPI) do Meta.
// Roda como função da Vercel em /api/capi. O site manda o evento com o mesmo
// event_id que o Pixel usa no navegador, e o Meta conta uma vez só.
//
// Variáveis de ambiente (Vercel → Settings → Environment Variables):
//   META_PIXEL_ID          obrigatório  ID do Pixel (conjunto de dados)
//   META_CAPI_TOKEN        obrigatório  token gerado no Gerenciador de Eventos (NUNCA no GitHub)
//   META_TEST_EVENT_CODE   opcional     código TESTxxxx, só enquanto testa
//   META_API_VERSION       opcional     padrão v23.0
//   ALLOWED_ORIGIN         opcional     ex.: https://agendabeleza.com.br (aceita só chamadas do seu site)

const crypto = require('crypto');

const EVENTOS_PERMITIDOS = new Set(['PageView', 'ViewContent', 'Lead', 'StartTrial', 'Contact']);
const sha256 = (v) => crypto.createHash('sha256').update(String(v).trim().toLowerCase()).digest('hex');

function limpaCustomData(c) {
  const out = {};
  if (!c || typeof c !== 'object') return out;
  for (const [k, v] of Object.entries(c).slice(0, 10)) {
    if (typeof v === 'string') out[k] = v.slice(0, 200);
    else if (typeof v === 'number' || typeof v === 'boolean') out[k] = v;
  }
  return out;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ ok: false, erro: 'use POST' });
  }

  const {
    META_PIXEL_ID: pixel,
    META_CAPI_TOKEN: token,
    META_TEST_EVENT_CODE: codigoTeste,
    META_API_VERSION: versao = 'v23.0',
    ALLOWED_ORIGIN: origemPermitida,
  } = process.env;

  if (!pixel || !token) {
    return res.status(500).json({ ok: false, erro: 'Faltam META_PIXEL_ID e META_CAPI_TOKEN nas variáveis da Vercel' });
  }

  if (origemPermitida) {
    const origem = req.headers.origin || req.headers.referer || '';
    if (!origem.startsWith(origemPermitida)) return res.status(403).json({ ok: false, erro: 'origem não permitida' });
  }

  let b = req.body;
  if (typeof b === 'string') {
    try { b = JSON.parse(b); } catch { return res.status(400).json({ ok: false, erro: 'JSON inválido' }); }
  }
  b = b || {};
  if (!EVENTOS_PERMITIDOS.has(b.event_name) || !b.event_id) {
    return res.status(400).json({ ok: false, erro: 'evento inválido' });
  }

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || (req.socket && req.socket.remoteAddress);
  const user_data = { client_ip_address: ip, client_user_agent: req.headers['user-agent'] };
  if (b.fbp) user_data.fbp = String(b.fbp).slice(0, 200);
  if (b.fbc) user_data.fbc = String(b.fbc).slice(0, 500);
  if (b.external_id) user_data.external_id = [sha256(b.external_id)];

  const payload = {
    data: [{
      event_name: b.event_name,
      event_time: Math.floor(Date.now() / 1000),
      event_id: String(b.event_id).slice(0, 100),
      event_source_url: String(b.event_source_url || '').slice(0, 500),
      action_source: 'website',
      user_data,
      custom_data: limpaCustomData(b.custom_data),
    }],
  };
  if (codigoTeste) payload.test_event_code = codigoTeste;

  try {
    const r = await fetch(`https://graph.facebook.com/${versao}/${pixel}/events?access_token=${encodeURIComponent(token)}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) {
      console.error('CAPI recusou', r.status, JSON.stringify(j));
      return res.status(502).json({ ok: false });
    }
    return res.status(200).json({ ok: true, recebidos: j.events_received });
  } catch (e) {
    console.error('CAPI falhou', e);
    return res.status(502).json({ ok: false });
  }
};
