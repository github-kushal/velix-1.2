# API Documentation

## ask_ollama(query)

Purpose:
Generate AI response using local LLM.

Returns:

- response
- intent
- parameters
- memory

---

## memory_detector(query)

Purpose:

Detect long-term memory candidates.

Returns:

- store
- type
- data

---

## parse_json(raw_output)

Purpose:

Parse and validate LLM output.

Returns:

Validated JSON object.

---

## execute(intent, parameters)

Purpose:

Execute detected skill.

---

## update_memory(data)

Purpose:

Update long-term memory storage.

---

## retrieve_memory(query)

Purpose:

Retrieve relevant memory.