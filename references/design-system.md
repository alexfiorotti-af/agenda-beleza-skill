# Design System — Agenda Beleza

Identidade visual do nicho beleza feminina: vibrante, acolhedora, premium sem ser
fria. Pense "studio de nail design com néon rosa e detalhes dourados", não
"software corporativo".

## Tokens de cor (definir em `:root`)

```css
:root {
  /* Marca */
  --rosa:        #E91E8C;  /* primária — magenta vibrante */
  --rosa-escuro: #C2185B;  /* pressed / ênfase */
  --rosa-claro:  #FCE4F1;  /* fundos de chip, hover */
  --lilas:       #9C27B0;  /* secundária — gradientes e acentos */
  --dourado:     #D4A72C;  /* destaque premium: preços, estrelas, badges */
  --pessego:     #FF8A65;  /* acento quente: avisos suaves, "amanhã" */

  /* Neutros quentes (nunca cinza puro frio) */
  --ink:      #2D1B2E;     /* texto principal — roxo quase preto */
  --ink-soft: #7A6B7D;     /* texto secundário */
  --fundo:    #FFF7FB;     /* fundo do app — branco rosado */
  --card:     #FFFFFF;
  --linha:    #F3DCEA;     /* bordas e divisores */

  /* Semânticas */
  --ok:     #2E9E6B;       /* confirmado / concluído */
  --alerta: #E6A23C;       /* pendente */
  --erro:   #D64550;       /* cancelado / conflito */

  /* Gradiente de marca (header, botão primário, dia selecionado) */
  --grad: linear-gradient(135deg, #E91E8C 0%, #9C27B0 100%);

  --raio: 16px;            /* raio padrão de cards */
  --sombra: 0 4px 16px rgba(233, 30, 140, .12);
}
```

Regras de uso:
- Gradiente `--grad` só em: header, botão primário (FAB "+"), dia ativo do
  calendário e tela de splash/empty state. Em excesso vira poluição.
- Texto sobre o gradiente: sempre `#FFFFFF`, peso ≥ 600.
- `--dourado` é raro e precioso: preços, totais do dia, badge "VIP".
- Status dos agendamentos: borda esquerda de 4px no card com a cor semântica
  (`--alerta` pendente, `--ok` confirmado, `--erro` cancelado, `--ink-soft` concluído).

## Tipografia

- Título/brand: `'Poppins', 'Segoe UI', system-ui, sans-serif` — pesos 600/700.
- Corpo: a mesma pilha, peso 400/500. Uma família só mantém o arquivo leve.
- Carregar do Google Fonts com `display=swap`; o app deve funcionar sem a fonte.
- Escala: brand 22px · título de seção 17px/700 · corpo 15px · meta 13px ·
  preço 15px/700 na cor `--dourado`.
- Nunca usar caixa alta em textos longos; só em labels pequenos (letter-spacing .04em).

## Componentes

**Header** — gradiente `--grad`, cantos inferiores arredondados (24px), contém:
nome do negócio, saudação ("Oi, Ana 💅" — emoji do ramo: 💅 unhas, ✂️ cabelo,
✨ estética/misto) e o resumo do dia ("Hoje: 5 atendimentos · R$ 380").

**Seletor de período** — pílulas horizontais roláveis logo abaixo do header:
`Hoje · Amanhã · Semana · Mês`. Ativa = fundo `--grad`, texto branco; inativa =
fundo `--card`, borda `--linha`.

**Tira de dias (strip)** — nas visões Hoje/Amanhã/Semana, uma fileira horizontal
de 7+ dias rolável (letra do dia + número); dia selecionado é um círculo com
`--grad`; dias com agendamento ganham um pontinho `--rosa` embaixo.

**Card de agendamento** — `--card`, raio `--raio`, sombra `--sombra`, borda
esquerda de status. Linha 1: hora (15px/700) + nome da cliente. Linha 2: serviço
+ duração. Direita: preço em `--dourado` e menu "⋮" (confirmar · WhatsApp ·
concluir · editar · cancelar).

**FAB** — botão "+" fixo (bottom: 84px; right: 20px), 56px, circular, `--grad`,
sombra forte. Abre o formulário de novo agendamento como bottom-sheet.

**Bottom-sheet / modal** — sobe de baixo, cantos superiores 24px, alça cinza,
fundo escurecido `rgba(45,27,46,.5)`. Todos os formulários vivem aqui.

**Tab bar** — fixa embaixo, 4 abas: Agenda · Clientes · Serviços · Ajustes.
Ícones inline em SVG (traço 1.8), ativa em `--rosa` com label, inativas em
`--ink-soft`.

**Empty state** — ilustração simples em SVG inline (ex.: esmalte/tesoura/estrela
nas cores da marca), frase gentil ("Nenhum horário por aqui ainda 🌸") e botão
de ação. Nunca uma tela branca muda.

**Calendário mensal** — grade 7×n, células quadradas, número do dia + pontinhos
de agendamento (máx. 3; depois "+2"). Dia atual com anel `--rosa`; selecionado
preenchido com `--grad`.

## Microinterações

- Transições de 150–200ms (`ease-out`) em cards, pílulas e sheet.
- Toque em card: leve `scale(.98)`.
- Toast de confirmação no topo ("Agendamento salvo ✨"), some em 2,5s.
- `prefers-reduced-motion`: desligar animações.
