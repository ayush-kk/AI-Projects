# NexusAI - Enhancement Roadmap

This document outlines a comprehensive roadmap for enhancing NexusAI from a feature-complete chatbot to a production-ready, enterprise-grade AI platform.

## Enhancement Phases

```mermaid
graph LR
    A[Phase 1: Core Improvements] --> B[Phase 2: Advanced Features]
    B --> C[Phase 3: Scale & Polish]
    C --> D[Phase 4: Enterprise Ready]
    
    style A fill:#4CAF50
    style B fill:#2196F3
    style C fill:#FF9800
    style D fill:#9C27B0
```

---

## Phase 1: Core Improvements

### 1.1 Dark Mode Toggle

**Objective:** Add a user-friendly dark mode toggle with persistent preference storage.

**Files to Modify/Create:**
- `frontend/src/components/ThemeToggle.jsx` (new)
- `frontend/src/App.jsx`
- `frontend/src/styles/themes.css` (new)
- `backend/models.py` (add theme preference to User model)

**Implementation Steps:**

1. **Create Theme Context**
   ```bash
   # frontend/src/contexts/ThemeContext.jsx
   ```
   - Implement React Context for theme state
   - Add localStorage persistence
   - Provide theme toggle function

2. **Design Dark Mode Styles**
   ```css
   /* Create CSS variables for light/dark themes */
   :root[data-theme="light"] { --bg: #ffffff; --text: #000000; }
   :root[data-theme="dark"] { --bg: #1a1a1a; --text: #ffffff; }
   ```

3. **Create Toggle Component**
   - Add sun/moon icon button
   - Animate transition between themes
   - Position in header/sidebar

4. **Update Backend User Preferences**
   ```python
   # Add to User model
   theme_preference = Column(String, default="light")
   ```

5. **Persist to Database**
   - Create `/api/user/preferences` endpoint
   - Save theme choice on toggle
   - Load on user login

**Verification:**
- [ ] Toggle switches between light/dark smoothly
- [ ] Preference persists after page reload
- [ ] All components render correctly in both themes
- [ ] Database stores user preference

---

### 1.2 RAG Pipeline with ChromaDB

**Objective:** Implement Retrieval-Augmented Generation for document-aware conversations.

**New Dependencies:**
```bash
# Backend
pip install chromadb sentence-transformers pypdf langchain
```

**Files to Create:**
- `backend/services/rag_service.py`
- `backend/services/embeddings_service.py`
- `backend/llm/rag_chain.py`
- `frontend/src/components/DocumentManager.jsx`

**Implementation Steps:**

1. **Setup ChromaDB**
   ```python
   # backend/services/rag_service.py
   import chromadb
   from chromadb.config import Settings
   
   client = chromadb.Client(Settings(
       chroma_db_impl="duckdb+parquet",
       persist_directory="./chroma_storage"
   ))
   ```

2. **Create Embedding Service**
   ```python
   from sentence_transformers import SentenceTransformer
   
   class EmbeddingService:
       def __init__(self):
           self.model = SentenceTransformer('all-MiniLM-L6-v2')
       
       def embed_text(self, text: str):
           return self.model.encode(text).tolist()
   ```

3. **Implement Document Ingestion**
   - Parse uploaded PDFs/TXT files
   - Chunk text into 512-token segments
   - Generate embeddings for each chunk
   - Store in ChromaDB with metadata

4. **Create Retrieval Endpoint**
   ```python
   @app.post("/api/rag/query")
   async def query_documents(query: str, top_k: int = 5):
       results = collection.query(
           query_embeddings=[embedding_service.embed_text(query)],
           n_results=top_k
       )
       return results
   ```

5. **Integrate with Chat Service**
   - Retrieve relevant chunks before LLM call
   - Inject context into system prompt
   - Stream response with citations

6. **Frontend Document Manager**
   - Upload documents for indexing
   - View indexed document list
   - Toggle RAG on/off per conversation

**Verification:**
- [ ] Documents successfully chunked and indexed
- [ ] Retrieval returns relevant context
- [ ] LLM responses reference uploaded documents
- [ ] Citations link back to source documents

