---
name: landing-beleza
description: Cria página de venda (landing page) para app ou serviço do nicho beleza (nail designer, manicure, cabeleireira, salão, lash, estética) com mockups reais das telas, fotos tratadas, texto na língua da profissional e rastreamento pronto (GTM, GA4, Pixel e CAPI na Vercel).
license: MIT
---

# Landing page do nicho beleza

Gera uma página de venda em um único `index.html` (sem framework), com mockups feitos de capturas REAIS do produto, fotos do cliente tratadas, e rastreamento completo: `dataLayer`, container do GTM em JSON para importar, e uma função da Vercel para a API de Conversões do Meta.

Implementação de referência: a pasta `site/` e a pasta `tracking/` deste repositório (Agenda Beleza). Copie a estrutura; troque conteúdo, cores e IDs.

## Processo

1. **Junte o material antes de desenhar**: o produto rodando (URL ou HTML), as fotos do cliente, o ID do GTM, o WhatsApp de contato e o modelo de negócio (grátis, pago, sob consulta). Não invente preço nem depoimento.
2. **Capture as telas reais** com Playwright, 390×844 a 2x, idioma do navegador igual ao do público (`--lang=pt-BR`; datas em formato brasileiro). Se os dados de exemplo deixarem a tela vazia, injete uma agenda de exemplo realista via `localStorage` antes de capturar. Feche toasts e sugestões abertas antes de cada foto. Salve em WebP q82.
3. **Trate as fotos** com Pillow: recorte retrato 3:4 para o topo, 2:3 para faixa escura, 1:1 para detalhes. Abra a folha de contato e confira o enquadramento: fotos maiores que o esperado deslocam os recortes.
4. **Escreva o texto** (voz abaixo), depois o HTML (estrutura abaixo).
5. **Rastreamento**: `dataLayer` no site, container GTM gerado por script, função CAPI. Teste a função com `fetch` simulado antes de publicar.
6. **Um olhar só**: captura de página inteira em 390px e 1366px com as fontes embutidas (`@fontsource-variable/*` injetado com `bypassCSP`), conferindo rolagem lateral (`scrollWidth`), erros de script e o `dataLayer`. Corrija o que aparecer e confira de novo só o que mudou.
7. Gere a imagem de compartilhamento 1200×630 a partir do próprio topo da página.
8. Branch + PR, ficha do projeto atualizada, guia passo a passo de publicação.

## Estrutura da página (ordem que converte neste nicho)

1. **Topo fixo**: marca, 4 links, botão principal.
2. **Abertura**: frase curta que nomeia o resultado emocional ("Agenda cheia, cabeça tranquila."), parágrafo que diz o que o produto faz em ações concretas, dois botões (usar e WhatsApp), três garantias curtas. Visual: foto em arco + celular com a tela principal sobreposto + 1 ou 2 cartões flutuantes com dados que BATEM com a captura (mesmo nome, hora e valor).
3. **Dores**: 4 problemas na fala dela, cada um com a resposta do produto ("Na Agenda Beleza: …").
4. **Para quem é**: os ofícios com ícone, fotos de ambiente.
5. **Telas**: mockup interativo (abas acessíveis com setas do teclado) com "o que é" e "por que ajuda" para cada tela. Demonstrar sem explicar o porquê não convence.
6. **Como funciona**: 3 passos ligados por uma linha, sem números.
7. **Faixa escura**: frase de posicionamento + 4 fatos + botão.
8. **Comparativo**: "jeito antigo × produto", tarefa por tarefa. No celular vira lista.
9. **Preço**: o que é de graça e o que é sob medida, com preço real ou "sob medida". Nunca valor inventado.
10. **Dúvidas**: respostas honestas, inclusive sobre limites (onde ficam os dados, o que ainda não faz).
11. **Chamada final** com leque de 3 celulares.
12. **Rodapé** com contato em texto selecionável e preferência de cookies.

## Voz: a língua da profissional

| Assim não | Assim sim |
| --- | --- |
| Otimize a gestão do seu negócio | Saiba quem vem hoje sem abrir o caderninho |
| Reduza o no-show | Cliente que esquece e deixa a cadeira vazia |
| Gestão de conflitos de agenda | Duas clientes marcadas no mesmo horário |
| Dashboard de faturamento | Quanto entrou hoje |
| Solução completa e inovadora | Grátis, sem cadastro, abre no celular |

