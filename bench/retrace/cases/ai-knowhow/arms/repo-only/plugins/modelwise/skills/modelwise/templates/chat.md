# Template: questions, explanations, brainstorming (text.chat)

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| QUESTION | The actual question | (required) |
| WHO | Your level and context ("beginner", "senior Go dev", "for my 10-year-old") | General audience |
| PURPOSE | Why you're asking: decision, learning, writing something | Learning |
| FORMAT | Short answer, steps, table, pros/cons, N ideas | Short answer, then details |

## Universal skeleton
```
QUESTION: <...>
ABOUT ME: <level, context>
I NEED THIS TO: <purpose>
FORMAT: <...>
```

## Rendered for Claude
```xml
<about_me>WHO. PURPOSE.</about_me>
<question>QUESTION</question>
<output_format>FORMAT. Lead with the direct answer.</output_format>
```

## Rendered for OpenAI
```markdown
QUESTION

Context: WHO. Purpose: PURPOSE.
Format: FORMAT. Lead with the direct answer.
```

## Example (illustrative: shows the structure, never copy its specifics)
**Basic:** "what is kubernetes"
**Structured:** "What is Kubernetes? I'm a frontend developer who has used Docker locally but never deployed anything. I'm deciding whether our 3-person team needs it. Give me a 3-sentence answer, then a short 'when you need it / when you don't' list."

## Token savers
- Fastest tier, lowest effort. Raise only for genuinely hard questions.
- Ask a new question in a **new chat**. Long chats resend the whole history every message.