---

### 1.3 Function Calling / Tool Use

**Objective:** Enable the LLM to call external functions (calculator, API requests, database queries).

**Files to Create:**
- `backend/tools/tool_registry.py`
- `backend/tools/calculator.py`
- `backend/tools/web_api.py`
- `backend/tools/database_query.py`
- `backend/llm/function_calling.py`

**Implementation Steps:**

1. **Define Tool Schema**
   ```python
   # backend/tools/tool_registry.py
   tools = {
       "calculator": {
           "description": "Performs mathematical calculations",
           "parameters": {
               "expression": {"type": "string", "description": "Math expression"}
           }
       },
       "weather_api": {
           "description": "Fetches current weather",
           "parameters": {
               "city": {"type": "string", "description": "City name"}
           }
       }
   }
   ```

2. **Implement Tool Functions**
   ```python
   # backend/tools/calculator.py
   def calculate(expression: str) -> float:
       return eval(expression)  # Use safe eval in production
   ```

3. **Create Function Calling Logic**
   ```python
   # Detect function calls in LLM response
   # Execute corresponding tool
   # Feed result back to LLM
   # Continue conversation
   ```

4. **Update Prompt Engineering**
   - Inject tool descriptions into system prompt
   - Train LLM to output JSON for function calls
   - Handle multi-step tool use

5. **Add Tool Execution to Chat Flow**
   - Parse LLM response for tool calls
   - Execute tools with error handling
   - Display tool results in UI

**Verification:**
- [ ] LLM correctly identifies when to use tools
- [ ] Tools execute successfully
- [ ] Results integrate into conversation flow
- [ ] Error handling prevents crashes

---

### 1.4 Conversation Starters & Templates

**Objective:** Provide pre-built conversation templates and quick-start prompts.

**Files to Create:**
- `backend/services/template_service.py`
- `frontend/src/components/TemplateGallery.jsx`
- `frontend/src/components/StarterPrompts.jsx`

**Implementation Steps:**

1. **Define Template Schema**
   ```python
   # backend/models.py
   class ConversationTemplate(Base):
       id = Column(Integer, primary_key=True)
       name = Column(String, unique=True)
       description = Column(String)
       category = Column(String)  # "coding", "writing", "analysis"
       system_prompt = Column(Text)
       starter_messages = Column(JSON)
       suggested_model = Column(String)
   ```

2. **Seed Default Templates**
   ```python
   templates = [
       {
           "name": "Code Review Assistant",
           "category": "coding",
           "system_prompt": "You are an expert code reviewer...",
           "starter_messages": ["Review this code:", "Explain this function:"],
           "suggested_model": "codellama"
       },
       {
           "name": "Creative Writing Coach",
           "category": "writing",
           "system_prompt": "You are a creative writing mentor...",
           "starter_messages": ["Help me write a story about:", "Improve this paragraph:"]
       }
   ]
   ```

3. **Create Template API**
   ```python
   @app.get("/api/templates")
   async def list_templates(category: Optional[str] = None):
       query = db.query(ConversationTemplate)
       if category:
           query = query.filter_by(category=category)
       return query.all()
   
   @app.post("/api/conversations/from-template/{template_id}")
   async def create_from_template(template_id: int):
       # Create conversation with template settings
   ```

4. **Build Template Gallery UI**
   - Grid view of template cards
   - Filter by category
   - Preview template details
   - "Start Conversation" button

5. **Add Starter Prompts to Chat Input**
   - Show suggested prompts when conversation is empty
   - Click to auto-fill input
   - Animate appearance

**Verification:**
- [ ] Templates load correctly
- [ ] Conversations initialize with template settings
- [ ] Starter prompts appear and function
- [ ] Users can create custom templates

---

## Phase 2: Advanced Features

### 2.1 Long-Term Memory

**Objective:** Store and recall user preferences, facts, and context across conversations.

**Database Changes:**
```sql
CREATE TABLE user_memory (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    memory_type VARCHAR(50),  -- 'preference', 'fact', 'instruction'
    key VARCHAR(255),
    value TEXT,
    created_at TIMESTAMP,
    last_accessed TIMESTAMP,
    access_count INTEGER DEFAULT 0
);

CREATE INDEX idx_user_memory_user ON user_memory(user_id);
CREATE INDEX idx_user_memory_type ON user_memory(memory_type);
```

