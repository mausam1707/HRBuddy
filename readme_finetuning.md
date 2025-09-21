# Fine-Tuning Ollama for Teams Bot

This guide explains how to **teach Ollama LLM your documents permanently** so the bot can respond without loading files every time.

---

## **Step 1: Prepare Your Documents**

- Place all `.txt`, `.pdf`, `.docx` files in a single folder, for example:

D:\Agent\documents

yaml
Copy code

- Optional: Clean text for better training (remove headers, footers, or irrelevant content).

---

## **Step 2: Create an Ollama Dataset**

1. Open a terminal in your project folder.
2. Run the following command:

```bash
ollama dataset create mydataset --files "D:\Agent\documents"
mydataset is the name of your dataset.

Ollama will read all files and prepare them for fine-tuning.

Step 3: Fine-Tune a Custom Model
Run:

bash
Copy code
ollama finetune mymodel:latest --dataset mydataset
mymodel = name of your new custom model.

:latest = base model to fine-tune (e.g., gemma:2b for low-memory systems).

Note: Fine-tuning may take several minutes depending on document size and model.

Step 4: Update Bot Configuration
Edit config.py:

python
Copy code
DEFAULT_MODEL = "mymodel"  # Use your fine-tuned model
This tells your bot to use the fine-tuned model instead of the base model.

Step 5: Simplify Bot Runtime
After fine-tuning:

You no longer need to load documents every time.

Update teams_bot.py:

python
Copy code
async def on_message_activity(self, turn_context: TurnContext):
    user_message = turn_context.activity.text
    response = await self.ollama_llm.query(user_message)
    await turn_context.send_activity(f"**Response:**\n{response}")
Step 6: Test Your Bot
Start Ollama server:

bash
Copy code
ollama serve
Run your bot:

bash
Copy code
python app.py
Send a message — the bot should respond quickly using learned knowledge from your documents.

Notes
Fine-tuned model remembers documents permanently; you can delete the original files.

If documents are updated, you must re-fine-tune the model.

Ensure your system has enough RAM for large datasets or models