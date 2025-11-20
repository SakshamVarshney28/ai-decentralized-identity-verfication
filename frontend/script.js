// frontend/script.js
// FaceAuth Frontend JavaScript
// Uses full API_URL so requests reach Django backend at http://127.0.0.1:8000/api

const API_URL = "http://127.0.0.1:8000/api"; // <-- make sure Django is running here

// Helper: try to read CSRF token from cookies (if present)
function getCookie(name) {
  const match = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
  return match ? match.pop() : null;
}

function defaultHeaders() {
  const headers = { "Content-Type": "application/json" };
  const csrftoken = getCookie("csrftoken");
  if (csrftoken) headers["X-CSRFToken"] = csrftoken;
  return headers;
}

class FaceAuthApp {
  constructor() {
    this.currentStream = null;
    this.capturedImage = null;
    this.isRegisterMode = true;

    this.initializeElements();
    this.attachEventListeners();
    window.faceAuthApp = this; // expose so switchTab() can reuse instance
  }

  initializeElements() {
    // Registration elements
    this.regUsername = document.getElementById("reg-username");
    this.regPassword = document.getElementById("reg-password");
    this.regVideo = document.getElementById("reg-video");
    this.regCanvas = document.getElementById("reg-canvas");
    this.regStartCamera = document.getElementById("reg-start-camera");
    this.regCapture = document.getElementById("reg-capture");
    this.regSubmit = document.getElementById("reg-submit");
    this.regLoading = document.getElementById("reg-loading");
    this.regText = document.getElementById("reg-text");

    // Login elements
    this.loginUsername = document.getElementById("login-username");
    this.loginPassword = document.getElementById("login-password");
    this.loginVideo = document.getElementById("login-video");
    this.loginCanvas = document.getElementById("login-canvas");
    this.loginStartCamera = document.getElementById("login-start-camera");
    this.loginCapture = document.getElementById("login-capture");
    this.loginSubmit = document.getElementById("login-submit");
    this.loginLoading = document.getElementById("login-loading");
    this.loginText = document.getElementById("login-text");

    // Common elements
    this.status = document.getElementById("status");

    // disable capture/submit initially
    if (this.regCapture) this.regCapture.disabled = true;
    if (this.regSubmit) this.regSubmit.disabled = true;
    if (this.loginCapture) this.loginCapture.disabled = true;
    if (this.loginSubmit) this.loginSubmit.disabled = true;
  }