**Implementation Steps:**

1. **Create Memory Service**
   ```python
   # backend/services/memory_service.py
   class MemoryService:
       def store_memory(self, user_id, key, value, memory_type):
           # Store with embedding for semantic search
       
       def recall_memory(self, user_id, query, limit=5):
           # Semantic search across memories
       
       def update_memory(self, memory_id, new_value):
           # Update existing memory
   ```

2. **Extract Facts from Conversations**
   - Use LLM to identify user preferences/facts
   - Prompt: "Extract memorable facts from this conversation"
   - Store structured data

3. **Inject Memories into Context**
   - Retrieve relevant memories before each response
   - Add to system prompt: "Remember: User prefers Python, lives in NYC..."

4. **Memory Management UI**
   - View stored memories
   - Edit/delete memories
   - Memory analytics (most used, recent)

**Verification:**
- [ ] System remembers user preferences
- [ ] Memories persist across conversations
- [ ] Relevant memories retrieved contextually
- [ ] Users can manage their memory store

---

### 2.2 Plugin System

**Objective:** Allow third-party extensions to add functionality.

**Architecture:**
```
plugins/
├── manifest.json          # Plugin metadata
├── __init__.py            # Plugin entry point
├── handlers/
│   ├── on_message.py      # Message hooks
│   ├── on_file_upload.py  # File hooks
│   └── on_conversation_start.py
├── tools/
│   └── custom_tool.py     # Custom tools
└── ui/
    └── settings.jsx       # Settings panel
```

**Implementation Steps:**

1. **Design Plugin Interface**
   ```python
   # backend/plugins/base.py
   class Plugin:
       name: str
       version: str
       
       def on_install(self):
           pass
       
       def on_message(self, message: Message) -> Optional[Message]:
           pass
       
       def register_tools(self) -> List[Tool]:
           return []
   ```

2. **Create Plugin Loader**
   ```python
   # backend/plugins/loader.py
   def load_plugins():
       plugins_dir = Path("./plugins")
       for plugin_path in plugins_dir.iterdir():
           manifest = json.load(plugin_path / "manifest.json")
           module = import_module(f"plugins.{manifest['name']}")
           plugin = module.Plugin()
           register_plugin(plugin)
   ```

3. **Add Plugin Hooks**
   - `before_message`: Modify incoming messages
   - `after_message`: Post-process responses
   - `on_file_upload`: Handle custom file types
   - `register_routes`: Add custom API endpoints

4. **Plugin Marketplace UI**
   - Browse available plugins
   - Install/uninstall
   - Configure plugin settings

5. **Example Plugins**
   - Code Executor: Run Python/JavaScript snippets
   - Wolfram Alpha: Mathematical queries
   - Spotify: Music recommendations

**Verification:**
- [ ] Plugins load successfully
- [ ] Hooks trigger at correct times
- [ ] Plugins can add tools and routes
- [ ] Uninstalling cleans up properly

---

### 2.3 AI Agents (Multi-Step Reasoning)

**Objective:** Enable the AI to plan and execute multi-step tasks autonomously.

**Implementation Steps:**

1. **Create Agent Framework**
   ```python
   # backend/agents/base_agent.py
   class Agent:
       def __init__(self, llm, tools):
           self.llm = llm
           self.tools = tools
       
       async def run(self, task: str):
           plan = await self.create_plan(task)
           for step in plan:
               result = await self.execute_step(step)
               if result.needs_replanning:
                   plan = await self.replan(task, result)
           return final_result
   ```

2. **Implement Planning**
   ```python
   async def create_plan(self, task):
       prompt = f"Break down this task into steps: {task}"
       response = await self.llm.complete(prompt)
       return parse_steps(response)
   ```

3. **Add Execution Loop**
   - Execute step
   - Observe result
   - Decide next action (continue, replan, finish)

