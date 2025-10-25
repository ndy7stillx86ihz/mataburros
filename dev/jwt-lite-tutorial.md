# JWT

## La base: cómo funciona un JWT

Un JWT son tres partes pegadas con puntos: `header.payload.signature`

Cada parte es JSON convertido a Base64URL (ojo, no es Base64 normal, usa `-` y `_` en vez de `+` y `/`, y no tiene padding).

**Generación de firma con HMAC (simétrico):**
```
paso1 = base64url({"alg":"HS256","typ":"JWT"})
paso2 = base64url({"sub":"user123","exp":1730728800})
data = paso1 + "." + paso2

firma = HMAC_SHA256(data, secret_compartido)
jwt_final = data + "." + base64url(firma)
```

La clave secreta sirve tanto para firmar como para verificar. Si se filtra, game over.

**Generación con RSA (asimétrico, mejor para producción):**
```
data = base64url(header) + "." + base64url(payload)

// Firmar con clave PRIVADA (solo el servidor la tiene)
firma = RSA_SHA256_sign(data, clave_privada)
jwt_final = data + "." + base64url(firma)

// Verificar con clave PÚBLICA (puede estar en cualquier microservicio)
es_valido = RSA_SHA256_verify(data, firma, clave_publica)
```

Ventaja: aunque alguien tenga la clave pública, no puede crear tokens falsos.

**Header típico:**
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-2024-oct"
}
```

El `kid` (key id) es crucial para rotación de claves. Te dice qué clave usar para verificar.

**Payload con los claims importantes:**
```json
{
  "iss": "https://auth.miapp.com",
  "sub": "user_abc123",
  "aud": "api.miapp.com",
  "exp": 1730728800,
  "iat": 1730727000,
  "jti": "uuid-token-12345",
  "roles": ["user", "premium"],
  "email": "user@example.com"
}
```

Claims críticos:
- `exp` (expiration): timestamp Unix de cuándo expira
- `iat` (issued at): cuándo se creó
- `jti` (JWT ID): identificador único para este token específico
- `sub` (subject): ID del usuario
- `iss` (issuer): quién lo emitió
- `aud` (audience): para qué servicio es

## Dónde guardar los tokens (cliente)

Tienes básicamente tres opciones, cada una con sus tradeoffs:

**Opción A: HttpOnly Cookies (la más segura para web)**
```javascript
// Backend setea la cookie
response.cookie('access_token', jwt, {
  httpOnly: true,     // JavaScript no puede leerla (anti-XSS)
  secure: true,       // Solo HTTPS
  sameSite: 'strict', // Anti-CSRF
  maxAge: 900000      // 15 minutos
})

// Frontend: no haces nada, el browser la manda automáticamente
fetch('/api/user/profile')  // Cookie incluida automáticamente
```

Pros: Protección contra XSS. Aunque inyecten código malicioso, no pueden robar el token.
Contras: Necesitas protección CSRF (usa SameSite o tokens CSRF). No funciona cross-domain fácilmente.

**Opción B: localStorage + Authorization header**
```javascript
// Guardar tras login
localStorage.setItem('access_token', jwt)

