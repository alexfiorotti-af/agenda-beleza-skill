# Especificação funcional — Agenda Beleza

## Arquitetura do arquivo único

Um `index.html` com três blocos:

1. `<style>` — todo o CSS (tokens do design system primeiro).
2. `<body>` — header, container de views, FAB, tab bar e um único bottom-sheet
   reutilizável.
3. `<script>` — estado + render. Padrão simples e legível:

```js
const state = { view: 'agenda', period: 'hoje', anchorDate: todayISO(), ... };
function render() { /* redesenha a view ativa a partir do state + storage */ }
// toda ação do usuário: muda state/dados → save() → render()
```

Sem roteador, sem framework. `render()` monta strings de template por view.
Eventos via delegação (`document.addEventListener('click', …)` lendo `data-action`).

`<head>` obrigatório: `charset`, `viewport` (`width=device-width, initial-scale=1,
viewport-fit=cover`), `theme-color` rosa, `<title>` com o nome do negócio e um
favicon em SVG data-URI (ex.: coração/esmalte rosa).

Strings de UI no objeto `t = { hoje: 'Hoje', amanha: 'Amanhã', ... }`.

## Navegação

Tab bar com 4 abas → 4 views: **Agenda** (inicial), **Clientes**, **Serviços**,
**Ajustes**. O FAB "+" aparece nas views Agenda (novo agendamento), Clientes
(nova cliente) e Serviços (novo serviço).

## View 1 — Agenda (coração do app)

Pílulas de período: `Hoje · Amanhã · Semana · Mês`.

- **Hoje / Amanhã**: tira de dias rolável (14 dias a partir de hoje) + lista de
  cards do dia ordenada por hora. Tocar em outro dia da tira muda `anchorDate`
  (a pílula vira a data, ex. "Qui 29"). Cabeçalho da lista: "5 atendimentos ·
  R$ 380 previstos".
- **Semana**: seg–dom da semana do `anchorDate`, agrupada por dia com subtítulo
  ("Segunda, 27/10 — 3 horários"); setas ‹ › trocam de semana. Dias sem nada:
  linha discreta "Livre 🌿".
- **Mês**: calendário em grade com pontinhos; setas ‹ › trocam o mês; tocar num
  dia mostra a lista daquele dia abaixo da grade. Botão "Hoje" volta à data atual.

Card de agendamento (ver design system) com menu "⋮": Confirmar · WhatsApp ·
Concluir · Editar · Cancelar. Cancelar pede confirmação.

## Fluxo: novo agendamento (bottom-sheet)

Campos, nesta ordem:
1. **Cliente** — busca com autocomplete nas clientes salvas + opção "+ Nova
   cliente: '{texto}'" que cria na hora (nome e, opcionalmente, telefone).
2. **Serviço** — chips com nome e preço; selecionar preenche duração e preço
   (editáveis depois).
3. **Data** — `input type="date"` com valor padrão = dia que estava aberto.
4. **Horário** — grade de chips de horários gerados de `openTime` a `closeTime`
   em passos de `slotMinutes`; chips já ocupados aparecem desabilitados com a
   inicial da cliente. Também aceita digitar hora livre.
5. **Observações** — textarea opcional.
6. Botão primário "Salvar horário ✨".

Validação: cliente + serviço + data + hora obrigatórios; checagem de conflito
(ver data-model) com "Salvar mesmo assim". Ao salvar: toast + volta para a lista
do dia salvo.

Editar reutiliza o mesmo sheet preenchido.

## View 2 — Clientes

Busca no topo + lista alfabética (avatar = iniciais sobre fundo `--rosa-claro`,
nome, telefone). Tocar abre o sheet da cliente: dados, observações, histórico
(últimos e próximos horários dela) e atalhos "WhatsApp" e "Agendar horário"
(abre o sheet de agendamento com a cliente pré-selecionada). Editar/excluir
(excluir pede confirmação e NÃO apaga agendamentos passados — mantém `clientName`).

## View 3 — Serviços

Lista de cards: pontinho de cor, nome, duração, preço em `--dourado`, toggle
ativo/inativo. FAB cria; tocar edita (nome, preço, duração, cor entre 6 opções).
Serviço inativo some do formulário de agendamento mas mantém o histórico.

## View 4 — Ajustes

- Nome do negócio, nome da profissional, ramo (emoji da saudação), WhatsApp.
- Dias de atendimento (chips D S T Q Q S S), horário de abertura/fechamento,
  tamanho do slot (15/30/60).
- **Backup**: "Exportar dados" (baixa JSON com tudo) e "Importar dados" (file
  input; valida e substitui com confirmação). Texto explicando que os dados
  vivem só neste navegador.
- "Limpar dados de exemplo" (remove tudo com `demo: true`) — some depois de usado.
- Rodapé: versão do app + "Feito com 💖 — open source".

## Comportamentos globais

- Primeiro uso (`ab.settings` vazio): sheet de boas-vindas pedindo nome do
  negócio, seu nome e ramo (3 campos, 30 segundos) → semeia serviços do ramo +
  dados demo → cai na Agenda/Hoje.
- Dados persistem entre sessões; recarregar nunca perde nada.
- Toast para toda ação de sucesso; mensagens de erro no próprio sheet.
- O app inteiro deve caber confortavelmente em ~60–90 KB de HTML.

## Checklist de aceite (verificar antes de entregar)

- [ ] Abrir pela primeira vez → boas-vindas → Agenda/Hoje com dados demo
- [ ] Criar agendamento para hoje → aparece na lista na posição certa por hora
- [ ] Criar no mesmo horário → aviso de conflito com "salvar mesmo assim"
- [ ] Amanhã, Semana e Mês mostram os mesmos dados coerentes (contagens batem)
- [ ] Concluir/cancelar muda a cor da borda do card e o resumo do dia
- [ ] Botão WhatsApp abre wa.me com a mensagem pronta
- [ ] Recarregar a página mantém tudo
- [ ] Testado mentalmente em 390 px de largura sem scroll horizontal