4. **Build Common Agents**
   - Research Agent: Search web, summarize findings
   - Data Analysis Agent: Query DB, create visualizations
   - Code Generation Agent: Plan, write, test code

5. **Agent UI**
   - Show agent thought process
   - Display plan and current step
   - Allow human-in-the-loop intervention

**Verification:**
- [ ] Agent successfully completes multi-step tasks
- [ ] Replanning works when obstacles encountered
- [ ] Thought process visible to user
- [ ] Agent knows when to stop

---

### 2.4 Multi-User Collaboration

**Objective:** Allow multiple users to collaborate in shared conversations.

**Database Changes:**
```sql
CREATE TABLE conversation_participants (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    user_id INTEGER REFERENCES users(id),
    role VARCHAR(20),  -- 'owner', 'editor', 'viewer'
    joined_at TIMESTAMP,
    UNIQUE(conversation_id, user_id)
);

CREATE TABLE conversation_invites (
    id INTEGER PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    inviter_id INTEGER REFERENCES users(id),
    invitee_email VARCHAR(255),
    token VARCHAR(255) UNIQUE,
    expires_at TIMESTAMP,
    accepted_at TIMESTAMP NULL
);
```

**Implementation Steps:**

1. **Add Sharing Endpoints**
   ```python
   @app.post("/api/conversations/{id}/invite")
   async def invite_user(id: int, email: str, role: str):
       # Generate invite token
       # Send email
   
   @app.post("/api/invites/{token}/accept")
   async def accept_invite(token: str):
       # Add user to conversation
   ```

2. **Implement Real-Time Sync**
   ```python
   # Broadcast to all participants
   @socketio.on('message')
   async def on_message(data):
       message = create_message(data)
       participants = get_participants(data['conversation_id'])
       for participant in participants:
           emit('new_message', message, room=participant.user_id)
   ```

3. **Add Presence Indicators**
   - Show who's currently viewing
   - Typing indicators
   - Online/offline status

4. **Permission System**
   - Owner: Full control
   - Editor: Send messages, invite others
   - Viewer: Read-only access

5. **Collaboration UI**
   - Share button in conversation header
   - Participant list with avatars
   - Presence indicators
   - Leave conversation option

**Verification:**
- [ ] Multiple users see messages in real-time
- [ ] Permissions enforced correctly
- [ ] Presence indicators accurate
- [ ] Invites sent and accepted successfully

---

## Phase 3: Scale & Polish

### 3.1 PostgreSQL Migration

**Objective:** Migrate from SQLite to PostgreSQL for production scalability.

**Implementation Steps:**

1. **Install PostgreSQL Dependencies**
   ```bash
   pip install psycopg2-binary alembic
   ```

2. **Create Alembic Migration**
   ```bash
   alembic init migrations
   alembic revision --autogenerate -m "Initial migration"
   ```

3. **Update Database URL**
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/nexusai
   ```

4. **Create Migration Script**
   ```python
   # scripts/migrate_sqlite_to_postgres.py
   # Export SQLite data
   # Import into PostgreSQL
   ```

5. **Test Migration**
   - Verify data integrity
   - Test all queries
   - Benchmark performance

6. **Update Production Config**
   - Use connection pooling
   - Add read replicas
   - Configure backups

**Verification:**
- [ ] All data migrated successfully
- [ ] Application works with PostgreSQL
- [ ] Performance improved
- [ ] Backups configured

---

### 3.2 Docker Deployment

**Objective:** Containerize application for easy deployment.

**Files to Create:**
- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `nginx.conf`

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: nexusai
      POSTGRES_USER: nexusai
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://nexusai:${DB_PASSWORD}@postgres:5432/nexusai
      GROQ_API_KEY: ${GROQ_API_KEY}
      HUGGINGFACE_API_KEY: ${HUGGINGFACE_API_KEY}
    volumes:
      - ./backend:/app
      - uploads:/app/uploads
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"

volumes:
  postgres_data:
  uploads:
  ollama_data:
```

**Implementation Steps:**

