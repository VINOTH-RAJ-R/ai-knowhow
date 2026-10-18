# Template: voice: speech, transcription, real-time (audio.speech)

Claude models don't generate or transcribe audio natively. In this registry, audio tasks route to OpenAI's audio models. Claude can still write the script.

## Fill these slots
| Slot | Why it matters | Default if missing |
|---|---|---|
| MODE | text-to-speech / transcription / live voice agent | (required) |
| TEXT or AUDIO | Script to speak, or audio file to transcribe | (required) |
| VOICE | Voice, accent, pace, emotion | Warm, neutral accent, medium pace |
| LANGUAGE | Language(s) | Detect |
| OUTPUT | mp3/wav, transcript with timestamps, speaker labels | mp3 / plain transcript |

## TTS instruction skeleton
```
VOICE: <persona: e.g. "calm customer-support agent">
TONE & PACE: <...>
PRONUNCIATION: <names, acronyms, numbers spelled how>
SCRIPT: <exact text>
```
OpenAI's steerable TTS models accept a separate `instructions` field for VOICE/TONE. Keep the script itself clean.

## Transcription skeleton
```
Language: <...>. Domain vocabulary: <product names, jargon> (pass as a prompt to improve accuracy).
Output: <text | timestamps | speaker labels>
```

## Real-time voice agent
System prompt sections: Role & goal → Personality & tone → Conversation flow (greeting, steps, closing) → Rules (what never to say, when to hand off to a human) → Pronunciations → Example phrases.

## Token savers
- Write and polish the script with a cheap text model first, then do one TTS pass.
- Transcribe with the smaller transcription model unless accuracy on hard audio is critical.
