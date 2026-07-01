# Setup

MAMMAL is required for biomedical cancer interpretation. PhuckCancer can use a local installed MAMMAL package/model or a configured MAMMAL API provider. If neither provider is available, interpretation endpoints fail closed with a clear unavailable error.

MariaDB/MySQL is the database for demo persistence. SQLite is not used. Ollama is optional for local LLM explanations. The cBioPortal connector is optional for external cancer genomics import.

Backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
uvicorn app.main:app --host 0.0.0.0 --port 8717 --reload
```

Frontend:

```bash
npm install
npm run build
npm run dev
```

The frontend is available at:

```text
http://SERVER-IP:5179
```

MAMMAL local provider:

```bash
pip install biomed-multi-alignment[examples]
```

or:

```bash
git clone https://github.com/BiomedSciAI/biomed-multi-alignment.git
pip install -e ./biomed-multi-alignment[examples]
```

MAMMAL API provider:

```env
MAMMAL_REQUIRED=true
MAMMAL_PROVIDER=api
MAMMAL_API_BASE_URL=http://localhost:9000
MAMMAL_API_TOKEN=
MAMMAL_API_INTERPRET_PATH=/v1/interpret
MAMMAL_API_HEALTH_PATH=/health
```

MariaDB:

```bash
sudo apt install mariadb-server mariadb-client
mysql -u root -p
```

```sql
CREATE DATABASE phuckcancer_demo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'phuckcancer_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON phuckcancer_demo.* TO 'phuckcancer_user'@'localhost';
FLUSH PRIVILEGES;
```

```bash
mysql -u phuckcancer_user -p phuckcancer_demo < db/schema.sql
mysql -u phuckcancer_user -p phuckcancer_demo < db/seed_cancer_demo.sql
```

Optional Ollama:

```bash
ollama pull gemma4:e4b
```

Documentation-only MAMMAL loading example:

```python
from mammal.model import Mammal

model = Mammal.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m")
model.eval()
```

If that import path changes upstream, confirm the latest official usage from the MAMMAL repository.
