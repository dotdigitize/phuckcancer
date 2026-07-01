# Setup

Backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m pytest
uvicorn app.main:app --reload
```

Frontend:

```bash
npm install
npm run build
npm run dev
```

Optional MariaDB:

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

Optional MAMMAL:

```bash
pip install biomed-multi-alignment[examples]
```

or:

```bash
git clone https://github.com/BiomedSciAI/biomed-multi-alignment.git
pip install -e ./biomed-multi-alignment[examples]
```

Documentation-only loading example:

```python
from mammal.model import Mammal

model = Mammal.from_pretrained("ibm/biomed.omics.bl.sm.ma-ted-458m")
model.eval()
```

If that import path changes upstream, confirm the latest official usage from the MAMMAL repository.
