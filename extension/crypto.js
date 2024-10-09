// crypto.js
async function getKeyMaterial(pin) {
    const enc = new TextEncoder();
    return window.crypto.subtle.importKey(
      "raw",
      enc.encode(pin),
      { name: "PBKDF2" },
      false,
      ["deriveKey"]
    );
  }
  
  async function getKey(pin) {
    const keyMaterial = await getKeyMaterial(pin);
    return window.crypto.subtle.deriveKey(
      {
        name: "PBKDF2",
        salt: new TextEncoder().encode("unique_salt"),
        iterations: 100000,
        hash: "SHA-256"
      },
      keyMaterial,
      { name: "AES-GCM", length: 256 },
      true,
      ["encrypt", "decrypt"]
    );
  }
  
  export async function encryptSecret(secret, pin) {
    const key = await getKey(pin);
    const iv = window.crypto.getRandomValues(new Uint8Array(12));
    const enc = new TextEncoder().encode(secret);
    const encrypted = await window.crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, enc);
    return { encrypted, iv };
  }
  
  export async function decryptSecret(encrypted, iv, pin) {
    const key = await getKey(pin);
    const decrypted = await window.crypto.subtle.decrypt({ name: "AES-GCM", iv }, key, encrypted);
    return new TextDecoder().decode(decrypted);
  }
  