1. **Create Backend Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Create Frontend Dockerfile**
   ```dockerfile
   FROM node:18 AS build
   WORKDIR /app
   COPY package*.json .
   RUN npm install
   COPY . .
   RUN npm run build
   
   FROM nginx:alpine
   COPY --from=build /app/dist /usr/share/nginx/html
   COPY nginx.conf /etc/nginx/nginx.conf
   ```

3. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       location / {
           root /usr/share/nginx/html;
           try_files $uri /index.html;
       }
       location /api {
           proxy_pass http://backend:8000;
       }
       location /ws {
           proxy_pass http://backend:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
       }
   }
   ```

4. **Add Health Checks**
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```

5. **Create Deploy Script**
   ```bash
   #!/bin/bash
   docker-compose down
   docker-compose build
   docker-compose up -d
   docker-compose logs -f
   ```

**Verification:**
- [ ] Containers build successfully
- [ ] Services communicate properly
- [ ] Data persists across restarts
- [ ] Logs accessible

---

### 3.3 Monitoring Dashboard

**Objective:** Real-time monitoring of system health and usage metrics.

**Implementation Steps:**

1. **Add Prometheus Metrics**
   ```bash
   pip install prometheus-client
   ```
   ```python
   from prometheus_client import Counter, Histogram, Gauge
   
   message_counter = Counter('messages_total', 'Total messages sent')
   response_time = Histogram('response_time_seconds', 'LLM response time')
   active_users = Gauge('active_users', 'Currently active users')
   ```

2. **Setup Grafana Dashboard**
   ```yaml
   # docker-compose.yml
   prometheus:
     image: prom/prometheus
     volumes:
       - ./prometheus.yml:/etc/prometheus/prometheus.yml
   
   grafana:
     image: grafana/grafana
     ports:
       - "3000:3000"
   ```

3. **Track Key Metrics**
   - Messages per minute
   - Average response time
   - Error rate
   - Active users
   - Model usage distribution
   - API quota consumption

4. **Create Alerts**
   - High error rate
   - Slow responses (> 10s)
   - Database connection issues
   - Disk space low

5. **Build Admin Panel**
   - User statistics
   - System health overview
   - Cost analytics
   - Usage trends

**Verification:**
- [ ] Metrics collected accurately
- [ ] Dashboard displays real-time data
- [ ] Alerts trigger correctly
- [ ] Admin can view all metrics

---

### 3.4 Progressive Web App (PWA)

**Objective:** Make the app installable and work offline.

**Implementation Steps:**

1. **Create Service Worker**
   ```javascript
   // frontend/public/sw.js
   self.addEventListener('install', (e) => {
       e.waitUntil(
           caches.open('nexusai-v1').then(cache => {
               return cache.addAll([
                   '/',
                   '/index.html',
                   '/static/js/bundle.js',
                   '/static/css/main.css'
               ]);
           })
       );
   });
   
   self.addEventListener('fetch', (e) => {
       e.respondWith(
           caches.match(e.request).then(response => {
               return response || fetch(e.request);
           })
       );
   });
   ```

2. **Add Manifest**
   ```json
   {
       "name": "NexusAI",
       "short_name": "NexusAI",
       "start_url": "/",
       "display": "standalone",
       "background_color": "#ffffff",
       "theme_color": "#4CAF50",
       "icons": [
           {
               "src": "/icon-192.png",
               "sizes": "192x192",
               "type": "image/png"
           },
           {
               "src": "/icon-512.png",
               "sizes": "512x512",
               "type": "image/png"
           }
       ]
   }
   ```

3. **Register Service Worker**
   ```javascript
   // frontend/src/index.jsx
   if ('serviceWorker' in navigator) {
       navigator.serviceWorker.register('/sw.js');
   }
   ```

4. **Add Offline Fallback**
   - Cache conversations locally
   - Queue messages when offline
   - Sync when connection restored

5. **Implement Push Notifications**
   ```javascript
   Notification.requestPermission().then(permission => {
       if (permission === 'granted') {
           // Subscribe to push notifications
       }
   });
   ```

**Verification:**
- [ ] App installable on mobile/desktop
- [ ] Works offline with cached content
- [ ] Messages queue when offline
- [ ] Push notifications work

---

## Phase 4: Enterprise Ready

### 4.1 Role-Based Access Control (RBAC)

