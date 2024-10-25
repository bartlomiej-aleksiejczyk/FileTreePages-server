class SafeHtmlViewer extends HTMLElement {
  constructor() {
    super();
    // Attach a Shadow DOM to keep the styling isolated
    this.attachShadow({ mode: "open" });

    // Create a sandboxed iframe
    this.iframe = document.createElement("iframe");
    this.iframe.style.width = "100%";
    this.iframe.style.height = "100%";
    this.iframe.setAttribute("sandbox", ""); // Empty for full sandbox

    // Add iframe to the Shadow DOM
    this.shadowRoot.appendChild(this.iframe);
  }

  connectedCallback() {
    // Get the HTML content from the 'html' attribute or inner HTML
    const unsanitizedHtml = this.getAttribute("html") || this.innerHTML;

    // Set the iframe's srcdoc to the content
    this.iframe.srcdoc = `
      <!DOCTYPE html>
      <html>
      <head>
        <!-- Add any specific styles here if needed -->
      </head>
      <body>
        ${unsanitizedHtml}
      </body>
      </html>
    `;
  }
}

// Define the custom element
customElements.define("safe-html-viewer", SafeHtmlViewer);
