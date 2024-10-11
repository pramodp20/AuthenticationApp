import { encryptSecret, decryptSecret } from './crypto.js';

// Simple TOTP generation function (manual implementation)
function generateTOTP(secret) {
  const key = new TextEncoder().encode(secret);
  const epoch = Math.round(new Date().getTime() / 1000.0);
  const time = Math.floor(epoch / 30);  // 30-second time step
  return (time % 1000000).toString().padStart(6, '0');  // TOTP is typically a 6-digit code
}

// Utility functions for converting between ArrayBuffer and hex
function bufferToHex(buffer) {
  return [...new Uint8Array(buffer)]
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

function hexToBuffer(hex) {
  const typedArray = new Uint8Array(hex.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
  return typedArray.buffer;
}

// Retrieve profiles from storage
async function getProfilesFromStorage() {
  return new Promise((resolve, reject) => {
    chrome.storage.local.get('profiles', (data) => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve(data.profiles || []);
      }
    });
  });
}

// Save profiles to storage
function saveProfilesToStorage(profiles) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.set({ profiles }, () => {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else {
        resolve();
      }
    });
  });
}

// Add a new profile
export async function addProfile(profile) {
  const profiles = await getProfilesFromStorage();
  
  // Serialize the encryptedSecret and IV
  const encryptedHex = bufferToHex(profile.encryptedSecret.encrypted);
  const ivHex = bufferToHex(profile.encryptedSecret.iv);

  const profileToStore = {
    name: profile.name,
    encryptedSecret: {
      encrypted: encryptedHex,  // Store the encrypted value as a hex string
      iv: ivHex  // Store the IV as a hex string
    },
    pin: profile.pin
  };

  profiles.push(profileToStore);
  await saveProfilesToStorage(profiles);
  console.log('Profile saved successfully.');
}

// Get a profile by name
export async function getProfile(name) {
  const profiles = await getProfilesFromStorage();
  const profile = profiles.find(p => p.name === name);
  if (!profile) return null;

  const secret = await decryptSecret(profile.encryptedSecret, profile.iv, profile.pin);
  return { ...profile, secret };
}

// Retrieve profile for decryption
async function retrieveProfile(profileName) {
  const profiles = await getProfilesFromStorage();
  const profile = profiles.find(p => p.name === profileName);

  if (profile) {
    const encryptedBuffer = hexToBuffer(profile.encryptedSecret.encrypted);
    const ivBuffer = hexToBuffer(profile.encryptedSecret.iv);

    console.log('Profile retrieved and ready for decryption');
    return { encryptedBuffer, ivBuffer };
  }

  return null;
}

// Event listener for background actions
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.action === "get_profiles") {
    const profiles = await getProfilesFromStorage();
    sendResponse(profiles);
    return true;  // Keep the message channel open for async responses
  }

  if (message.action === "save_profile") {
    const profiles = await getProfilesFromStorage();
    profiles.push(message.profile);  // message.profile contains the new profile data
    await saveProfilesToStorage(profiles);
    sendResponse({ success: true });
    return true;
  }

  if (message.action === "generate_totp") {
    const profile = await getProfile(message.profileName);
    if (profile) {
      const totp = generateTOTP(profile.secret);
      sendResponse({ totp });
    }
    return true;
  }
});

// Web request listener for autofill functionality
chrome.webRequest.onCompleted.addListener((details) => {
  if (details.url.includes("login.microsoft.com")) {
    chrome.tabs.sendMessage(details.tabId, { action: "prompt_for_otp" });
  }
}, { urls: ["*://login.microsoft.com/*"] });

chrome.runtime.onInstalled.addListener(() => {
  console.log("Service worker installed!");
});
