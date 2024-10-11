// content.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "prompt_for_otp") {
    promptForOtp();
  }
});


async function promptForOtp() {
  const profile = await getProfile("Microsoft");
  const pin = prompt("Enter your 6-digit PIN:");
  
  if (pin === profile.pin) {
    const otp = generateTOTP(profile.secret);
    autofillOTP(otp);
  } else {
    alert("Incorrect PIN!");
  }
}

function autofillOTP(otp) {
  const otpInput = document.querySelector("input[aria-label='Enter code']");
  if (otpInput) {
    otpInput.value = otp;
  }
}