Palavras do ofício: horário, encaixe, cliente, manutenção, confirmar, caderninho, cadeira vazia, folga, studio. Trate por "você", no feminino quando for natural. Frases curtas. Nada de frase enigmática que só funciona com narração.

## Visual (padrão AF, modo "Convencer")

- Fundo porcelana `#F7F2EF`, cartões brancos sem borda e sem sombra; nude `#EFE7E2` em faixas alternadas; ameixa `#2D1B2E` para texto e faixa escura.
- **Um acento** (esmalte `#C8246A`, ou a cor do produto). Sobre o fundo escuro, use uma versão clara do acento para texto (`#F59AC0`).
- **Dourado em um lugar só** (ex.: o valor do dia no cartão flutuante), em `#8A620F` para ter contraste.
- Fontes: Fraunces (eixo SOFT 100) nos títulos + Instrument Sans no texto, com fallback do sistema.
- Proibido: degradê em botão/título/fundo, emoji como ícone, rótulo pequeno acima do título, numeração 01/02/03, palavra em itálico colorido dentro do título, vidro/blur, borda colorida grossa à esquerda.
- Ícones SVG de traço 1.8, uma família, `currentColor`, num `<symbol>` reaproveitado.
- Mockup de celular em CSS: moldura `#1B1120`, raio 44px, ilha no topo. **A imagem dentro precisa de `height:auto`**: os atributos `width`/`height` da tag viram altura fixa e a captura aparece gigante e cortada.
- Sombra só no que flutua (cartões sobre a foto, celulares, aviso de cookies).
- Entradas suaves só com JS ativo (classe `.js`), visíveis em repouso e desligadas com `prefers-reduced-motion`.

## Rastreamento

**Contrato do `dataLayer`** (todo evento leva `event_id` único; os parâmetros são zerados a cada envio para não vazar valor velho):

| Evento | Quando | Meta |
| --- | --- | --- |
| `consent_update` | ao carregar e ao escolher no aviso | PageView (com consentimento) |
| `open_app` | botão de usar o produto | StartTrial |
| `whatsapp_click` | qualquer link `wa.me` | Lead |
| `view_features` | seção de telas aparece | ViewContent |
| `section_view`, `scroll_depth`, `mockup_interaction`, `faq_open`, `cta_click` | engajamento | só GA4 |

**Consentimento (LGPD)**: Consent Mode v2 com padrão negado antes do GTM; aviso com "Aceitar" e "Agora não"; escolha guardada em `localStorage`. No GTM, um gatilho de bloqueio (`consent_ads` diferente de `granted`) segura todas as tags do Meta. O site também não chama a CAPI sem consentimento.

**GTM**: gere o container com script (veja `tracking/build_gtm.py`): Tag do Google + uma tag de evento GA4 com `{{Event}}` como nome e todos os parâmetros, Pixel base (uma vez por página) e uma tag por evento do Meta com `eventID: {{DLV - event_id}}`. IDs de GA4 e Pixel ficam em constantes para a pessoa preencher depois de importar.

**CAPI**: função `api/capi.js` na Vercel (mesma origem do site, sem CORS). Lista fechada de eventos, IP e navegador lidos do cabeçalho, `fbp`/`fbc` do cookie (ou montado do `fbclid`), `external_id` anônimo em SHA-256, `test_event_code` por variável. Token só em variável de ambiente, nunca no repositório.

## Antes de entregar

- [ ] Nenhuma rolagem lateral em 390px; nada sobreposto ao título no celular
- [ ] Cartões flutuantes batem com a captura (nome, hora, valor)
- [ ] Nenhum depoimento ou número inventado; limites do produto ditos nas Dúvidas
- [ ] `dataLayer` recebe `consent_update` ao carregar e os eventos ao clicar
- [ ] JSON do GTM: toda tag aponta para gatilho existente e toda `{{variável}}` existe
- [ ] Função CAPI testada com `fetch` simulado (aceita, recusa evento fora da lista, recusa GET)
- [ ] Imagem 1200×630 gerada e `og:image` com endereço completo depois do domínio definido
- [ ] Fotos de banco: conferir se a licença permite uso em site e em repositório público
