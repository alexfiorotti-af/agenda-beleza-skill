# Modelo de dados e regras de agenda — Agenda Beleza

## Chaves de armazenamento (localStorage)

Prefixo único para não colidir com outros apps no mesmo domínio:

| Chave | Conteúdo |
|---|---|
| `ab.settings` | objeto de configurações |
| `ab.services` | array de serviços |
| `ab.clients`  | array de clientes |
| `ab.appointments` | array de agendamentos |
| `ab.version`  | inteiro do schema (começa em 1) para migrações futuras |

Encapsule leitura/escrita em `load(key, fallback)` / `save(key, value)` com
`try/catch` (modo privado pode lançar). Após qualquer mutação: `save` + re-render.

## Schemas

```js
// ab.settings
{
  businessName: "Studio Beleza",
  ownerName: "Ana",
  branch: "misto",            // "unhas" | "cabelo" | "estetica" | "misto"
  phone: "",                  // WhatsApp da profissional, só dígitos com DDI: "5527996..."
  workDays: [1,2,3,4,5,6],    // 0=dom … 6=sáb
  openTime: "08:00",
  closeTime: "19:00",
  slotMinutes: 30,
  currency: "BRL",
  locale: "pt-BR"
}

// ab.services[]
{ id, name, price, durationMin, color, active: true }
// color: uma de 6 cores fixas da paleta para o pontinho do serviço

// ab.clients[]
{ id, name, phone, notes, createdAt }
// phone: só dígitos; exibir formatado. notes: "alérgica a acrílico", etc.

// ab.appointments[]
{
  id,                 // crypto.randomUUID() com fallback Date.now()+random
  clientId,           // ou null com clientName avulso
  clientName,         // denormalizado p/ exibição rápida
  serviceId,
  serviceName,        // denormalizado
  price,              // copiado do serviço no momento (preço pode mudar depois)
  date: "2026-10-26", // ISO local, NUNCA Date serializado nem UTC
  start: "14:00",
  durationMin: 60,
  status: "pendente", // "pendente" | "confirmado" | "concluido" | "cancelado"
  notes: "",
  demo: false,        // true nos dados de exemplo
  createdAt: Date.now()
}
```

## Regras de data (fonte nº 1 de bugs — siga à risca)

- `todayISO()` deve usar a data **local**: `new Date()` + montar `YYYY-MM-DD`
  manualmente (ou `toLocaleDateString('sv-SE')`). **Nunca** `toISOString().slice(0,10)`
  — vira ontem/amanhã conforme o fuso.
- Comparações de dia são comparações de string ISO (`a.date === todayISO()`).
- Minutos desde meia-noite: `toMin("14:30") → 870` para toda aritmética de horário.
- Fim do agendamento = `start + durationMin`.

## Conflito de horário

Ao salvar (criar ou editar), rejeitar se existir outro agendamento **não
cancelado** no mesmo `date` com sobreposição:

```js
const overlap = (aStart, aEnd, bStart, bEnd) => aStart < bEnd && bStart < aEnd;
```

Mensagem: "Esse horário bate com o atendimento da(o) {cliente} às {hora}." com
opção "Salvar mesmo assim" (encaixe é prática comum no nicho — avisar, não proibir).

## Consultas por período

- **Hoje / Amanhã / dia escolhido**: filtrar por `date`, ordenar por `start`.
- **Semana**: segunda a domingo da semana que contém a data âncora; agrupar por dia,
  mostrar dias vazios com estado vazio curto.
- **Mês**: contagem por dia para os pontinhos do calendário; tocar num dia abre a
  lista daquele dia.
- Resumo do header: soma de `price` dos agendamentos do dia com status ≠ cancelado.

## Status — transições

pendente → confirmado → concluído; qualquer um → cancelado (com confirmação).
Concluído e cancelado não voltam (menos cliques errados). "Concluir" é o que
alimenta qualquer relatório financeiro futuro.

## Mensagem de WhatsApp

Ação "WhatsApp" do agendamento abre:

```
https://wa.me/{client.phone}?text={encodeURIComponent(msg)}
```

```
Oi, {primeiroNome}! 💖 Confirmando seu horário de {serviço} {diaFormatado} às {hora}
aqui no {businessName}. Qualquer coisa me avisa. Até lá! ✨
```

`diaFormatado`: "hoje", "amanhã" ou "sexta, 30/10" via `Intl.DateTimeFormat(locale)`.
Se a cliente não tiver telefone, abrir `wa.me` sem número (usuária escolhe o contato).

## Seeds de serviços por ramo

- **unhas**: Esmaltação em gel (R$ 70 · 60min), Alongamento fibra (R$ 150 · 150min),
  Manutenção (R$ 90 · 90min), Pé e mão tradicional (R$ 55 · 75min), Spa dos pés (R$ 65 · 60min)
- **cabelo**: Corte feminino (R$ 80 · 60min), Escova (R$ 60 · 45min),
  Coloração (R$ 180 · 120min), Hidratação (R$ 90 · 60min), Progressiva (R$ 250 · 150min)
- **estetica**: Design de sobrancelha (R$ 45 · 30min), Extensão de cílios (R$ 160 · 120min),
  Limpeza de pele (R$ 120 · 60min), Depilação buço (R$ 20 · 15min)
- **misto**: 2–3 itens de cada lista acima.

Semeie também 5 clientes fictícios (nomes femininos brasileiros comuns, telefones
claramente falsos tipo `5500999990001`) e 6–10 agendamentos `demo: true`
espalhados entre hoje, amanhã e os próximos 5 dias, com status variados.
