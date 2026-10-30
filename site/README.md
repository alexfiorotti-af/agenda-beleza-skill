# Site da Agenda Beleza

Página de venda da Agenda Beleza, com o app em `/app`, mockups reais das telas e rastreamento pronto (GTM + GA4 + Pixel + API de Conversões do Meta).

## Estrutura

```
site/
├── index.html        # a página (GTM-W97LQMJD já configurado no topo)
├── app/index.html    # o app Agenda Beleza (cópia de demo/agenda-beleza.html)
├── api/capi.js       # função da Vercel que envia eventos à API de Conversões
├── img/              # fotos, capturas das telas e imagem de compartilhamento
│   └── PROMPTS.md    # prompts para gerar novas fotos no mesmo conceito
└── vercel.json
```

Os arquivos de rastreamento ficam fora do site, em `../tracking/`:
`gtm-container-GTM-W97LQMJD.json` (importar no GTM), `tracking-plan.json` (o que é medido) e `build_gtm.py` (gera o container).

## Publicar

1. Na Vercel: Add New → Project → importe este repositório.
2. Em **Root Directory**, escolha `site`. Framework: Other. Deploy.
3. Em Settings → Environment Variables, crie `META_PIXEL_ID` e `META_CAPI_TOKEN` e faça um novo deploy.
4. Importe o container do GTM e preencha as duas constantes.

O passo a passo completo, com o caminho de cada clique, está no guia "Rastreamento do site Agenda Beleza".

## Usar em outro projeto

Troque `gtmId` e o número de WhatsApp no início do `index.html` (`window.AB_CONFIG` e os links `wa.me`). Sem isso, os eventos vão para o GTM da AF.