// Usar en cada request
const token = localStorage.getItem('access_token')
fetch('/api/user/profile', {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

Pros: Fácil para SPAs, funciona cross-domain, no hay problemas CSRF.
Contras: Vulnerable a XSS. Si meten un script, pueden hacer `localStorage.getItem('access_token')` y robarlo.

**Opción C: sessionStorage**
```javascript
sessionStorage.setItem('access_token', jwt)
```

Como localStorage pero se borra al cerrar la pestaña. Más seguro para sesiones temporales.

**Qué usar:** Si tu app es solo web y mismo dominio, HttpOnly cookies. Si necesitas mobile apps, otros dominios, o APIs públicas, usa headers Authorization con localStorage pero asegúrate de tener buena sanitización contra XSS.

## Almacenamiento en servidor

Los access tokens NO se almacenan (son stateless, ese es el punto). Pero los refresh tokens sí:

**Tabla de refresh tokens:**
```sql
CREATE TABLE refresh_tokens (
  id UUID PRIMARY KEY,
  user_id INTEGER NOT NULL,
  token_hash VARCHAR(255) NOT NULL,  -- hash SHA-256, nunca plaintext
  device_info JSONB,
  ip_address VARCHAR(45),
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  last_used TIMESTAMP,
  revoked BOOLEAN DEFAULT FALSE,
  revoked_at TIMESTAMP,
  INDEX idx_user_id (user_id),
  INDEX idx_token_hash (token_hash),
  INDEX idx_expires (expires_at)
)
```

Por qué hash: si hackean tu DB, no pueden usar los refresh tokens directamente.

**Blacklist de access tokens (Redis):**
```javascript
// Cuando haces logout
const payload = decodeJWT(accessToken)
const ttl = payload.exp - Math.floor(Date.now() / 1000)

redis.setex(`blacklist:${payload.jti}`, ttl, 'revoked')
```

Solo guardas en blacklist el tiempo que queda hasta que expire naturalmente. Así Redis los limpia solo.

## El patrón access + refresh tokens

Este es el setup estándar en producción:

**Login inicial:**
```javascript
function login(email, password, deviceInfo) {
  user = db.authenticate(email, password)
  if (!user) throw new Error('Credenciales inválidas')
  
  // Access token: corto, solo para requests
  accessToken = jwt.sign({
    sub: user.id,
    email: user.email,
    roles: user.roles,
    exp: now() + 15_MINUTES,
    iat: now(),
    jti: generateUUID(),
    token_version: user.token_version
  }, privateKey, { algorithm: 'RS256', header: { kid: currentKeyId } })
  
  // Refresh token: largo, para renovar access
  refreshToken = crypto.randomBytes(32).toString('hex')
  
  db.saveRefreshToken({
    user_id: user.id,
    token_hash: sha256(refreshToken),
    device_info: deviceInfo,
    ip_address: req.ip,
    expires_at: now() + 7_DAYS
  })
  
  return { accessToken, refreshToken }
}
```

**Request normal con access token:**
```javascript
GET /api/posts
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...

// Backend valida
function protectedEndpoint(req) {
  token = req.headers.authorization.split(' ')[1]
  payload = validateJWT(token)  // Verifica firma, exp, etc.
  
  user = db.getUser(payload.sub)
  return getUserPosts(user.id)
}
```

**Cuando access token expira (15 min después):**
```javascript
POST /auth/refresh
{ "refresh_token": "abc123..." }

function refreshEndpoint(refreshToken) {
  // Buscar en DB
  tokenData = db.query(`
    SELECT * FROM refresh_tokens 
    WHERE token_hash = ? AND revoked = false
  `, sha256(refreshToken))
  
  if (!tokenData) throw new Error('Refresh token inválido')
  if (tokenData.expires_at < now()) throw new Error('Refresh token expirado')
  
  user = db.getUser(tokenData.user_id)
  
  // Nuevo access token
  newAccessToken = jwt.sign({
    sub: user.id,
    exp: now() + 15_MINUTES,
    token_version: user.token_version
  }, privateKey)
  
  // Opcional: rotar refresh token también (más seguro)
  newRefreshToken = crypto.randomBytes(32).toString('hex')
  db.update(tokenData.id, {
    token_hash: sha256(newRefreshToken),
    last_used: now()
  })
  
  return { accessToken: newAccessToken, refreshToken: newRefreshToken }
}
```

**Tiempos recomendados:**
- Access token: 15-30 minutos (algunos usan 5 minutos para apps críticas)
- Refresh token: 7-30 días (o hasta que hagan logout)

## Validación correcta de JWT

El orden importa. Muchos bugs de seguridad vienen de validar en orden incorrecto:

```javascript
function validateJWT(token, expectedAudience) {
  // 1. Split y decode header sin verificar todavía
  parts = token.split('.')
  if (parts.length !== 3) throw new Error('Formato inválido')
  
  header = JSON.parse(base64decode(parts[0]))
  
  // 2. Verificar algoritmo ANTES de verificar firma (evita algorithm confusion)
  if (header.alg !== 'RS256') {
    throw new Error('Algoritmo no permitido')
  }
  
  // 3. Obtener clave correcta usando kid
  if (!header.kid) throw new Error('kid faltante')
  publicKey = keyStore.getPublicKey(header.kid)
  if (!publicKey) throw new Error('Clave no encontrada')
  
  // 4. Verificar firma criptográfica
  signature = base64decode(parts[2])
  data = parts[0] + '.' + parts[1]
  if (!crypto.verify('RSA-SHA256', data, publicKey, signature)) {
    throw new Error('Firma inválida')
  }
  
  // 5. Ahora sí, decodear payload
  payload = JSON.parse(base64decode(parts[1]))
  
  // 6. Validar exp
  if (!payload.exp || payload.exp < now()) {
    throw new Error('Token expirado')
  }
  
  // 7. Validar nbf si existe
  if (payload.nbf && payload.nbf > now()) {
    throw new Error('Token todavía no válido')
  }
  
  // 8. Validar issuer
  if (payload.iss !== 'https://auth.miapp.com') {
    throw new Error('Issuer inválido')
  }
  
  // 9. Validar audience
  if (payload.aud !== expectedAudience) {
    throw new Error('Token no es para este servicio')
  }
  
  // 10. Check blacklist (solo si implementaste logout)
  if (redis.exists(`blacklist:${payload.jti}`)) {
    throw new Error('Token revocado')
  }
  
  // 11. Validar versión (para invalidar todos los tokens del usuario)
  user = db.getUser(payload.sub)
  if (payload.token_version !== user.token_version) {
    throw new Error('Token version inválida')
  }
  
  return payload
}
```

## Cómo revocar tokens

Problema: JWT es stateless por diseño, no puedes "cancelarlo" una vez emitido. Soluciones:

**Estrategia 1: Blacklist con Redis (más común)**
```javascript
function logout(accessToken, refreshToken) {
  payload = jwt.decode(accessToken)
  
  // Agregar access token a blacklist
  ttl = payload.exp - now()
  if (ttl > 0) {
    redis.setex(`blacklist:${payload.jti}`, ttl, 'revoked')
  }
  
  // Revocar refresh token en DB
  db.execute(`
    UPDATE refresh_tokens 
    SET revoked = true, revoked_at = NOW()
    WHERE token_hash = ?
  `, sha256(refreshToken))
}

// En cada validación
if (redis.exists(`blacklist:${payload.jti}`)) {
  throw new Error('Token revocado')
}
```

Pros: Funciona inmediatamente. Contras: Necesitas Redis (estado), chequeo extra en cada request.

**Estrategia 2: Token versioning (sin blacklist)**
```javascript
// User table
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  email VARCHAR(255),
  token_version INTEGER DEFAULT 0
)

// Al generar token
jwt = sign({
  sub: user.id,
  token_version: user.token_version,
  exp: now() + 15_MIN
})

// Al validar
if (jwt.token_version !== user.current_token_version) {
  throw new Error('Token inválido')
}

// Para revocar todos los tokens del usuario
db.execute(`UPDATE users SET token_version = token_version + 1 WHERE id = ?`, userId)
```

Pros: Sin Redis, un solo query. Contras: Necesitas un query a DB por cada validación (o cachear token_version).

**Estrategia 3: Tokens cortos + sin revocación**
```javascript
// Access tokens de 5 minutos
// Solo revocas refresh tokens

// Para logout
db.revokeRefreshToken(refreshToken)

// El access token expira en 5 min de todas formas
```

Pros: Más simple, menos overhead. Contras: Hasta 5 min de ventana si alguien roba un token.

**Cuál usar:** Para apps normales, estrategia 3. Para apps sensibles (bancos, salud), estrategia 1 o 2.

## Rotación de claves en producción

Deberías rotar claves cada 90 días. Así es como se hace sin downtime:

**Setup: múltiples claves activas**
```javascript
// Key store
const keys = {
  'key-2024-08': {
    publicKey: '-----BEGIN PUBLIC KEY-----...',
    privateKey: '-----BEGIN PRIVATE KEY-----...',
    createdAt: '2024-08-01',
    status: 'deprecated'
  },
  'key-2024-10': {
    publicKey: '-----BEGIN PUBLIC KEY-----...',
    privateKey: '-----BEGIN PRIVATE KEY-----...',
    createdAt: '2024-10-01',
    status: 'active'
  },
  'key-2024-11': {
    publicKey: '-----BEGIN PUBLIC KEY-----...',
    privateKey: '-----BEGIN PRIVATE KEY-----...',
    createdAt: '2024-11-01',
    status: 'active'
  }
}

// Clave actual para FIRMAR
currentSigningKey = 'key-2024-11'

// Claves válidas para VERIFICAR (incluye viejas durante overlap)
validKeys = ['key-2024-10', 'key-2024-11']
```

**Proceso de rotación:**
```javascript
// Día 1: Generar nueva clave
function rotateKeys() {
  newKeyId = 'key-2024-12'
  
  // Generar par RSA
  { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048,
    publicKeyEncoding: { type: 'spki', format: 'pem' },
    privateKeyEncoding: { type: 'pkcs8', format: 'pem' }
  })
  
  keys[newKeyId] = { publicKey, privateKey, createdAt: now(), status: 'active' }
  
  // Actualizar clave de firma
  currentSigningKey = newKeyId
  
  // Mantener overlap: acepta la vieja y la nueva
  validKeys = ['key-2024-11', 'key-2024-12']
  
  console.log('Nueva clave activa, overlap de 30 min')
}

// Día 1 + 30 minutos: Remover clave vieja
function cleanupOldKeys() {
  // Ya todos los tokens con key-2024-11 expiraron
  validKeys = ['key-2024-12']
  
  // Marcar como deprecated pero mantener en caso de auditoría
  keys['key-2024-11'].status = 'deprecated'
  
  // Después de 90 días, eliminar completamente
  delete keys['key-2024-08']
}
```

**Firmar con nueva clave:**
```javascript
function generateToken(payload) {
  const header = {
    alg: 'RS256',
    typ: 'JWT',
    kid: currentSigningKey  // Indica qué clave usaste
  }
  
  const privateKey = keys[currentSigningKey].privateKey
  
  return jwt.sign(payload, privateKey, {
    algorithm: 'RS256',
    header: header
  })
}
```

**Verificar con cualquier clave válida:**
```javascript
function verifyToken(token) {
  const header = jwt.decode(token, { complete: true }).header
  
  // Validar que el kid sea de una clave válida
  if (!validKeys.includes(header.kid)) {
    throw new Error('Clave expirada o inválida')
  }
  
  const publicKey = keys[header.kid].publicKey
  
  return jwt.verify(token, publicKey, {
    algorithms: ['RS256']
  })
}
```

**Calendario de rotación:**
```
Día 0: Clave A activa (firma y verifica)
Día 90: Generar clave B
        - Firmar con B
        - Verificar A y B (overlap)
Día 90 + 30min: Solo verificar B, deprecar A
Día 180: Generar clave C, repeat...
```

**Exponer claves públicas (JWKS endpoint):**
```javascript
GET /.well-known/jwks.json

{
  "keys": [
    {
      "kid": "key-2024-11",
      "kty": "RSA",
      "use": "sig",
      "alg": "RS256",
      "n": "0vx7agoebG...",
      "e": "AQAB"
    },
    {
      "kid": "key-2024-12",
      "kty": "RSA",
      "use": "sig",
      "alg": "RS256",
      "n": "xjlbY3Pj...",
      "e": "AQAB"
    }
  ]
}
```

Otros microservicios pueden fetchear este endpoint para obtener las claves públicas y verificar tokens.

## Manejo de múltiples dispositivos

Usuario quiere ver sesiones activas y cerrar otras:

**Guardar info del dispositivo:**
```javascript
function login(email, password, req) {
  user = authenticate(email, password)
  
  deviceInfo = {
    device_id: req.body.device_id || generateUUID(),
    device_name: req.body.device_name || 'Unknown Device',
    device_type: req.body.device_type || detectDeviceType(req.userAgent),
    os: parseOS(req.userAgent),
    browser: parseBrowser(req.userAgent),
    ip: req.ip,
    user_agent: req.userAgent
  }
  
  refreshToken = generateSecureToken()
  
  db.saveRefreshToken({
    user_id: user.id,
    token_hash: sha256(refreshToken),
    device_info: deviceInfo,
    expires_at: now() + 7_DAYS
  })
  
  return { accessToken, refreshToken, deviceId: deviceInfo.device_id }
}
```

**Ver sesiones activas:**
```javascript
GET /user/sessions

function getActiveSessions(userId) {
  return db.query(`
    SELECT 
      device_info->>'device_name' as device,
      device_info->>'os' as os,
      device_info->>'ip' as ip,
      created_at,
      last_used,
      CASE WHEN last_used > NOW() - INTERVAL '5 minutes' 
           THEN true ELSE false END as is_current
    FROM refresh_tokens
    WHERE user_id = ? AND revoked = false AND expires_at > NOW()
    ORDER BY last_used DESC
  `, userId)
}
```

**Cerrar sesión en dispositivo específico:**
```javascript
DELETE /user/sessions/:device_id

function revokeDevice(userId, deviceId) {
  db.execute(`
    UPDATE refresh_tokens
    SET revoked = true, revoked_at = NOW()
    WHERE user_id = ? AND device_info->>'device_id' = ?
  `, userId, deviceId)
}
```

**Cerrar todas las sesiones (cambio de password):**
```javascript
function changePassword(userId, newPassword) {
  // Hash nueva password
  db.updatePassword(userId, hash(newPassword))
  
  // Revocar todos los refresh tokens
  db.execute(`
    UPDATE refresh_tokens
    SET revoked = true, revoked_at = NOW()
    WHERE user_id = ?
  `, userId)
  
  // Incrementar token_version para invalidar access tokens
  db.execute(`
    UPDATE users
    SET token_version = token_version + 1
    WHERE id = ?
  `, userId)
  
  // Opcional: agregar todos los JTIs activos a blacklist
  activeTokens = getActiveAccessTokens(userId)
  activeTokens.forEach(token => {
    redis.setex(`blacklist:${token.jti}`, token.ttl, 'password_change')
  })
}
```

## Vulnerabilidades comunes y cómo prevenirlas

**Algorithm confusion attack:**
```javascript
// Ataque: cambiar RS256 a HS256
// El atacante usa la clave PÚBLICA como si fuera HMAC secret
// Si no validas el algoritmo, el servidor puede verificar con la pública como HMAC

// MAL
function verify(token) {
  return jwt.verify(token, publicKey)  // Acepta cualquier algoritmo
}

// BIEN
function verify(token) {
  return jwt.verify(token, publicKey, { algorithms: ['RS256'] })  // Solo RS256
}
```

**None algorithm attack:**
```javascript
// Ataque: {"alg": "none"} sin firma

// MAL
if (!header.alg || header.alg === 'none') {
  return payload  // NUNCA
}

// BIEN
allowedAlgorithms = ['RS256', 'RS384', 'RS512']
if (!allowedAlgorithms.includes(header.alg)) {
  throw new Error('Algoritmo no permitido')
}
```

**Weak HMAC secrets:**
```javascript
// MAL
secret = 'myapp123'  // Brute-forceable

// BIEN
secret = crypto.randomBytes(32).toString('hex')
// Resultado: 'a7f3c9e2b1d4f8e9a0c5b7d3e1f9a8c4b6d2e8f1a9c5d7e3f0b1d6a4c8e2f5b'
```

**No validar claims:**
```javascript
// MAL
payload = jwt.verify(token, publicKey)
userId = payload.sub  // Sin validar exp, aud, etc.

// BIEN
payload = jwt.verify(token, publicKey, {
  issuer: 'https://auth.miapp.com',
  audience: 'api.miapp.com',
  maxAge: '30m'
})
```

**JWT en URLs:**
```javascript
// MAL: tokens en query params se loguean en todas partes
GET /download?token=eyJhbGc...

// BIEN: siempre en headers o cookies
Authorization: Bearer eyJhbGc...
```

**Datos sensibles en payload:**
```javascript
// MAL
jwt = sign({
  sub: user.id,
  password: user.password,  // NUNCA
  ssn: user.ssn,            // NUNCA
  credit_card: user.card    // NUNCA
})

// BIEN
jwt = sign({
  sub: user.id,
  roles: user.roles,
  email: user.email  // OK si no es super sensible
})
```

Recuerda: el payload es solo Base64, cualquiera puede leerlo. No es encriptación.

## Checklist para producción

Antes de deployar:

- [ ] HTTPS obligatorio en todos los endpoints
- [ ] Access tokens: 15-30 min max
- [ ] Refresh tokens: hasheados en DB
- [ ] HttpOnly cookies si es web app
- [ ] Algoritmo forzado en validación (no confiar en header)
- [ ] Validar TODOS los claims: exp, iss, aud, nbf
- [ ] Rate limiting en /login y /refresh (5 intentos por minuto)
- [ ] Blacklist implementada para logout
- [ ] Token versioning para cambio de password
- [ ] Rotación de claves cada 90 días
- [ ] Logging de intentos de tokens inválidos
- [ ] Monitoring de tokens expirados (si hay muchos, quizá el tiempo es muy corto)
- [ ] No poner datos sensibles en payload
- [ ] 2FA para acciones críticas aunque tengas token válido

## Flujo completo end-to-end

```
1. Login
   POST /auth/login
   { email, password, device_info }
   →
   { 
     access_token (15 min),
     refresh_token (7 días),
     token_type: "Bearer"
   }

2. Usar API
   GET /api/posts
   Authorization: Bearer <access_token>
   →
   { posts: [...] }

3. Token expira (15 min después)
   GET /api/posts
   Authorization: Bearer <expired_token>
   →
   401 { error: "token_expired" }

4. Frontend detecta 401, refreshea automáticamente
   POST /auth/refresh
   { refresh_token }
   →
   {
     access_token (nuevo, 15 min),
     refresh_token (nuevo si rotas)
   }

5. Retry request original
   GET /api/posts
   Authorization: Bearer <new_access_token>
   →
   { posts: [...] }

6. Logout
   POST /auth/logout
   { access_token, refresh_token }
   →
   // Blacklist access token JTI
   // Revoke refresh token en DB
   200 { message: "logged_out" }

7. Cambio de password
   POST /user/change-password
   { old_password, new_password }
   →
   // Update password
   // Increment token_version
   // Revoke all refresh tokens
   200 { message: "password_changed" }

8. Re-login en todos los dispositivos
   (Porque token_version cambió)
```

## Cuándo NO usar JWT

No todo problema se resuelve con JWT. Alternativas:

**Sesiones tradicionales con cookies:**
```javascript
// Session ID opaco en cookie
session_id = '3f2a8b9c1d4e5f6a7b8c9d0e1f2a3b4c'
redis.set(session_id, { user_id: 123, roles: ['admin'] }, ttl: 3600)

// Ventajas:
// - Revocación instantánea (borras de Redis)
// - Menos datos en cada request
// - Más fácil de entender

// Cuando usar:
// - App monolítica
// - No necesitas microservicios
// - Necesitas revocación instantánea frecuente
```

**Opaque tokens (random UUID):**
```javascript
// Token: 'd4f7b9c2e8a1f5d3b6c9e2a8f1b4d7c6'
db.save({ token: hash(token), user_id: 123, expires: ... })

// Ventajas:
// - Control total sobre validez
// - Puede llevar más datos en server
// - Revocación trivial

// Cuando usar:
// - OAuth2 para terceros
// - Necesitas auditoría detallada
// - Tokens de larga vida
```

**OAuth2 con external providers:**
```javascript
// Delegar autenticación a Google, GitHub, etc.

// Cuando usar:
// - No quieres manejar passwords
// - Login social
// - Acceso a APIs de terceros
```

JWT es excelente para arquitecturas distribuidas, microservicios, y cuando necesitas que cada servicio verifique tokens independientemente sin llamar a una DB central. Para apps simples, sesiones tradicionales pueden ser más fáciles.
