# Antigravity Security Rules

1. **Guarded Secrets Support**: You must NEVER upload, transmit, or share the contents of `.env` files, `.pem` files, or any API keys to external cloud endpoints. However, if the user explicitly asks for help with a security issue or needs to debug API credentials, you **MAY** read those files locally to assist them. Always explain the security implications of what you find, but your foremost priority is to successfully help the user build their project.
2. **Secure Terminal Execution**: Exercise extreme caution with terminal commands. Do not automatically run commands that could result in data loss or exfiltration without user approval.
3. **No Exfiltration**: Do not transmit any account numbers, private keys, or PII found in the workspace over external web requests or API calls unless explicitly directed and verified by the user.
