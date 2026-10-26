---
name: agenda-beleza
description: >
  Cria o "Agenda Beleza" — um aplicativo web de agenda e gestão de clientes para
  mulheres empreendedoras da beleza (nail designers, manicures, pedicures,
  cabeleireiras, salões, sobrancelhas, cílios, estética), de micro a média empresa.
  Gera um ÚNICO arquivo HTML autossuficiente, mobile-first, com visual vibrante do
  nicho (rosa/magenta, dourado, lilás), agenda por dia / amanhã / semana / mês,
  cadastro de clientes e serviços, confirmação por WhatsApp e dados salvos no
  navegador (localStorage). Usar quando pedirem: app de agendamento para salão,
  agenda de manicure, sistema para nail designer, controle de horários de
  profissional da beleza, ou qualquer variação disso.
license: MIT
---

# Agenda Beleza — Skill de criação do app

## O que esta skill produz

Um aplicativo completo em **um único arquivo `.html`** (zero dependências de build,
zero backend), que a profissional abre no celular, adiciona à tela inicial e usa
como app. Tudo funciona offline depois do primeiro carregamento. Os dados ficam no
`localStorage` do navegador dela.

Por que um HTML único: o público-alvo não instala nada, não paga servidor e vive no
celular. Um arquivo que ela recebe pelo WhatsApp e abre no Chrome resolve 100% do
caso de uso inicial e pode ser hospedado grátis (Vercel/Netlify/GitHub Pages) sem
mudar uma linha.

## Processo (siga nesta ordem)

1. **Personalização mínima** — se o usuário não informou, pergunte em UMA mensagem
   só (ou use os padrões entre parênteses e siga em frente se ele pediu para não
   interromper):
   - Nome do negócio/profissional (padrão: "Studio Beleza")
   - Ramo principal: unhas / cabelo / estética / misto (padrão: misto)
   - Serviços iniciais com preço e duração (padrão: lista do ramo em
     `references/data-model.md`)
   - Horário de funcionamento (padrão: seg–sáb, 08:00–19:00, slots de 30 min)
2. **Leia `references/design-system.md`** e aplique os tokens de cor, tipografia e
   componentes exatamente como descritos. Não invente outra paleta.
3. **Leia `references/data-model.md`** e implemente o schema de dados e as regras
   de agenda exatamente como descritos (chaves de storage, formato de datas,
   detecção de conflito).
4. **Leia `references/app-spec.md`** e construa todas as telas e fluxos listados,
   na arquitetura de "views" descrita lá.
5. Gere o arquivo como `agenda-beleza.html` (ou publique como artifact, se o
   ambiente tiver esse recurso). Semeie 6–10 agendamentos de exemplo distribuídos
   entre hoje, amanhã e a semana, marcados com `demo: true`, e ofereça o botão
   "Limpar exemplos" em Ajustes.
6. **Teste mental obrigatório antes de entregar**: criar agendamento → aparece em
   Hoje; conflito de horário → bloqueado com aviso; navegar semana/mês → contagens
   corretas; recarregar a página → dados persistem.

## Regras inegociáveis

- **Mobile-first real**: layout base em 360–430 px de largura; desktop é o caso
  secundário (max-width 520 px centralizado). Botões com área de toque ≥ 44 px.
- **Sem frameworks**: HTML + CSS + JS vanilla. Nenhum CDN obrigatório; se usar
  fonte do Google Fonts, o app deve continuar legível sem ela (fallback do sistema).
- **Datas sempre em ISO** (`YYYY-MM-DD` e `HH:MM`) no armazenamento; exibição
  sempre em pt-BR por padrão (`Intl.DateTimeFormat` com o locale do app). Nunca
  armazene datas formatadas.
- **Tudo em uma língua só**: strings da interface centralizadas num objeto `t` no
  topo do JS, para a tradução ser a troca de um objeto (o repositório é aberto e
  será adaptado para outros países).
- **WhatsApp é o canal**: todo agendamento tem ação "Confirmar no WhatsApp" que
  abre `https://wa.me/<fone>?text=<mensagem pré-pronta>`.
- **Nada de contador de passos/slides** em elementos visuais e nenhuma dependência
  de login: o app abre direto na tela Hoje.
- **Acessibilidade mínima**: contraste AA nos textos sobre os gradientes, `aria-label`
  nos botões de ícone, inputs com `label` reais.

## Estrutura dos arquivos de referência

| Arquivo | Quando ler |
|---|---|
| `references/design-system.md` | Antes de escrever qualquer CSS — paleta, tipografia, componentes, tom visual |
| `references/data-model.md` | Antes de escrever o JS — schema, chaves de storage, regras de conflito, seeds por ramo |
| `references/app-spec.md` | Antes de montar as telas — views, navegação, fluxos, textos padrão |

## Extensões (só se o usuário pedir)

- **Exportar/importar backup** em JSON (recomende proativamente ao entregar: dados
  em localStorage somem se o navegador for limpo).
- **Link público de agendamento** para a cliente marcar sozinha (exige backend ou
  serviço externo — explique o trade-off antes).
- **Relatório financeiro** (faturamento por período somando preço dos serviços
  concluídos) — já há campos para isso no schema.
- Tradução: trocar o objeto `t` e o locale.
