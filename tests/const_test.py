# Biden"s state of the union document
PDFFILE = "data/Following is a transcript of President Biden.pdf"
TXTFILE = "working/Following is a transcript of President Biden.txt"
RAGPROMPT = "How many jobs Joe Biden wants to create ?"
CHUNKFILE = "working/biden_chunks.json"
CHKEMBFILE2 = "working/biden_emb_chunks2.json"
CHKEMBFILE = "working/biden_emb_chunks.json"
PRTEMBFILE = "working/biden_emb_prompt.json"
NEARESTFILE = "working/biden_nearest.json"

CFG_OLLAMA = "working/cfg/ollama_cfg.json"
CFG_HF = "working/cfg/huggingface.json"
CFG_AWSCLAUDE = "working/cfg/awsclaude.json"
CFG_AWSMISTRAL = "working/cfg/awsmistral.json"
CFG_AWSTITAN = "working/cfg/awstitan.json"
CFG_SCHUNK = "working/cfg/schunk.json"
CFG_CCHUNK = "working/cfg/cchunk.json"
CFG_PDFLM = "working/cfg/pdfparselm.json"
CFG_PDFPY = "working/cfg/pdfparsepy.json"
CFG_HTML = "working/cfg/htmlparse.json"
CFG_EMBDS_ST = "working/cfg/embdsst.json"
CFG_FAISS = "working/cfg/faiss_index.json"
CFG_FAISS_MEM = "working/cfg/faiss_mem.json"
CFG_CHROMADB = "working/cfg/chromadb.json"

# FAISS
VSTORELOC = "vstore"
VSTORENAME = "biden"

DOCTEXT = "Transcript of President Biden’s State of the Union address in 2023. \
Mr. Speaker. Madam Vice President. Our First Lady and Second Gentleman. \
Members of Congress and the Cabinet. Leaders of our military. \
Mr. Chief Justice, Associate Justices, and retired Justices of the Supreme Court. \
And you, my fellow Americans. \
I start tonight by congratulating the members of the 118th Congress and the new Speaker of the \
House, Kevin McCarthy. \
Mr. Speaker, I look forward to working together. \
I also want to congratulate the new leader of the House Democrats and the first Black House \
Minority Leader in history, Hakeem Jeffries. "

SIMPLEPROMPT = "Do you know pytorch ?"

SENT_1 = "My cat is totally red"
SENT_2 = "I think my cat is magenta"

SENT_1_1 = "A man walks into a bar and buys a drink"
SENT_1_2 = "A bloke swigs alcohol at a pub"