**Objective:** Implement granular permissions system for enterprise users.

**Implementation Steps:**

1. **Define Roles**
   ```python
   # backend/models.py
   class Role(Base):
       id = Column(Integer, primary_key=True)
       name = Column(String, unique=True)  # admin, manager, user, viewer
       permissions = Column(JSON)  # List of permission strings
   
   class UserRole(Base):
       user_id = Column(Integer, ForeignKey('users.id'))
       role_id = Column(Integer, ForeignKey('roles.id'))
   ```

2. **Create Permission Decorator**
   ```python
   def require_permission(permission: str):
       def decorator(func):
           @wraps(func)
           async def wrapper(*args, **kwargs):
               user = get_current_user()
               if not user.has_permission(permission):
                   raise HTTPException(403, "Insufficient permissions")
               return await func(*args, **kwargs)
           return wrapper
       return decorator
   
   @app.delete("/api/users/{id}")
   @require_permission("users.delete")
   async def delete_user(id: int):
       pass
   ```

3. **Add Admin Panel**
   - Manage users
   - Assign roles
   - Create custom roles
   - View audit logs

4. **Frontend Permission Checks**
   ```javascript
   {user.hasPermission('admin.access') && (
       <AdminButton />
   )}
   ```

**Verification:**
- [ ] Permissions enforced on all endpoints
- [ ] Admins can manage roles
- [ ] UI adapts to user permissions
- [ ] Unauthorized access blocked

---

### 4.2 Audit Logging

**Objective:** Log all significant user actions for compliance and security.

**Implementation Steps:**

1. **Create Audit Log Table**
   ```sql
   CREATE TABLE audit_logs (
       id SERIAL PRIMARY KEY,
       user_id INTEGER REFERENCES users(id),
       action VARCHAR(100),
       resource_type VARCHAR(50),
       resource_id INTEGER,
       details JSON,
       ip_address VARCHAR(45),
       user_agent TEXT,
       timestamp TIMESTAMP DEFAULT NOW()
   );
   
   CREATE INDEX idx_audit_user ON audit_logs(user_id);
   CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);
   ```

2. **Create Audit Middleware**
   ```python
   @app.middleware("http")
   async def audit_middleware(request: Request, call_next):
       response = await call_next(request)
       if request.method in ["POST", "PUT", "DELETE"]:
           log_audit(
               user_id=request.state.user.id,
               action=f"{request.method} {request.url.path}",
               ip_address=request.client.host
           )
       return response
   ```

3. **Log Important Actions**
   - User login/logout
   - Conversation creation/deletion
   - File uploads
   - Permission changes
   - Settings modifications

4. **Build Audit Viewer**
   - Filter by user, action, date
   - Export to CSV
   - Real-time log streaming

**Verification:**
- [ ] All actions logged correctly
- [ ] Logs tamper-proof
- [ ] Admins can view audit trail
- [ ] Performance not impacted

---

### 4.3 SSO / OAuth Integration

**Objective:** Support enterprise SSO (SAML, OAuth2, OIDC).

**Implementation Steps:**

1. **Install OAuth Libraries**
   ```bash
   pip install authlib python-saml
   ```

2. **Add OAuth Providers**
   ```python
   # backend/auth/oauth.py
   from authlib.integrations.starlette_client import OAuth
   
   oauth = OAuth()
   oauth.register(
       'google',
       client_id=GOOGLE_CLIENT_ID,
       client_secret=GOOGLE_CLIENT_SECRET,
       server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
       client_kwargs={'scope': 'openid email profile'}
   )
   ```

3. **Create OAuth Endpoints**
   ```python
   @app.get("/api/auth/oauth/{provider}")
   async def oauth_login(provider: str):
       redirect_uri = "http://localhost:8000/api/auth/callback"
       return await oauth.create_client(provider).authorize_redirect(redirect_uri)
   
   @app.get("/api/auth/callback")
   async def oauth_callback():
       token = await oauth.google.authorize_access_token()
       user_info = token['userinfo']
       # Create or update user
   ```

