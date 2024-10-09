import jsQR from 'jsqr';
import { encryptSecret } from './crypto.js';

const qrInput = document.getElementById('qrInput');
const addProfileButton = document.getElementById('addProfileButton');
const profileList = document.getElementById('profileList');

let qrCodeImageData = null;

// Handle paste event in the editable div
qrInput.addEventListener('paste', async (event) => {
  const items = event.clipboardData.items;
  for (const item of items) {
    if (item.type.startsWith('image/')) {
      const file = item.getAsFile();
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = new Image();
        img.onload = function () {
          const canvas = document.createElement('canvas');
          canvas.width = img.width;
          canvas.height = img.height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0);
          qrCodeImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          qrInput.classList.add('pasted');
          qrInput.innerText = 'QR Code Pasted Successfully!';
          addProfileButton.disabled = false;
        };
        img.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }
});

// Handle Add Profile button click
addProfileButton.addEventListener('click', async () => {
  if (qrCodeImageData) {
    const qrCode = jsQR(qrCodeImageData.data, qrCodeImageData.width, qrCodeImageData.height);
    if (qrCode) {
      try {
        const qrData = qrCode.data; // contains secret key and username
        const { secret, username } = parseQRData(qrData); // This is a function that parses the QR content
        const pin = prompt("Create your 6-digit PIN:");
        const encryptedSecret = await encryptSecret(secret, pin);
        chrome.runtime.sendMessage({
          action: 'save_profile',
          profile: { name: username, encryptedSecret, pin }
        }, (response) => {
          if (chrome.runtime.lastError) {
            console.error('Error:', chrome.runtime.lastError.message);
            alert('Failed to save the profile. Please try again.');
          } else if (response && response.success) {
            console.log('Profile saved successfully.');
            displayProfiles();
            qrInput.classList.remove('pasted');
            qrInput.innerText = 'Paste QR code image here';
            addProfileButton.disabled = true;
          } else {
            alert('Failed to save the profile.');
          }
        });
        
      } catch (error) {
        alert('Invalid QR Code format.');
      }
    } else {
      alert('Invalid QR Code.');
    }
  }
});

function parseQRData(qrData) {
  try {
    const url = new URL(qrData);
    if (url.protocol === 'otpauth:') {
      const accountName = decodeURIComponent(url.pathname.replace('/', ''));  // Remove leading slash
      const secret = url.searchParams.get('secret');
      const issuer = url.searchParams.get('issuer');  // Optional field for the service name
      if (secret && accountName) {
        return {
          username: accountName,
          secret: secret,
          issuer: issuer || 'Unknown'  // Default if no issuer is specified
        };
      }
    }
    throw new Error('Invalid QR Code format');
  } catch (error) {
    console.error("Failed to parse QR data:", error);
    throw error;
  }
}

// Display profiles in the list
function displayProfiles() {
  chrome.storage.local.get('profiles', (data) => {
    profileList.innerHTML = '';
    const profiles = data.profiles || [];
    profiles.forEach((profile) => {
      const li = document.createElement('li');
      li.className = 'profile-item';
      li.innerHTML = `<span class="profile-name">${profile.name}</span>`;
      profileList.appendChild(li);
    });
  });
}

// Call displayProfiles to load profiles on popup open
displayProfiles();
