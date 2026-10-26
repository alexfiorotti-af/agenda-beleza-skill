# 💅 Agenda Beleza — Agent Skill

Skill open source (formato **Agent Skills** — `SKILL.md` + referências em Markdown)
que ensina qualquer IA a gerar um **aplicativo de agenda completo, em um único
arquivo HTML**, para mulheres empreendedoras da beleza: nail designers, manicures,
pedicures, cabeleireiras, salões, sobrancelhas, cílios e estética — de micro a
média empresa.

## O que o app gerado faz

- 📅 **Agenda por período**: Hoje · Amanhã · Semana · Mês, com tira de dias e
  calendário mensal
- ➕ Agendamento em segundos, com detecção de conflito de horário (e opção de encaixe)
- 👩 Cadastro de clientes com histórico e observações
- 💰 Catálogo de serviços com preço, duração e resumo de faturamento do dia
- 💬 Confirmação de horário por **WhatsApp** com mensagem pronta
- 📲 Mobile-first, visual vibrante do nicho (magenta, lilás, dourado), funciona
  offline e salva tudo no navegador (localStorage) — **zero backend, zero custo**

## ✨ Demo ao vivo

Veja o app que esta skill gera, funcionando no navegador (melhor no celular):

**👉 [alexfiorotti-af.github.io/agenda-beleza-skill/demo/agenda-beleza.html](https://alexfiorotti-af.github.io/agenda-beleza-skill/demo/agenda-beleza.html)**

Os dados são exemplos (`demo: true`) e ficam só no seu navegador — remova-os em
Ajustes → "Limpar dados de exemplo". O código está em [`demo/agenda-beleza.html`](demo/agenda-beleza.html).

## Como usar

### No Claude (Code / claude.ai / plugin)
Copie a pasta para o diretório de skills do seu ambiente (ex.:
`~/.claude/skills/agenda-beleza/`) e peça:

> "Crie o app de agenda para a manicure Ana, ramo unhas."

### Em qualquer outra IA (ChatGPT, Gemini, etc.)
O formato é Markdown puro. Cole o conteúdo de `SKILL.md` + os três arquivos de
`references/` como instrução/contexto e faça o mesmo pedido. Nada aqui depende de
recurso proprietário.

## Estrutura

```
agenda-beleza/
├── SKILL.md                      # instruções principais + processo
└── references/
    ├── design-system.md          # paleta, tipografia, componentes
    ├── data-model.md             # schema, localStorage, regras de conflito, seeds
    └── app-spec.md               # telas, fluxos, checklist de aceite
```

## Personalização

Na hora de pedir o app, informe: nome do negócio, ramo (unhas / cabelo / estética
/ misto), serviços com preços e horário de funcionamento. Sem isso, a skill usa
padrões sensatos e dados de exemplo removíveis.

## Roadmap / contribuições

PRs são bem-vindos. Ideias abertas: link público para a cliente se agendar
sozinha, relatório financeiro mensal, lembretes automáticos, PWA com manifest,
tradução (as strings já são centralizadas num objeto `t`).

## Licença

[MIT](LICENSE) — use, adapte e revenda à vontade.

---

Criado por **Alex Fiorotti** · AF Tecnologia e Marketing / AF USA LLC
📧 alexfiorotti@gmail.com · 📱 WhatsApp +55 27 99601-5367