4. **Add SAML Support**
   ```python
   from onelogin.saml2.auth import OneLogin_Saml2_Auth
   
   @app.post("/api/auth/saml")
   async def saml_login():
       auth = OneLogin_Saml2_Auth(request, saml_settings)
       return auth.login()
   ```

5. **Frontend OAuth Buttons**
   ```jsx
   <button onClick={() => window.location = '/api/auth/oauth/google'}>
       Sign in with Google
   </button>
   ```

**Verification:**
- [ ] Google OAuth works
- [ ] Microsoft OAuth works
- [ ] SAML login successful
- [ ] User profiles sync correctly

---

### 4.4 API Key Management

**Objective:** Allow users to generate API keys for programmatic access.

**Database Schema:**
```sql
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    key_hash VARCHAR(255) UNIQUE,
    name VARCHAR(100),
    scopes JSON,  -- ["conversations.read", "messages.write"]
    rate_limit INTEGER DEFAULT 1000,  -- requests per hour
    last_used TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    revoked_at TIMESTAMP NULL
);
```

**Implementation Steps:**

1. **Create API Key Generator**
   ```python
   import secrets
   
   def generate_api_key():
       key = f"nxai_{secrets.token_urlsafe(32)}"
       key_hash = hash_password(key)
       return key, key_hash
   ```

2. **Add API Key Endpoints**
   ```python
   @app.post("/api/keys")
   async def create_api_key(name: str, scopes: List[str]):
       key, key_hash = generate_api_key()
       api_key = APIKey(
           user_id=current_user.id,
           key_hash=key_hash,
           name=name,
           scopes=scopes
       )
       db.add(api_key)
       db.commit()
       return {"key": key}  # Only shown once!
   
   @app.delete("/api/keys/{id}")
   async def revoke_api_key(id: int):
       api_key = db.query(APIKey).get(id)
       api_key.revoked_at = datetime.now()
       db.commit()
   ```

3. **Implement API Key Authentication**
   ```python
   async def get_api_key(api_key: str = Header(None, alias="X-API-Key")):
       if not api_key:
           raise HTTPException(401, "API key required")
       key_hash = hash_password(api_key)
       db_key = db.query(APIKey).filter_by(key_hash=key_hash).first()
       if not db_key or db_key.revoked_at:
           raise HTTPException(401, "Invalid API key")
       return db_key
   ```

4. **Add Rate Limiting**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=lambda: api_key.id)
   
   @app.post("/api/chat")
   @limiter.limit("1000/hour")
   async def chat(api_key: APIKey = Depends(get_api_key)):
       pass
   ```

5. **Build API Key Manager UI**
   - Create new keys
   - View existing keys (masked)
   - Set scopes and expiration
   - Revoke keys
   - View usage stats

**Verification:**
- [ ] API keys authenticate successfully
- [ ] Rate limiting enforced
- [ ] Scopes restrict access correctly
- [ ] Revoked keys rejected

---

## Quick Reference

| Enhancement | Difficulty | Impact | Recommended Order |
|-------------|------------|--------|-------------------|
| Dark Mode | Easy | Medium | 1 |
| Conversation Templates | Easy | Medium | 2 |
| RAG Pipeline | Medium | High | 3 |
| Function Calling | Medium | High | 4 |
| Long-Term Memory | Medium | Medium | 5 |
| PostgreSQL Migration | Medium | High | 6 |
| Docker Deployment | Easy | High | 7 |
| Multi-User Collaboration | Hard | Medium | 8 |
| Plugin System | Hard | High | 9 |
| AI Agents | Hard | High | 10 |
| PWA | Medium | Medium | 11 |
| Monitoring Dashboard | Medium | Medium | 12 |
| RBAC | Medium | Medium | 13 |
| Audit Logging | Easy | Medium | 14 |
| SSO/OAuth | Medium | Medium | 15 |
| API Key Management | Medium | High | 16 |

---

## Getting Started

1. **Choose your phase** based on current needs
2. **Follow implementation steps** for each enhancement
3. **Run verification checklist** before moving to next feature
4. **Document changes** in your project wiki
5. **Deploy incrementally** to avoid breaking changes

**For questions or contributions, please open an issue on GitHub!**