  attachEventListeners() {
    // Registration events
    if (this.regStartCamera)
      this.regStartCamera.addEventListener("click", () =>
        this.startCamera("reg")
      );
    if (this.regCapture)
      this.regCapture.addEventListener("click", () => this.captureImage("reg"));
    if (this.regSubmit)
      this.regSubmit.addEventListener("click", () => this.submitRegistration());

    // Login events
    if (this.loginStartCamera)
      this.loginStartCamera.addEventListener("click", () =>
        this.startCamera("login")
      );
    if (this.loginCapture)
      this.loginCapture.addEventListener("click", () =>
        this.captureImage("login")
      );
    if (this.loginSubmit)
      this.loginSubmit.addEventListener("click", () => this.submitLogin());

    // Tab switching - uses textContent of the tab element
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.addEventListener("click", (e) => {
        const tabName = e.target.textContent.trim().toLowerCase();
        this.switchTab(tabName);
      });
    });
  }

  switchTab(tabName) {
    document
      .querySelectorAll(".tab")
      .forEach((tab) => tab.classList.remove("active"));
    document
      .querySelectorAll(".tab-content")
      .forEach((content) => content.classList.remove("active"));

    if (tabName === "register") {
      const firstTab = document.querySelector(".tab:first-child");
      if (firstTab) firstTab.classList.add("active");
      const regContent = document.getElementById("register-tab");
      if (regContent) regContent.classList.add("active");
      this.isRegisterMode = true;
    } else {
      const lastTab = document.querySelector(".tab:last-child");
      if (lastTab) lastTab.classList.add("active");
      const loginContent = document.getElementById("login-tab");
      if (loginContent) loginContent.classList.add("active");
      this.isRegisterMode = false;
    }

    // Stop camera when switching tabs
    this.stopCamera();
    this.hideStatus();
  }

  async startCamera(mode) {
    try {
      this.showStatus("Starting camera...", "info");

      const video = mode === "reg" ? this.regVideo : this.loginVideo;
      const startBtn =
        mode === "reg" ? this.regStartCamera : this.loginStartCamera;
      const captureBtn = mode === "reg" ? this.regCapture : this.loginCapture;

      // Stop existing stream
      this.stopCamera();

      // request camera
      this.currentStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
          facingMode: "user",
        },
      });

      video.srcObject = this.currentStream;
      await video.play();

      if (startBtn) startBtn.disabled = true;
      if (captureBtn) captureBtn.disabled = false;

      this.showStatus(
        'Camera started! Click "Capture Face" when ready.',
        "success"
      );
    } catch (error) {
      console.error("Error starting camera:", error);
      this.showStatus(
        "Error starting camera. Please check permissions.",
        "error"
      );
    }
  }

  stopCamera() {
    if (this.currentStream) {
      this.currentStream.getTracks().forEach((track) => track.stop());
      this.currentStream = null;
    }
  }

  captureImage(mode) {
    try {
      const video = mode === "reg" ? this.regVideo : this.loginVideo;
      const canvas = mode === "reg" ? this.regCanvas : this.loginCanvas;
      const captureBtn = mode === "reg" ? this.regCapture : this.loginCapture;
      const submitBtn = mode === "reg" ? this.regSubmit : this.loginSubmit;

      if (!video || !canvas) {
        this.showStatus("Video or canvas element missing.", "error");
        return;
      }

      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;

      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      this.capturedImage = canvas.toDataURL("image/jpeg", 0.8);

      if (captureBtn) captureBtn.disabled = true;
      if (submitBtn) submitBtn.disabled = false;

      this.showStatus(
        "Face captured successfully! You can now submit.",
        "success"
      );
    } catch (error) {
      console.error("Error capturing image:", error);
      this.showStatus("Error capturing image. Please try again.", "error");
    }
  }

  async submitRegistration() {
    if (!this.validateRegistrationForm()) return;
    this.setLoading("reg", true);
    this.hideStatus();

    try {
      const payload = {
        username: this.regUsername.value.trim(),
        password: this.regPassword.value,
        face_image: this.capturedImage
          ? this.capturedImage.split(",")[1]
          : null,
      };

      const res = await fetch(`${API_URL}/register/`, {
        method: "POST",
        headers: defaultHeaders(),
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        // attempt to read JSON error if any
        let errorMessage = "Registration failed: server error";
        try {
          const errorData = await res.json();
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          const text = await res.text();
          console.error("Registration HTTP error:", res.status, text);
          errorMessage = `Registration failed (${res.status}): ${text.substring(0, 100)}`;
        }
        console.error("Registration error:", errorMessage);
        this.showStatus(errorMessage, "error");
        return;
      }

      const data = await res.json();

      if (data.success) {
        this.showStatus(
          "Registration successful! You can now login using the Login tab.",
          "success"
        );
        // Don't clear form or switch tabs - let user stay on registration tab
        // User can manually switch to login tab when ready
        // this.clearRegistrationForm();
      } else {
        this.showStatus(data.error || "Registration failed", "error");
      }
    } catch (error) {
      console.error("Registration error:", error);
      this.showStatus("Network error. Please check your connection.", "error");
    } finally {
      this.setLoading("reg", false);
    }
  }

  async submitLogin() {
    if (!this.validateLoginForm()) return;
    this.setLoading("login", true);
    this.hideStatus();

    try {
      const payload = {
        username: this.loginUsername.value.trim(),
        password: this.loginPassword.value,
        face_image: this.capturedImage
          ? this.capturedImage.split(",")[1]
          : null,
      };

      const res = await fetch(`${API_URL}/verify/`, {
        method: "POST",
        headers: defaultHeaders(),
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        // attempt to read JSON error if any
        let errorMessage = "Login failed: server error";
        try {
          const errorData = await res.json();
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          const text = await res.text();
          console.error("Login HTTP error:", res.status, text);
          errorMessage = `Login failed (${res.status}): ${text.substring(0, 100)}`;
        }
        console.error("Login error:", errorMessage);
        this.showStatus(errorMessage, "error");
        return;
      }

      const data = await res.json();

      if (data.success) {
        // store dashboard payload and redirect
        const dashboardData = data.dashboard_data || {};
        localStorage.setItem(
          "faceauth_dashboard_data",
          JSON.stringify(dashboardData)
        );
        const dashStr = encodeURIComponent(JSON.stringify(dashboardData));
        window.location.href = `dashboard.html?data=${dashStr}`;
      } else {
        this.showStatus(data.error || "Login failed", "error");
      }
    } catch (error) {
      console.error("Login error:", error);
      this.showStatus("Network error. Please check your connection.", "error");
    } finally {
      this.setLoading("login", false);
    }
  }

  validateRegistrationForm() {
    if (!this.regUsername || !this.regUsername.value.trim()) {
      this.showStatus("Please enter a username", "error");
      return false;
    }
    if (!this.regPassword || !this.regPassword.value.trim()) {
      this.showStatus("Please enter a password", "error");
      return false;
    }
    if (!this.capturedImage) {
      this.showStatus("Please capture your face first", "error");
      return false;
    }
    return true;
  }

  validateLoginForm() {
    if (!this.loginUsername || !this.loginUsername.value.trim()) {
      this.showStatus("Please enter a username", "error");
      return false;
    }
    if (!this.loginPassword || !this.loginPassword.value.trim()) {
      this.showStatus("Please enter a password", "error");
      return false;
    }
    if (!this.capturedImage) {
      this.showStatus("Please capture your face first", "error");
      return false;
    }
    return true;
  }

  setLoading(mode, isLoading) {
    const loading = mode === "reg" ? this.regLoading : this.loginLoading;
    const text = mode === "reg" ? this.regText : this.loginText;
    const submitBtn = mode === "reg" ? this.regSubmit : this.loginSubmit;

    if (isLoading) {
      if (loading) loading.classList.remove("hidden");
      if (text) text.classList.add("hidden");
      if (submitBtn) submitBtn.disabled = true;
    } else {
      if (loading) loading.classList.add("hidden");
      if (text) text.classList.remove("hidden");
      if (submitBtn) submitBtn.disabled = false;
    }
  }

  clearRegistrationForm() {
    if (this.regUsername) this.regUsername.value = "";
    if (this.regPassword) this.regPassword.value = "";
    this.capturedImage = null;
    if (this.regCapture) this.regCapture.disabled = true;
    if (this.regSubmit) this.regSubmit.disabled = true;
    if (this.regStartCamera) this.regStartCamera.disabled = false;
    this.stopCamera();
  }

  showStatus(message, type) {
    if (!this.status) return;
    this.status.textContent = message;
    this.status.className = `status ${type}`;
    this.status.classList.remove("hidden");
  }

  hideStatus() {
    if (!this.status) return;
    this.status.classList.add("hidden");
  }
}

// Initialize app on DOM ready
document.addEventListener("DOMContentLoaded", () => {
  new FaceAuthApp();
});

// Global function for tab switching (used in HTML)
function switchTab(tabName) {
  const app = window.faceAuthApp || new FaceAuthApp();
  app.switchTab(tabName);
}
